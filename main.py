import cv2
#import numpy as np
#from PIL import Image #图像处理库PIL-convert()


img = cv2.imread("./new.bmp") #读取图片
#img2 = Image.fromarray(np.uint8(img1))
#img = img1.convert("1") #PIL的方法 转成二值图像
fo = open("dat.txt", "w") 


def judge(imge, x, y): 
    Grey = imge[y, x, 0] * 299 / 1000 + imge[y, x, 1] * 587 / 1000 + imge[y, x, 2] * 114 / 1000
    if Grey == 255:
        return '0'
    elif Grey == 0:
        return '1'
    else:
        return '0'
    
if __name__ == "__main__":
    #px = img[200, 100]
    #print(px)
    size = img.shape
    print (size)
    
    for i in range(size[0]):   
        for j in range(size[1]):
            print(judge(img, j, i))
            fo.write(judge(img, j, i))
        print('\n')
        fo.write('\n')
    fo.close()
    
    cv2.namedWindow("Image")
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

