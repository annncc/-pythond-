import socket
from os.path import commonprefix

words = {'how are you?':'Fine,thank you.',
         'how old are you?':'21',
         'what is your name?':'Guoan',
         "what's your name?":'guoan',
         'where do you work?':'University',
         'bye':'Bye'}
HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定socket
s.bind((HOST, PORT))
# 开始监听一个客户端连接，表示自己是服务端程序，1表示可以同时服务的客户端数量
s.listen(1)
print('Listening on port:',PORT)
conn, addr = s.accept()                 # 返回一个用于通信的套接字以及客户端地址
print('Connected by', addr)
while True:                             # 开始聊天
    data = conn.recv(1024).decode()
    if not data:                        # 对于TCP连接，没有接收到数据表示对方已关闭
        break
    print('Received message:', data)
    m = 0
    key = ''
    for k in words.keys():              # 尽量猜测对方要表达的真正意思
        data = ' '.join(data.split())   # 删除多余的空白字符
        if len(commonprefix([k, data])) > len(k)*0.7:   # 与某个“键”非常接近，就直接返回
            key = k
            break
        length = len(set(data.split())&set(k.split()))  # 使用选择法，选择一个重合度较高的“键”
        if length > m:
            m = length
            key = k
    conn.sendall(words.get(key, 'Sorry.').encode())     # 选择合适的信息进行回复
conn.close()
s.close()