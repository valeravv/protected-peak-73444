from django.db import models
from django.contrib import admin
from django.utils.html import format_html
import datetime
import base64
from io import BytesIO
from PIL import Image
from pyzbar.pyzbar import decode
from dateutil.parser import parse



#export CFLAGS=""
#./configure --disable-video --without-gtk --without-qt --prefix=$build_dir/vendor --without-imagemagick --without-python  >/dev/null 2>&1
# --prefix=/app/vendor 
#make  >/dev/null 2>&1
#make install  >/dev/null 2>&1
#find / -name "*zbar*.so"

#https://github.com/valeravv/heroku-buildpack-zbar.git

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)


# {"unrz":"9020000000122401", 
#  "fio":"С********** А****** З********",
#  "enFio":"S********** A****** Z********",
#  "birthdate":"21.05.1977",
#  "doc":"80** ***827",
#  "enDoc":"",
#  "stuff":"Гам-КОВИД-Вак Комбинированная векторная вакцина для профилактики коронавирусной инфекции, вызываемой вирусом SARS-CoV-2",
#  "enStuff":"Gam-COVID-Vac (“Sputnik V”), combined heterologous recombinant adenovirus (rAd)-based vaccine for prophylaxis of coronavirus infectious diseases caused by SARS-CoV-2",
#  "singlePhase":"N",
#  "qr":"iVBORw0KGgoAAAANSUhEUgAAAPoAAAD6AQAAAACgl2eQAAADc0lEQVR4Xu2W0W0cMRBDNY1I/XeRUqRGJL83uksCIzD8kZ0vr+31rZYHEBySUjtfX7/a55VP1w/gXt8BzNZiee8tdpyzW5wZaw5fFAHWOWvt1sbag4c1Y7c+dh++qALAaM3W5Tjm4POQMl/gRSFgw2iD2733ONzBVwOcTo7JAUFyS7gSwExmYzFmZwWh+uvTX9N8GJCm/df1Nm0BwGt2/LHekulcHt/hrQCwNPFHOvUGGbMQnjbmJfk8gMEQXQwC8uga3mIaedYBpIc6khPavSwQHm+RVgAsLwipVqYXjrJ0ZEUAZLlZafbYNLW0iRStlSIA/hATW51QDSRygTDBRQAby/6cOR7EOUlyeC8CzCTEhBarkTtL6oVbXtN8HrCMjetahdiSnYDmvHtrDUB2eNToZqff2OLj41IRoOcz3DQIGMpMwtMaKwLcmEJTYkuqYaGcXK0CUGCEhchuzTu2LeInmRYBcIw+5cUyQ8iEX6bnHLe3GgAEI1F3TIP8+JXQzXdYzwMUplmkZNg229ZXCgfHIgDucHtHKYskk3OyvzBxFeCYGuiRk1AbfSNa91YBEKZpDa5ph3L30SPPNW0JAGHUpd3Xd4dzUtyrAHJSHByzvI6GEcZqEcAly+uljE3q2P6UWAFg25tqwiPeRSvY4V/w4xqmAEBmnZgvh8nl3jxz6N0iwDXH0jS3v0D5KkNUBFCgLSmpYhyE0rbDc04VwOYME9xt8uOc+EbkwFKoEkDk6rBFFcwfDzo6uQiQdYU5wre/kSpmsdUAXJCmR6thgBwU/s15VQHCsGIR1xIa6ZVtixQBEMqc8us/Y/P6CimqAqQx/Mvkappjk3q7JVYAkKSnvbAwGE++Xmma/jbt04A98EyqpVWY3ZFr2CaXZAFAOnc8OS16ZLjHNM+/17TPA7Z7CSZJfTI0DE1MWC01gDx0a1GPvduNhDEZXtu0CIBExGXZn1NmfIAcJN1gigCOZHq4CeU5tmcOSwMlyQKAYfVkoWGYFLjU64hJkjUAjBsqc8XakvZhvqf5OEBe0jy5q9rpvNzp4PewHges3FAjk5PQ3Fzizq8KgB5ZXo6s+WZ72MuxXZJFgMgE41PLFKHsNP6fQoC7urGhRZjaMrUSP2UAh4VMctInt91bdloVIKfinKCoYicVky5fKgJ8ff0A7vUfAB+S4sg1zfRo+wAAAABJRU5ErkJggg==",
#  "lastName":"",
#  "expiredAt":"20.01.2022",
#  "status":"1",
#  "en":false}

class Stuff(models.Model):
    unrz = models.BigIntegerField("unrz", primary_key=True)
    r = models.IntegerField("r", null=True)
    n = models.IntegerField("n", null=True)
    fio = models.CharField("Ф*И*О*", max_length=150)
    birthdate = models.DateField("ДР")
    doc = models.CharField("Документ", max_length=20)
    stuff = models.CharField("Вакцина", max_length=250)
    singlePhase = models.CharField("Ф", max_length=1)
    qr = models.TextField("QR")
    qr_url = models.CharField("url", max_length=250, null=True)
    expiredAt = models.DateField("До")
    status = models.CharField("С", max_length=1)

    datetime.datetime.now().strftime("%d.%m.%Y")


    @classmethod
    def from_db(cls, db, field_names, values):
        # Default implementation of from_db() (subject to change and could
        # be replaced with super()).
        instance = super().from_db(db,field_names,values)
        if not instance.r:
            instance.r = instance.unrz // 10000000000000
        if not instance.n:     
            instance.n = instance.unrz % 10000000000000 
        #if not instance.qr_url:
        #    instance.qr_url = instance.scanQR()
        return instance

        # update hello_stuff set qr_url = null where unrz = 9890000003714315
        # select unrz,qr_url from hello_stuff where unrz = 9890000003714315

    @classmethod
    def fromJson(cls,j):
        instance = cls(
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
        if not instance.r:
            instance.r = instance.unrz // 10000000000000
        if not instance.n:     
            instance.n = instance.unrz % 10000000000000 
        if not instance.qr_url:
            instance.qr_url = instance.scanQR()
        return instance

    def getJson(self):
        return {
            "unrz":str(self.unrz),
            "fio":self.fio,
            "birthdate":self.birthdate.strftime("%d.%m.%Y"),
            "doc":self.doc,
            "stuff":self.stuff,
            "singlePhase":self.singlePhase,
            "qr":self.qr,
            "qr_url":self.qr_url,
            "expiredAt":self.expiredAt.strftime("%d.%m.%Y"),
            "status":self.status
        }
    
    def scanQR(self):
        b = base64.b64decode(self.qr)
        im_file = BytesIO(b)
        img = Image.open(im_file)
        return decode(img)[0].data.decode('utf-8')
        #b = base64.b64decode(s.qr)
        '''
        n = np.frombuffer(b, dtype=np.uint8)
        inputImage =cv2.imdecode(n,-1)
        qrDecoder = cv2.QRCodeDetector()
        data, bbox, rectifiedImage = qrDecoder.detectAndDecode(inputImage)
        return data


        from pyzbar.pyzbar import decode
        from PIL import Image
        decode(Image.open('imageToSave.png'))
        '''
class StuffAdmin(admin.ModelAdmin):
    list_display = ('unrz', 'r', 'n', 'fio', 'birthdate', 'doc', 'qr_url', 'expiredAt')
    #list_display = ('unrz', 'fio', 'birthdate','doc','custom_qr')
    def custom_qr(self, obj):
        return format_html(
            '<img  src="data:image/png;base64,{0}"></a>',
            obj.qr
        )
    custom_qr.short_description = 'QRCode'
    custom_qr.allow_tags = True
