from fastapi import APIRouter, FastAPI

from app.api.auth.auth_register import auth_register
from app.api.auth.auth_login import auth_login
from app.api.auth.auth_logout import auth_logout
from app.api.auth.auth_refresh_token import auth_refresh_token, RefreshTokenResponseModel
from app.api.auth.get_profile import get_profile, GetProfileResponseModel
from app.api.auth.edit_profile import edit_profile

from app.api.transactions.transaction_getList import transaction_getList, GetTransactionListResponseModel
from app.api.transactions.transaction_create import transaction_create, CreateTransactionResponseModel
from app.api.transactions.cancel_transaction import transaction_cancel
from app.api.transactions.update_transaction import transaction_update

from app.api.recommender.new_menu_recommender import new_menu_recommendation

api_router = APIRouter()

api_router.add_api_route('/api/v1/auth/register', auth_register, methods=['POST'], tags=['Auth'], status_code=201)
api_router.add_api_route('/api/v1/auth/login', auth_login, methods=['POST'], tags=['Auth'])
api_router.add_api_route('/api/v1/auth/logout', auth_logout, methods=['POST'], tags=['Auth'], status_code=204)
# api_router.add_api_route('/api/v1/auth/refresh_token', auth_refresh_token, methods=['POST'], tags=['Auth'], response_model=RefreshTokenResponseModel)
# api_router.add_api_route('/api/v1/auth/profile', get_profile, methods=['GET'], tags=['Auth'], response_model=GetProfileResponseModel)
# api_router.add_api_route('/api/v1/auth/profile', edit_profile, methods=['PUT'], tags=['Auth'], status_code=204)

api_router.add_api_route('/api/v1/transactions/get_list',transaction_getList, methods=['GET'], tags=['Transaction'], response_model=GetTransactionListResponseModel)
api_router.add_api_route('/api/v1/transactions/create',transaction_create, methods=['POST'], tags=['Transaction'], response_model=CreateTransactionResponseModel)
api_router.add_api_route('/api/v1/transactions/update',transaction_update, methods=['PUT'], tags=['Transaction'], status_code=204)
api_router.add_api_route('/api/v1/transactions/cancel',transaction_cancel, methods=['DELETE'], tags=['Transaction'], status_code=204)

api_router.add_api_route('/api/v1/recommender/new_menu',new_menu_recommendation, methods = ['GET'], tags=['Recommender'], status_code=204)