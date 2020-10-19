import copy,json
import pickle
from time import *

def get_sequence(blank_move_list):
    sequence = ""
    for i in range(len(blank_move_list) - 1):
        row1 = blank_move_list[i][0]
        col1 = blank_move_list[i][1]
        row2 = blank_move_list[i + 1][0]
        col2 = blank_move_list[i + 1][1]
        if row2 - row1 == 1:
            sequence += "w"
        elif row2 - row1 == -1:
            sequence += "s"
        elif col2 - col1 == 1:
            sequence += "a"
        else:
            sequence += "d"
    return sequence

begin_time = time()

# dic = dict()
# print(len(all_list))
all_route_list = []
all_list = []

total_route_list = []
blank_coordinate = [0,1]
total_route_list.append([blank_coordinate])

total_list = []
lable_list= [[0,1,2],[3,4,5],[6,7,8]]
total_list.append(lable_list)

middle_list =[]
middle_route_list = []

print(len(total_route_list))
for i in range(30):
    print(i)

    for indx in range(len(total_route_list)):
        # print(len(total_route_list))
        blank_coordinate = total_route_list[indx][-1]  # 新添加的子节点的父节点
        # print(blank_coordinate)
        if len(total_route_list[indx]) > 1:
            parent_blank_coordinate = total_route_list[indx][-2]  # 新添加子节点的爷爷节点，主要是防止空白块移动重复
            # print(parent_blank_coordinate)

        # 得到可以与当前空白块移动的位置坐标
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

        if len(total_route_list) > 1:  # 只要有多余一个节点，则每条路径都至少有两个节点存在
            child_coordinate_list.remove(parent_blank_coordinate)

        
        for child_coordinate in child_coordinate_list:
            ## a = list.copy(total_route_list[indx])#得到一个新节点路径，保存着之前与当前空白块的移动位置
            a = copy.deepcopy(total_route_list[indx])
            # a = total_route_list[indx].copy()
            a.append(child_coordinate)
            
            # print(middle_route_list)
            # 更新当前叶节点的3*3列表的状态
            b = copy.deepcopy(total_list[indx])
            # b = total_list[indx].copy()
            t = 0
            t = b[blank_coordinate[0]][blank_coordinate[1]]
            b[blank_coordinate[0]][blank_coordinate[1]] = b[child_coordinate[0]][child_coordinate[1]]
            b[child_coordinate[0]][child_coordinate[1]] = t
          
            middle_route_list.append(a)
            middle_list.append(b)
            # if b not in total_list:
            #     middle_route_list.append(a)  #使用这些筛选代码用时会非常的长
            #     middle_list.append(b)

            if b not in all_list:
                all_list.append(b)
                all_route_list.append(a)
    # middle_m_list = set(middle_list)/

            
    if i >= 15 and i !=26  :
        begin_time1 = time()
        # res = [middle_list.index(x) for x in set(middle_list)]
        middle_m_list = [str(i) for i in middle_list]
        se = set(middle_m_list)
        
        res = []
        # res = [middle_list.index(x) for eval(x) in se]

        for i in range(len(se)):
            a = middle_list.index(eval(list(se)[i]))
            res.append(a)
        del_res = {i for i in range(len(middle_list))} - set(res)
        # print(len(del_res))
        # print(len(middle_list))
        count = 0
        y = list(del_res)
        y.sort()

        # print(y)
        for j in y :
            del middle_list[j-count]
            del middle_route_list[j-count]
            count += 1
        end_time1 = time()

        print(begin_time1 - end_time1)

    #     middle_m_route_list = []
    #     middle_m_list = []
    #     for i in middle_list:
    #         if not i in middle_m_list:
    #             middle_m_list.append(i)
    #             middle_m_route_list.append(i)
    #     # middle_list = middle_m_list.copy()
    #     # middle_route_list = middle_m_route_list.copy()
    #     middle_list = copy.deepcopy(middle_m_list)
    #     middle_route_list = copy.deepcopy(middle_m_route_list)
    #     del middle_m_list,middle_m_route_list

    
    total_route_list = middle_route_list.copy()
    total_list = middle_list.copy()
    # print(len(total_list))
    print(len(total_route_list))
    print(len(all_list))
    # print(len(all_list))
    # print(len(all_route_list))
    middle_route_list = []
    middle_list = []

    if len(all_list) > 177000:
        break

all_sentence = []
print(len(all_list))
for i in range(len(all_route_list)):
    sentence = get_sequence(all_route_list[i])
    sentence = sentence[::-1]
    all_sentence.append(sentence)
print(len(all_sentence))

str_all_list = []
for i in range(len(all_route_list)):
    str_all_list.append(str(all_list[i]))

# print(str_all_route_list)

dic =dict()
for i in range(len(str_all_list)):
    key = str_all_list[i]

    dic[key] = all_sentence[i]


with open("11.pkl", 'wb') as t:     # 将数据写入pkl文件
    pickle.dump(dic, t)

end_time = time()
print("用时:",end_time - begin_time)


# with open("11.pkl", 'rb') as fo:     # 读取pkl文件数据
#     dict_data = pickle.load(fo, encoding='bytes')
  
# # print(dict_data.keys())    # 测试我们读取的文件
# # print(dict_data)
# print(dict_data["[[2, 4, 5], [1, 0, 8], [3, 6, 7]]"])


# # "[[2, 4, 5], [1, 0, 8], [3, 6, 7]]": "wassddwwaa"