import subprocess


def upload_youtube_video(
        file_path,
        title,
        description,
        keywords="""
        قرآن كريم, تلاوة قرآن, استماع قرآن, ختم قرآن, آيات قرآنية, شيخ عبد الباسط, الشيخ ماهر المعيقلي, الشيخ مشاري راشد,
        تعليم القرآن, قرآن للأطفال, سور قرآنية, حفظ القرآن
        """,
        category = "27",
        privacy_status = "public"
):
    command = [
        "python", "push_video.py",
        f'--file={file_path}',
        f'--title={title}',
        f'--description={description}',
        f'--keywords={keywords}',
        f'--category={category}',
        f'--privacyStatus={privacy_status}'
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    print("Return code:", result.returncode)