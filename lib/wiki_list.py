from selenium.webdriver.common.by import By
from selenium import webdriver
from . import screenshot
import requests,re,json,os

# 截取网页
def wiki_all_list():
    # 定义wiki地址
    url="https://wiki.flapi.cn/doku.php?id=02%E8%81%94%E6%9C%BAmod%E5%8C%BA:0%E9%A6%96%E9%A1%B5"
    # 获取网页内容
    headers = {
        "User-Agent": "Chrome/76.0.3809.132",
        "Accept-Encoding": "deflate, gzip",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "charsets": "utf-8"
    }
    r = requests.get(url, headers=headers)
    # 通过正则表达式获取所有的mod
    mod_list = re.findall(r'jsdata = (.*?)\n', r.text, re.DOTALL)
    # 将json格式的字符串转换为字典
    mod_list = json.loads(mod_list[0])
    return mod_list['tree']

def wiki_get_mod_list_url(temp_list,url,path='.'):
    # 如果目录不存在则创建
    """ if not os.path.exists(path) and re.findall(r'原版',path):
        os.makedirs(path) """
    if not os.path.exists(path):
        os.makedirs(path)
    temp_url=[]
    for i in temp_list:
        if isinstance(i,dict):
            # 这个值是一个字典，说明这是一个目录
            temp_url_list=wiki_get_mod_list_url(i['s'],url+":"+i['i'],path+"/"+i['i'])
            #将返回的数组合并到temp_url中
            temp_url.extend(temp_url_list)
        elif isinstance(i,list):
            # 这个值是一个列表，说明不会有子目录
            """ if not re.findall(r'原版',path):
                continue """
            for j in i:
                temp_url.append([url+":"+i+':'+j,path+'/'+j])
        else:
            # 这是一个页面,说明不会有子目录
            """ if not re.findall(r'原版',path):
                continue """
            temp_url.append([url+":"+i,path+'/'+i])
    return temp_url

def wiki_get_mod_list_url_count(temp_list):
    temp_url_count=0
    for i in temp_list:
        if isinstance(i,dict):
            # 这个值是一个字典，说明这是一个目录
            temp_url_list_count=wiki_get_mod_list_url_count(i['s'])
            #将返回的数据合并
            temp_url_count+=temp_url_list_count
        elif isinstance(i,list):
            # 这个值是一个列表，说明不会有子目录
            for j in i:
                temp_url_count+=1
        else:
            # 这是一个页面,说明不会有子目录
            temp_url_count+=1
    return temp_url_count

def wiki_get_key_value(temp_list,url,path='.'):
    temp_value_list={}
    for i in temp_list:
        if isinstance(i,dict):
            # 这个值是一个字典，说明这是一个目录
            temp_list=wiki_get_key_value(i['s'],url+":"+i['i'],path+"/"+i['i'])
            #将返回的字典合并
            temp_value_list.update(temp_list)
        elif isinstance(i,list):
            # 这个值是一个列表，说明不会有子目录
            for j in i:
                temp_value_list[j]=[path+'/'+j,url+":"+i+':'+j]
        else:
            # 这是一个页面,说明不会有子目录
            temp_value_list[i]=[path+'/'+i,url+":"+i]
    return temp_value_list

# 定义一个用于补全目录的函数(传入一个路径,然后依次补全)
def path_complete(path):
    # 先分割路径
    path_list=path.split('/')
    # 定义一个用于存放路径的变量
    path_temp=''
    # 遍历路径
    for i in path_list:
        # 如果是最后一个路径,则不需要补全
        if i==path_list[-1]:
            break
        # 如果路径为空,则跳过
        if i=='' or i=='.':
            continue
        # 如果路径不为空,则补全路径
        if(path_temp==''):
            path_temp=i
        else:
            path_temp=path_temp+'/'+i
        # 如果路径不存在,则创建
        if not os.path.exists(path_temp):
            os.makedirs(path_temp)

def select(name):
    wiki_url='https://wiki.flapi.cn/doku.php?id='
    temp_list=wiki_all_list()
    temp_key_value=wiki_get_key_value(temp_list,wiki_url,'./temp')
    if not name in temp_key_value:
        print('没有找到这个物品')
        return
    temp_select=temp_key_value[name]
    path_complete(temp_select[0])
    driver = webdriver.Chrome(executable_path='driver/chromedriver.exe')
    try:
        screenshot.wiki_screenshot(temp_select[1],driver,temp_select[0],100)
    except Exception as e:
        print(e)
    driver.quit()

""" list_count=wiki_list.wiki_get_mod_list_url_count(temp_list)
temp_count=0
temp_error_count=0
# 注意,path=dir dir必须是一个存在的目录
url_list=wiki_list.wiki_get_mod_list_url(temp_list,wiki_url,path='./temp')
driver = webdriver.Chrome(executable_path='driver/chromedriver.exe')
for(i,j) in url_list:
    temp_count+=1
    try:
        print('正在爬取第'+str(temp_count)+'/'+str(list_count)+'个页面('+str(temp_count/list_count*100)+'%) 共失败'+str(temp_error_count)+'个: '+i)
        # 这里经过优化,其实 widith 的值已经不再重要,但这里还是保留了,这个值越小速度越慢,值最大不能超过最大的可视区域
        screenshot.wiki_screenshot(i,driver,j,500)
    except Exception as e:
        print('爬取'+str(temp_count)+'/'+str(list_count)+'个页面时失败('+str(temp_count/list_count*100)+'%) 共失败'+str(temp_error_count)+'个: '+i)
        print(e)
        temp_error_count+=1
driver.quit()
 """

""" main.py
from selenium import webdriver
from lib import screenshot

wiki_url='https://wiki.flapi.cn/doku.php?id='
temp_list=wiki_list.wiki_all_list()
list_count=wiki_list.wiki_get_mod_list_url_count(temp_list)
temp_count=0
temp_error_count=0
# 注意,path=dir dir必须是一个存在的目录
url_list=wiki_list.wiki_get_mod_list_url(temp_list,wiki_url,path='./temp')
driver = webdriver.Chrome(executable_path='driver/chromedriver.exe')
for(i,j) in url_list:
temp_count+=1
try:
    print('正在爬取第'+str(temp_count)+'/'+str(list_count)+'个页面('+str(temp_count/list_count*100)+'%) 共失败'+str(temp_error_count)+'个: '+i)
    # 这里经过优化,其实 widith 的值已经不再重要,但这里还是保留了,这个值越小速度越慢,值最大不能超过最大的可视区域
    screenshot.wiki_screenshot(i,driver,j,500)
except Exception as e:
    print('爬取'+str(temp_count)+'/'+str(list_count)+'个页面时失败('+str(temp_count/list_count*100)+'%) 共失败'+str(temp_error_count)+'个: '+i)
    print(e)
    temp_error_count+=1
driver.quit() """