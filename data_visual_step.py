"""
purpose: 把資料庫裡面讀出資料視覺化 

input: howmach-資料庫所有資料(dict)；number-與想要看到排序前幾多的數量(預設十)

output: 視覺化圖表

"""


def qualify(howmach,number = 10):
    import numpy as np
    from pylab import savefig
    import matplotlib.pyplot as plt
    
    howmacharray = sorted(howmach.items(),key=lambda d:d[1],reverse = True) #把dict做排序，轉成數字排列大小的LIST(truple)
    many = howmacharray[0:number] #取出前 (number,預設10)的elements

    labels, ys = zip(*many) #把list每個elements拆開來,名子跟數量
    xs = np.arange(len(labels))  #計算有多少個數量,並變成一個arrange

    plt.bar(xs, ys, width=0.8, align='center')

    plt.ylabel("數量")
    plt.xlabel("程式語言")
    plt.title("The Program language") 
    plt.rcParams['font.sans-serif']=['SimHei'] #讓圖表正常顯視中文
    plt.rcParams['axes.unicode_minus']=False #讓圖表正常顯視負號

    plt.xticks(xs, labels) #排序x軸標籤,xs 設置有多少個, labels換成中文名稱
    savefig('bar_chart.png')
    savefig('bar_chart.pdf')
    plt.show()
    
    
    
"""
pursore: 查詢所有資料    /    查詢某語言數量

input: 輸入資料庫欄位名稱,資料庫名稱,資料表名稱   /     後面多補個欲查詢語言名稱

output: 全部資料庫的資訊(dict)      /        查詢結果(string)

"""

def connect_database(column_name,cloumn_number,datebase_name,table_name,query_name=None):
    
    import sqlite3
    with sqlite3.connect(datebase_name) as conn:
        c = conn.cursor()
        qryString = "SELECT {0},{1} FROM {2}".format(column_name,cloumn_number,table_name)
        c.execute(qryString)

        dict = {}
        for i in c.fetchall(): #把查詢結果轉成dict 
            dict[i[0]]=i[1]

        if bool(query_name) is True:  # 如果query_name 回傳該查詢結果
            return_text = "{0}'s quantity is {1}".format(query_name,dict[query_name])
            return return_text
        else:    #如果沒查詢，輸出全部資訊
            return dict      
