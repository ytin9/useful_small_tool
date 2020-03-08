# -*- coding: utf-8 -*-
#python 2 or python 3

# 可以用語法做批次轉檔 python exercise.py -q 100(最高) *(代表所有檔案) ./(輸出到原本資料夾)

'''
這些是必要裝得套件
sudo add-apt-repository ppa:strukturag/libheif
sudo apt-get update
sudo apt-get install libheif-examples
'''
import subprocess, os, sys
from os import listdir
from os.path import isfile, join

try:
    subprocess.call(['heif-convert'])
    subprocess.call(['clear'])
    try:
        路徑 = os.getcwd() 
        files = [f for f in listdir(路徑) if isfile(join(路徑, f))]
        for file in files:
            (name, ext) = os.path.basename(file).split('.')

            if ext == 'heic' or ext == 'HEIC':
                dest = name + '.jpg'
                orig = file
                print(dest)
                print(orig)
                try:
                    subprocess.call(['heif-convert', orig, dest])
                except:
                    print("語法錯誤或檔案有問題: %s", orig)
    except:
        print("語法錯誤")
except:
    print("套件錯誤")
