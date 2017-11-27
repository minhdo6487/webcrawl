import os
import urllib, requests
import uuid
import sys
import cv2
import time
import bs4

class get_image:
    @classmethod
    def from_text(cls, file_name):
        fileID = file_name
        with open(fileID, 'r') as f:
            data = f.readlines()

        if not os.path.exists('neg'):
            os.makedirs('neg')

        count_index = 0
        for item in data:
            #print item
            specific_id = uuid.uuid4()
            try:
                if requests.get(item.replace('\n','')).ok: 
                    if len(requests.get(item.replace('\n','')).content) > 10:
                        print item.replace('\n','')
                        urllib.urlretrieve(item.replace('\n',''), '/code/blog/opencv_model/neg/'+ str(specific_id) + '.jpg')
                        img = cv2.imread('/code/blog/opencv_model/neg/'+ str(specific_id) + '.jpg', cv2.IMREAD_GRAYSCALE)
                        dir_path  = "/code/blog/opencv_model/neg/"+str(specific_id)+".jpg"
                        resized_image = cv2.resize(img, (100, 100))
                        cv2.imwrite(dir_path,resized_image)
                #count_index += 1
            except Exception as e:
                print str(e)


if __name__ == '__main__':
    get_image.from_text('poinpen_edit_link.txt')
    #get_image.from_text('poinpen_edit_link_miss.txt')
