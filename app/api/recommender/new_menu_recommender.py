import pandas as pd
import numpy as np
import scipy
from scipy import stats

from pydantic import BaseModel
from fastapi import Response
from http import HTTPStatus

df_indonesiafood = pd.read_csv(r"C:\Users\Asus\Documents\FarizMatkul\Tst_rapih\kantinburjoitb\app\api\recommender\indonesian_foodsnack.csv")
df_borjufood = pd.read_csv(r"C:\Users\Asus\Documents\FarizMatkul\Tst_rapih\kantinburjoitb\app\api\recommender\burjoproducts.csv")

# def kesamaan(df, ingredients):
#         totalSim = []
#         a = 0
#         x = df_indonesiafood.iloc[ingredients, 2:].to_list()#ganti ingredients
#         for NameOfMenu in range(df.shape[0]):
#             Menu = df.iloc[NameOfMenu, 1:].to_list()
#             sim = scipy.stats.pearsonr(x, Menu)
#             sim = sim[0]
#             totalSim.append(sim)
#         return totalSim

# def sortBestRecommendation(totalSim):
#         sim = pd.DataFrame(totalSim, columns=['sim'])
#         sim.sort_values(by=['sim'], inplace=True, ascending=False)
#         sim = sim.reset_index()
#         sim = sim.iloc[1:11,0].to_list()
#         return sim

def new_menu_recommendation(menu_terlaris):
        LISTNAMAMENU = df_indonesiafood['name'].to_list()
        LISTMENUEXIST = df_borjufood['name'].to_list()
        final_df = df_indonesiafood.set_index('name')
        final_df = final_df.drop(LISTMENUEXIST)

        # if data in LISTNAMAMENU:
        #     a = False
        #     index = LISTNAMAMENU.index(data)
        # else :
        #     print('Menu ini tidak ada di kantin burjo!')

        
        index = LISTNAMAMENU.index(menu_terlaris)

        totalSim = []
        a = 0
        x = df_indonesiafood.iloc[index, 2:].to_list()#ganti ingredients
        for NameOfMenu in range(final_df.shape[0]):
            Menu = final_df.iloc[NameOfMenu, 1:].to_list()
            sim = scipy.stats.pearsonr(x, Menu)
            sim = sim[0]
            totalSim.append(sim)
        
        reccomend = pd.DataFrame(totalSim, columns=['kesamaan'])
        reccomend.sort_values(by=['kesamaan'], inplace= True, ascending= False)
        reccomend = reccomend.reset_index()
        reccomend = reccomend.iloc[1:11,0].to_list()
        # return (bestRecommendation_10)
        # print('kami sudah menemukan beberapa MENU BARU yang mungkin akan laris\nseperti:')

        # a=0
        # for recom in bestRecommendation_10:
        #     a+=1
        #     print(str(a)+'.', df_indonesiafood.iloc[recom,0])
    
        recommend_frame = []
        for recom in reccomend:
            recommend_frame.append(df_indonesiafood.iloc[recom,0])
        df = pd.DataFrame(recommend_frame, index=range(1, 11))
        return df.values.tolist()