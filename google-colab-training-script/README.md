### Google Colab Training Script

Here is the step-by-step instruction of how you can using provided script generate your own `.pth` trained model. Also, please, depending on your data pay attention to `get_traing_cfg()` function. Change those config varialbes value to make them fit your data sets.

As it's been told, this project is not created for production amounts of data, but only for tests, therefore, you can not change default values of config funtion, unless you think you will get different from expected result.

1. Import [this](google-colab-training-script.ipynb) script to your [Google Colab](https://colab.research.google.com/).
2. Upload `.zip` as `data.zip` with JSON files and sets of trainig and testing images. The structure of folder `data` within uploaded archive should look like this:
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
3. At the top, in `Runtime` settings click `Change runtime type` and there, select `GPU`.
4. Execute every block of code and the `main()` function. Then, after train, after refresh of folder structure you will be able to fine `model_final.pth`. **This is your trained model.**
5. Additionaly, you can play around with functions below `main()` function to see, if everything works.

*PS. After you are done with training, don't fotget to turn off `GPU` runtime mode since you are limited with `GPU` resources unless you don't have not free plan.*

- [Labelme and how you can install and use it](https://github.com/wkentaro/labelme)
- [How to convert labelme to COCO format](https://github.com/fcakyon/labelme2coco)
