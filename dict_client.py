#!/usr/bin/python3 
#coding=utf-8 

from socket import * 
import sys 

def do_register(s):
    print("欢迎注册电子词典用户！")
    username=input("请输入用户名：")
    passwd =input("请输入密码：")
    username_passwd=username+' '+passwd
    s.send(username_passwd.encode())
    recvfrom= s.recv(1024).decode()
    print(recvfrom)

def do_login(s):
    global username
    username=input("请输入用户名：")
    passwd =input("请输入密码：")
    username_passwd=username+' '+passwd
    s.send(username_passwd.encode())
    recvfrom=s.recv(1024).decode()
    print(recvfrom)
    if recvfrom =='Welcome login in dict!':
        erjijiemian(s)
    else :
        return

def erjijiemian(s):
    while True:
        print('''
            =================welcome=================
            　　　　　　1.查询单词　2.查询历史记录　3.退出
            请输入对应序号　
            =========================================
            '''
            )
        cmd =input("输入选项>>")
        if int(cmd) == 1:
            s.send('3'.encode())
            do_find(s)
        elif int(cmd) == 2:
            s.send('4'.encode())
            do_history(s)
        elif int(cmd) == 3:
            return
        else :
            print("please input right require")

def do_find(s):
    word=input("Please input word:")
    s.send(word.encode())
    meaning=s.recv(1024).decode()
    print(meaning)

def do_history(s):
    data = s.recv(4048).decode()
    print(data)

#创建网络连接
def main():
    if len(sys.argv) <3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return 

    while True:
        print(
            '''
            =========welcome=========
            --1.注册　２．登录　３．退出 --
            请输入对应的序号
            ==========================
            ''')
        cmd =input("输入选项>>")
        if int(cmd) == 1:
            s.send('1'.encode())
            do_register(s)
        elif int(cmd) == 2:
            s.send('2'.encode())
            do_login(s)
        elif int(cmd) == 3:
            return
        else :
            print('please input right require')




if __name__=='__main__':
    main()
