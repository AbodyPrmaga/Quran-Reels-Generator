import requests
import random
from datetime import datetime


readers = [
    'ar.alafasy',
    'ar.abdulbasitmurattal',
    'ar.ayub',
    'ar.saoodshuraym',
    'ar.mahermuaiqly',
    'ar.minshawi'
]

pram = random.choice(readers)

def get_ayah(surah, start_ayah, count, mp3_file):

    final_text = ""

    with open(f"{mp3_file}", "wb") as audio_file:
        for i in range(start_ayah, start_ayah + count):
            url = f"https://api.alquran.cloud/v1/ayah/{surah}:{i}/{pram}"

            res = requests.get(url).json()
            if "data" not in res:
                continue

            data = res["data"]

            if "text" not in data or "audio" not in data:
                continue

            final_text += data["text"]

            audio_url = data["audio"]
            audio_data = requests.get(audio_url).content
            audio_file.write(audio_data)

    print("✅ Done Download Ayah Succssfully!")
    print("TEXT : ")
    print(final_text)
