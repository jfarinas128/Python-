from bs4 import BeautifulSoup
from pyquery import PyQuery   
import HTMLParser
import urllib2


firstName = lastName= ' '
query = "Schwartz,Eric M".split(',')
for i,c in enumerate(query):
            if i == 0:
                lastName = c # get first 'last name' in list of professors
            elif i == 1:
                tempc =  c.split()
                firstName =  tempc[0] #get first name corresponding to last name
                
name = lastName + ', '+ firstName
prof_url = "http://www.ratemyprofessors.com/search.jsp?query="+firstName+ "%20"+ lastName
#print prof_url
page = urllib2.urlopen(prof_url)
soup = BeautifulSoup(page)

for listing in soup.find_all('span', attrs={'class': 'listing-name'}):
    #print listing
    for detail in listing.find_all('span'):
        #print detail
        if detail.string:
            
            foundName =  unicode(detail.string).strip()
            #print foundName
            school = unicode(detail.findNext('span').string).strip()
            #print school
            
            if (foundName == name) and 'University of Florida' in school:
                #print "Success!"
                link = [l['href'] for l in detail.findParents('a')]
                #print unicode(detail.nextSibling.string).strip()
                #print str(link[0])
                break
    else:
        continue
    break
            
'''old way
for prof in soup.find_all('span', attrs={'class': 'main'}):
    if prof.string:
        foundName =  unicode(prof.string).strip()
        print foundName
    
        if foundName == name:
            print "Success!"
            link = [l['href'] for l in prof.findParents('a')]
            print unicode(prof.nextSibling.string).strip()
            print str(link[0])
'''
prof_page_url = "http://www.ratemyprofessors.com" + link[0]
#print prof_page_url
prof_page = urllib2.urlopen(prof_page_url)
prof_soup = BeautifulSoup(prof_page)
rating = unicode([r for r in prof_soup.find_all('div', attrs={'class': 'grade'})][0].string).strip()#strip rating from tag here
print  str(firstName)+' '+str(lastName) + "'s Rating -> " + rating 

