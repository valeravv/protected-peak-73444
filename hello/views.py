import requests
from dateutil.parser import parse
from django.shortcuts import render
from json.decoder import JSONDecodeError
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponsePermanentRedirect, FileResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Greeting, Stuff

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

def cert(request, cert):
    html = open('hello/static/main.html', 'rb')
    return FileResponse(html)

def unrz(request, unrz):
    #Stuff.objects.get(unrz='9'+'020000000122401')
    try:
        s = Stuff.objects.get(unrz='9'+unrz)
        if not s.qr_url:
            s.qr_url = s.scanQR()
            s.save()
    except ObjectDoesNotExist:
        try:
            s = Stuff.objects.get( n = int(unrz) % 10000000000000)
            if not s.qr_url:
                s.qr_url = s.scanQR()
                s.save()
            return HttpResponsePermanentRedirect(str(s.unrz)[1:])
        except ObjectDoesNotExist:
            try:
                r = requests.get("https://www.gosuslugi.ru/api/vaccine/v2/cert/verify//unrz/"+unrz);
                print(r)
                j = r.json() 
                s = Stuff.fromJson(j)
                #update hello_stuff set r = unrz / 10000000000000 where r is null;
                #update hello_stuff set n = unrz % 10000000000000 where is null;
                #s.qr_url = s.scanQR()
                s.save()
            except JSONDecodeError:
                return HttpResponseNotFound('noJson')           
            except KeyError:
                return HttpResponseNotFound('empty')           
    return JsonResponse(s.getJson())

    '''

counter = 974506

timer = setInterval(function () {
    fetch(window.location.origin+'/unrz/0'+ (20000000000000 + counter))
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data);
  })
  .catch(function (err) {

  }); 
  counter++
},1100)

clearInterval(timer)



    '''
