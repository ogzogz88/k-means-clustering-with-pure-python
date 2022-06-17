#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd
import numpy as np
import random as rnd
import matplotlib.pyplot as plt

#load the dataset
hcv_data = pd.read_csv("hcvdat0.csv")

#read the data
hcv_data.head()

# yapılacaklar
# merkez hesaplamada mutlak değer al TAMAMLANDI
# merkezleri veri içinden değil rastgele aralıklar içinden seç TAMAMLANDI
# sınıf sayılarını logla TAMAMLANDI
# boş değerleri doldur TAMAMLANDI


# In[20]:


# see number of rows of the data
number_of_rows = len(hcv_data)
print("***********")
print("number_of_rows")
print(number_of_rows)
print("***********")


# In[21]:


# prepare dataframe

DATA_FRAME = hcv_data.iloc[0:615,:]
DATA_FRAME.drop(['Unnamed: 0','Category','Age','Sex'], inplace=True, axis=1)
DATA_FRAME.head()


# In[22]:


#check for null or missing values
DATA_FRAME.isna().sum()


# In[23]:


#To insert the mean value of each column into its missing rows: 
DATA_FRAME.fillna(DATA_FRAME.mean().round(1), inplace=True)


# In[24]:


#check for null or missing values
DATA_FRAME.isna().sum()


# In[25]:


# create random centroid generator. It uses the max and min values of the column

def create_random_centroids(data,n):
    column_len = len(data.columns)
    random_centroids = data.sample(n, ignore_index=True)
    print("before create_random_function")
    print(random_centroids)
    
    def create_random_values():
        max_vals =[]
        min_vals =[]
        random_vals=[]
        for i in range(column_len):
            max_vals.append(random_centroids[random_centroids.columns[i]].max())
            min_vals.append(random_centroids[random_centroids.columns[i]].min())
            random_vals.append(min_vals[i] + (max_vals[i]-min_vals[i])*rnd.random())
        return random_vals
    
    for i in range(n):
        random_centroids.iloc[i] = create_random_values()
    print("after create_random_function")
    print(random_centroids)
    return random_centroids


# In[26]:


# k-means clustering with pure python
# define the function

def k_means(K_number, data_frame):
   
   #centroids = data_frame.sample(n=K_number)
   centroids = create_random_centroids(data_frame, K_number)
   print("* * * * * * * * * ") 
   print("first centroids")
   print(centroids)
   print("* * * * * * * * * ") 
    
   #color =[]
   #def generate_color(K_number):
   #    for color_number in range(K_number):
   #         r = rnd.randint(0,255)
   #         g = rnd.randint(0,255)
   #         b = rnd.randint(0,255)
   #         color.append('#%02x%02x%02x' % (r, g, b))
            
   #generate_color(K_number)
   #print("- - - - - - - - -") 
   #print("color")
   #print(color)
   #print("- - - - - - - - -") 
    
   
   difference = 1

   while(difference!=0):
      i=1
      for index1,row_c in centroids.iterrows():
         # ED: euclidean distance
         ED=[]
         for index2,row_d in data_frame.iterrows():
            #d1=(row_c["CHE"]-row_d["CHE"])**2
            #d2=(row_c["CREA"]-row_d["CREA"])**2
            #d=np.sqrt(d1+d2)

            d_sum = 0
            for col_name in centroids.columns: 
                d_sum += (row_c[col_name] - row_d[col_name])**2
                
            distance = np.sqrt(d_sum)
                   
            ED.append(distance)
            #print("* * * * * * * * * ")  
            #print("ED(Euclidean Distance)")
            #print(ED)
            #print("* * * * * * * * * ")
        
        
         data_frame[i]=ED
         print("- - - - - - - - -")
         print("Class : %x" % i)
         print("- - - - - - - - -")   
         print("data_frame Value")
         print("- - - - - - - - -")  
         print(data_frame)
         i=i+1
        
      # find nearest centroid and append nearest centroid number to "Cluster" column
      C=[]
      for index,row in data_frame.iterrows():
          min_dist=row[1]
          pos=1
          for i in range(K_number):
              if row[i+1] < min_dist:
                  min_dist = row[i+1]
                  pos=i+1
          C.append(pos)
      data_frame["Cluster"]=C

      # specify new centroids
      centroids_new = data_frame.abs().groupby(["Cluster"]).mean()[centroids.columns]
                
      column_len = len(centroids.columns)
      #print("centroid column len")
      #print(column_len)
    
      # The sum() method adds all values in each column and returns the sum for each column      
      for i in range(column_len):
            difference = np.absolute((centroids_new[centroids_new.columns[i]].values - centroids[centroids.columns[i]].values)).sum()
            
            
      number_of_clusters = data_frame.groupby('Cluster').size()
      print("number_of_clusters")
      print(number_of_clusters)
    
      print("* * * * * * * * * ")
      print("difference")
      print(difference)
      print("* * * * * * * * * ")
        
      # update centroids value with the centroids_new
      centroids = data_frame.abs().groupby(["Cluster"]).mean()[centroids.columns]
      print("****************")
      print("new centroid")
      print(centroids)
      print("****************")



   #for k in range(K_number):
    #  data = data_frame[data_frame["Cluster"]==k+1]
     # plt.scatter(data["CHE"],data["CREA"],c=color[k])
   #plt.scatter(centroids["CHE"],centroids["CREA"],c='red')
   #plt.xlabel('CHE Value')
   #plt.ylabel('CREA Value')
   #plt.show()


# In[27]:


k_means(4,DATA_FRAME)


# In[ ]:




