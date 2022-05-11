FROM python:3.9-slim

COPY . /var/data/stt_service
RUN apt-get update && apt-get install -y wget unzip

WORKDIR /var/data/stt_service/trans
RUN mkdir vosk-models
RUN wget https://alphacephei.com/kaldi/models/vosk-model-ru-0.22.zip
RUN wget https://alphacephei.com/kaldi/models/vosk-model-spk-0.4.zip
RUN unzip vosk-model-ru-0.22.zip && mv vosk-model-ru-0.22 vosk-models
RUN unzip vosk-model-spk-0.4.zip && mv vosk-model-spk-0.4 vosk-models

RUN pip install -r ../requirements.txt

CMD [ "python", "manage.py", "runserver" ]
