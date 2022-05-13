import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


d=pd.read_csv('data/data.csv')
index=[0, 186, 372, 558, 744, 930, 1116, 1302, 1488, 1674, 1860
       , 2046, 2232, 2418, 2604, 2790, 2976, 3162, 3348, 3534
       , 3720, 3906, 4092, 4278, 4464, 4650, 4836, 5022, 5208
       , 5394, 5580, 5766, 5952, 6138, 6324, 6510, 6696, 6882
       , 7068, 7254, 7440, 7626, 7812, 7998, 8184, 8370, 8556
       , 8742, 8928, 9114, 9300, 9486, 9672, 9858, 10044, 10230
       , 10416, 10602, 10788, 10974, 11160, 11346, 11532, 11718
       , 11904, 12090, 12276, 12462, 12648, 12834, 13020, 13206
       , 13392, 13578, 13764, 13950, 14136, 14322, 14508, 14694
       , 14880, 15066, 15252, 15438, 15624, 15810, 15996, 16182
       , 16368, 16554, 16740, 16926, 17112, 17298, 17484, 17670
       , 17856, 18042, 18228, 18414, 18600, 18786, 18972, 19158
       , 19344, 19530]

for i in range (10,len(index)-7):
        
    selected=d[index[i]:index[i+1]]
    data=selected.groupby(['R','D']).max().tail(15)

   
    N = len(data['Cases'])
    c= ['#adb0ff','#ffb3ff','#90d595' ,'#e48381' ,'#aafbff' 
         ,'#f7bb5f' ,'#eafb50','#adb0ff','#ffb3ff','#90d595' 
         ,'#e48381' ,'#aafbff' ,'#f7bb5f' ,'#eafb50' ,'#90d595']

        
    x = np.log(data['Deaths'])
    y = np.log(data['Recovered'])
    colors = c[0:N]
    area =list(map(int, list(data['Cases'])))
    area=np.array(area)
    
    df = pd.DataFrame({
        'X': x,
        'Y': y,
        'Colors': colors,
        "bubble_size":area/10
        })

    
    fig,ax=plt.subplots(figsize=(15,8))
    
    
    plt.scatter('X', 'Y', s='bubble_size',alpha=0.5, data=df ,c='Colors' )
    plt.xlabel("Death cases", size=18)
    plt.ylabel("Recovered Cases", size=18)
   
    
    country=list(data['Country'])
    date=list(data['ObservationDate'])
    conf=list(data['Cases'])
    death= list(np.log(data['Deaths']))
    recovered = list(np.log(data['Recovered']))
    

    
    for j in range (0,len(country)):
        
        ax.annotate(country[j]+ '\n' + str(conf[j] ),
                    xy=( death[j]-0.0002 , recovered[j]-0.0002 ), xycoords='data')    
    
    
    ax.text(1,0.1,date[0],transform=ax.transAxes , color='#777777' ,size=32,ha='right',weight=800)
    
    
    plt.savefig('images/A/' + str(i+1) + '.png')

