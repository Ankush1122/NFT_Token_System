from .models import SmartContract
from .interface import *
from datetime import date


def my_cron_job():
    smart_contracts = SmartContract.objects.all()
    contracts = []
    for smart_contract in smart_contracts:
        contracts.append(getSmartContract(smart_contract))
    
    today = date.today()
    for contract in contracts:
        contract_status = getContractStatus(contract)
        if(contract_status["status"] == "Unexecuted" and today >= contract.getExpiryDate()):
            if(contract_status["conditions"] == "Unsatisfied"):
                print("Expire Contract")
            if(contract_status["conditions"] == "Satisfied"):
                if(contract.getPhysicalAsset()):
                    print("Call Backend")
                else:
                    print("Execute Contract")
