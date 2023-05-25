# import re
#
# emotion={
#     '[尴尬]': -1 }
# def analysisEmo(text):
#     ''' 判断是否含有表情，返回1则为正向，-1为负向，0则无法判断，需要根据句子情感值判断 '''
#     sentence_emo=[]
#     n = re.findall(r"\[(.+?)\]", str(text))
#     if len(n):
#         for k in n:
#             if '['+k+']' in emotion:
#                 sentence_emo.append(emotion['['+k+']'])
#     finnal_emo=0
#     for i in sentence_emo:
#         finnal_emo+=i
#     if finnal_emo>0:
#         return 1
#     if finnal_emo==0:
#         return 0
#     if finnal_emo<0:
#         return -1
# print(analysisEmo("哈哈哈哈[尴尬]"))
import os

directory = r'../video'
filepath = '../video/DouyinVideo.mp4'
if (os.path.exists(filepath)):
    os.remove(filepath)