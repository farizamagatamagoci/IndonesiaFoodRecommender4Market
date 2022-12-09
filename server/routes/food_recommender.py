import pandas as pd
from server.api_models.base_response_food import BaseResponseModelFood
import scipy
import os

from server.api_models.food_model import FoodModel

from fastapi import Depends
from server.auth.authentication import Authentication

class GetRecommenderFoodResponseModel(BaseResponseModelFood):
    class Config:
        schema_extra = {
            'example': {
                'Makanan Terlaris': {'Makanan Terlaris' : 'Bubur Sumsum',},
                'Makanan Rekomendasi': [
                    {
                    'nomor': 1,
                    'makanan' : 'Es Kacang Ijo'
                    }
                ]
            }
        }

# absolute_path = os.path.dirname("\foodsnack_prediction_api")
# df_indonesiafood = pd.read_csv(absolute_path, '..\server\models\data\indonesian_foodsnack.csv')
# df_borjufood = pd.read_csv(absolute_path, '..\server\models\data\burjoproducts.csv')
df_indonesiafood = pd.read_csv('indonesian_foodsnack.csv')
df_borjufood = pd.read_csv('burjoproducts.csv')

def new_menu_recommendation(menu_terlaris, payload = Depends(Authentication())):
    LISTNAMAMENU = df_indonesiafood['name'].to_list()
    LISTMENUEXIST = df_borjufood['name'].to_list()
    if not(menu_terlaris in LISTMENUEXIST):
        return("Menu tersebut tidak dijual")
    else:
        final_df = df_indonesiafood.set_index('name')
        final_df = final_df.drop(LISTMENUEXIST)

        
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

        recommend_frame = []
        a = 0
        for recom in reccomend:
            a += 1
            recommend_frame.append(
                FoodModel(
                    makananterlaris = menu_terlaris,
                    nomor = a,
                    makanan = final_df.index[recom]
                )
            )

        return GetRecommenderFoodResponseModel(
            Makanan_Terlaris= menu_terlaris,
            Makanan_Rekomendasi= recommend_frame
        )