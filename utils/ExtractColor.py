import numpy as np
import pandas as pd
from PIL import Image
from .Color import Color

# TODO: Make it faster, better algorithm
# requirement: I don't need to change to 'centroid' of frequent used coloour
# i.e. colour should be the same as in an image


def rgb_to_hex(row):
    r = row['R']
    g = row['G']
    b = row['B']
    return f"#{r:02x}{g:02x}{b:02x}"


def extract_palette(image_path, max_width=400, ratio_theshold=0.00001, deltaE_threshold=10):

    img = Image.open(image_path)
    img_size = np.array(img.size)

    # resize image
    if np.max(img_size) > max_width:
        img_size = img_size // (np.max(img_size) / max_width)
        img_size = np.array(img_size, dtype=np.int)
        img.resize((img_size[0], img_size[1]))

    # select only RGB
    img_arr = np.array(img)[:, :, :3]
    img_arr = img_arr.reshape((np.product(img_arr.shape[:2]), 3))

    rgb, counts = np.unique(img_arr, axis=0, return_counts=True)

    df = pd.DataFrame(data={'R': rgb[:, 0], 'G': rgb[:, 1], 'B': rgb[:, 2], 'freq': counts})

    df['hex'] = df[['R', 'G', 'B']].apply(rgb_to_hex, axis=1)
    df['ratio'] = df['freq'] / df['freq'].sum()

    df = df.sort_values(by=['ratio'], ascending=False, ignore_index=True)

    freq_used = df[df['ratio'] >= ratio_theshold]
    # unique flag
    freq_used['unique'] = 1

    # merge a less used colour to the most frequent used
    for i, color1 in freq_used.iterrows():
        if color1['unique'] == 1:
            c1 = Color(color1['hex'])
            # filter un-mearged colour below it
            unmerged = freq_used[freq_used['unique'] == 1].loc[(i + 1):, :]
            for j, color2 in unmerged.iterrows():
                c2 = Color(color2['hex'])
                if c1.delta_E(c2) < deltaE_threshold:
                    freq_used.loc[i, 'freq'] += color2['freq']
                    freq_used.loc[j, 'unique'] = 0

    freq_used = freq_used[freq_used['unique'] == 1].reset_index().drop(columns=['index'])
    freq_used['ratio'] = freq_used['freq'] / freq_used['freq'].sum()

    return freq_used[['hex', 'ratio']]
