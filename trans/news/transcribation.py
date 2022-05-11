import sys
import os
import wave
import json
import numpy as np
from vosk import Model, KaldiRecognizer, SpkModel
from django.conf import settings


class Transcrib(object):
    model_path = str(settings.VOSK_MODELS_PATH / "vosk-model-ru-0.22")
    spk_model_path = str(settings.VOSK_MODELS_PATH / "vosk-model-spk-0.4")
    model = Model(model_path)
    spk_model = SpkModel(spk_model_path)
    sample_rate = 16000

    def __init__(self):
        pass

    def set_wf(self, path):
        self.wf = wave.open(str(settings.MEDIA_ROOT / path), "rb")

    def check(self):

        if self.wf.getnchannels() != 1:
            return False, "Audio file must be mono."

        if self.wf.getsampwidth() != 2:
            return False, f"Audio file must be WAV format PCM. sampwidth={self.wf.getsampwidth()}"

        if self.wf.getcomptype() != "NONE":
            return False, f"Audio file must be WAV format PCM. comptype={self.wf.getcomptype()}"

        return True, "OK"

    def handle(self):
        text = []
        rec = KaldiRecognizer(self.model, self.wf.getframerate() * self.wf.getnchannels())
        rec.SetSpkModel(self.spk_model)

        self.wf.rewind()
        frame_read = 0
        while True:

            # end_point = frame_read / self.wf.getframerate()
            data = self.wf.readframes(self.wf.getframerate())

            if len(data) == 0:
                break

            frame_read += len(data) / 2

            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                # start_point = end_point - (res['spk_frames'] / self.wf.getframerate())
                # text.append({'time_code': [start_point, end_point], 'phrase': res['text']})
                text.append(res['text'])

        final = json.loads(rec.FinalResult())
        # start_point = end_point - (final['spk_frames'] / self.wf.getframerate())
        # text.append({'time_code': [start_point, end_point], 'phrase': final['text']})
        text.append(final['text'])
        return text
