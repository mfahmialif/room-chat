import socket
import threading
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 8888))
sock.listen(10)

list_client = []
list_group = {}
list_private = []
# fungsi yang akan dieksekusi pada setiap thread
def handle_thread(conn) :
        global list_client
        global list_group
        try:    
                # get header dari client
                headers = ""
                while True :
                        temp = conn.recv(4)
                        temp = temp.decode('ascii')
                        headers = headers + temp
                        if "\r\n\r\n" in headers:
                                headers = headers.replace("\r\n\r\n","")
                                break
                print(headers)
                cekRequest = headers.splitlines()[0]
                if "home.html" in cekRequest:
                        get = headers.splitlines()[0]
                        get = get.split("=",1)
                        get = get[1].split(" ",1)
                        dataGet = get[0].replace("%20"," ")
                        if dataGet not in list_client:
                                list_client.append(dataGet)
                        
                        f = open("web/home.html","r")
                        fIsi = f.read()
                        fIsi = fIsi.replace("anonymous", dataGet)
                        fUkuran = str(len(fIsi))
                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: text/html\r\n"+
                                "Content-length: "+fUkuran+"\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                fIsi)
                        f.close()

                elif "list-group.html" in cekRequest:
                        get = headers.splitlines()[0]
                        get = get.split("=",1)
                        get = get[1].split(" ",1)
                        dataGet = get[0].replace("%20"," ")
                        
                        f = open("web/list-group.html","r")
                        fIsi = f.read()
                        fIsi = fIsi.replace("anonymous", dataGet)
                        fUkuran = str(len(fIsi))
                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: text/html\r\n"+
                                "Content-length: "+fUkuran+"\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                fIsi)
                        f.close()
                
                elif "chat-group.html" in cekRequest:
                        ds = cekRequest.split("&")
                        username = ds[0].split("username=")[1].replace("%20", "")
                        room = ds[1].split("room=")[1].split(" ")[0].replace("%20", " ")

                        f = open("web/chat-group.html","r")
                        fIsi = f.read()
                        fIsi = fIsi.replace("anonymous", username)
                        fIsi = fIsi.replace("anonyroom", room)
                        fUkuran = str(len(fIsi))
                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: text/html\r\n"+
                                "Content-length: "+fUkuran+"\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                fIsi)
                        f.close()

                        if username not in list_group[room]["member"]:
                                list_group[room]["member"] += [username]

                elif "list-private.html" in cekRequest:
                        get = headers.splitlines()[0]
                        get = get.split("=",1)
                        get = get[1].split(" ",1)
                        dataGet = get[0].replace("%20"," ")
                        
                        f = open("web/list-private.html","r")
                        fIsi = f.read()
                        fIsi = fIsi.replace("anonymous", dataGet)
                        fUkuran = str(len(fIsi))
                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: text/html\r\n"+
                                "Content-length: "+fUkuran+"\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                fIsi)
                        f.close()

                elif "chat-private.html" in cekRequest:
                        ds = cekRequest.split("&")
                        username = ds[0].split("username=")[1].replace("%20", "")
                        penerima = ds[1].split("penerima=")[1].split(" ")[0].replace("%20", " ")
                        
                        f = open("web/chat-private.html","r")
                        fIsi = f.read()
                        fIsi = fIsi.replace("anonymous", username)
                        fIsi = fIsi.replace("anonymkepada", penerima)
                        fUkuran = str(len(fIsi))
                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: text/html\r\n"+
                                "Content-length: "      +fUkuran+"\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                fIsi)
                        f.close()
                
                elif "buat-group.html" in cekRequest:
                        get = headers.splitlines()[0]
                        get = get.split("=",1)
                        get = get[1].split(" ",1)
                        dataGet = get[0].replace("%20"," ")
                        ukuranDataGet = str(len(dataGet))
                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: text/html\r\n"+
                                "Content-length: "+ukuranDataGet+"\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                dataGet)
                        if dataGet not in list_group:
                                list_group[dataGet] = {"member": [], "pesan": []}
                        print(list_group)
                
                elif "get-group.json" in cekRequest:
                        dataListGroup = json.dumps(list_group)
                        dataListUkuran = str(len(dataListGroup))
                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: application/json\r\n"+
                                "Content-length: "+dataListUkuran+"\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                dataListGroup)
                        

                elif "kirim-pesan-group.html" in cekRequest:
                        ds = cekRequest.split("&")
                        username = ds[0].split("username=")[1].replace("%20", "")
                        room = ds[1].split("room=")[1].split(" ")[0].replace("%20", " ")
                        pesan = ds[2].split("pesan=")[1].split(" ")[0].replace("%20", " ")

                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: text/html\r\n"+
                                "Content-length: 6\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                "sukses")

                        list_group[room]["pesan"] += [username+" => "+pesan]

                elif "get-client.json" in cekRequest:
                        dataListClient = json.dumps(list_client)
                        dataListUkuran = str(len(dataListClient))
                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: application/json\r\n"+
                                "Content-length: "+dataListUkuran+"\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                dataListClient)

                elif "kirim-pesan-private.html" in cekRequest:
                        ds = cekRequest.split("&")
                        username = ds[0].split("username=")[1].replace("%20", "")
                        kepada = ds[1].split("kepada=")[1].split(" ")[0].replace("%20", " ")
                        pesan = ds[2].split("pesan=")[1].split(" ")[0].replace("%20", " ")

                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: text/html\r\n"+
                                "Content-length: 6\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                "sukses")
                        
                        # temp = {"pesan":pesan, "client": username+","+kepada}
                        temp = {"pesan":pesan, "pengirim": username, "kepada": kepada}
                        list_private.append(temp)

                elif "get-private.json" in cekRequest:
                        dataListPrivate = json.dumps(list_private)
                        dataListUkuran = str(len(dataListPrivate))
                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: application/json\r\n"+
                                "Content-length: "+dataListUkuran+"\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                dataListPrivate)
                
                elif "logout.html" in cekRequest:
                        get = headers.splitlines()[0]
                        get = get.split("=",1)
                        get = get[1].split(" ",1)
                        dataGet = get[0].replace("%20"," ")
                        if dataGet not in list_client:
                                list_client.append(dataGet)
                        
                        f = open("web/index.html","r")
                        fIsi = f.read()
                        fUkuran = str(len(fIsi))
                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: text/html\r\n"+
                                "Content-length: "+fUkuran+"\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                fIsi)
                        f.close()

                        list_client.remove(dataGet)
                        for lg in list_group:
                                if dataGet in list_group[lg]["member"]:
                                        list_group[lg]["member"].remove(dataGet)
                                

                else:
                        f = open("web/index.html","r")
                        fIsi = f.read()
                        fUkuran = str(len(fIsi))
                        response = ("HTTP/1.1 200 OK\r\n"+
                                "Content-type: text/html\r\n"+
                                "Content-length: "+fUkuran+"\r\n"+
                                "Connection: close\r\n"+
                                "\r\n"+
                                fIsi)
                        f.close()
                        
                conn.send(response.encode('ascii'))
        except (socket.error, KeyboardInterrupt):
                conn.close()
                print("Client menutup koneksi")
    
try:
        
        while True :
                conn, client_addr = sock.accept()
                
                # buat thrad baru setiap ada koneksi pada client
                clientThread = threading.Thread(target=handle_thread,args=(conn,))
                clientThread.start()

except KeyboardInterrupt:
        print("Server mati")

# ditampung di server datanya
# client get data sesuai namanya