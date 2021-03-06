import sys   # Jan 21 9:27 pm
import socket
import threading
import os
import hashlib
import random
from Crypto.Cipher import DES3


prDc={}

toGrpFlag=False
grpName=''


active_users=[]



g=2

p_str='''FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
'''

p_str=p_str.replace(' ','')
p_str=p_str.replace('\n','')

#print(p_str)


p=int(p_str,16)  # Value of p in integer


class Encrypt():
    def pad(self,text):
        while(len(text)%8!=0):
            text+=b' '
        
        return text

    def trimKey(self,key_str):

        key_str=key_str[0:24]
        return key_str



    def des3Decrypt(self,key_str,encrypted_text):

        key=key_str

        cipher_decrypt = DES3.new(key, DES3.MODE_ECB) 
        pl=cipher_decrypt.decrypt(encrypted_text)  # Return type is in bytes

        #print(pl.decode())
        '''
        f=open('test/abc.mp4','wb')
        f.write(pl)
        f.close()
        '''

        return pl  # In Bytes




    def des3Encrypt(self,key_str,msg):
        #key = 'Sixteen byte key'

        key=key_str
        cipher_encrypt = DES3.new(key, DES3.MODE_ECB)

        '''


        f=open('abc.mp4', 'rb')
        content=f.read()
        f.close()
        '''
        content = msg

        plaintext=content

        #plaintext = 'Abhisek'
        plaintext=self.pad(plaintext)      

        encrypted_text = cipher_encrypt.encrypt(plaintext)

        #print(encrypted_text)

        return encrypted_text  # encrypted text is in bytes

        



    def generateRandom(self):
        no=random.randint(0,100)
        no=str(no)
        #print(no)

        return no.encode()



    def createSharedKey(self,public_key_bob,pr_key_alice):

        ka=int(pow(public_key_bob,pr_key_alice,p))  # shared key by alice

        return ka



    def generatePublicKey(self,pr_key_alice):


        public_key_alice=int(pow(g,pr_key_alice,p))  # Public key of Alice generated...

        return public_key_alice




    def generatePrivateKey(self):

        pr_msg_alice=b'2020201020'
        pr_nonce=self.generateRandom()
        pr_msg_alice+=pr_nonce

        crypt_msg=hashlib.sha256()
        crypt_msg.update(pr_msg_alice)


        #print(crypt_msg.hexdigest())

        pr_key_alice=crypt_msg.hexdigest()  # Gets private key in hashed string format (hex format)
        pr_key_alice=int(pr_key_alice,16)  # key in integer..

        #print(pr_key_alice) 


        return pr_key_alice

    def generateRandomGroupKey(self):

        no=random.randint(pow(10,23),pow(10,24)-1)
        no=str(no).encode()  # 24Byte key
        #print(no)


        crypt_msg=hashlib.sha256()
        crypt_msg.update(no)


        #print(crypt_msg.hexdigest())

        pr_key_alice=crypt_msg.hexdigest()  # Gets private key in hashed string format (hex format)
        pr_key_alice=int(pr_key_alice,16)  # key in integer..

        print(len(no))

        return pr_key_alice # int  return type






    def keyCall(self,s):

        prKey=self.generatePrivateKey()

        publicKey=self.generatePublicKey(prKey)
        print(publicKey)

        s.sendall(('K'+str(publicKey)).encode())


        bob_public_key=s.recv(1024).decode()

        print('Bob public key is '+str(bob_public_key))

        sharedKey=self.createSharedKey(int(bob_public_key),prKey)


        return str(sharedKey)





host="127.0.0.1"
port=7004
islogged=0
tosend={}
curr_user=""


obj = Encrypt()

