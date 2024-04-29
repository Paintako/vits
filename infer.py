import argparse
import torch
import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence, cleaned_text_to_sequence
import numpy as np
from scipy.io.wavfile import write
import time
import re
import os
import librosa
from utils import load_wav_to_torch
from mel_processing import spectrogram_torch

speaker_dict = {}

def load_speaker_dict():
    with open(f'/home/p76111652/Linux_DATA/synthesis/corpus/22050/dataset/mixed_5_id.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip().split("|")
            speaker_dict[line[1]] = line[0]

def process_text(input_text, english_flag):
    input_text = input_text.upper()
    if not english_flag:
        input_text = input_text.lower()
    # output_text = re.sub(r'[^\w\s]', ',', input_text)    
    return input_text

def get_text(text, langauge):
    cleaner_names = ['zh_cleaners']
    text_norm = cleaned_text_to_sequence(text)
    text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

hps = utils.get_hparams_from_file("logs/text_encoder1/config.json")

net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model).cuda()
_ = net_g.eval()

_ = utils.load_checkpoint("logs/text_encoder1/G_255000.pth", net_g, None)

def synthesis(text, speaker_id, speaker_name, filename, english_flag, langauge):
    processed_text = process_text(text, english_flag)
    result_np_arr = []
    start_time = time.time()
    processed_text = processed_text.replace(", ",",")    
    for each in str(processed_text).split(","):
        # prevent None
        if not each:
            continue
        each = each.strip()
        stn_tst = get_text(each, langauge)
        with torch.no_grad():
            x_tst = stn_tst.cuda().unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
            sid = torch.LongTensor([int(speaker_id)]).cuda()
            audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=0.6, noise_scale_w=0.8, length_scale=1.0)[0][0,0].data.cpu().float().numpy()
            result_np_arr.append(audio)

    concatenated_audio = np.concatenate(result_np_arr)
    elapsed_time = time.time() - start_time
    print(f"Synthesis for speaker {speaker_id} took {elapsed_time} seconds.")
    if not os.path.exists(f'./gen_audio'):
        os.makedirs(f'./gen_audio')
    if not os.path.exists(f'./gen_audio/{speaker_name}'):
        os.makedirs(f'./gen_audio/{speaker_name}')

    write(f"./gen_audio/{speaker_name}/{filename}",22050, concatenated_audio)


def get_audio(filename):
    audio, sampling_rate = load_wav_to_torch(filename)
    audio_norm = audio / 32768.0
    audio_norm = audio_norm.unsqueeze(0)
    spec_filename = filename.replace(".wav", ".spec.pt")
    spec = spectrogram_torch(audio_norm, 1024, 22050, 256, 1024, center=False)
    spec = torch.squeeze(spec, 0)
    torch.save(spec, spec_filename)
    return spec, audio_norm


def vc(reference_path: os.path, source, target):
    spec, audio_norm = get_audio(reference_path)
    spec = spec.unsqueeze(0).cuda()
    spec_lengths = torch.LongTensor([spec.size(2)]).cuda().float()
    sid_src = torch.LongTensor([source]).cuda()

    write("source.wav", 44100, spec.data.cpu().float().numpy())

    with torch.no_grad():
        sid_tgt1 = torch.LongTensor([target]).cuda()
        audio1 = net_g.voice_conversion(spec, spec_lengths, sid_src=sid_src, sid_tgt=sid_tgt1)[0][0,0].data.cpu().float().numpy()
        write_path = "new.wav"
        write(write_path, 44100, audio1)

def synthsis_file(language, speaker_id):
    with open(f'gen_text/{language}.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
    
    for line in lines:
        filename, text = line.strip().split("|")
        synthesis(text, speaker_id, speaker_id, filename, False, language)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    text = ""
    parser.add_argument("--text", default=text)
    parser.add_argument("--sid", default=0)
    parser.add_argument("--lang", default=0)
    parser.add_argument("--en", default=False)

    file_list = ['zh', 'ctl', 'ha', 'tw']
    speaker_list = [0,1,56,57,59,60,61,62]
    for file in file_list:
        for speaker in speaker_list:
            synthsis_file(file, speaker)