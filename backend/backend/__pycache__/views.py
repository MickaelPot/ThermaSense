from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .serializers import UserSerializer
from .model_user import User
from django.contrib.auth.hashers import make_password, check_password

#from controler_communication_LORA import demandeTemperature



@csrf_exempt
def getTemperature(request):
    if request.method=='GET':

        from random import randint
        from sys import exit
        from time import time

        from rak811.rak811_v3 import Rak811


        # Send packet every P2P_BASE + (0..P2P_RANDOM) seconds
        P2P_BASE = 30
        P2P_RANDOM = 60

        # Magic key to recognize our messages
        P2P_MAGIC = b'\xca\xfe'

        lora = Rak811()

        # Most of the setup should happen only once...
        print('Setup')
        # Set module in LoRa P2P mode
        response = lora.set_config('lora:work_mode:1')
        for r in response:
            print(r)

        # RF configuration
        # - Avoid LoRaWan channels (You will get quite a lot of spurious packets!)
        # - Respect local regulation (frequency, power, duty cycle)
        freq = 869.800
        sf = 7
        bw = 0  # 125KHz
        ci = 1  # 4/5
        pre = 8
        pwr = 16
        lora.set_config(f'lorap2p:{int(freq*1000*1000)}:{sf}:{bw}:{ci}:{pre}:{pwr}')

        data=""

        print('Entering send/receive loop')
        counter = 0
        try:
            while True:
                # Calculate next message send timestamp
                next_send = time() + P2P_BASE + randint(0, P2P_RANDOM)
                # Set module in receive mode
                lora.set_config('lorap2p:transfer_mode:1')
                # Loop until we reach the next send time
                # Don't enter loop for small wait times (<1 1 sec.)
                while (time() + 1) < next_send:
                    wait_time = next_send - time()
                    print('Waiting on message for {:0.0f} seconds'.format(wait_time))
                    # Note that you don't have to listen actively for capturing message
                    # Once in receive mode, the library will capture all messages sent.
                    lora.receive_p2p(wait_time)
                    while lora.nb_downlinks > 0:
                        message = lora.get_downlink()
                        data = message['data']
                        break
                    print(data)
                    break
                # Time to send message
                counter += 1
                print('Send message {}'.format(counter))
                # Set module in send mode
                lora.set_config('lorap2p:transfer_mode:2')
                lora.send_p2p(P2P_MAGIC + bytes.fromhex('{:08x}'.format(counter)))
                break

        except:  # noqa: E722
            pass

        print('All done')
    

        #iot = demandeTemperature()
        iot= data.decode("utf-8")
        data = {
            'temperature': iot,
        }
        return JsonResponse(data,safe=False)
    
@api_view(['POST'])
def addUser(request):
    data = JSONParser().parse(request)
    boolean_valide= False
    try:
        if "mail" in data:
            user = User.objects.get(mail=data["mail"])
            return JsonResponse({"message": "mail existant"},safe=False)
    except User.DoesNotExist:
        boolean_valide=True
    if boolean_valide:
        if("password" in data):
            data["password"]=make_password(data["password"])
        user_serializer=UserSerializer(data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({"message": "success"},safe=False)
        return JsonResponse({"message": "unsuccess"},safe=False)
    return JsonResponse({"message": "unsuccess"},safe=False)
    
@api_view(['POST'])
def getUser(request):
    data = JSONParser().parse(request)
    if "mail" in data:
        user=User.objects.filter(mail=data["mail"])
        if len(user)>0:
            user=user[0]
            user_serializer=UserSerializer(user)
            return JsonResponse(user_serializer.data,safe=False)
        return JsonResponse({"message": "unsuccess"},safe=False)
    return JsonResponse({"message": "unsuccess"},safe=False)
    
@api_view(['PUT'])
def updateUser(request):
    data = JSONParser().parse(request)
    if "id" in data:
        try:
            user = User.objects.get(pk=data["id"])
        except User.DoesNotExist:
            return JsonResponse({"message": "unsuccess"})
        if("password" in data):
            data["password"]=make_password(data["password"])
        user_serializer=UserSerializer(user, data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({"message": "success"},safe=False)
        return JsonResponse({"message": "unsuccess"},safe=False)
    return JsonResponse({"message": "unsuccess"},safe=False)
    
@api_view(['DELETE'])
def deleteUser(request):
    data = JSONParser().parse(request)
    if "mail" in data:
        user=User.objects.filter(mail=data["mail"])
        if len(user)>0:
            user=user[0]
            user.delete()
            return JsonResponse({"message": "success"},safe=False)
        return JsonResponse({"message": "unsuccess"},safe=False)
    return JsonResponse({"message": "unsuccess"},safe=False)

@api_view(['POST'])
def authorizeUser(request):
    data = JSONParser().parse(request)
    if "mail" in data:
        try:
            user = User.objects.get(mail=data["mail"])
            if("password" in data):
                if check_password(data["password"], user.password):
                    return JsonResponse({"message": "success"},safe=False)
                return JsonResponse({"message": "mot de passe incorrect"},safe=False)
            return JsonResponse({"message": "mot de passe manquant"},safe=False) 
        except User.DoesNotExist:
            return JsonResponse({"message": "compte inexistant"})
    return JsonResponse({"message": "mail manquant"},safe=False)

