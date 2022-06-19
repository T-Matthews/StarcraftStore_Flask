from pprint import PrettyPrinter, pprint
from bs4 import BeautifulSoup
import requests
import re

initial_units={}

data = requests.get('https://starcraft.fandom.com/wiki/List_of_StarCraft_II_units').text
soup = BeautifulSoup(data,'lxml')
# soup = soup.find_all(class_="mw-parser-output")
soup=soup.find_all(text=re.compile("^Versus.*"))
for x in range(1,len(soup)):
    if x==1:
        protoss=soup[x].parent.parent.find_next_sibling('div')
    elif x==2:
        terran =soup[x].parent.parent.find_next_sibling('div')
    else:
        zerg = soup[x].parent.parent.find_next_sibling('div')

p1=protoss.find_all('div',class_='navbox4empty',limit=3)
for j in range(len(p1)):
    p2=p1[j].find_all('li')
    for i in range(len(p2)):
        # print(p1[i])
        url=p2[i].a['href']
        x=p2[i].get_text('a')
        if x[-10:]=='a (aLotVa)':
            x=x[:-10]
        if x[-10:]=='a (aHotSa)':
            x=x[:-10]
        # print(url,x)
        if x=='Carriera\naInterceptor':
            x='Carrier'
        initial_units[x]={
            'url':'http://www.starcraft.fandom.com'+url
            }


t1=terran.find_all('div',class_='navbox4empty',limit=3)
for j in range(len(t1)):
    t2=t1[j].find_all('li')

    for i in range(len(t2)):
        url=t2[i].a['href']

        x=t2[i].get_text('a')
        if x[-10:]=='a (aLotVa)':
            x=x[:-10]
        if x[-10:]=='a (aHotSa)':
            x=x[:-10]
        # print(url,x)
        initial_units[x]={
            'url':'http://www.starcraft.fandom.com'+url
            }


z1=zerg.find_all('div',class_='navbox4empty',limit=3)
for j in range(len(z1)):
    z2=z1[j].find_all('li')

    for i in range(len(z2)):
        url=z2[i].a['href']

        x=z2[i].get_text('a')
        if x[-10:]=='a (aLotVa)':
            x=x[:-10]
        if x[-10:]=='a (aHotSa)':
            x=x[:-10]
        # print(url,x)
        initial_units[x]={
            'url':'http://www.starcraft.fandom.com'+url
            }
# print(initial_units)