# Table of contents

1. [Detectron2 Flask API](#detectron2-flask-api)
2. [Documentation](#documentation)
    1. [Requirements](#requirements)
        1. [Docker and docker compose](#docker-and-docker-compose)
        2. [PTH model](#pth-model)
    2. [Installation](#installation)
    3. [Usage](#usage)
3. [Contact and references](#contact-and-references)
4. [License](#license)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

---

# Detectron2 Flask API

**Detectron2 Flask API** - is a simple `Python` written repository that allows you to run `detectron2` within **Docker** container and use `Flask` written **API** in order to interact with it.

Image, that is build in this repo works not with **GPU** (**CUDA**), but **CPU**, what allows you not to have graphic card by **NVIDIA**. More, about how everything works you will find in the [Documentation](#documentation) section.

---

## Documentation

The section of documentation is devided on 3 parts - [what you need](#requirements), [how you can install it](#installation) and [how you can use it](#usage).

### Requirements

#### Docker and docker compose

The **API** itself works within `Docker` container build by special image. So that, the first thing you are required to have in order to use is installed `Docker` and `docker-compose`. To check that type `docker --version` and `docker-compose --version`

```
> docker --version
Docker version 20.10.21, build baeda1f
```

```
> docker-compose --version
Docker Compose version v2.12.2
```

#### PTH model

The second thing you need to have is build `.pth` trained model. More about what `.pth` means and what is used for you can read [here](https://fileinfo.com/extension/pth).

>A PTH file is a machine learning model created using PyTorch, an open-source machine learning library. It contains algorithms used to automatically perform a task, such as pscaling or identifying an image. PTH files can be used in a variety of machine learning and algorithm-related applications, but are most commonly used to upscale images.

Not going deep in details you will need prepare to sets of data - for **testing** and **traing** using [labelme](https://github.com/wkentaro/labelme). Then you need to convert those 2 sets to **COCO** format, because this format is read by `detecton2`.

Here is how after convertion to **COCO** your sets of data are supposed to look:

```
├── test
│   ├── 1.png
│   ...
├── test.json
├── train
│   ├── 21.png
│   ...
└── train.json
```

In order to train model in normal preiod of time (because one way or another training **GPU** will make the whole process faster than training on **CPU**) and for free, you can use **Google Colab**.

The only thing you are required to do, is in **Runtime** settings **change runtime time** to GPU, *but be careful with that, since amount of resources you are allowed to use is limited. Use this method only for testing purposes.*

Script and step-by-step instuction of how you can generate your own `.pth` model can be found in [this](google-colab-training-script) folder.

### Installation

In order to install, using terminal, open folder where you want to save and type:

```
git clone https://github.com/bl4drnnr/detectron2-flask-api.git
```

### Usage

---

## Contact and references

- Developer contact - [mikhail.bahdashych@protonmail.com](mailto:mikhail.bahdashych@protonmail.com)
- Detectron2 GitHub repository - [link](https://github.com/facebookresearch/detectron2)
- Detectron2 installation instruction - [link](https://detectron2.readthedocs.io/en/latest/tutorials/install.html)
- Detectron2 official documentation - [link](https://detectron2.readthedocs.io/en/latest/index.html)
- Flask official documentation - [link](https://flask.palletsprojects.com/en/2.2.x/)
- Google Colab - [link](https://colab.research.google.com/)
- Google Colab detectron2 tutorial - [link](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5)
- Detectron2 : The bare basic end to end tutorial - [link](https://towardsdatascience.com/detectron2-the-basic-end-to-end-tutorial-5ac90e2f90e3)
- `labelme` official repository - [link](https://github.com/wkentaro/labelme)
- `labelme2coco` official repository - [link](https://github.com/fcakyon/labelme2coco)

---

## License

Licensed by [MIT License](LICENSE).