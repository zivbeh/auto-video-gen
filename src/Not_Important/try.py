from moviepy.editor import *
frame_rate = 24
# List of slide images or video clips
slides = []
for i in range(1, frame_rate*3):
    slides.append('./resources/images/image1.jpg')
for i in range(1, frame_rate*2):
    slides.append('./resources/images/image2.jpg')
for i in range(1, frame_rate*1):
    slides.append('./resources/images/image3.jpg')

# Create a list of clips with transitions
clips_with_transitions = []
for i in range(len(slides)):
    slide = slides[i]

    # Add a crossfade transition between slides
    if i > 0:
        transition = CrossfadeVideoClip(duration=1)  # Adjust the duration as needed
        clips_with_transitions.append(transition)

    clips_with_transitions.append(slide)

# Concatenate the clips together
final_clip = concatenate_videoclips(clips_with_transitions)

# Export the final slideshow
final_clip.write_videofile("slideshow_with_transitions.mp4", fps=frame_rate)  # Adjust the file name and fps as needed
