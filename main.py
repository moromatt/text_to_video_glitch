#!/usr/bin/env python
"""Foobar.py: Description of what foobar does."""
__author__ = "amxrfe"
__copyright__ = "Copyright 2020, Planet Earth"


from utils import *

# load text file
text_path = './text_file/text.txt'
# output video name
video_name = 'text_to_chaos_video.mp4'
# set text config
word_range = 5
text_size = 140
# set text color
text_color = (588, 255, 255)
# background color
background_color = (0, 0, 0)
# set image size
h_img, w_img = [592, 1920]
# set the percentage of how many letters should vary
f_percent = 0.3

# set font type and size
unicode_font = ImageFont.truetype("simsun.ttc", text_size, encoding='unic')
# set number of frames per chunk, add at the end C frames with the correct chunk
n_frames_per_chunk = 20
n_frames_per_chunk_chaos = 15
n_frames_per_correct_chunk = 10
# fps image
fps = float(n_frames_per_chunk + n_frames_per_correct_chunk)

# get text and sanitize
text = get_text(text_path)

# split in random chunks
text_list = create_chunks(text, word_range)

list_of_images = list()
for idx, chunk in enumerate(text_list):
    # get N random chunks
    chaos_chunk_order = list()
    chaos_chunk = list()
    for _ in range(n_frames_per_chunk_chaos):
        chaos_chunk_order.append(make_chaos(chunk, f_percent))
    # double C randomic frames
    for i in range(len(chaos_chunk_order)):
        chaos_chunk.append(chaos_chunk_order[i])
        if random.choice([True, False]):
            chaos_chunk.extend([chaos_chunk_order[i]] * 2)
    # union of N random chunks with K times the original chunk
    tot_chunks = chaos_chunk + [chunk] * n_frames_per_correct_chunk

    for word in tot_chunks:
        img_pil = Image.new("RGBA", (w_img, h_img), color=background_color)
        draw = ImageDraw.Draw(img_pil)
        w, h = draw.textsize(word, font=unicode_font)
        draw.text(((w_img - w) / 2, (h_img - h) / 2), word, font=unicode_font, fill=text_color)
        img = np.array(img_pil)

        # display results
        list_of_images.append(img)

imageio.mimwrite(path_imgs + '/' + video_name, np.array(list_of_images), fps=fps)
