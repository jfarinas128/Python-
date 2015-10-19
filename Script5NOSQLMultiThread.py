from bs4 import BeautifulSoup
from pyquery import PyQuery   
import urllib2
import string
import Queue
import threading

'''
def do_job(target, args_list):
    #results = Queue.Queue()
    def task_wrapper(*args):
        target(*args)
    threads = [threading.Thread(target=task_wrapper, args=args) for args in args_list]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    #return results

'''
'''
def worker():
        i, url = q.get()
        #print "requesting ", i, url       # if you want to see what's going on
        strip_page(url)
        q.task_done()
'''


class workerthread(threading.Thread):
        def __init__(self,queue):
                threading.Thread.__init__(self)
                self.queue=queue
        def run(self):
                while True:
                    i, url= self.queue.get()
                    strip_page(url)
                    self.queue.task_done()

                        
def strip_page(html):
    updateR = False
    if html:
        print "OPENING: " + html + "\n"
        page = urllib2.urlopen(html)
        pages = str(page.read()) 
        started = False
        moveA = False
        count = 0
        pq = PyQuery(pages)
        tag = pq('td')
        for c in  pq('td'):
            if (pq(c).text().__len__() == 8 and pq(c).text()[3:4] == " ") or (pq(c).text().__len__() == 9 and pq(c).text()[3:4] == " "):
                y = 0
                text_file.write("----------------------------------------------------------------" + "\n")
                text_file.write( pq(c).text() +"\n")
                text_file.write("----------------------------------------------------------------"+"\n")
                started = True
                moveA = False
            if (not(pq(c).text().__len__() == 8 and pq(c).text()[3:4] == " ") or (pq(c).text().__len__() == 9 and pq(c).text()[3:4] == " ")) and started == True:
                y +=1 
                #text_file.write pq(c).text() + "    INDEX: " + str(y)
                if y == 7 and moveA != True:
                     text_file.write("Lecture Day: " + pq(c).text() + "\n")
                if y == 21 and moveA != True:
                     text_file.write("Discussion Day: " + pq(c).text()+ str(y) + "\n")
                if y == 22 and moveA != True:
                     text_file.write("Discussion Period: " + pq(c).text()+ str(y) + "\n")
                if y == 23 and moveA != True:
                     text_file.write("Discussion Building: " + pq(c).text()+ str(y) + "\n")
                if y == 24 and moveA != True:
                     text_file.write("Discussion Room: " + pq(c).text()+ str(y) + "\n")
                if y == 5 and moveA != True:
                     if (len(pq(c).text()) == 0) or (len(pq(c).text()) == 1):
                         moveA = True
                     else: text_file.write("Section: " + pq(c).text() + "\n")
                if y == 6 and moveA != True:
                     text_file.write("Credits: " + pq(c).text() + "\n")
                if y == 8 and moveA != True:
                     text_file.write("Lecture Period: " + pq(c).text() + "\n")
                if y == 9 and moveA != True:
                     text_file.write("Lecture Building: " + pq(c).text() + "\n")
                if y == 10 and moveA != True:
                     text_file.write("Lecture Room: " + pq(c).text() + "\n")
                if y == 12 and moveA != True:
                    text_file.write("Course Name: " + pq(c).text() + "\n")
                if y == 13 and moveA != True:
                    text_file.write("Course Instructor: " + pq(c).text() + "\n")
                    if updateR:
                        #text_file.write(getrmp(pq(c).text(),count))
                        count = count +1


                if y == 6 and moveA == True:
                     text_file.write("Section: " + pq(c).text() + "\n")
                if y == 7 and moveA == True:
                     text_file.write("Credits: " + pq(c).text() + "\n")
                if y == 9 and moveA == True:
                     text_file.write("Lecture Period: " + pq(c).text() + "\n")
                if y == 22 and moveA == True:
                     text_file.write("Discussion Day: " + pq(c).text()+  "\n")
                if y == 23 and moveA == True:
                     text_file.write("Discussion Period: " + pq(c).text()+  "\n" )
                if y == 24 and moveA == True:
                     text_file.write("Discussion Building: " + pq(c).text()+  "\n")
                if y == 25 and moveA == True:
                     text_file.write("Discussion Room: " + pq(c).text()+  "\n")
                if y == 8 and moveA == True:
                     text_file.write("Lecture Day: " + pq(c).text() + "\n")
                if y == 10 and moveA == True:
                     text_file.write("Lecture Building: " + pq(c).text() + "\n")
                if y == 11 and moveA == True:
                     text_file.write("Lecture Room: " + pq(c).text() + "\n")
                if y == 13 and moveA == True:
                     text_file.write("Course Name: " + pq(c).text() + "\n")
                if y == 14 and moveA == True:
                     text_file.write("Course Instructor: " + pq(c).text() + "\n")
                     if updateR:
                        #text_file.write(getrmp(pq(c).text(),count))
                        count = count +1

                if y == 36 and moveA == True:
                     text_file.write("Discussion2 Day: " + pq(c).text()+  "\n")
                if y == 37 and moveA == True:
                     text_file.write("Discussion2 Time: " + pq(c).text()+ "\n")
                if y == 38 and moveA == True:
                     text_file.write("Discussion2 Building: " + pq(c).text()+ "\n")
                if y == 39 and moveA == True:
                     text_file.write("Discussion2 Room: " + pq(c).text()+  "\n")

    return                                    
#past 24 and 25 for eel, 3 disc period classes
url = "http://www.registrar.ufl.edu/soc/201508/all/"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
listings = {}
endings = [option.get('value') for option in soup.findAll('option')]
departments = [str(option.text) for option in soup.find_all('option')]

for index,value in enumerate(departments):
    listings[value] = endings[index]

#url_list = [(url+listings[listing],) for listing in listings]

url_list = [url+listings[listing] for listing in listings]

#print url_list
text_file = open("../../Output.txt", "w")

#for site in url_list:
#   strip_page(site)
    
#do_job(strip_page, url_list)

threads = []
q = Queue.Queue()

for i in range(100):
        worker=workerthread(q)
        worker.daemon=True
        worker.start()
for i,url in enumerate(url_list):
    q.put((i,url))
q.join()

text_file.close()
