from lib import wiki_list
from selenium.webdriver.common.by import By
from selenium import webdriver
from lib import screenshot

wiki_list.select("巨大化魔法")

""" wiki_url='https://wiki.flapi.cn/doku.php?id='
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