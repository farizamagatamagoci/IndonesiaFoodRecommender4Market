        
import pandas as pd
import numpy as np
import scipy
from scipy import stats

from pydantic import BaseModel
from app.api_models.base_response import BaseResponseModel

df_indonesiafood = pd.read_csv(r"C:\Users\Asus\Documents\FarizMatkul\Tst_rapih\kantinburjoitb\app\api\recommender\indonesian_foodsnack.csv")
df_borjufood = pd.read_csv(r"C:\Users\Asus\Documents\FarizMatkul\Tst_rapih\kantinburjoitb\app\api\recommender\burjoproducts.csv")

## pr: 
# cara nyari barang terfavorit gimana (querynya)
# masukin ke GET end pointnya gimana

class GetNewMenuListResponseModel(BaseResponseModel):
    class Config:
        schema_extra = {
            'example': {
                'data': [
                    {
                    'no': 1,
                    'Menu rekomendasi': 'Es Kelapa Tua',
                    }
                ],
                'meta': {},
                'success': True,
                'code': 200,
                'message': 'Success'
            }
        }

class MenuTerlaris(BaseModel):
    menu_laris : str

def kesamaan(df, ingredients):
        totalSim = []
        a = 0
        x = df_indonesiafood.iloc[ingredients, 2:].to_list()#ganti ingredients
        for NameOfMenu in range(df.shape[0]):
            Menu = df.iloc[NameOfMenu, 1:].to_list()
            sim = scipy.stats.pearsonr(x, Menu)
            sim = sim[0]
            totalSim.append(sim)
        return totalSim

def sortBestRecommendation(totalSim):
        sim = pd.DataFrame(totalSim, columns=['sim'])
        sim.sort_values(by=['sim'], inplace=True, ascending=False)
        sim = sim.reset_index()
        sim = sim.iloc[1:11,0].to_list()
        return sim

async def new_menu_recommendation(data: MenuTerlaris):
        # print('Berikut menu di Kantin Burjo ITB:')
        # for NamaMenu in range(df_indonesiafood.shape[0]):
        #     print(str(NamaMenu+1)+'.', df_indonesiafood.iloc[NamaMenu,0])

        # a = True
        LISTNAMAMENU = df_indonesiafood['name'].to_list()

        final_df = df_indonesiafood.set_index('name')
        final_df = final_df.drop(LISTNAMAMENU)

        # if data in LISTNAMAMENU:
        #     a = False
        #     index = LISTNAMAMENU.index(data)
        # else :
        #     print('Menu ini tidak ada di kantin burjo!')

        
        index = LISTNAMAMENU.index(data)
        totalSim = kesamaan(final_df, index)
        bestRecommendation_10 = sortBestRecommendation(totalSim)
        # return (bestRecommendation_10)
        # print('kami sudah menemukan beberapa MENU BARU yang mungkin akan laris\nseperti:')

        # a=0
        # for recom in bestRecommendation_10:
        #     a+=1
        #     print(str(a)+'.', df_indonesiafood.iloc[recom,0])
    
        recommend_frame = []
        a=0
        for recom in bestRecommendation_10:
            recommend_frame.append(df_indonesiafood.iloc[recom,0])
        df = pd.DataFrame(recommend_frame, index=range(1, 10))
        return final_df