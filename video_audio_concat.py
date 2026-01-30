from get_ayah import get_ayah
from get_video import get_video
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from upload_command import upload_youtube_video
from pydub import AudioSegment
from datetime import datetime
from colorama import Back
import random
import os

surah = random.randint(36,114)
start_ayah = 5
count = 4
timestamp = f"{datetime.now().strftime('%d_%m_%Y %H_%M_%S')}"

final_video = f"{timestamp}_video.mp4"
mp3_file = f"{timestamp}_audio.mp3"

print("📖🎧 Ayah Audio Processing Started")

get_ayah(surah,start_ayah,count,mp3_file)

if not os.path.exists(mp3_file) or os.path.getsize(mp3_file) < 10000:
    raise RuntimeError(Back.RED + "Audio file is invalid or empty")
    

audio = AudioSegment.from_file(mp3_file)

duration_seconds = len(audio) // 1000  

print("🚀🎬 Video Action Started")

get_video(final_video,duration_seconds)

print("🔗✨ Ayah Concat Completed")

video = VideoFileClip(final_video)
audio = AudioFileClip(mp3_file)

if video.duration < audio.duration:
    loops = int(audio.duration // video.duration) + 1
    video = concatenate_videoclips([video] * loops)
    video = video.subclip(0, audio.duration)

final_video_ = video.set_audio(audio)

final_video_.write_videofile(
    f"{timestamp}_output.mp4",
    codec="libx264",
    audio_codec="aac"
)

print("="*40)
output_path = os.path.abspath(f"{timestamp}_output.mp4")
print("📂 Full video path:", output_path)
print("="*40)

print("Start Uploading Video..")

quran_titles = [
    "تلاوة روحانية من القرآن الكريم – استمع وارتح",
    "آيات من القرآن الكريم بصوت خاشع",
    "القرآن الكريم – رحلة صوتية للطمأنينة",
    "استماع لتلاوة القرآن الكريم بصوت مؤثر",
    "ختم القرآن الكريم – استمع للآيات المباركة",
    "تلاوة هادئة من سور القرآن الكريم",
    "القرآن الكريم بصوت شجي – تهدئة النفس",
    "آيات قرآنية للتدبر والتفكر",
    "استمع للقرآن الكريم في أي وقت ومكان",
    "تعليم وحفظ القرآن الكريم بسهولة"
]


upload_youtube_video(
    file_path=f'{output_path}',
    title=f'{random.choice(quran_titles)}',
    description="""
استمع إلى تلاوة خاشعة وعميقة من آيات القرآن الكريم، بصوت شيخ متقن وجميل يأخذك في رحلة روحية بين كلمات الله، لتشعر بالطمأنينة والسكينة.
هذا الفيديو يقدم لك فرصة للاستماع إلى القرآن في أي وقت، سواء للراحة النفسية، أو للتدبر والتعلم، أو لحفظ وتلاوة السور. دع أصوات الآيات تلامس قلبك وتغذي روحك، وتجعلك أقرب إلى الله، مع تجربة سمعية رائعة تجمع بين الإتقان الصوتي والجمال الروحي.

#قرآن #تلاوة #استماع_قرآن #آيات_قرآنية #ختم_القرآن
#  #شيخ_عبد_الباسط #الشيخ_ماهر_المعيقلي #الشيخ_مشاري_راشد
#  #تعليم_القرآن #حفظ_القرآن #سور_قرآنية #روحانية
#  #سلام_نفسي #إسلام #إيمان #ذكر_الله #هدوء #طمأنينة #روحانيات
"""
)


for i in (final_video, mp3_file,output_path):
    os.remove(i)

print("Done Deleting...")

print("✨ Done ALL Actions Succssfully!")