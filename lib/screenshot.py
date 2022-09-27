from selenium.webdriver.common.by import By
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time,os

def wiki_screenshot(url,driver,path,width=500):
    #driver = webdriver.Chrome()
    window_width = driver.get_window_size()['width']
    driver.set_window_size(window_width, width+160)
    driver.get(url)
    # 假设可视区域高度
    window_height = width
    # 获取元素高度
    element_height = driver.find_element(By.CLASS_NAME, 'page').size['height']
    # 更新元素起始位置
    element_y = driver.find_element(By.CLASS_NAME, 'page').location['y']
    # 计算需要滚动的次数
    scroll_times = element_height / window_height
    # 如果是整数，就不用加1
    if scroll_times % 1 == 0:
        scroll_times = int(scroll_times)
    else:
        scroll_times = int(scroll_times) + 1
    # 这个用于存储裁剪周期(当浏览器无法滚动到底部时,会出现多次裁剪同一区域的情况)
    crop_cycle=0
    # 定义一个变量用于存储滚动条最后一次距离底部的距离
    distance_to_bottom=0
    for i in range(scroll_times):
        # 如果图片需要反复裁剪,则不需要再次滚动(提供效率)
        if crop_cycle==0:
            # 计算出滚动条离页面底部的距离
            distance_to_bottom = driver.execute_script("return document.body.scrollHeight - window.pageYOffset - window.innerHeight")
            # 滚动到元素可视区域
            driver.execute_script("window.scrollTo(0, {})".format(element_y))
            # 截图
            driver.find_element(By.CLASS_NAME, 'page').screenshot(path+str(i)+'page.png')
        # 如果有图片则拼接
        page=Image.open(path+str(i)+'page.png')
        # 裁剪图片,只要可视区域(如果是最后一次滚动,则裁剪剩余部分)
        start_crop_height=0
        if i == scroll_times - 1:
            # 最后一次滚动,裁剪剩余部分
            crop_height = element_height - window_height * i
        else:
            crop_height = window_height
        # 这里还有一种情况,一次可滚动距离可能不足一个可视区域
        if distance_to_bottom < window_height:
            # 裁剪开始的位置需要加上裁剪周期
            start_crop_height = window_height - distance_to_bottom - 17 + crop_cycle*window_height
            crop_height=crop_height+start_crop_height
            # 裁剪周期+1
            crop_cycle+=1
        crop_box = (0, start_crop_height, page.width, crop_height)
        page = page.crop(crop_box)
        try:
            page.save(path+str(i)+'crop.png')
        except:
            print('裁剪失败','详细信息:','裁剪区域: '+str(crop_box),'图片大小: '+str(page.size))
        if i!=0:
            # 拼接图片(新图片在下)
            input=Image.open(path+'input.png')
            newImage = Image.new('RGB', (page.width, page.height + input.height))
            newImage.paste(input, (0, 0))
            newImage.paste(page, (0, input.height))
            page=newImage
        page.save(path+'input.png')
        # 获取下一个可视区域的元素起始位置
        element_y += window_height
    # 截取 docInfo 类
    docInfo = driver.find_element(By.CLASS_NAME, 'docInfo')
    # 滚动到元素可视区域
    driver.execute_script("arguments[0].scrollIntoView();", docInfo)
    # 截图
    docInfo.screenshot(path+'docInfo.png')
    # 将图片合并
    page = Image.open(path+'input.png')
    docInfo = Image.open(path+'docInfo.png')
    newImage = Image.new('RGB', (page.width, page.height + docInfo.height))
    newImage.paste(page, (0, 0))
    newImage.paste(docInfo, (0, page.height))
    # 获取当前时间
    now = time.strftime('%Y-%m-%d %H:%M:%S'+" Boringmj Bot", time.localtime(time.time()))
    # 图片加上当前时间(字体大小为 20,颜色为红色)
    draw = ImageDraw.Draw(newImage)
    draw.text((0, 0), now, (255, 0, 0), font=ImageFont.truetype('C:\\Windows\\Fonts\\Arial.ttf', 12))
    # 保存图片
    newImage.save(path+'wiki.png')
    # 删除临时文件
    for i in range(scroll_times):
        os.remove(path+str(i)+'page.png')
        os.remove(path+str(i)+'crop.png')
    os.remove(path+'input.png')
    os.remove(path+'docInfo.png')
    # 关闭浏览器
    #driver.quit()