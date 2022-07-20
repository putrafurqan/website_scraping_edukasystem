import numpy as np
import PIL
from PIL import Image
from os import walk

import os
import shutil

"""
collate multiple images file into a single image (stacked vertically)
"""

mapel = "Bahasa Inggris"

mypath = mapel
list_im = next(walk(mypath), (None, None, []))[2]
for item in list_im:
     
    smstr = item[8:9]
    bab = item[16:17]
    dir_path = mypath + "\\semester " + smstr + "\\bab" + bab
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    try:
        shutil.move(mypath + "\\" + item,dir_path)
    except:
        None
smstr_container = next(os.walk(mypath + '\\.'))[1]

for smstr in smstr_container:
    bab_container = next(os.walk(mypath + "\\"+smstr + "\\."))[1]

    for bab in bab_container:
        file_container = mypath + "\\" + smstr + "\\" + bab + "\\"
        list_file = next(walk(file_container), (None, None, []))[2]
        x=0
        for j in range(0,len(list_file)):
            if list_file[j-x][:3] == "com":
                list_file.pop(j-x)
                x+=1

        a = list_file[0].index("-")
        b = list_file[0].index("-",(a+8))
        names = list_file[0][a+8:b-1]
        print( names)
        
        imgs    = [ PIL.Image.open(file_container + i) for i in list_file ]
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])
        sum_x = 0
        sum_y = 0
        divi = 0
        for i in min_shape:
            sum_x += i[1][0]
            sum_y += i[1][1]
            divi+=1

        try:
            min_shape = [round(sum_x/divi),round(sum_y/divi)]
            imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

            # for a vertical stacking it is simple: use vstack
            imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
            imgs_comb = PIL.Image.fromarray( imgs_comb)
            imgs_comb.save( "render\\" + mapel + "\\" + names + ".png" )
            print(file_container)

        #"too large file size" exception
        except:
            print(file_container + " : FILE SIZE IS TOO LARGE") 
            lista = list_file[:round(len(list_file)/2)]
            listb = list_file[round(len(list_file)/2):]
            imgsa    = [ PIL.Image.open(file_container + i) for i in lista ]
            imgsb    = [ PIL.Image.open(file_container + i) for i in listb ]

            imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgsa ) )

            # for a vertical stacking it is simple: use vstack
            imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgsa ) )
            imgs_comb = PIL.Image.fromarray( imgs_comb)
            imgs_comb.save( "render\\" + mapel + "\\" + names + " (1).png" )
            print(file_container)
            imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgsb ) )
            imgs_comb = PIL.Image.fromarray( imgs_comb)
            imgs_comb.save( "render\\" + mapel + "\\" + names + " (2).png" )
            print(file_container)