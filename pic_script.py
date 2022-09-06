import cv2,os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

############旋转图像,参数中的旋转角度可正可负#######################
def rotate_pic(src,angle,centerPoint):###angle为旋转角度(支持正负角度),centerPoint为旋转中心的坐标
    print(centerPoint)
    M = cv2.getRotationMatrix2D(centerPoint, angle, 1)######cv2.getRotationMatrix2D(旋转中心点坐标,旋转角度,缩放比例)
    im = cv2.warpAffine(src, M, (src.shape[1]*2, src.shape[0]*2))####cv2.warpAffine(图像,仿射矩阵,(旋转后的图像宽,旋转后的图像高))
    return im

#######################在图片上写汉字##############################
def cv2AddChineseText(src,text, position=(10,10), textColor=(0, 255, 0), textSize=30):
    if (isinstance(src, np.ndarray)):  # 判断是否OpenCV图片类型
        src = Image.fromarray(cv2.cvtColor(src, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(src)
    # 字体的格式
    fontStyle = ImageFont.truetype("simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    dst=cv2.cvtColor(np.asarray(src), cv2.COLOR_RGB2BGR)
    return dst

#######################将图片合成视频##############################
def frame2video(srcPath, videoname):
    ls_src=os.listdir(srcPath)
    frame = cv2.imread(srcPath+os.sep+ls_src[0])
    size_raw = frame.shape
    size = (size_raw[1], size_raw[0])
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(videoname, fourcc, 1, size)
    for i in ls_src:
        frame = cv2.imread(srcPath+os.sep+i)
        out.write(frame)
    out.release()

#########################抽帧#####################################
def video2frame(mp4Path,framePath):
    camera = cv2.VideoCapture(mp4Path)
    num = 0
    while True:
        res, image = camera.read()
        if res:
            num+=1
            cv2.imwrite(framePath+os.sep+str(num)+".jpg",image)
        else:
            print('MP4抽帧完成')
            break
    camera.release()

###################横向拼接srcPath下的所有图片######################
def hengxiang_pingjie(srcPath):
    ls_src=[]
    for i in os.listdir(srcPath):
        src=cv2.imread(srcPath+os.sep+i)
        ls_src.append(src)
    ls_pj=[]
    maxh=max([j.shape[0] for j in ls_src])
    for p in ls_src:
        pdfaceimg = np.zeros((maxh, p.shape[1], 3), np.uint8)
        pdfaceimg[0:p.shape[0],0:p.shape[1]]=p
        ls_pj.append(pdfaceimg)
    dst=cv2.hconcat(ls_pj)
    return dst

###################竖向拼接srcPath下的所有图片######################
def shuxiang_pingjie(srcPath):
    ls_src=[]
    for i in os.listdir(srcPath):
        src=cv2.imread(srcPath+os.sep+i)
        ls_src.append(src)
    ls_pj=[]
    maxw=max([j.shape[1] for j in ls_src])
    for p in ls_src:
        pdfaceimg = np.zeros((p.shape[0],maxw, 3), np.uint8)
        pdfaceimg[0:p.shape[0],0:p.shape[1]]=p
        ls_pj.append(pdfaceimg)
    dst=cv2.vconcat(ls_pj)
    return dst

if __name__ == '__main__':
    jpgPath="D:/DataSet/bfzhao/srcPath/data4/imgs/7361f03ff080a9c687bc97bd31c4b98f-2aaab569b69cb4e3b8459a9377d2abbe44d9631a.jpg"
    src=cv2.imread(jpgPath)
    x=src.shape[1]/2
    y=src.shape[0]/2
    dst0=rotate_pic(src, 45, (x,y))
    dst1=cv2AddChineseText(src, "王姣姣", position=(10, 10), textColor=(0, 255, 0), textSize=30)
    srcPath="D:/DataSet/bfzhao/srcPath/data1/img/"
    videoname="D:/DataSet/bfzhao/srcPath/data1/res/video.mp4"
    frame2video(srcPath, videoname)
    mp4Path="D:/DataSet/bfzhao/srcPath/data2/mp4/ch01001_20220815094853.mp4.cut.mp4"
    framePath="D:/DataSet/bfzhao/srcPath/data2/res/"
    video2frame(mp4Path, framePath)
    srcPath_pj="D:/DataSet/bfzhao/srcPath/data3/imgs/"
    hxpj=hengxiang_pingjie(srcPath_pj)
    sxpj=shuxiang_pingjie(srcPath_pj)

