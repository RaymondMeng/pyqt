import cv2
#import numpy as np
#from PIL import Image #图像处理库PIL-convert()

#第二版于2021.10.26 15：00修改
#整体思想：激光点不作为mode的中心，因为这样无法区分前进方向，改为右下角，遍历通过判断小正方形的某一边来判断状态机的值
#从而判断前进方向

#第三版于2021.10.26 15：52修改
#激光点还是作为mode中心，可以通过一个方向指针来指引方向

#后续想法，引入链表等数据结构，有方向性的指引，并且有头有尾

dot_pos = {'\0'}
i = 0
real_x = 0 #真实x坐标
real_y = 0 #真实y坐标
mode = 0 #激光点四周点的情况
direct_p = 0 #方向指针：0：不动  1：向右前进  2：向左前进  3：向上前进  4：向下前进  5：向左上方前进  6：向左下方前进  7：向右上方前进  8：向右下方前进

img = cv2.imread("./new.bmp") #读取图片
#img2 = Image.fromarray(np.uint8(img1))
#img = img1.convert("1") #PIL的方法 转成二值图像
fo = open("dat.txt", "w") 
fo1 = open("result.txt", "w")

#向x正方向走一个像素点
def xcorr_one(x, y):
    #fo1.write("PA"+x1+'0'+','+y1+'0')
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x+1) + ',' + str(y) + ';')
    fo1.write("PU;")
    real_x = x+1
    real_y = y
    direct_p = 1

#向x负方向走一个像素点
def xfalse_one(x, y):
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x-1) + ',' + str(y) + ';')
    fo1.write("PU;")
    real_x = x-1
    real_y = y
    direct_p = 2

#向y正方向走一个像素点
def ycorr_one(x, y):
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x) + ',' + str(y+1) + ';')
    fo1.write("PU;")
    real_x = x
    real_y = y+1
    direct_p = 4

#向y负方向走一个像素点
def yfalse_one(x, y):
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x) + ',' + str(y-1) + ';')
    fo1.write("PU;")
    real_x = x
    real_y = y-1
    direct_p = 3

#向左上方走一个像素点
def x_135_one(x, y):
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x-1) + ',' + str(y-1) + ';')
    fo1.write("PU;")
    real_x = x-1
    real_y = y-1
    direct_p = 5

#向左下方走一个像素点
def x_225_one(x, y):
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x-1) + ',' + str(y+1) + ';')
    fo1.write("PU;")
    real_x = x-1
    real_y = y+1
    direct_p = 6

#向右上方走一个像素点
def x_45_one(x, y):
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x+1) + ',' + str(y-1) + ';')
    fo1.write("PU;")
    real_x = x+1
    real_y = y-1
    direct_p = 7

#向右下方走一个像素点
def x_315_one(x, y):
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x+1) + ',' + str(y+1) + ';')
    fo1.write("PU;")
    real_x = x+1
    real_y = y+1
    direct_p = 8


functions = {
                0x28: xcorr_one(real_x, real_y), #x正方向
                0x82: xfalse_one(real_x, real_y), #x负方向
                0x0a: ycorr_one(real_x, real_y), #y正方向
                0xa0: yfalse_one(real_x, real_y), #y负方向
                0x14: x_45_one(real_x, real_y), 
                0x15: x_135_one(real_x, real_y),
                0x16: x_315_one(real_x, real_y),
                0x17: x_225_one(real_x, real_y),
                0x28: xcorr_one(real_x, real_y),
                0x22: xcorr_one(real_x, real_y) if direct_p == 1 else xfalse_one(real_x, real_y), #判断前进方向
                0x88: ycorr_one(real_x, real_y) if direct_p == 4 else yfalse_one(real_x, real_y),
                0x00: 0
            }

def judge(imge, x, y): 
    
    Grey = imge[y, x, 0] * 299 / 1000 + imge[y, x, 1] * 587 / 1000 + imge[y, x, 2] * 114 / 1000
    if Grey == 255:
        return 0
    elif Grey == 0:
        return 1
    else:
        return 0

'''    
#初步想法：弄一个状态机，就是循迹吧，把周围8个像素点变成一个二进制数串，然后进行判断
def order_FSM(bin):
    s
'''

#像素点的周围8个点的颜色情况
'''
-------1 0 1           01010101
-------0 0 0         从左往右，从上往下 依次从高位排起
-------1 0 1
'''

def binary_create(x, y, bind):
    bind = judge(img, x, y-1)<<7 | judge(img, x+1, y-1)<<6 | judge(img, x+1, y)<<5 | judge(img, x+1, y+1)<<4 |\
             judge(img, x, y+1)<<3 | judge(img, x-1, y+1)<<2 | judge(img, x-1, y)<<1 | judge(img, x-1, y-1)
    

if __name__ == "__main__":
    #px = img[200, 100]
    #print(px)
    size = img.shape
    print (size)
    
    for i in range(size[0]):   
        for j in range(size[1]):
            real_x = i
            real_y = j
            #print(judge(img, j, i)+'0')
            #fo.write(judge(img, j, i)+'0')
            #count = 0 
            if(judge(img, real_y, real_x)): #如果第一次识别到黑像素点开始激光雕刻 
                break
        if(judge(img, real_y, real_x)):
            break
    while(judge(img, real_y, real_x)):
        binary_create(real_y, real_x, mode)
        func = functions[mode]
        print('\n')
        fo1.write('\n')
    fo1.close()
    
    cv2.namedWindow("Image")
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

