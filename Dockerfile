FROM python:3.8-slim-buster

RUN apt-get update && apt-get -y install nano vim git build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev python3-opencv sudo curl
RUN ln -sv /usr/bin/python3 /usr/bin/python

RUN pip install --user 'git+https://github.com/facebookresearch/fvcore'

RUN pip install torch==1.10+cpu torchvision==0.11.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
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

EXPOSE 8080

ENTRYPOINT ["python", "main.py"]
