import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from server.models import user
from server.models import user_login
from server.models import transaction
from server.models import food
from server.utils.db import db_engine

from server.routes.auth_registration import auth_register
from server.routes.auth_login import auth_login
from server.routes.transaction_create import transaction_create, CreateTransactionResponseModel
from server.routes.transaction_getList import transaction_getList, GetTransactionListResponseModel
from server.routes.transaction_update import transaction_update
from server.routes.transaction_cancel import transaction_cancel
from server.routes.food_recommender import new_menu_recommendation, GetRecommenderFoodResponseModel

import warnings
warnings.filterwarnings('ignore')

description= """
Ini adalah API untuk mencatat seluruh transaksi penjualan di suatu warung, mengetahui barang paling laku, dan prediksi barang lain yang kemungkinan laku dijual

## Mencatat seluruh transaksi penjualan di suatu toko
1. Mendapatkan seluruh transaksi yang sudah berjalan
2. Membuat transaksi baru
3. Mengupdate sebuah transaksi
4. Menghapus sebuah transaksi

## Mengetahui makanan paling laku
Anda dapat melihat X makanan paling laku di warung tersebut dari transaksi yang sudah berjalan

## Rekomendasi makanan lain yang kemungkinan laku di toko tersebut
Anda dapat melihat rekomendasi makanan lain yang kemungkinan laku dijual di toko tersebut berdasarkan bahan-bahan dasar dari makanan tersebut

-> disini saya akan memakai database warung di Kantin Burjo ITB sebagai subjek secara langsung
"""
user.Base.metadata.create_all(db_engine)
user_login.Base.metadata.create_all(db_engine)
transaction.Base.metadata.create_all(db_engine)
food.Base.metadata.create_all(db_engine)

app = FastAPI(
    title = "Food Snack Prediction API",
    description = description
)

@app.get('/', tags=["Lihat Menu Disini!"] ,response_class= HTMLResponse)
def index():
    output = ("""18220081 - Muhamad Fariz Ramadhan : Tugas API untuk TST <br> 
    ----------------------------------- <br>
    Selamat datang di Kantin Burjo ITB ! <br>
    Berikut adalah daftar menu makanan dan minuman yang dijual: <br>
    1	Sosis Bakar <br>
    2	Ngohiong Ayam Udang <br>
    3	Rawon Ayam <br>
    4	Usus Goreng Crispy <br>
    5	Ceker Rica Rica <br>
    6	Ceker Kecap Pedas <br>
    7	Ayam Suwir Kecap <br>
    8	Burung Puyuh Bakar <br>
    9	Dangkot Ayam <br>
    10	Ayam Bumbu Merah <br>
    11	Pepes Peda <br>
    12	Pempek Kapal Selam <br>
    13	Sambal Udang Goreng Petai <br>
    14	Udang Bakar Madu <br>
    15	Gulai Aceh Ikan Tongkol <br>
    16	Ikan Kerapu Asam Manis <br>
    17	Tahu Bulat <br>
    18	Martabak Tahu <br>
    19	Tempe Mendoan Purwokerto <br>
    20	Sapo Tahu <br>
    21	Tahu Gejrot <br>
    22	Tahu Rambutan<br>
    23	Perkedel Tempe<br>
    24	Tahu Kukus<br>
    25	Bacem Tahu Tempe<br>
    26	Sayur Pepaya Muda <br>
    27	Ote Ote <br>
    28	Beberuk Terong <br>
    29	Sayur Asem Jakarta <br>
    30	Sambal Pencok Kacang Panjang <br>
    31	Sambal Belut<br> 
    32	Sambal Pecak<br>
    33	Sambal Embe<br>
    34	Sambal Dabu Dabu<br>
    35	Nasi Daun Jeruk<br>
    36	Indomie Seblak<br>
    37	Mie Tek Tek Kuah<br>
    38	Mie Goreng Basah <br>
    39	Kimbab <br>
    40	Nasi Mandhi <br>
    41	Bola Bola Mie <br>
    42	Ketupat <br>
    43	Nasi Ayam Semarang <br>
    44	Nasi Tiwul <br>
    45	Risotto <br>
    46	Mie Goreng Nyemek <br>
    47	Bubur Korea (Dakjuk) <br>
    48	Nasi Gemuk <br>
    49	Nasi Tomat <br>
    50	Crepes Teflon <br>
    51	Oreo Goreng <br>                    
    52	Gingerbread (Kue Jahe) <br>                    
    53	Kue Baruasa <br>                    
    54	Kue Janda Genit <br>                    
    55	Martabak Manis Mini <br>                    
    56	Bolu Chocolatos <br>                    
    57	Burger Bun <br>                                      
    58	Brownies Chocolatos <br>                                
    59	Tela Tela Singkong <br>                    
    60	Madu Mongso <br>                    
    61	Ubi Goreng <br>                    
    62	Banana Roll <br>                    
    63	Tape Ketan <br>                    
    64	Kacang Atom (Sukro) Homemade <br>                    
    65	Kue Talam <br>                    
    66	Bihun Gulung <br>                    
    67	Wedang Angsle <br>                    
    68	Telur Gulung <br>                    
    69	Choi Pan <br>                    
    70	Pisang Gulung <br>                    
    71	Lontong Medan <br>                    
    72	Pisang Goreng Madu <br>                    
    73	Cibay Pedas <br>                    
    74	Timus Singkong <br>                    
    75	Cucuru Bayao <br>                    
    76	Pisang Goreng Pontianak <br>                    
    77	Sekoteng <br>                    
    78	Kue Mendut <br>                    
    79	Puding Telor Ceplok <br>                    
    80	Puding Susu <br>                    
    81	Es Lilin Nutrijel Pelangi <br>                    
    82	Vla Puding Buah <br>                    
    83	Rempeyek Teri <br>                    
    84	Keripik Bayam <br>                    
    85	Keripik Singkong <br>                    
    86	Rengginang <br>                    
    87	Kentang Mustofa <br>                    
    88	Kerupuk Nasi <br>                    
    89	Keripik Singkong Balado <br>                    
    90	Coffee Jelly <br>                    
    91	Es Kopi Susu <br>                    
    92	King Mango Thai <br>                    
    93	Sale Pisang <br>                    
    94	Dalgona Coffee <br>                    
    95	Es Krim Strawberry <br>                    
    96	Dalgona Milo <br>                    
    97	MPASI 6 Bulan (Bubur Kabocha) <br>                    
    98	Teh Susu Telur (Talua) Khas Medan <br>                    
    99	Es Alpukat <br>                    
    100	Bandrek <br>                    
    """)
    return output

app.add_api_route('/api/v1/auth/register', auth_register, methods=['POST'], tags=['Auth'], status_code=201)
app.add_api_route('/api/v1/auth/login', auth_login, methods=['POST'], tags=['Auth'])
app.add_api_route('/api/v1/transactions/create',transaction_create, methods=['POST'], tags=['Transaction'], response_model=CreateTransactionResponseModel)
app.add_api_route('/api/v1/transactions/get_list',transaction_getList, methods=['GET'], tags=['Transaction'], response_model=GetTransactionListResponseModel)
app.add_api_route('/api/v1/transactions/update',transaction_update, methods=['PUT'], tags=['Transaction'], status_code=204)
app.add_api_route('/api/v1/transactions/cancel',transaction_cancel, methods=['DELETE'], tags=['Transaction'], status_code=204)

app.add_api_route('/api/v1/recommender/new_menu',new_menu_recommendation, methods = ['GET'], tags=['Recommender'])

if __name__ == '__main__':
    uvicorn.run("app", host = "0.0.0.0", port = 8090, reload = True)