#!/usr/bin/env python3

import os
import random
import sys
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth.exceptions
import pickle

# Retry settings
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (OSError, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

def get_authenticated_service():
    creds = None
    # Load credentials if previously saved
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If no valid credentials, do OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def initialize_upload(youtube, options):
    tags = options.keywords.split(",") if options.keywords else None
    body = {
        "snippet": {
            "title": options.title,
            "description": options.description,
            "tags": tags,
            "categoryId": options.category
        },
        "status": {
            "privacyStatus": options.privacyStatus
        }
    }

    insert_request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)

def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0

    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response and 'id' in response:
                print(f"Video id '{response['id']}' was successfully uploaded.")
            elif response:
                print(f"Unexpected response: {response}")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occurred: {e}"

        if error:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                print("No longer attempting to retry.")
                break
            sleep_seconds = random.random() * (2 ** retry)
            print(f"Sleeping {sleep_seconds:.2f} seconds before retrying...")
            time.sleep(sleep_seconds)
            error = None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Video file to upload")
    parser.add_argument("--title", help="Video title", default="Test Title")
    parser.add_argument("--description", help="Video description", default="Test Description")
    parser.add_argument("--category", default="22", help="Numeric video category")
    parser.add_argument("--keywords", help="Video keywords, comma separated", default="")
    parser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES, default="public", help="Video privacy status")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        sys.exit("Please specify a valid file using the --file parameter.")

    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")