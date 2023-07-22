from django.contrib import admin
from .models import SmartContract, Block, Transaction, Input, Output, BlockChain

admin.site.register(SmartContract)
admin.site.register(Block)
admin.site.register(Transaction)
admin.site.register(Input)
admin.site.register(Output)
admin.site.register(BlockChain)
