from requests import request
import json
from datetime import datetime
import pandas as pd
from pandas import json_normalize 
import scipy
from server.api_models.food_model import FoodModel
from server.api_models.base_response_diabetesfood import BaseResponseModelDiabetesFood

class FoodsforDiabetes(BaseResponseModelDiabetesFood):
    class Config:
        schema_extra = {
            'example': {
                'Status Diabates': {'Kamu Diabetes'},
                'Makanan Terfavorit': {'Makanan Terfavorit' : 'Bubur Sumsum',},
                'Makanan Rekomendasi': [
                    {
                    'nomor': 1,
                    'makanan' : 'Es Kacang Ijo'
                    }
                ]
            }
        }

def DiabetesCekFood (pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, diabetespedigreefunction,age, makanan_fav):
    # url_diabetes = "https://tugasbesar.azurewebsites.net/token"
    # data = {
    #     "username": "string",
    #     "password": "string"
    # }
    # response_diabetes = request("POST", url_diabetes, data=data)
    
    # access_token = response_diabetes.json()["access_token"]
    # token_type = response_diabetes.json()["token_type"]

    # #make request
    url_diabetes = f"https://diabetestubes.azurewebsites.net/Diabetes_Prediction"
    headers = {
        "accept": "application/json",
    #     "Authorization": token_type + " " + access_token, 
        "Content-Type": "application/json"
    }
    params ={
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": bloodpressure,
        "SkinThickness": skinthickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": diabetespedigreefunction,
        "Age": age
        }

    response_diabetes = request("POST", url_diabetes, headers=headers, json= params)
    result_diabetes = response_diabetes.json()
    #-----nembak fayy beres

    df_indonesiafood = pd.read_csv('indonesian_foodsnack.csv')
    
    LISTNAMAMENU = df_indonesiafood['name'].to_list()
    if not(makanan_fav in LISTNAMAMENU):
        return("Coba Makanan Lain!")
    else:
        # if(result_diabetes == 1):
        #     df_indonesiafood = df_indonesiafood.drop(df_indonesiafood.loc[:, 'cokelat': 'tepung', 'susu'].column, axis =1)
        
        index = LISTNAMAMENU.index(makanan_fav)
        
        df_indonesiafood = df_indonesiafood.set_index('name')
        totalSim = []
        a = 0
        x = df_indonesiafood.iloc[index, 1:].to_list()#ganti ingredients
        for NameOfMenu in range(df_indonesiafood.shape[0]):
            Menu = df_indonesiafood.iloc[NameOfMenu, 1:].to_list()
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
                    nomor = a,
                    makanan = df_indonesiafood.index[recom]
                )
            )
        
        return BaseResponseModelDiabetesFood(
            Status_Diabetes= response_diabetes,
            Makanan_Terfavorit= makanan_fav,
            Makanan_Rekomendasi= reccomend
        )