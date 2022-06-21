from datetime import datetime
from gettext import find
from bs4 import BeautifulSoup
import requests
import re
from main import initial_units
import pprint
import pandas as pd

import psycopg2


z_flag=True
t_flag=True
p_flag=True
mineral_flag=True
vespene_flag=True
# grid_unit={}
id=0
misc_images={}
d={
    'id':[],
    'name':[],
    'race':[],
    'minerals':[],
    'vespene':[],
    'supply':[],
    'desc':[],
    'unit_tier':[],
    'unit_image':[],    
    'url':[]
    }


for k,v in initial_units.items():
    data = requests.get(v['url']).text
    soup = BeautifulSoup(data,'lxml')

    sidebar=soup.find('aside')
    
    #Get all unit model images
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
   
   
    #Get race of each unit; terran/zerg/protoss
    race=sidebar.find('div',attrs={'data-source' : 'race'})
    race=race.find('a',attrs={'href': True})
    race=race.get_text('a')

    #If the first unit of each race, get that race's unique image for supply
    if race == 'Protoss' and p_flag==True:
        p_flag=False
        p_supply_image=soup.find('img',attrs={'alt':'Psi'})['src']
    
    if race == 'Terran' and t_flag==True:
        t_flag=False
        t_supply_image=soup.find('img',attrs={'alt':'Supply'})['src']
    
    if race == 'Zerg' and z_flag==True:
        z_flag=False
        z_supply_image=soup.find('img',attrs={'alt':'Control'})['src']
    
    #Get minerals and vespene icons. Not needed every loop, will just grab from stalker
    if k=='Stalker':
        minerals_icon=soup.find('img',attrs={'alt':'Minerals'})['src']
        vespene_icon=soup.find('div',attrs={'data-source':'costgas'})
        vespene_icon=vespene_icon.find('a',attrs={'class':'image'})['href']



    #About half of the units have a 'role' description. Grab that if it exists. 
    try:
        desc=sidebar.find('div',attrs={'data-source' : 'role'})
        desc=desc.find('div',attrs={'class': 'pi-font'})
        desc=desc.get_text('a')
    except:
        desc=""
    
    #If a unit costs minerals, grab that value. Shave off extra blank space or text
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

    
     #If a unit costs gas, grab that value. Shave off extra blank space or text
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

     #If a unit costs supply, grab that value. Shave off extra blank space or text
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
        tier = 4
    """
    ###  id = db.Column(db.Integer, primary_key=True)
    ###  name = db.Column(db.String(50), nullable=False)
    ###  created=db.Column(db.DateTime, default=datetime.utcnow())
    ###  race = db.Column(db.String(20), nullable=False)
    ###  minerals = db.Column(db.Integer)
    ###  vespene = db.Column(db.Integer)
    ###  supply = db.Column(db.Integer)
    ###  desc = db.Column(db.String(300))
    ###  unit_tier = db.Column(db.Integer)
    ###  unit_image = db.Column(db.String(80))
    ###  url=db.Column(db.String(80))

    """
    d['id'].append(id)
    d['name'].append(k.lower())
    d['race'].append(race)
    d['minerals'].append(int(minerals))
    d['vespene'].append(int(vespene))
    #Banelings have .5 supply. 
    # Irritating, so am rounding to 1. Hope to refine later on.
    if supply =='0.5':
        supply='1'
    d['supply'].append(int(supply))
    d['desc'].append(desc)
    d['unit_tier'].append(tier)
    d['unit_image'].append(image)
    d['url'].append(v['url'])
    
    id+=1
 

    
    print(k)

#Add oneoffs after the fact!
misc_images['p_supply_icon']=p_supply_image
misc_images['t_supply_icon']=t_supply_image
misc_images['z_supply_icon']=z_supply_image
misc_images['mineral_icon']=minerals_icon
misc_images['vespene_icon']=vespene_icon



# print(d)

df=pd.DataFrame(data=d)
print(df)





# Starcraft_Units={
#         'race':{
#             'Protoss':{
#                 'units':{
#                     'tier0':{},
#                     'tier1':{},
#                     'tier2':{},
#                     'tier3':{},
#                     'tier4':{},
#                 },
#                 'p_supply_icon':""
#             },
#             'Terran':{
#                 'units':{
#                     'tier0':{},
#                     'tier1':{},
#                     'tier2':{},
#                     'tier3':{},
#                     'tier4':{},
#                 },
#                 't_supply_icon':""
#             },
#             'Zerg':{
#                 'units':{
#                     'tier0':{},
#                     'tier1':{},
#                     'tier2':{},
#                     'tier3':{},
#                     'tier4':{},
#                 },
#                 'z_supply_icon':""
#             },
#         },
#         "mineral_icon":"",
#         "vespene_icon":""
#     }
#

   # unit= {
    #         'image':image,
    #         'race':race,
    #         'desc':desc,
    #         'minerals':minerals,
    #         'vespene':vespene,
    #         'supply':supply,
    #         'url':v['url']}
    
    
    
    # if race == "Protoss" and tier == 'tier0':
    #     Starcraft_Units['race']['Protoss']['units']['tier0'][k]=unit 
    # elif race == "Protoss" and tier == 'tier1':
    #     Starcraft_Units['race']['Protoss']['units']['tier1'][k]=unit 
    # elif race == "Protoss" and tier == 'tier2':
    #     Starcraft_Units['race']['Protoss']['units']['tier2'][k]=unit 
    # elif race == "Protoss" and tier == 'tier3':
    #     Starcraft_Units['race']['Protoss']['units']['tier3'][k]=unit 
    # elif race == "Protoss" and tier == 'tier4':
    #     Starcraft_Units['race']['Protoss']['units']['tier4'][k]=unit 

    # elif race == "Terran" and tier == 'tier0':
    #     Starcraft_Units['race']['Terran']['units']['tier0'][k]=unit 
    # elif race == "Terran" and tier == 'tier1':
    #     Starcraft_Units['race']['Terran']['units']['tier1'][k]=unit 
    # elif race == "Terran" and tier == 'tier2':
    #     Starcraft_Units['race']['Terran']['units']['tier2'][k]=unit 
    # elif race == "Terran" and tier == 'tier3':
    #     Starcraft_Units['race']['Terran']['units']['tier3'][k]=unit 
    # elif race == "Terran" and tier == 'tier4':
    #     Starcraft_Units['race']['Terran']['units']['tier4'][k]=unit 

    # elif race == "Zerg" and tier == 'tier0':
    #     Starcraft_Units['race']['Zerg']['units']['tier0'][k]=unit 
    # elif race == "Zerg" and tier == 'tier1':
    #     Starcraft_Units['race']['Zerg']['units']['tier1'][k]=unit 
    # elif race == "Zerg" and tier == 'tier2':
    #     Starcraft_Units['race']['Zerg']['units']['tier2'][k]=unit 
    # elif race == "Zerg" and tier == 'tier3':
    #     Starcraft_Units['race']['Zerg']['units']['tier3'][k]=unit 
    # elif race == "Zerg" and tier == 'tier4':
    #     Starcraft_Units['race']['Zerg']['units']['tier4'][k]=unit 