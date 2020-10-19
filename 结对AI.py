from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import json, requests, base64, os, copy
import pickle


def cut_image(image):  # 将一张图片切割成九张小图，返回九张小图组成的列表
    img_size = image.size
    width = img_size[0]  # 图片的宽度
    height = img_size[1]  # 图片的高度
    item_width = width / 3.0
    item_height = height / 3.0
    item_location_list = []
    image_list = []
    # 将需要得到的小图的对顶坐标添加到列表，便于后续直接切割图片
    for row in range(3):
        for col in range(3):
            item_location = (col * item_width, row * item_height, (col + 1) * item_width, (row + 1) * item_height)
            item_location_list.append(item_location)
    # 将切割image图片
    for item_location in item_location_list:
        image_list.append(image.crop(item_location))  # image.crop(item_location)是切割图片的函数
    return image_list


def get_white_arr():  # 获取空白块的矩阵
    image = Image.open(r'C:\\Users\\ASUS\\Desktop\\用来得到空白快的矩阵的图片.jpg')  # 先从接口处下载一张乱图，切割后得到空白的图片

    char_lists = cut_image(image)
    char9_list = []
    for image in char_lists:
        char_arr = np.array(image)
        char9_list.append(char_arr)
    white_arr = char9_list[6]
    return white_arr


def get_35photo_list35():  # 获取36张原图的九个小图的矩阵组成的列表
    list_35 = []
    for i in range(35):
        image = Image.open(r'C:\\Users\\ASUS\\Desktop\\无框图片\\' + str(i) + '.jpg')
        image_list = cut_image(image)
        list_9 = []
        for image in image_list:
            image_arr = np.array(image)  # 将图片以数组的形式读入变量
            list_9.append(image_arr)
        list_35.append(list_9)
    return list_35


def get_messy_pictures_list9():  # 从接口处获得一张排序混乱的图片并得到切割后九张小图的矩阵组成的列表
    url = "http://47.102.118.1:8089/api/challenge/start/5ff2452f-13ea-447e-83be-b0d91346d01b"
    hdata = {
        "teamid": 55,
        "token": "6ef4189d-40b3-476e-bcd6-ca9cd9b24ce0"
    }
    r = requests.post(url, json=hdata)

    datadir = json.loads(r.text)
    datadir2 = datadir['data']

    imgdata = base64.b64decode(datadir2['img'])
    step = datadir2['step']
    swap = datadir2['swap']
    uuid = datadir['uuid']
    # path = r"C:\Users\ASUS\Desktop\软工图片\\char1.jpg"
    path = r"char1.jpg"

    file = open(path, 'wb')
    file.write(imgdata)
    file.close()
    img = Image.open(path)
    img_list = cut_image(img)
    messy_pictures_list9 = []
    for image in img_list:
        image_arr = np.array(image)
        messy_pictures_list9.append(image_arr)
    return messy_pictures_list9, step, swap, uuid


def identify_label_pictures(get_messy_pictures_list9, get_35photo_list35):  # 图像识别并标号
    list_label_35 = [0] * 35
    white_arr = get_white_arr()
    for one in get_messy_pictures_list9:
        if ((one == white_arr).all()):  # 如果是空白块则跳过，比较是否为同一个矩阵，需要加.all(),不然默认为比较矩阵元素内部的元素是否相等
            continue
        for i in range(35):
            for j in range(9):

                if (one == get_35photo_list35[i][j]).all():
                    list_label_35[i] += 1
    real_indx = list_label_35.index(8)  # 识别原图，得到原图在存储35张图片矩阵的位置
    lable_list_9 = []  # 将原图的九个小矩阵转为在原图的位置，如
    for i in range(9):
        lable_list_9.append(get_35photo_list35[real_indx][i].tolist())

    lable_list = []  # 存放打乱后的图片的数字标签

    for i in range(9):
        a = get_messy_pictures_list9[i].tolist()  # 将列表中的矩阵转换为列表
        if a == white_arr.tolist():
            lable_list.append(10)  # 先给白图一个标签10
            continue
        xiaotu_indx = lable_list_9.index(a)
        lable_list.append(xiaotu_indx)
    for i in range(9):  # 将白图的数值10更改为其原来的位置标签
        if i not in lable_list:
            white = i
    # white_index = lable_list.index(10)
    lable_list[lable_list.index(10)] = white
    lable_list = [lable_list[0:3], lable_list[3:6], lable_list[6:9]]
    for i in range(len(lable_list)):
        for j in range(len(lable_list)):
            if lable_list[i][j] == white:
                column = j
                row = i
    blank_coordinate = [row, column]  # 记录空白位置的坐标
    return lable_list, blank_coordinate,white



