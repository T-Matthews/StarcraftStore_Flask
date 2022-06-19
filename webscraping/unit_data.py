from gettext import find
from bs4 import BeautifulSoup
import requests
import re
from main import initial_units


for k,v in initial_units.items():
    data = requests.get(v['url']).text
    soup = BeautifulSoup(data,'lxml')

    sidebar=soup.find('aside')

    if k == 'Dark templar':
        image=sidebar.find('div',attrs={'data-source':'image2'})
        image=image.find('div',attrs={'class':'wds-tab__content'})
        image=image.find('a')['href']
    elif k in['Warp prism','Siege tank','Viking','Liberator','Zergling','Roach','Overlord']:
        image=soup.find('div',attrs={'data-source':'image2'})
        image=image.img['src']
    elif k == 'Interceptor':
        image=soup.find('figure',attrs={'data-source':'image'})
        image=image.img['src']

    else:
        image=soup.find('figure',attrs={'data-source':'image2'})
        image=image.a['href']
   
   
   
    race=sidebar.find('div',attrs={'data-source' : 'race'})
    race=race.find('a',attrs={'href': True})
    race=race.get_text('a')

     
    try:
        desc=sidebar.find('div',attrs={'data-source' : 'role'})
        desc=desc.find('div',attrs={'class': 'pi-font'})
        desc=desc.get_text('a')
    except:
        desc=""
    
 
    if k in ['Archon','MULE','Larva','Broodling','Infested terran','Changeling','Locust']:
        minerals=0
    else:
    
        minerals=soup.find('div',attrs={'data-source':'costmin'})
        minerals=minerals.div.find(text=True)

        if 'div' in minerals:
            minerals=minerals[0:minerals.find('d')]
        if '(' in minerals:
            minerals=minerals[0:minerals.find('(')]
        minerals=minerals.replace(" ","")

    

    if k in ['Archon','MULE','Queen','Warp prism','Interceptor','Overlord','Probe','SCV','Drone','Larva','Broodling','Infested terran','Changeling','Locust','Marine','Hellion','Hellbat','Zealot','Zergling']:
        vespene=0
    elif k == 'Ravager':
        vespene=soup.find('div',attrs={'data-source':'costgas'})
        vespene=vespene.p.find(text=True)
    else:
    
        vespene=soup.find('div',attrs={'data-source':'costgas'})
        vespene=vespene.div.find(text=True)

        if 'div' in vespene:
            vespene=vespene[0:vespene.find('d')]
        if '(' in vespene:
            vespene=vespene[0:vespene.find('(')]
        vespene=vespene.replace(" ","")

    if k in ['MULE','Interceptor','Overlord','Overseer','Interceptor','Larva','Broodling','Infested terran','Changeling','Locust']:
        supply='0'
    else:
        supply=soup.find('div',attrs={'data-source':'supply'})
        supply=supply.div.find(text=True)
    if '(' in supply:
        supply=supply[0:supply.find('(')]
    supply=supply.replace(" ","")

    """
    UNIT TIER IS A NON-TECHNICAL METRIC THAT IS NEITHER AGREED UPON OR IMPORTANT IN A MECHANICAL WAY.
    HOWEVER, I WANT TO DISPLAY DATA BASED ON TIER, THEREFORE I HAVE MANUALLY ENTERED UNIT TIERS BELOW.
    """
    print(k)
    if k in {'Probe','Interceptor','SCV','MULE','Larva','Drone','Overlord',
    'Overseer','Broodling','Changeling','Infested terran','Locust'}:
        tier = 0
    if k in {'Zealot','Adept','Stalker','Sentry','Marine','Reaper','Marauder',
    'Zergling','Baneling','Roach','Ravager','Queen'}:
        tier = 1
    if k in {'Immortal','Warp prism','Observer','Phoenix','Void ray','Oracle',
    'Ghost','Hellion','Hellbat','Siege tank','Cyclone','Widow mine','Hydralisk',
    'Lurker','Swarm host','Mutalisk'}:
        tier = 2
    if k in {'High templar','Dark templar','Archon','Disruptor','Banshee',
    'Raven','Liberator','Infestor','Corruptor','Viper'}:
        tier = 3
    if k in {'Carrier','Colossus','Tempest','Mothership','Thor','Battlecruiser',
    'Ultralisk','Brood lord'}:
        tier = 'Legendary'



    initial_units[k]['image']=image
    initial_units[k]['race']=race
    initial_units[k]['desc']=desc
    initial_units[k]['minerals']=minerals
    initial_units[k]['vespene']=vespene
    initial_units[k]['supply']=supply
    initial_units[k]['tier']=tier


    # # description=Text page has so many hyperlinks embedded that extraction of text
    # #   blocks will be a real chore. May come back to this, but likely will not.





print(initial_units)


#GET SUPPLY ICONS, MINERAL, VESPENE icons.
