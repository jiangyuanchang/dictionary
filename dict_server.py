'''
name : jyc
data : 

'''

from socket import * 
import os 
import time 
import signal 
import pymysql
import sys

DICY_TEXT='./dict.txt'
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

def do_child(c,db):
    cursor=db.cursor()
    while True:
        cmd = c.recv(1024).decode()
        if cmd =='1':
            print('执行注册操作')
            do_register(c,db,cursor)
        elif cmd == '2':
            print('执行登录操作')
            do_login(c,db,cursor)
        elif cmd == '3':
            print('%s执行查询操作'%name)
            do_find(c,db,cursor)
        elif cmd =='4':
            print('查询%s的查询历史'%name)
            do_history(c,cursor)
        elif not cmd:
            sys.exit("为%s服务的子进程退出"%name)

def do_find(c,db,cursor):
    global name 
    word=c.recv(1024).decode()
    try:
        sql_select ="select * from words where word='%s'"%word
        cursor.execute(sql_select)
        data = cursor.fetchone()
        if not data:
            c.send(('Do not find %s'%word).encode())
        else :
            c.send(data[2].encode())
            sql_insert ="insert into history(name,word,time) \
                        values('%s','%s','%s')"%(name,word,time.ctime())
            cursor.execute(sql_insert)
            db.commit()

    except Exception as e:
        print(e)

def do_login(c,db,cursor):
    username_passwd=c.recv(1024).decode().split(' ')
    try:
        sql_select = "select * from user where name='%s'"%\
                username_passwd[0]
        cursor.execute(sql_select)
        data = cursor.fetchone()
        if data==None:
            c.send("You do not register a zhanghao!".encode())
        elif data[2]!=username_passwd[1]:
            c.send("Passwd error!".encode())
        elif data[2]==username_passwd[1]:
            c.send("Welcome login in dict!".encode())
    except Exception as e:
        print(e)
    global name 
    name = username_passwd[0]

def do_register(c,db,cursor):
    username_passwd=c.recv(1024).decode().split(' ')
    try:
        sql_select = "select * from user where name='%s'"%\
                username_passwd[0]
        cursor.execute(sql_select)
        data = cursor.fetchone()
        if  data!=None:
            c.send('username had been registered'.encode())
            # baocuo 
            cursor.close()
            return 
        sql_insert = "insert into user(name,passwd) values('%s','%s')"%(username_passwd[0],username_passwd[1])
        cursor.execute(sql_insert)
        db.commit()
        c.send('register success'.encode())
    except Exception as e:
        print(e)
        c.send('register failed'.encode())

def do_history(c,cursor):
    global name
    sql_select = "select word,time from history where name='%s'"\
                %name
    cursor.execute(sql_select)
    data = cursor.fetchall()
    print(data)
    if len(data)>=1:
        data_str = "word     time \n"
        for i  in range(len(data)):
            data_str+=(data[i][0]+'  '+data[i][1]+'\n')
        c.send(data_str.encode())
    else :
        c.send('do not find history'.encode())
#流程控制
def main():
    db =pymysql.connect('localhost'\
            ,'root','123456','dict')
    
    #创建套接字
    s =socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    #处理僵尸进程，忽略子进程信号的方法
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr = s.accept()
            print("connect from",addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        #这里用ctrl+c子进程能接收到么？
        except Exception as e:
            print(e)
            continue 

        #创建子进程
        pid = os.fork()
        if pid ==0:
            s.close()
            print("子进程准备处理请求")
            do_child(c,db)
        else :
            c.close()
            continue

if __name__=="__main__":
    main()