import mss
import cv2
import numpy as np
import pyautogui as pg
import time
import random
import quanju
    
def detecter(source_name,template_name):
    screenshot = mss.mss().shot(output='numpy.jpg') 
# 读取源图像和模板图像
    source_image = cv2.imread(source_name, 0)  # 以灰度模式读取
    template_image = cv2.imread(template_name, 0)  # 以灰度模式读取

# 获取模板图像的宽度和高度
    w, h = template_image.shape[::-1]

# 使用cv2.matchTemplate函数进行模板匹配
    res = cv2.matchTemplate(source_image, template_image, cv2.TM_CCOEFF_NORMED)

# 设置一个阈值，低于该阈值的匹配将被忽略
    threshold = 0.9
    loc = np.where(res >= threshold)

# 如果找到了匹配项，则绘制矩形框并计算中心点位置
    if loc[0].size > 0:
        for pt in zip(*loc[::-1]):
            cv2.rectangle(source_image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
        # 计算中心点位置
            center_x = pt[0] + w // 2
            center_y = pt[1] + h // 2
        # 在源图像上绘制中心点
            cv2.circle(source_image, (center_x, center_y), 5, (255, 0, 0), -1)
            print(f"匹配成功！中心点位置: ({center_x}, {center_y})")
            return(center_x,center_y)
    else:
        print("未找到匹配项。")
        return False

'''
# 显示结果图像
    cv2.imshow('Detected', source_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''

def mouse_mover(center_x,center_y):
    pg.moveTo(center_x, center_y,duration=0.5)
    time.sleep(1)
    pg.click(center_x, center_y,duration=0.5)
    time.sleep(random.randint(3,4))
    #pg.click(center_x, center_y,duration=0.1)  #为了防止弹出今日首胜

def next_page(pics,first_ornot,x,opp_win_lose):
    
    if detecter("numpy.jpg","xx.jpg") or  x:
        while not detecter("numpy.jpg","toindex.jpg"):

            x,y=detecter("numpy.jpg","xx.jpg")
            print(f"x坐标：{x},{y}")
            mouse_mover(x,y)
            print("已点击X")
        while not detecter("numpy.jpg","join.jpg"):
            x,y=detecter("numpy.jpg","toindex.jpg")
            mouse_mover(x,y)
            print("已点击<-")
        while not detecter("numpy.jpg","join_10+0.jpg"):   

            x,y=detecter("numpy.jpg","join.jpg")
            mouse_mover(x,y)
            print("已点击+")

        #if detecter("numpy.jpg","join_10+0.jpg"):
        x,y=detecter("numpy.jpg","join_10+0.jpg")
        mouse_mover(x,y)
        print("已点击下一轮")
        nextpage_win_lose(opp_win_lose)
        print("下一局胜负:%d"%(quanju.win_or_not))
        while not detecter("numpy.jpg","white\\Rooks.jpg"):
            time.sleep(1)
        return True
    else:
        print("还没有到下一局，继续")
        return False

def nextpage_win_lose(opp_win_lose):
    
    num = random.randint(0, 100) 
    quanju.win_or_not=1 if num<=opp_win_lose else 0
     
    
