FROM python:3.8-slim-buster

RUN apt-get update && apt-get -y install nano vim git build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev python3-opencv sudo curl
RUN ln -sv /usr/bin/python3 /usr/bin/python

RUN pip install --user 'git+https://github.com/facebookresearch/fvcore'

RUN pip install torch==1.10.1+cu113 torchvision==0.11.2+cu113 torchaudio===0.10.1+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
RUN pip install cython
RUN pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
RUN python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html

ENV FVCORE_CACHE="/tmp"

RUN pip install --user jupyterlab
RUN pip install opencv-python
RUN pip install Flask
RUN pip install Flask-RESTful
RUN pip install Werkzeug
RUN pip install requests
RUN pip install flask-cors

WORKDIR /home/detectron
COPY . .

ARG EXPOSE_PORT
ENV EXPOSE_PORT=${EXPOSE_PORT}

EXPOSE ${EXPOSE_PORT}

ARG APPLICATION_PORT
ENV APPLICATION_PORT=${APPLICATION_PORT}

ENTRYPOINT ["python", "main.py"]
