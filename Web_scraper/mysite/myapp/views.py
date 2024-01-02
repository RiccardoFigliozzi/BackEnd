from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
from bs4 import BeautifulSoup
from .models import Link

# Create your views here.

def scrape(req):

    if req.method=="POST":
        site = req.POST.get('site','')
        page = requests.get(site)
        parser = BeautifulSoup(page.text,'html.parser')


        for link in parser.find_all('a'):
            link_address = link.get('href')
            link_text = link.string
            Link.objects.create(address=link_address,name=link_text)
        return HttpResponseRedirect('/')

    else:
        data = Link.objects.all()

    return render(req,'myapp/result.html',{'data': data})

def clear(req):
    Link.objects.all().delete()
    return render(req,'myapp/result.html')