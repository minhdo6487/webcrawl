FROM python:2.7.10

RUN apt-get update \
  && apt-get install -y supervisor \
  && rm -rf /var/lib/apt/lists/*


ENV PYTHONUNBUFFRED 1



ENV STATIC_ROOT /static
ENV MEDIA_DIR /media
ENV DATA_DIR /cache

RUN mkdir /app
ADD requirements.txt /app/requirements.txt
ADD ./webcrawl/ /app/

WORKDIR /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#COPY ./devops_config/supervisor.conf /etc/supervisor/conf.d/

CMD ["supervisord", "-n"]