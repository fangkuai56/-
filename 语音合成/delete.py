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
        print(filename)
    audio_norm = audio / max_wav_value
    audio_norm = audio_norm.unsqueeze(0)
    spec_filename = filename.replace(".wav", ".spec.pt")
    if os.path.exists(spec_filename):
        spec = torch.load(spec_filename)
    else:
        spec = spectrogram_torch(audio_norm, filter_length,
                                 sampling_rate, hop_length, win_length,
                                 center=False)
        spec = torch.squeeze(spec, 0)
        torch.save(spec, spec_filename)
    return spec, audio_norm


def get_text(text):
    if cleaned_text:
        text_norm = cleaned_text_to_sequence(text)
    else:
        text_norm = text_to_sequence(text, text_cleaners)
    if add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

with open("filelists/genshin_train_filelist.txt.cleaned") as f:
    for file in f.read().split("\n"):
        name = file.split("|")
        get_audio(name[0])
        get_text(name[1])

