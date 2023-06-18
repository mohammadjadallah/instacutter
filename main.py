from moviepy.editor import *
from flask import Flask, request, render_template, send_file
import math
import zipfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'selected_file' not in request.files:
            return 'No file uploaded', 400
        
        file = request.files['selected_file']
        file.save('uploaded_video.mp4')
        
        parts_time = int(request.form.get('options', 15))  # Get selected parts time, default is 15 seconds

        # Call the function to prepare and process the video
        prepare_video(video_path='uploaded_video.mp4', parts_time=parts_time)

        # Return the processed zip file as a download
        return send_file('processed_videos.zip', as_attachment=True, mimetype='application/zip')
    
    return render_template('index.html')



def prepare_video(video_path: str = None, parts_time: int = None):
    # Read the video file
    clip = VideoFileClip(video_path)

    # Get the length of the video
    size_video = clip.duration
    print(size_video)

    times = math.floor(size_video / parts_time)

    start = 0
    end = parts_time

    processed_video_paths = []  # List to store paths of processed videos

    for i in range(times + 1):
        subclip_start = start
        subclip_end = end if i != times else size_video
        subclip = clip.subclip(subclip_start, subclip_end)
        output_path = f'static/output/edited{i}.mp4'
        subclip.write_videofile(output_path, codec='libx264')
        processed_video_paths.append(output_path)
        start += parts_time
        end += parts_time

    # Create a zip file and add processed videos to it
    with zipfile.ZipFile('processed_videos.zip', 'w') as zipf:
        for path in processed_video_paths:
            zipf.write(path)



if __name__ == '__main__':
    app.run()
