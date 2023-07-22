from rest_framework.response import Response
from rest_framework.decorators import api_view
from .interface import *
from .models import SmartContract
from .cron import my_cron_job


@api_view(['POST'])
def create_new_blockchain(request):
    response = createBlockChain(int(request.data["difficulty"]), int(
        request.data["blockSize"]), request.data["trustedPublicKey"], request.data["coinToken"], int(request.data["genesisAmount"]))
    return Response(response)


@api_view(['POST'])
def get_balance(request):
    response = getBalance(request.data["publicKey"], request.data["token"])
    return Response(response)


@api_view(['POST'])
def make_transaction(request):
    contract = None
    if (request.data["smartContract"] != "None"):
        contract = SmartContract.objects.filter(
            id=request.data["smartContract"])
        if not contract:
            return Response({"status": False, "response": "Contract not found, use valid id"})
        else:
            contract = getSmartContract(contract[0])
    response = makeTransaction(request.data["sender"], request.data["reciever"], int(
        request.data["amount"]), request.data["token"], request.data["privateKey"], contract, False)
    return Response(response)


@api_view(['POST'])
def issue_transaction(request):
    response = issueTransaction(request.data["owner"], int(
        request.data["amount"]), request.data["token"], request.data["privateKey"])
    return Response(response)


@api_view(['GET', 'POST'])
def generate_encryption_keys_pair(request):
    response = generateEncryptionKeysPair()
    return Response(response)


@api_view(['POST'])
def expire_contract(request):
    contract = None
    if (request.data["smartContract"] != "None"):
        contract = SmartContract.objects.filter(
            id=request.data["smartContract"])
        if not contract:
            return Response({"status": False, "response": "Contract not found, use valid id"})
        else:
            contract = getSmartContract(contract[0])
    response = expireContract(
        contract, request.data["trustedPrivateKey"])
    return Response(response)


@api_view(['POST'])
def execute_contract(request):
    contract = None
    if (request.data["smartContract"] != "None"):
        contract = SmartContract.objects.filter(
            id=request.data["smartContract"])
        if not contract:
            return Response({"status": False, "response": "Contract not found, use valid id"})
        else:
            contract = getSmartContract(contract[0])
    response = executeContract(
        contract, request.data["trustedPrivateKey"])
    return Response(response)


@api_view(['POST'])
def get_contract_status(request):
    contract = None
    if (request.data["smartContract"] != "None"):
        contract = SmartContract.objects.filter(
            id=request.data["smartContract"])
        if not contract:
            return Response({"status": False, "response": "Contract not found, use valid id"})
        else:
            contract = getSmartContract(contract[0])
    response = getContractStatus(contract)
    return Response(response)


@api_view(['POST'])
def get_nft_history(request):
    response = getNFTHistory(request.data["token"])
    return Response(response)


@api_view(['GET', 'POST'])
def get_all_transactions(request):
    response = getAllTransactions()
    return Response(response)


@api_view(['GET', 'POST'])
def get_blockchain(request):
    response = getBlockChain()
    time.sleep(30)
    return Response(response)


@api_view(['GET', 'POST'])
def cron_job(request):
    my_cron_job()
    return Response("successfully executed cron job")
