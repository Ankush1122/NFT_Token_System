from django.urls import path
from . import views

urlpatterns = [
    path('create_new_blockchain/', views.create_new_blockchain,
         name="create_new_blockchain"),
    path('get_balance/', views.get_balance, name="get_balance"),
    path('make_transaction/', views.make_transaction, name="make_transaction"),
    path('issue_transaction/', views.issue_transaction, name="issue_transaction"),
    path('generate_encryption_keys_pair/', views.generate_encryption_keys_pair,
         name="generate_encryption_keys_pair"),
    #path('expire_contract/', views.expire_contract, name="expire_contract"),
    #path('execute_contract/', views.execute_contract, name="execute_contract"),
    #path('get_contract_status/', views.get_contract_status, name="get_contract_status"),
    path('get_nft_history/', views.get_nft_history, name="get_nft_history"),
    path('get_all_transactions/', views.get_all_transactions,
         name="get_all_transactions"),
    path('get_blockchain/', views.get_blockchain, name="get_blockchain"),
    #path('cron_job/', views.cron_job, name="cron_job")
]
