import argparse
import functools
import numpy as np
import tensorflow as tf
from utils.reader import load_audio
from utils.utility import add_arguments, print_arguments
import os,shutil
import gc

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('audio_path1',      str,    './audio_db/Paimon.wav',          '标准的派蒙音频')   # 自己准备的标准音频，下面两个也是
add_arg('input_shape',      str,    '(257, 257, 1)',          '数据输入的形状')
add_arg('threshold',        float,   0.75,                     '判断是否为同一个人的阈值')
add_arg('model_path',       str,    './models/infer_model.h5',  '预测模型的路径')    # 训练模型
args = parser.parse_args()

# 加载模型
model = tf.keras.models.load_model(args.model_path,compile=False)
model = tf.keras.models.Model(inputs=model.input, outputs=model.get_layer('batch_normalization').output)

# 数据输入的形状
input_shape = eval(args.input_shape)

# 预测音频
def infer(audio_path):
    data = load_audio(audio_path, mode='test', spec_len=input_shape[1])
    data = data[np.newaxis, :]
    feature = model.predict(data)
    return feature

if __name__ == '__main__':
    # 预测的两个音频文件
    feature1 = infer(args.audio_path1)[0]
    #   feature2 = infer(args.audio_path2)[0]
    # feature3 = infer(args.audio_path3)[0]
    datapath = "../dataset/paimon2"        #上传到集群的解包音频文件位置

    dirs = os.listdir(datapath)
    for audio in dirs:
        personx = '../dataset/paimon2/%s' % (audio)
        featurex = infer(personx)[0]
    # 对角余弦值
        dist1 = np.dot(feature1, featurex) / (np.linalg.norm(feature1) * np.linalg.norm(featurex))
        #if dist1 > args.threshold:
        if dist1 <= args.threshold:
            print("%s 符合派蒙模型，相似度为：%f" % (personx, dist1))
            shutil.move("../dataset/paimon/%s" % (audio),"../dataset/others2")      # 移动音频文件，路径自选
        #else:
         #   shutil.move("/Users/jinyuxin/Desktop/虚拟偶像语音合成模型/dataset/Paimon/%s" % (audio),"/Users/jinyuxin/Desktop/虚拟偶像语音合成模型/dataset/others")      # 移动音频文件，路径自选
        # else:
        #     dist2 = np.dot(feature2, featurex) / (np.linalg.norm(feature2) * np.linalg.norm(featurex))
        #     if dist2 > args.threshold:
        #         print("%s 符合可莉模型，相似度为：%f" % (personx, dist2))
        #         shutil.move("./test2/%s" % (audio),"./dataset/Klee")
        #     else:
        #         dist3 = np.dot(feature3, featurex) / (np.linalg.norm(feature3) * np.linalg.norm(featurex))
        #         if dist3 > args.threshold:
        #             print("%s 符合心海模型，相似度为：%f" % (personx, dist3))
        #             shutil.move("./test2/%s" % (audio),"./dataset/Kokomi")
        gc.collect()
