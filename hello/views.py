import requests
from dateutil.parser import parse
from django.shortcuts import render
from json.decoder import JSONDecodeError
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
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
            r = requests.get("https://www.gosuslugi.ru/api/vaccine/v2/cert/verify//unrz/"+unrz);
            print(r)
            j = r.json() 
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 91213a4 (move logic to Stuff Model)
            s = Stuff.fromJson(j)
            #update hello_stuff set r = unrz / 10000000000000 where r is null;
            #update hello_stuff set n = unrz % 10000000000000 where is null;
            #s.qr_url = s.scanQR()
<<<<<<< HEAD
=======
            s = Stuff(
                unrz = int(j["unrz"]),
                birthdate = parse(j["birthdate"],dayfirst=True),
                expiredAt = parse(j["expiredAt"],dayfirst=True),
                fio = j["fio"],
                doc = j["doc"],
                stuff = j["stuff"],
                singlePhase = j["singlePhase"],
                qr = j["qr"],
                status = j["status"],
            )
            s.qr_url = s.scanQR()
>>>>>>> 9685726 (add qr scan)
=======
>>>>>>> 91213a4 (move logic to Stuff Model)
            s.save()
        except JSONDecodeError:
            return HttpResponseNotFound('noJson')           
        except KeyError:
            return HttpResponseNotFound('empty')           
    return JsonResponse(s.getJson())


    '''

<<<<<<< HEAD
<<<<<<< HEAD
counter = 974506
=======
counter = 122555
>>>>>>> e8c74ee (change api)
=======
counter = 974506
>>>>>>> 60a25a3 (add r and n calc)

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

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 60a25a3 (add r and n calc)

function unrz(r,u) {
    return (r + 100).toString().substring(1) + (u + 10000000000000).toString().substring(1)
}

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
ri = 0; u = 1287837;

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
=======
r = 1; u = 898125;

timer = setInterval(function () {
    fetch('https://protected-peak-73444.herokuapp.com/unrz/'+unrz(r,u))
>>>>>>> 60a25a3 (add r and n calc)
=======
ri = 0; u = 1287696;
=======
ri = 0; u = 1287834;
>>>>>>> ddf2e56 (rebase)

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
>>>>>>> 57c1977 (planned = true)
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data);
<<<<<<< HEAD
<<<<<<< HEAD
    next_n()
  })
  .catch(function (err) {
    next_r()
  }); 
},600)
}

planned = true

plan()
=======
    clearInterval(timer)
=======
    next_n()
>>>>>>> 57c1977 (planned = true)
  })
  .catch(function (err) {
    next_r()
  }); 
<<<<<<< HEAD
},1100)
<<<<<<< HEAD
>>>>>>> 60a25a3 (add r and n calc)
=======
=======
},600)
>>>>>>> ddf2e56 (rebase)
}
>>>>>>> 57c1977 (planned = true)

planned = true

plan()

clearInterval(timer)

for u=898124 
for(var u=898124; u<898133; u++) {
    for (var r=01; r<100; r++) {

    }
}

<<<<<<< HEAD
=======
>>>>>>> e8c74ee (change api)
=======
>>>>>>> 60a25a3 (add r and n calc)
    '''
