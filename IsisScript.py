#Script for PYTHON2.7

import sys, signal, os
import time
import smtplib
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4 import QtCore


#url = "https://www.isis.ufl.edu/cgi-bin/nirvana?MDASTRAN=RSI-GRADES"
url = "https://www.isis.ufl.edu/cgi-bin/nirvana?MDASTRAN=RSS-RGCHK2"
count = 0
def checkSearch():
    file1 = open("Output.txt", "r")
    start = False
    for line in file1:
        if '<div id="wellbody">' in line:#begin looking
            start = True
        if '<input type="SUBMIT" value="Show More sections">' in line:#end of results
            start = False
        if start:
            if '<input type="hidden" name="COMASECT" value="1524">' in line: #looking by section number
                return True
    return False
    
def JSEval(code):
    return web.page().mainFrame().evaluateJavaScript(code)

def onLoadStarted():
    print("Loading started: %s" % web.page().mainFrame().url().toString())

def onLoadFinished(result):
    global count
    count +=1
    print("Loading finished: %s" % web.page().mainFrame().url().toString())
    print str(count)
    if not result:
        print("Request failed")
        return
    if count == 2:  #only send log in data via post one time for security
        JSEval("_form = document.getElementsByName('loginForm')[0];")
        JSEval("_form.username.value='%s';" % username \
        + "_form.password.value='%s';" % password \
        + "_form.submit();")
        print("Login data sent")
    if count == 4:
          JSEval("document.searchform.MDASTRAN.value = 'RSS-CSE   ';")
          JSEval("document.searchform.MDASKEYY.value = '%s';" % course)
          JSEval("document.searchform.submit();")
    if count == 5:
          sourcepage = web.page().mainFrame()
          html = sourcepage.toHtml()
          text_file = open("Output.txt", "w")  #write output to file .txt type for logging/debug
          text_file.write(html)
          text_file.close()
          found = checkSearch()
          server = smtplib.SMTP( "smtp.gmail.com", 587 )
          server.starttls()
          server.login( GUname, GPwd )
          server.sendmail( GUname, '', str(found) )#send text saying whether it's true or not
          time.sleep(300)  
          os.system("script427.py")
          
          '''
    if web.page().mainFrame().url().toString() == url:  #FOR CEN Project to obtain course info
          x = staticint()
          sourcepage = web.page().mainFrame()
          html = sourcepage.toPlainText()  #or toHtml() whichever works better
          #print(html)   #debug output HTML source
          text_file = open("Output.txt", "w")  #write output to file .txt type
          text_file.write(html)
          text_file.close()
          if x == 2:
              print("Output Created!")
              sys.exit()
              '''


if  __name__ =='__main__':
    #while True:
        username = raw_input("Enter Username: ")
        password = raw_input("Enter Password: ")
        course = raw_input("Enter Course Desired: ")
        GUname = ''
        GPwd = ''
        app = QApplication(sys.argv)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        web = QWebView()
        QtCore.QObject.connect(web, QtCore.SIGNAL("loadFinished(bool)"), onLoadFinished)
        QtCore.QObject.connect(web, QtCore.SIGNAL("loadStarted()"), onLoadStarted)
        web.load(QUrl(url))
        web.show()
        sys.exit(app.exec_())