class Client_send(Encrypt):

    def serverthread(self,curr_port):
        global toGrpFlag
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            s.bind((host,int(curr_port)))

            s.listen() 
            while True:
                conn,addr=s.accept()
                #print(conn)
                print('Connected to ',addr)
                #data=conn.recv(1024)
                # print(data)
                # data = data.decode()
                '''if(data.split(b";")[0]!=b'sendfile'):
                    print(data.decode())
                else:
                    # conn,addr=s.accept()
                    destfile = data.split(b";")[1].split(b"/")[-1]
                    data = (data.split(b";")[2])

                    with open(destfile,'ab') as f:
                        f.write(data)
                        # f.flush()
                        while True:
                            data = conn.recv(1024)  
                                
                            if(len(data)<1024):
                                break        
                            f.write(data)
                    print("new file received")
                    f.close()'''

                data=conn.recv(1024)
                print(data)
                msg=data.decode()

                print(msg)

                
                if(msg[0]=='K'):
                    tmp=int(msg[1:])  # Public key alice
                    #print('Alice public key: '+str(tmp))

                    server_key=obj.generatePrivateKey()  # Created private key

                    #print('Server_key is '+str(server_key))

                    serv_public_key=obj.generatePublicKey(server_key)  # created public key on server side

                    #print('Serv public key is '+str(serv_public_key))

                    conn.sendall(str(serv_public_key).encode())  # sent the public key to the server

                    kb=obj.createSharedKey(tmp,server_key)
                    kb=obj.trimKey(str(kb))

                    encrypt_msg_recvd=conn.recv(1024)

                    msg=obj.des3Decrypt(kb,encrypt_msg_recvd)  # In Bytes..

                    msg=msg.decode()
                
                else:
                    msglist=msg.split(';')
                    encrypt_msg_recvd=conn.recv(1024)
                    kb=msglist[2]

                    msg=obj.des3Decrypt(kb,encrypt_msg_recvd)  # In Bytes..

                    msg=msg.decode()
                    






                ####################################################################


                mylst=msg.strip().split(';',2)
                print(mylst)
                if mylst[0]!='sendfile':
                    print(mylst[0])
                else:
                    cont=b""
                    path=mylst[1].split('/')[-1]
                    cont=mylst[2].encode()
                    f=open(path,'wb')
                    while True:
                        encrypt_msg_recvd=conn.recv(1024)

                        data=obj.des3Decrypt(kb,encrypt_msg_recvd)  # In Bytes..
                        #data=conn.recv(1024)
                        cont+=data
                        if len(data)<1024:
                            break
                    
                    
                    f.write(cont)
                    f.close()


                

                
            
            # s.close()

    def sendmsg(self,s,usr,mesage):
        global toGrpFlag
        strn = "port;"+usr+";"+curr_user
        print(strn)
        s.sendall(strn.encode())
        data = s.recv(1024).decode()
        mylst=data.split(";")
        if(mylst[-1]=='0'):
            print(mylst[0])
        else:
            if(mylst[-1]=='1G'):
                toGrpFlag=True
            for usr in mylst:
                if usr!=mylst[-1]:
                    cli_port=int(usr)
                    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:

                        if(toGrpFlag==False):

                            s.connect((host,cli_port))
                            ska=obj.keyCall(s)  # For sending and receiving public keys  # shared key is in string here

                            ska=obj.trimKey(ska)  # trim to 24 Bytes

                            #s.sendall(mesage.encode())
                            encrypt_text=obj.des3Encrypt(ska,mesage.encode())  # Encryption decryption done here..
                            s.sendall(encrypt_text)
                        
                        else:

                            s.connect((host,cli_port))
                            
                            ska=obj.generateRandomGroupKey()  # For sending and receiving public keys  # shared key is in string here

                            ska=str(ska)
                            ska=obj.trimKey(ska)  # trim to 24 Bytes

                            s.sendall(("G;"+usr+';'+ska).encode())
                            prDc[usr]=ska
                            grpName=usr

                            #s.sendall(mesage.encode())
                            encrypt_text=obj.des3Encrypt(ska,mesage.encode())  # Encryption decryption done here..

                            s.sendall(encrypt_text)
            toGrpFlag=False


            print("Message sent successfully")
            s.close()


    def sendfile(self,s,usr,filepath):
        global toGrpFlag
        strn = "port;"+usr+";"+curr_user
        s.sendall(strn.encode())
        data = s.recv(1024).decode()
        mylst=data.split(";")
        if(mylst[-1]=='0'):
            print(mylst[0])
        else:
            if(mylst[-1]=='1G'):
                toGrpFlag=True
            for usr in mylst:
                if usr!=mylst[-1]:
                    cli_port=int(usr)
                    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                        s.connect((host,cli_port))
                        message = "sendfile;"+filepath+";"

                        f=open(filepath,'rb')
                        cont=f.read()
                        message=message.encode()
                        f.close()

                        if toGrpFlag==False:
                            ska=obj.keyCall(s)  # For sending and receiving public keys  # shared key is in string here

                            ska=obj.trimKey(ska)  # trim to 24 Bytes

                            #s.sendall(mesage.encode())
                            encrypt_text=obj.des3Encrypt(ska,message)  # Encryption decryption done here..
                            s.sendall(encrypt_text)

                            encrypt_text=obj.des3Encrypt(ska,cont)
                            s.sendall(encrypt_text)


                            #s.sendall(message)
                            #s.sendall(cont)
                            
                        else:
                            ska=obj.generateRandomGroupKey()  # For sending and receiving public keys  # shared key is in string here

                            ska=str(ska)
                            ska=obj.trimKey(ska)  # trim to 24 Bytes

                            s.sendall(("G;"+usr+';'+ska).encode())
                            prDc[usr]=ska
                            grpName=usr

                            #s.sendall(mesage.encode())
                            encrypt_text=obj.des3Encrypt(ska,message)  # Encryption decryption done here..

                            s.sendall(encrypt_text)

                            encrypt_text=obj.des3Encrypt(ska,cont)  # Encryption decryption done here..

                            s.sendall(encrypt_text)
                        print("File sent successfully")
            s.close()

    def signup(self,clsock,id,passw):
        
        strn = "signup;"+id+";"+passw
        s.send(strn.encode())
        data = s.recv(1024).decode()
        print(data)


    def login(self,clsock,id,passw,curr_port):
        global islogged
        global curr_user

        if(islogged==0):
            strn = "login;"+id+";"+passw+";"+curr_port
            s.sendall(strn.encode())
            data = s.recv(1024).decode()
            print(data.split(";")[0])
            if(data.split(";")[1]=='1'):
                islogged=1
            curr_user=id
        else:
            print("someone is already logged in")

    def creategrp(self,s,grpname):
        global islogged
        global curr_user

        if islogged==1:
            strn="create;"+grpname+";"+curr_user
            s.sendall(strn.encode())
            data = s.recv(1024).decode()
            print(data)
        else:
            print("user not logged in")

    def joingrp(self,s,grpname):
        global islogged
        global curr_user

        if islogged==1:
            strn="join;"+grpname+";"+curr_user
            s.sendall(strn.encode())
            data = s.recv(1024).decode()
            print(data)
        else:
            print("user not logged in") 

    def listgrp(self,s):
        global islogged

        if islogged==1:
            strn="list;"
            s.sendall(strn.encode())
            data = s.recv(1024).decode()
            grplist=data.split(";")
            for i in grplist:
                print(i)
        else:
            print("user not logged in")   

clobj = Client_send()

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((host,port))
    curr_port=sys.argv[1]

    t1=threading.Thread(target=clobj.serverthread,args=(curr_port,))
            
    t1.start()
    while True:
        data=input()
        mylst = data.split()
        print("")
        if(mylst[0].lower()=="login"):
            clobj.login(s,mylst[1],mylst[2],curr_port)
        elif(mylst[0].lower()=="signup"):
            if(islogged==0):
                clobj.signup(s,mylst[1],mylst[2])
            else:
                print("already logged in")
        elif(mylst[0].lower()=="send"):
            if(islogged==1):
                if(mylst[1]!="file"):
                    mystr = (" ").join(mylst[2:])
                    clobj.sendmsg(s,mylst[1],mystr)
                else:
                    clobj.sendfile(s,mylst[3],mylst[2])
            else:
                print("user not logged in")
        elif(mylst[0].lower()=="create"):
            clobj.creategrp(s,mylst[1])
        elif(mylst[0].lower()=="join"):
            clobj.joingrp(s,mylst[1])
        elif(mylst[0].lower()=="list"):
            clobj.listgrp(s)
        else:
            print("Invalid Command")
        print()
    s.close()