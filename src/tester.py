import ffmpeg

stream_url = "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4"

# Input seeking example: https://trac.ffmpeg.org/wiki/Seeking
(
    ffmpeg
    .input(stream_url, ss='00:00:03')  # Seek to third second
    .output("frame.png", pix_fmt='rgb24', frames='1')  # Select PNG codec in RGB color space and one frame.
    .overwrite_output()
    .run()
)