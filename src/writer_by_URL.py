from moviepy.editor import *
import requests

frame_rate = 24
# Load images

# URL of the image
image_urls = ['https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg', 'https://cdn.pixabay.com/photo/2015/12/01/20/28/road-1072821_1280.jpg']
# Download the image

image_clips = []
for url in image_urls:
    response = requests.get(url)
    image_data = response.content
    image_clip = ImageClip(image_data)
    image_clip = image_clip.set_duration(1)
    image_clips.append(image_clip)

image_sequence = concatenate_videoclips(image_clips)

# # Load voiceover audio
# voiceover = AudioFileClip('./resources/audio/audio.mp3')
# print(image_sequence.duration)
# # Set the audio to match the duration of the image sequence
# voiceover = voiceover.set_duration(image_sequence.duration)

# # Combine images and voiceover
# video = image_sequence.set_audio(voiceover)

# Export the video as an MP4 file
image_sequence.write_videofile('./output/output.mp4', codec='mpeg4', audio_codec='aac')
