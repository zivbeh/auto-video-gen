from moviepy.editor import *

frame_rate = 24
# Load images
# ['image1.jpg', 'image2.jpg', 'image3.jpg']
lst = []
for i in range(1, frame_rate*3):
    lst.append('./resources/images/image1.jpg')
for i in range(1, frame_rate*2):
    lst.append('./resources/images/image2.jpg')
for i in range(1, frame_rate*1):
    lst.append('./resources/images/image3.jpg')
image_sequence = ImageSequenceClip(lst, frame_rate)

# Load voiceover audio
voiceover = AudioFileClip('./resources/audio/audio.mp3')
print(image_sequence.duration)
# Set the audio to match the duration of the image sequence
voiceover = voiceover.set_duration(image_sequence.duration)

# Combine images and voiceover
video = image_sequence.set_audio(voiceover)

# Export the video as an MP4 file
video.write_videofile('./output/output.mp4', codec='mpeg4', audio_codec='aac')