def solve(lable_list, blank_coordinate, step, swap):

    # total_route_list.append(blank_coordinate)#用来保存根节点到每个叶节点的路径
    if lable_list == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
        return  
    else:

        # 移动空白快的主要代码

        # blank_coordinate = [0,1]

        total_route_list = []  # 列表里面的每一个元素用来存放每一个叶节点的祖先
        total_list = []  # 用来存放每一个叶节点当前的3*3的列表状态
        total_route_list.append([blank_coordinate])  # 初始化根节点
        total_list.append(lable_list)  # 初始化当前3*3列表状态
        # print(total_route_list)
        # print(total_list)

        middle_route_list = []  # 添加节点前与添加节点后total_route_list的中间转化列表
        middle_list = []  # 添加节点前与添加节点后total_list的中间转化列表
        answer_list = []
        # for c in range(100):
        while True:

            if len(total_route_list[0]) == (step + 1):
                # print(len(total_list),total_list)
                # print(len(total_route_list[0]))
                for indx in range(len(total_list)):
                    # current_blank_coordinate = total_route_list[indx][-1]#当前状态的空白位置
                    # current_blank_num = total_list[indx][current_blank_coordinate[0]][current_blank_coordinate[1]]#当前状态的空白数字
                    # yiwei_list = total_list[indx][0] + total_list[indx][1] + total_list[indx][2]

                    change_coordinate1 = [(swap[0] - 1) // 3, (swap[0] - 1) % 3]  # 记录要交换的位置在3*3列表的位置
                    change_coordinate2 = [(swap[1] - 1) // 3, (swap[1] - 1) % 3]

                    # t = yiwei_list[swap[0] - 1]
                    # yiwei_list[swap[0] - 1] = yiwei_list[swap[1] - 1]
                    # yiwei_list[swap[1] - 1] = t
                    t = total_list[indx][change_coordinate1[0]][change_coordinate1[1]]
                    total_list[indx][change_coordinate1[0]][change_coordinate1[1]] = total_list[indx][change_coordinate2[0]][change_coordinate2[1]]
                    total_list[indx][change_coordinate2[0]][change_coordinate2[1]] = t
                    # 判断交换的两个图片是否有空图，有则更新空白图片的位置
                    if change_coordinate1 == total_route_list[indx][-1]:
                        total_route_list[indx][-1] = change_coordinate2
                    if change_coordinate2 == total_route_list[indx][-1]:
                        total_route_list[indx][-1] = change_coordinate1
                # print(total_list)
                # print(len(total_list),len(total_route_list[0]))

                                            
            
                return total_list,total_route_list,answer_list

            # 对每一条从根节点到叶节点的路径继续添加子节点
            for indx in range(len(total_route_list)):
                # print(len(total_route_list))
                blank_coordinate = total_route_list[indx][-1]  # 新添加的子节点的父节点
                # print(blank_coordinate)
                if len(total_route_list[indx]) > 1:
                    parent_blank_coordinate = total_route_list[indx][-2]  # 新添加子节点的爷爷节点，主要是防止空白块移动重复
                    # print(parent_blank_coordinate)

                # 得到可以与当前空白块移动的位置坐标
                child_coordinate_list = []
                if blank_coordinate == [0,0]:
                    child_coordinate_list = [[0,1],[1,0]]
                elif blank_coordinate == [0,1]:
                    child_coordinate_list = [[0,0],[0,2],[1,1]]
                elif blank_coordinate == [0,2]:
                    child_coordinate_list = [[0,1],[1,2]]
                elif blank_coordinate == [1,0]:
                    child_coordinate_list = [[0,0],[1,1],[2,0]]
                elif blank_coordinate == [1,1]:
                    child_coordinate_list = [[0,1],[1,0],[1,2],[2,1]]
                elif blank_coordinate == [1,2]:
                    child_coordinate_list = [[0,2],[1,1],[2,2]]
                elif blank_coordinate == [2,0]:
                    child_coordinate_list = [[2,1],[1,0]]
                elif blank_coordinate == [2,1]:
                    child_coordinate_list = [[2,0],[1,1],[2,2]]
                else:
                    child_coordinate_list = [[2,1],[1,2]]

                # print(child_coordinate_list)
                if len(total_route_list) > 1:  # 只要有多余一个节点，则每条路径都至少有两个节点存在
                    child_coordinate_list.remove(parent_blank_coordinate)

                # print(child_coordinate_list)
                # middle_route_list = []
                # middle_list = []
                # print(child_coordinate_list)
                for child_coordinate in child_coordinate_list:
                    # a = list.copy(total_route_list[indx])#得到一个新节点路径，保存着之前与当前空白块的移动位置
                    a = copy.deepcopy(total_route_list[indx])
                    a.append(child_coordinate)
                    middle_route_list.append(a)
                    # print(middle_route_list)
                    # 更新当前叶节点的3*3列表的状态
                    b = copy.deepcopy(total_list[indx])
                    t = 0
                    t = b[blank_coordinate[0]][blank_coordinate[1]]
                    b[blank_coordinate[0]][blank_coordinate[1]] = b[child_coordinate[0]][child_coordinate[1]]
                    b[child_coordinate[0]][child_coordinate[1]] = t

                    # print(total_list[indx])
                    # print(middle_list)
                    middle_list.append(b)
                    # print(middle_list)
                    # b = []

                    # 若当前列表状态为[[0,1,2],[3,4,5],[6,7,8]]，将路径保存在答案列表当中
                    if b == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
                        total_route_list = middle_route_list.copy()
                        total_list = middle_list.copy()
                        answer_list.append(a)

                        return  total_list,total_route_list,answer_list
                        # print(a)
            total_route_list = middle_route_list.copy()
            total_list = middle_list.copy()
            middle_route_list = []
            middle_list = []
            #  if answer_list:
            #     print(answer_list)
            #     break


def get_yes_best_answer(total_list,total_route_list,white):
    path = str(white) + '.pkl'
    with open(path, 'rb') as fo:     # 读取pkl文件数据
        dic = pickle.load(fo, encoding='bytes')
    yes_count_list = []
    yes_route_list = []
    yes_best_answer = ""
    
    for indx in range(len(total_list)):
        # key = str(total_list[indx]).replace(',',',')
        # print(key)
        if str(total_list[indx]) in dic:
            # print(total_route_list[indx])
            sentence1 = get_sequence(total_route_list[indx])

            sentence2 = dic[str(total_list[indx])]

            sentence = sentence1  + sentence2
            # print('yes')
            # return sentence
            yes_route_list.append(sentence)
            yes_count_list.append(len(sentence))
    if yes_count_list:
        min_count = min(yes_count_list)
        min_index = yes_count_list.index(min_count)
        # print("yes:",min_count)
        # print("yes:",min_index)
        yes_best_answer = yes_route_list[min_index]


    return yes_best_answer

def get_no_best_answer(total_list,total_route_list,white):
    path = str(white) + '.pkl'
    with open(path,'rb') as fo:
        dic = pickle.load(fo,encoding = 'bytes')

    no_route_list = []
    no_count_list = []
    change_list = []
    change = []
    no_best_answer = ""
    # print(len(total_list))
    
    for index in range(len(total_list)):
        if str(total_list[index]) not in dic:
            for i in range(0,8):
                for j in range(1,9):
                    a = copy.deepcopy(total_list[index])
                    i1 = i//3
                    i2 = i%3
                    j1 = j//3
                    j2 = j%3
                    t = a[i1][i2]
                    a[i1][i2] = a[j1][j2]
                    a[j1][j2] = t
                    if str(a) in dic:
                        sentence1 = get_sequence(total_route_list[index])
                        sentence2 = dic[str(a)]
                        # print(len(sentence2))

                        sentence = sentence1 + sentence2
                        change = [i+1,j+1]
                        no_route_list.append(sentence)
                        no_count_list.append(len(sentence))
                        change_list.append(change)
    if no_count_list:
       
        print(len(no_count_list))
        min_count = min(no_count_list)
        min_index = no_count_list.index(min_count)
        print("no:",min_count)
        no_best_answer = no_route_list[min_index]
        print(len(no_route_list))
        change = change_list[min_index]
    return no_best_answer,change

def get_sequence(blank_move_list):
    sequence = ""
    for i in range(len(blank_move_list) - 1):
        row1 = blank_move_list[i][0]
        col1 = blank_move_list[i][1]
        row2 = blank_move_list[i + 1][0]
        col2 = blank_move_list[i + 1][1]
        if row2 - row1 == 1:
            sequence += "s"
        elif row2 - row1 == -1:
            sequence += "w"
        elif col2 - col1 == 1:
            sequence += "d"
        else:
            sequence += "a"
    return sequence


if __name__ == '__main__':
    get_messy_pictures_list9, step, swap, uuid = get_messy_pictures_list9()
    print(step, swap)

    get_35photo_list35 = get_35photo_list35()

    lable_list, blank_coordinate,white = identify_label_pictures(get_messy_pictures_list9, get_35photo_list35)
    print(lable_list, blank_coordinate,white)

    # lable_list = [[1,4,5],[2,3,0],[7,6,8]]
    # lable_list = [[3,2,1],[6,0,5],[7,4,8]]
    # lable_list = [[3,1,2],[4,0,8],[6,5,7]]
    # lable_list = [[0,2,5],[1,3,6],[7,8,4]]
    # lable_list = [[0,1,2],[3,4,5],[7,8,9]]
    # lable_list = [[2,3,5],[4,6,8],[1,0,7]]
    # lable_list = [[2,6,3],[7,4,5],[1,0,8]]
    # lable_list = [[0,1,6],[7,4,3], [8,5,2]]
    # 11 [8, 3]
# [[0, 1, 2], [4, 5, 6], [3, 7, 8]] [1, 2] 6
# aas []
# {"owner":55,"rank":15,"step":3,"success":true,"timeelapsed":2166}
# 15 [2, 4]
# [[0, 1, 6], [7, 4, 3], [8, 5, 2]] [1, 1] 4
#  []
# {"owner":55,"rank":-1,"step":-1,"success":false,"timeelapsed":3572}


    # blank_coordinate = [1,1]
    # step = 15
    # swap = [2,4]
    # white = 4

    total_list,total_route_list,answer_list= solve(lable_list, blank_coordinate, step, swap)
    # print(len(total_route_list[0]))
    change = []
    best_answer = ""
    no_best_answer = ""
    yes_best_answer = get_yes_best_answer(total_list,total_route_list,white)
    if answer_list:
        best_answer = get_sequence(answer_list[0])
    elif yes_best_answer:
        yes_best_answer = get_yes_best_answer(total_list,total_route_list,white)
        best_answer = yes_best_answer
    else:
        no_best_answer,change = get_no_best_answer(total_list,total_route_list,white)
        best_answer = no_best_answer

    print(best_answer,change)
    # print(best_answer,change)

    # if answer_list:
    #     best_answer = get_sequence(answer_list[0])

    # else:
    #     yes_best_answer = get_yes_best_answer(total_list,total_route_list,white)
    #     best_answer = yes_best_answer
    # else:
    #     yes_best_answer = get_yes_best_answer(total_list,total_route_list,white)
    #     no_best_answer,change = get_no_best_answer(total_list,total_route_list,white)
    #     if len(yes_best_answer) == 0:
    #         best_answer = no_best_answer
    #     elif len(no_best_answer) == 0:
    #         best_answer = yes_best_answer
    #         change = []
    #     else:
    #         if len(yes_best_answer) <= len(no_best_answer):
    #             best_answer = yes_best_answer
    #             change = []
    #         else:
    #             best_answer = no_best_answer
    # print(best_answer,change)




url = "http://47.102.118.1:8089/api/challenge/submit"
hdata = {
    "uuid": uuid,
    "teamid": 55,
    "token": "6ef4189d-40b3-476e-bcd6-ca9cd9b24ce0",
    "answer": {
        "operations": best_answer,
        "swap": change,
    }
}

r = requests.post(url, json=hdata)
print(r.text)