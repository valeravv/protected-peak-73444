import requests
from dateutil.parser import parse
from django.shortcuts import render
from json.decoder import JSONDecodeError
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponsePermanentRedirect
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
    fetch('https://protected-peak-73444.herokuapp.com/unrz/0'+ (20000000000000 + counter))
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

function unrz(r,u) {
    return (r + 100).toString().substring(1) + (u + 10000000000000).toString().substring(1)
}

ri = 0; u = 1287955;

regs = [77,78,24,66,61,02,16,72,74,52,63,05,24,26,54,42,59,]

function next_r() {
  ri = ri + 1;
  if (ri >= regs.length) {
    next_n()
  } else {
    plan()
  }
}

function next_n() {
  ri = 0;
  u = u + 1
  plan()
}

function plan() {
if (planned) setTimeout(function () {
  fetch('https://protected-peak-73444.herokuapp.com/unrz/'+unrz(regs[ri],u))
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data);
    next_n()
  })
  .catch(function (err) {
    next_r()
  }); 
},600)
}

planned = true

plan()


    '''
