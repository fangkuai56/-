import os
from pandas.core.frame import DataFrame
 
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root) #当前目录路径（包含所有子目录）
        print("===============")
        #print(dirs) #当前路径下所有子目录（同一路径下的存一个列表中）
        print("===============")
        a=DataFrame(files) #当前路径下所有非目录子文件（同一路径下的存一个列表中）--列表变矩阵框
        a.to_excel("/Users/jinyuxin/Desktop/虚拟偶像语音合成模型/提取派蒙文件名.xlsx",header=0,index=0)#保存到指定路径下
 
file_name("/Users/jinyuxin/Desktop/虚拟偶像语音合成模型/dataset/Paimon")#文件夹路径

