

from google.colab import drive
drive.mount('/content/gdrive')

cd /content/gdrive/My Drive/Haar_cascade

"""Importing all the important libraries"""

import urllib.request
import cv2
import numpy as np
import os
import shutil

"""I used my 2nd link in the function defined below and 1st link is 
http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513
"""

#since the count of the file is 52. let's start with pic_num =53
def store_raw_images():
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152'   
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num =53
    
    if not os.path.exists('neg'):
        os.makedirs('neg')
        
    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "neg/"+str(pic_num)+".jpg")
            img = cv2.imread("neg/"+str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("neg/"+str(pic_num)+".jpg",resized_image)
            pic_num += 1
            
        except Exception as e:
            print(str(e))  
  
store_raw_images()

#how to get the number of files in a directory
path, dirs, files = next(os.walk("neg"))
file_count = len(files)
file_count

#check the totoal number of files(images) in neg directory
path, dirs, files=next(os.walk('neg'))
final_number_of_files=len(files)
final_number_of_files

#now fetching a ugly image viz. in uglies folder in haar_Cascade directory
mkdir uglies

#now deleting all the ulgy images
def find_uglies():
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))
find_uglies()

#checking the remaining 'neg' images
path, dirs, files=next(os.walk('neg'))
remaining_final_neg_images=len(files)
remaining_final_neg_images

def create_pos_n_neg():
    for file_type in ['neg']:
        
        for img in os.listdir(file_type):

            if file_type == 'pos':
                line = file_type+'/'+img+' 1 0 0 50 50\n'
                with open('info.dat','a') as f:
                    f.write(line)
            elif file_type == 'neg':
                line = file_type+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)
create_pos_n_neg()

# all the trained information will be stored in a data folder

mkdir data

"""All my positive images will be store in info folder"""

mkdir info

ls

#In case u need to recreate the positive images u can remove info direc using the command
#shutil.rmtree('info')

"""Here, use this command to create the positive images and store them in info direc"""

!opencv_createsamples -img watch5050.jpg -bg bg.txt -info info/info.lst -pngoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1050

"""Create a vec file to train your model using this command"""

!opencv_createsamples -info info/info.lst -num 1050 -w 20 -h 20 -vec positives.vec

"""Train your model"""

!opencv_traincascade -data data -vec positives.vec -bg bg.txt -numPos 950 -numNeg 475 -numStages 10 -w 20 -h 20

