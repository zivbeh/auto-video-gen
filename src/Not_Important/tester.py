from moviepy.editor import *

image_files = ["./resources/images/image3.jpg", "./resources/images/image1.jpg", "./resources/images/image2.jpg"]

# Set the duration for each image clip and define the duration for the transitions between clips (in seconds)
clip_durations = [1, 2, 1]  # Duration of each image clip
transition_duration = 1.5  # Duration of the transition between clips

# Create a list of clips with transitions between them
clips_with_transition = []
for i in range(len(image_files)):
    clip = ImageSequenceClip([image_files[i]], durations=[clip_durations[i]])
    next_clip = ImageSequenceClip([image_files[(i + 1) % len(image_files)]], durations=[clip_durations[(i + 1) % len(image_files)]])
    clip_with_transition = concatenate_videoclips([clip.crossfadein(transition_duration), next_clip])
    clips_with_transition.append(clip_with_transition)

# Concatenate the clips into a single video
final_clip = concatenate_videoclips(clips_with_transition)

# Export the final video to a file
final_clip.write_videofile("slideshow_with_transitions.mp4", fps=24)


