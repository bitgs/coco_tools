#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 22:39:57 2019

@author: yuan
"""
import json


dataDir='/data/coco'
dataType='val2017'
annFile='%s/annotations/instances_%s.json'%(dataDir,dataType)


dataset = json.load(open(annFile, 'r'))
image_name_list = []
image_shape_list = []
bbox_list = []
category_id_list = []
annotations = dataset["annotations"]
for i in range(len(annotations)):
    if i %10000==0:
        print(i)
    annotations[i]["bbox"][2] = round(annotations[i]["bbox"][0]+annotations[i]["bbox"][2])
    annotations[i]["bbox"][3] = round(annotations[i]["bbox"][1]+annotations[i]["bbox"][3])
    annotations[i]["bbox"][0] = round(annotations[i]["bbox"][0])
    annotations[i]["bbox"][1] = round(annotations[i]["bbox"][1])
    if annotations[i]["image_id"] not in image_name_list:
        image_name_list.append(annotations[i]["image_id"])
        bbox_list.append([annotations[i]["bbox"]])
        category_id_list.append([annotations[i]["category_id"]])
    else:
        bbox_list[image_name_list.index(annotations[i]["image_id"])].append(annotations[i]["bbox"])
        category_id_list[image_name_list.index(annotations[i]["image_id"])].append(annotations[i]["category_id"])

category_id_dict = dataset["categories"]
image_dict = dataset["images"]
image_shape_list = [[0,0] for i in range(len(image_name_list))]
for i in range(len(image_dict)):
    if i %10000==0:
        print(i)
    if image_dict[i]['id'] in image_name_list:
        image_shape_list[image_name_list.index(image_dict[i]['id'])][0] = image_dict[i]["width"]
        image_shape_list[image_name_list.index(image_dict[i]['id'])][1] = image_dict[i]["height"]
        image_name_list[image_name_list.index(image_dict[i]['id'])] = '/data/coco/train2017/' + '{}.jpg'.format(image_name_list[image_name_list.index(image_dict[i]['id'])]).rjust(16, '0')


for i in range(len(category_id_list)):
    if i %10000==0:
        print(i)
    for j in range(len(category_id_list[i])):
        for k in range(len(category_id_dict)):
            if category_id_list[i][j] == category_id_dict[k]["id"]:
                category_id_list[i][j] = k
f = open('./val.txt','w')
for i in range(len(image_name_list)):
    if i %10000==0:
        print(i)
    f.write('{} {} {} {}'.format(i, image_name_list[i], image_shape_list[i][0], image_shape_list[i][1]))
    for j in range(len(category_id_list[i])):
        f.write(" {} {} {} {} {}".format(category_id_list[i][j], bbox_list[i][j][0]
        , bbox_list[i][j][1], bbox_list[i][j][2], bbox_list[i][j][3]))
    f.write('\n')
f.close()

import os
name = os.listdir("/data/coco/val2017")
name.sort()
temp = ['' for i in range(len(name))]
with open('val.txt', 'r') as f:
    data = f.readlines()
    

for i in range(len(data)):
    if i %10000==0:
        print(i)
    temp[name.index(data[i].split(' ')[1][21:])] = data[i]
    
out_list = []
for i in range(len(temp)):
    if i %10000==0:
        print(i)
    if temp[i] != '':
        out_list.append(temp[i])

# =============================================================================
# with open('test.txt', 'r') as f:
#     out_list = f.readlines()
# =============================================================================
f = open('./val_voc_format.txt','w')
for i in range(len(out_list)):
    if i %10000==0:
        print(i)
    temp = out_list[i].split(' ')[1:]
    temp2 = '{}'.format(i)
    for j in range(len(temp)):
        temp2 = temp2+' '+temp[j]
    f.write(temp2)
f.close()
    