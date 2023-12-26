import numpy as np
import transformers
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import torch
import librosa
import glob

__model = None
__tokenizer = None
ARTIFACTS_DIR = "artifacts"
PRETRAINED_MODEL_NAME = "facebook/wav2vec2-base-960h"

def get_transcription():
    test_file_path_dir = r"static/*.*"

    for test_file_path in glob.glob(test_file_path_dir, recursive=True):
        audio, sampling_rate = librosa.load(test_file_path, sr=16000)

    if audio is None:
        raise ValueError("Unsupported file format")

    input_values = __tokenizer(audio, return_tensors='pt').input_values
    logits = __model(input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcriptions = __tokenizer.decode(predicted_ids[0])
    return transcriptions

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __model
    global __tokenizer

    def load_from_directory(directory):
        return Wav2Vec2ForCTC.from_pretrained(directory), Wav2Vec2Tokenizer.from_pretrained(directory)

    if __model is None or __tokenizer is None:
        try:
            __model, __tokenizer = load_from_directory(ARTIFACTS_DIR)
            print(type(__model))
            print(type(__tokenizer))
        except:
            __model, __tokenizer = load_from_directory(PRETRAINED_MODEL_NAME)
            __model.save_pretrained(ARTIFACTS_DIR)
            __tokenizer.save_pretrained(ARTIFACTS_DIR)
    print("Loading saved artifacts...done")

if __name__ == '__main__':
    load_saved_artifacts()
    transcribed_txt = get_transcription()
    print(transcribed_txt)
