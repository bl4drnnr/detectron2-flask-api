### Google Colab Training Script

1. Import [this](google-colab-training-script.ipynb) script to your [Google Colab](https://colab.research.google.com/).
2. Upload `.zip` with JSON files and sets of trainig and testing images. The structure of folder within uploaded archive should look like this:
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
