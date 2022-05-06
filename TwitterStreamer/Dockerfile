FROM python:3.9.12
WORKDIR /home/ubuntu/CCC_Project2/TwitterStreamer
COPY . .
RUN pip install -r stream_requirements.txt
RUN pip install nltk
RUN python3 -m nltk.downloader vader_lexicon
CMD python3 tweetStreamer.py