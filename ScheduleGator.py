import mysql.connector
from bs4 import BeautifulSoup
from pyquery import PyQuery   
import urllib2
import string

class Course():
    name = ""
    section =  ""
    cname = ""
    lday = ""
    ltime = ""
    dday = ""
    dtime = ""
    dbuild = ""
    droom = ""
    lroom = ""
    cedits = ""
    lbuild = ""
    cinst = ""
    dept = ""
    prof_id = ""
    d2day = ""
    d2time = ""
    d2build = ""
    d2room = ""

    def store(self):
      course_data = (str(self.name), self.section, self.cedits, str(self.cname), self.dept, str(self.lday), str(self.ltime), str(self.lbuild), str(self.lroom), str(self.cinst), self.prof_id, ','.join(map(str, gettimes(self.ltime))) )
      add_course = ("INSERT INTO courses "
                    "(course_name, section, credits, title, department, lecture_day, lecture_period, lecture_building, lecture_room, instructor, professor_id, lecture_period_array)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
      add_discussion = ("INSERT INTO discussions"
                        "(course_id, discussion_day, discussion_period, discussion_building,discussion_room, discussion_period_array)"
                        "VALUES(%s, %s, %s, %s, %s, %s)")
      cursor.execute(add_course, course_data)
      course_id = cursor.lastrowid
      discussion_data = (course_id, self.dday, self.dtime, self.dbuild, self.droom, ','.join(map(str, gettimes(self.dtime))))
      discussion2_data = (course_id, self.d2day, self.d2time, self.d2build, self.d2room, ','.join(map(str, gettimes(self.d2time))))
      if self.dbuild:
        cursor.execute(add_discussion, discussion_data)
      if self.d2build:
        cursor.execute(add_discussion, discussion2_data)
      cnx.commit()

def getrmp(profName):
  firstName = ' '
  lastName = ' '
  query = profName.split(',')
  duplicate = False
  if professors.has_key(profName):
    return professors[profName]#key index is id of professor for table in db
  else:
    duplicate = True 
  for i,c in enumerate(query):
            if i == 0:
                lastName = c #get first 'last name' in list of professors
            elif i == 1:
                tempc =  c.split()
                firstName =  tempc[0] #get first name corresponding to last name              
  name = lastName + ', '+ firstName
  prof_url = "http://www.ratemyprofessors.com/search.jsp?query="+firstName+ "%20"+ lastName
  try:
    page = urllib2.urlopen(prof_url)
    soup = BeautifulSoup(page)
  except:
    rating ="N/A"
  try:
    for listing in soup.find_all('span', attrs={'class': 'listing-name'}):
        for detail in listing.find_all('span'):
            if detail.string:         
                foundName =  unicode(detail.string).strip()
                school = unicode(detail.findNext('span').string).strip()    
                if (foundName == name) and 'University of Florida' in school:
                    link = [l['href'] for l in detail.findParents('a')]
                    break
        else:
            continue
        break
  except:
    rating = "N/A"
  try:
    prof_page_url = "http://www.ratemyprofessors.com" + link[0]
    prof_page = urllib2.urlopen(prof_page_url)
    prof_soup = BeautifulSoup(prof_page)
    rating = unicode([r for r in prof_soup.find_all('div', attrs={'class': 'grade'})][0].string).strip()#strip rating from tag here
    print  str(firstName)+' '+str(lastName) + "'s Rating -> " + rating 
  except:
    rating = "N/A"
  if duplicate:
    add_professor = ("INSERT INTO professors"
                     "(first, last, rating)"
                     "VALUES(%s,%s,%s)")
    professor_data = (firstName,lastName,rating)
    cursor.execute(add_professor, professor_data)
    professor_id = cursor.lastrowid
    professors[profName] = professor_id
    cnx.commit()
  return professor_id
                       
def gettimes(ltime):#Interpret course periods into numerical values for comparison
    if len(ltime)==4 and '-' not in ltime:
        ltime = ltime[0:2] + '-' + ltime[2:4]
    time_strings = [str(time) for time in ltime.split('-')]
    time_ints = []
    special_cases = {'E1':12, 'E2':13, 'E3':14, 'TBA':0}
    for element in time_strings:
        if element.isdigit():
            time_ints.append(int(element))
        if element in special_cases:
            time_ints.append(special_cases[element])
    if len(time_ints)==2:
        return range(time_ints[0], time_ints[1]+1)
    else:
        return time_ints

if __name__ == '__main__':
    semester = str(raw_input("Which Semester?"))
    year = int(raw_input("Which Year"))
    config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'schedulegator',
     }
    if semester.lower() == 'fall':
        semester = "08"
    elif semester.lower() == 'spring':
        semester = "01"
    elif semester.lower() == 'summer':
        semester = "06"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    professors = {}
    try:
      cursor.execute("truncate courses")
      cursor.execute("truncate discussions")
      cursor.execute("truncate professors")
    except mysql.connector.Error as err:
      print("Failed to clear tables".format(err))
    
    base_url = "http://www.registrar.ufl.edu/soc/"+str(year)+str(semester)+"/all/"
    page = urllib2.urlopen(base_url)
    soup = BeautifulSoup(page)
    listings = {}
    endings = [option.get('value') for option in soup.findAll('option')]
    departments = [str(x.text) for x in soup.find_all('option')]

    for index,value in enumerate(departments):
        listings[value] = endings[index]
        
    url_list = [base_url+listings[listing] for listing in listings]
    
    for key in listings:
        updateR = True
        ending = listings[key].strip()
        if ending:
            print "OPENING: " + base_url + ending
            page = urllib2.urlopen(base_url+ ending)
            pages = str(page.read()) 
            started = False
            shifted = False
            g = Course()
            pq = PyQuery(pages)
            for c in pq('td'):
                if (pq(c).text().__len__() == 8 and pq(c).text()[3:4] == " ") or (pq(c).text().__len__() == 9 and pq(c).text()[3:4] == " "):
                    y = 0
                    if g.name != "":
                          g.dept = key # Department added to each course
                          g.store()#store in DB HERE
                    g = Course()
                    g.name = pq(c).text()
                    started = True
                    shifted = False
                if (not(pq(c).text().__len__() == 8 and pq(c).text()[3:4] == " ") or (pq(c).text().__len__() == 9 and pq(c).text()[3:4] == " ")) and started == True:
                                    y +=1 
                                    if y == 7 and shifted != True:
                                         g.lday = pq(c).text()
                                    if y == 21 and shifted != True:
                                         g.dday = pq(c).text()
                                    if y == 22 and shifted != True:
                                         g.dtime = pq(c).text()
                                    if y == 23 and shifted != True:
                                         g.dbuild = pq(c).text()
                                    if y == 24 and shifted != True:
                                         g.droom = pq(c).text()
                                    if y == 5 and shifted != True:
                                         if (len(pq(c).text()) == 0) or (len(pq(c).text()) == 1):
                                                 shifted = True
                                         else: g.section = pq(c).text()
                                    if y == 6 and shifted != True:
                                         g.cedits = pq(c).text()
                                    if y == 8 and shifted != True:
                                         g.ltime = pq(c).text()
                                    if y == 9 and shifted != True:
                                         g.lbuild = pq(c).text()
                                    if y == 10 and shifted != True:
                                         g.lroom = pq(c).text()
                                    if y == 12 and shifted != True:
                                         g.cname = pq(c).text()
                                    if y == 13 and shifted != True:
                                         g.cinst = pq(c).text()
                                         if updateR:
                                             g.prof_id = getrmp(g.cinst)
                                                         
                                    if y == 6 and shifted == True:
                                         g.section = pq(c).text()
                                    if y == 7 and shifted == True:
                                         g.cedits = pq(c).text()
                                    if y == 9 and shifted == True:
                                         g.ltime = pq(c).text()
                                    if y == 22 and shifted == True:
                                         g.dday = pq(c).text()
                                    if y == 23 and shifted == True:
                                         g.dtime = pq(c).text()
                                    if y == 24 and shifted == True:
                                         g.dbuild = pq(c).text()
                                    if y == 25 and shifted == True:
                                         g.dbuild = pq(c).text()
                                    if y == 8 and shifted == True:
                                         g.lday = pq(c).text()
                                    if y == 10 and shifted == True:
                                         g.lbuild = pq(c).text()
                                    if y == 11 and shifted == True:
                                         g.lroom = pq(c).text()
                                    if y == 13 and shifted == True:
                                         g.cname = pq(c).text()
                                    if y == 14 and shifted == True:
                                         g.cinst = pq(c).text()
                                         if updateR:
                                             g.prof_id = getrmp(g.cinst)
                                             
                                    if y == 36 and shifted == True:
                                         g.d2day = pq(c).text()
                                    if y == 37 and shifted == True:
                                         g.d2time = pq(c).text()
                                    if y == 38 and shifted == True:
                                         g.d2build = pq(c).text()
                                    if y == 39 and shifted == True:
                                         g.d2room = pq(c).text()
    cursor.close()
    cnx.close()


