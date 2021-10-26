import cv2
#import numpy as np
#from PIL import Image #图像处理库PIL-convert()

dot_pos = {'\0'}
i = 0
real_x = 0
real_y = 0
mode = 0

img = cv2.imread("./new.bmp") #读取图片
#img2 = Image.fromarray(np.uint8(img1))
#img = img1.convert("1") #PIL的方法 转成二值图像
fo = open("dat.txt", "w") 
fo1 = open("result.txt", "w")

#向x正方向走一个像素点
def xcorr_one(x, y):
    #fo1.write("PA"+x1+'0'+','+y1+'0')
    fo1.write("PU;")
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x+1) + ',' + str(y) + ';')

#向x负方向走一个像素点
def xfalse_one(x, y):
    fo1.write("PU;")
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x-1) + ',' + str(y) + ';')

#向y正方向走一个像素点
def ycorr_one(x, y):
    fo1.write("PU;")
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x) + ',' + str(y+1) + ';')

#向y负方向走一个像素点
def yfalse_one(x, y):
    fo1.write("PU;")
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x) + ',' + str(y-1) + ';')

#向左上方走一个像素点
def x_135_one(x, y):
    fo1.write("PU;")
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x-1) + ',' + str(y-1) + ';')

#向左下方走一个像素点
def x_225_one(x, y):
    fo1.write("PU;")
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x-1) + ',' + str(y+1) + ';')

#向右上方走一个像素点
def x_45_one(x, y):
    fo1.write("PU;")
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x+1) + ',' + str(y-1) + ';')

#向右下方走一个像素点
def x_315_one(x, y):
    fo1.write("PU;")
    fo1.write("PA" + str(x) + ',' + str(y) + ';' + "PD;" + "Pr" + str(x+1) + ',' + str(y+1) + ';')


functions = {
                0x10: xcorr_one(real_x, real_y),
                0x11: xfalse_one(real_x, real_y),
                0x12: ycorr_one(real_x, real_y),
                0x13: yfalse_one(real_x, real_y),
                0x14: x_45_one(real_x, real_y),
                0x15: x_135_one(real_x, real_y),
                0x16: x_315_one(real_x, real_y),
                0x17: x_225_one(real_x, real_y)
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
-------0 0 0         从左往右，从上往下 依次从低位排起
-------1 0 1
'''

def binary_create(x, y, bind):
    bind = judge(img, x-1, y)<<7 | judge(img, x-1, y+1)<<6 | judge(img, x, y+1)<<5 | judge(img, x+1, y+1)<<4 |\
             judge(img, x+1, y)<<3 | judge(img, x+1, y-1)<<2 | judge(img, x, y-1)<<1 | judge(img, x-1, y-1)
    

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
            #if(judge(img, real_x, real_y))
            binary_create(real_x, real_y, mode)
            func = functions[mode]
            
        print('\n')
        fo1.write('\n')
    fo1.close()
    
    cv2.namedWindow("Image")
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

