

import os

from django.conf import settings
from .messages import HTTP_STATUS_MESSAGES
from django.http import JsonResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt 
def login(request):
    #Sadece POST isteklerini kabul etmeliyiz:
    #GET kullanırsak header kısmında gözükür ve bunu istemiyoruz
    if request.method == 'POST':
        
        try:
            #Frontendten aldığımız username ve password JSON formatında 
            #Ve bunu kullanmak için parse ediyoruz
            body= json.loads(request.body)

            #Parse ettiğimiz datadan username ve passwordu çekiyoruz
            username = body.get("username")
            password = body.get("password")

            #Kullanıcı adı veya şifre boşsa hata mesajı yazdırma.
            if not username or not password:
                return JsonResponse({"error": "Kullanıcı adı ve şifre gereklidir"}, status=400)

        #Eğer boş data vs. yollanırsa yakalıyor ve hata mesajını veriyoruz
        except json.JSONDecodeError:
            return JsonResponse({"error":"geçersiz JSON"},status=400)
        
        #Yollayacağımız API 
        url="https://agentcreatortestapi.global-bilgi.entp/security/login"

        #Yollayacağımız json mesajı
        #"username": "telliatestalim","password": "6h87&s6Y"
        payload={
            "scope": "openid",
            "grant_type": "password",
            "client_id": "agent-creator-test",
            "username": username,
            "password": password
        }

        #API'ye istek atma ve response alma
        try:
            #Headersı JSON formatında veri yolladığımızı söylemek için kullanıyoruz.
            headers={"Content-Type":"application/json"}

            #API'ye isteği burda atıyoruz.
            response= requests.post(url,json=payload,headers=headers,timeout=30, verify='_.global-bilgi.entp.crt')
            #Status kodunu alıp, uygun olan mesajı messages.py dosyasından çekiyoruz.
            status_code=response.status_code
            status_message=HTTP_STATUS_MESSAGES.get(status_code,"Bilinmeyen Değer")
            #Status koduna göre doğrulama yapıyoruz.
            #Username ve password başarılıysa:
            if 200<=status_code<300:
                data=response.json()
                #Datayı Frontende yolluyoruz.
                return JsonResponse({"message":status_message,      
                                     "status_code":status_code,
                                     "data":data},
                                     status=status_code)
            
            #Username ve password başarısızsa:
            else:
                #Status koda göre hata mesajını yolluyoruz.
                return JsonResponse({"error":status_message,
                                     "status_code":status_code},
                                     status= status_code)  
        except requests.Timeout:
            return JsonResponse({"error":"API Zaman Aşımı"},
                                status=408)
        except requests.ConnectionError:
            return JsonResponse({"error":"API Bağlantı Hatası"},
                                status=503)
        except Exception as e:
            return JsonResponse({"error":f"Beklenmeyen Hata: {str(e)}"},
                                status=500)
    else:
        return JsonResponse({"error":"Sadece POST isteği kabul edilir"},status=405)
    

def agentId(request):
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(BASE_DIR, "config.json")

    with open(config_path, "r") as f:
        config = json.load(f)
    
    agent= config["agent"]
    url= config["url"]+agent
    cert=config["verify"]
    response = requests.get(url,verify=cert)
    data= response.json()
    agent_id= data["agentId"]
    name= data["name"]
    return JsonResponse({"agent_id": agent_id,
                         "name": name})
