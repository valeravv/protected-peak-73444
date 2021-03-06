import requests
from dateutil.parser import parse
from django.shortcuts import render
from json.decoder import JSONDecodeError
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command
from django.views.generic import ListView
import gzip, shutil, os, tempfile
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required
import django_tables2 as tables
from django_tables2 import SingleTableView

from .models import Stuff

# Create your views here.

def clist(request):
    return render(request, "clist.html")

class StuffTable(tables.Table):
    qr_url = tables.URLColumn()
    unrz_url = tables.URLColumn(Stuff.unrz_url)
    class Meta:
        model = Stuff
        template_name = "django_tables2/bootstrap4.html"
        fields = ("unrz", "r", "n", "fio", "birthdate", "expiredAt", "qr_url")

class StuffTableView(SingleTableView):
    paginate_by = 50
    model = Stuff
    table_class = StuffTable

class StuffListView(ListView):
    paginate_by = 50
    model = Stuff
    template_name = 'clist.html'

    def get_queryset(self):
        #filter_val = self.request.GET.get('filter', 'give-default-value')
        order = self.request.GET.get('orderby', 'unrz')
        new_context = Stuff.objects.all(
        ).order_by(order)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(StuffListView, self).get_context_data(**kwargs)
        context['has_permission'] = self.request.user.is_authenticated
        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', 'unrz')
        return context



@login_required
def dump(request):
    if request.user.is_authenticated:
        datastr = tempfile.NamedTemporaryFile(mode='w+',delete=False)
        call_command('dumpdata',format='json',indent=3,stdout=datastr)
        datastr.close()
        databytes = open(datastr.name,'rb')
        zipfile = tempfile.NamedTemporaryFile(mode='w+b',suffix='.json.gz')
        gzipped = gzip.GzipFile(mode='wb',fileobj=zipfile, compresslevel=9)
        shutil.copyfileobj(databytes, gzipped)
        databytes.close()
        os.unlink(databytes.name)
        gzipped.close()
        zipfile.seek(0)
        return FileResponse(zipfile, filename='data.json.gz')
    else:
        raise Http404()

@login_required
def dumpin(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                f = gzip.open(request.FILES['file'],'rb')
                dir_temp = tempfile.TemporaryDirectory()
                jdata = open(dir_temp.name + '/data.json','wb+')
                shutil.copyfileobj(f,jdata)
                print(jdata.name)
                call_command('loaddata',jdata.name)
                return HttpResponseRedirect('../')
        else:
            form = UploadFileForm()
        return render(request, 'upload.html', {'form': form, 
                'title': 'load dump',
                'site_title': 'My Site',
                'site_header': 'load dump',
                'has_permission': request.user.is_authenticated  
            })
    else:
        raise Http404()

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
