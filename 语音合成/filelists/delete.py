from utils import load_wav_to_torch, load_filepaths_and_text
from text import text_to_sequence, cleaned_text_to_sequence
import os
import commons
import torch
from mel_processing import spectrogram_torch
sampling_rate = 22050
max_wav_value = 32768.0
filter_length = 1024
hop_length = 256
win_length = 1024
cleaned_text=True
text_cleaners=["chinese_cleaners1"]
add_blank=True

def get_audio(filename):
    audio, sampling_rate = load_wav_to_torch(filename)
    if sampling_rate != sampling_rate:
        raise ValueError("{} {} SR doesn't match target {} SR".format(
            sampling_rate, sampling_rate))
    if(audio > max_wav_value):
        print(filename)


with open("filelists/genshin_val_filelist.txt.cleaned") as f:
    for file in f.read().split("\n"):
        name = file.split("|")
        if len(name) == 2:
            get_audio(name[0])
