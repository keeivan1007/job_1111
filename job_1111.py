"""
purpose:讀取資料庫,抓job裡面然後job1111沒有的url,爬出內容並與url存回資料庫

input:

output:

Foreign Database : 抓 job→job1111(table)網址

Inside Datebase : 對照 job1111 → job1111 如果job1111裡沒有url的則開始爬內容，並把url,info存進job1111

"""

def crawler_new_href():
    
    import sqlite3
    
    with sqlite3.connect('job1111.sqlite') as conn:

            the_job1111_href =[] 
            
            c = conn.cursor()  
            qryString = "SELECT href FROM job1111"  #拉 job1111 資料庫所有href
            c.execute(qryString)
            for a in c.fetchall():
                the_job1111_href.append(a[0])  #先塞進一個list裡面
                
            with sqlite3.connect('job.sqlite') as conn:
                
                do_number = 0 #計算有多少筆完成
                c = conn.cursor() #拉 job1111 所有href
                qryString = "SELECT href FROM job1111" #找出info是空的url並out出網址list
                c.execute(qryString)
                for a in c.fetchall():
                    if a[0] not in the_job1111_href:
                        join_into_job1111(a[0])
                        do_number += 1
                        
            print('Has crawled {} info!'.format(do_number))


"""

purpose:把僅限1111網,工作頁面的內容爬取下來並與網址一起存進資料庫   #支援crawler_new_href()

input：1111網頁（前面無https:)

ouput:


info內容：原生html內容,工作內容與求才條件,存進資料庫

CrawlerError：寫進的例外如果網頁迴傳有誤彈出例外

"""
        
def join_into_job1111(url): #解析出內文並回存進資料庫
    
    import requests
    import sqlite3
    import time
    from bs4 import BeautifulSoup
    
    try:
        https = 'https://'
        requests = requests.get(https+url)
        if requests.status_code !=200: #如果網頁異常拋出例外
            raise CrawlerError('CrawlerError','requests is error!') 

        htmlcode = BeautifulSoup(requests.text,'lxml')
        info = htmlcode.find('div','w680').text #取w680便可抓到內文資訊
        new_info = info.replace('\n',' ').replace('、',' ').encode('ascii','ignore')
        final_info = new_info.decode()
        
        time.sleep(1)
        
        with sqlite3.connect('job1111.sqlite') as conn:
            c = conn.cursor()  #p-10-12 ,3-17
            insert_string = "INSERT INTO job1111 (href,info) VALUES (?, ?)"
            c.execute(insert_string, (url, final_info))
    
    except CrawlerError:
        with sqlite3.connect('job1111.sqlite') as conn:
            c = conn.cursor()  #p-10-12 ,3-17
            insert_string = "INSERT INTO job1111 (href,info) VALUES (?, ?)"
            c.execute(insert_string, (url, '找不到網頁'))
        print(url)
        
        
class CrawlerError(Exception): #爬蟲例外 例外方法寫在def裏面
    pass

