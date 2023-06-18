# # Importing required module
# from moviepy.editor import *

# try:  
#     # video = input("Name of the file: ")
#     # uploading the video
#     video = VideoFileClip("video.mp4") 

#     time = int(input("""Choose one of the following choices(1, 2,..., 6):
# 1. 0-15 seconds
# 2. 0-30 seconds
# 3. 0-45 seconds
# 4. 0-60 seconds
# 5. 0-75 seconds
# 6. 0-90 seconds
# ___________________________
# [input]:"""))
    
#     if time == 1:
#         video = video.subclip(0, 20)
#     if time == 2:
#         video = video.subclip(0, 35)
#     if time == 3:
#         video = video.subclip(0, 50)
#     if time == 4:
#         video = video.subclip(0, 65)
#     if time == 5:
#         video = video.subclip(0, 80)
#     if time == 6:
#         video = video.subclip(0, 95)
        
#     #time is always in seconds
#     # trimming some part of the video
#     video = video.cutout(5, 10)
#     # display clip
#     video.write_videofile('edited.mp4',codec='libx264')
# except Exception as e:
#     print(e)

import ffmpeg
import math
import zipfile

def prepare_video(video_path: str = None, parts_time: int = None):
    # Get the length of the video
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])

    times = math.floor(duration / parts_time)

    start = 0
    end = parts_time

    processed_video_paths = []  # List to store paths of processed videos

    for i in range(times + 1):
        output_path = f'static/output/edited{i}.mp4'
        ffmpeg.input(video_path).output(output_path, ss=start, to=end, codec='libx264').run(overwrite_output=True)
        processed_video_paths.append(output_path)
        start += parts_time
        end += parts_time

    # Create a zip file and add processed videos to it
    with zipfile.ZipFile('processed_videos.zip', 'w') as zipf:
        for path in processed_video_paths:
            zipf.write(path)

prepare_video(r"E:\pycharmProjects\pythonProject\instaCutter\uploaded_video.mp4", 15)
