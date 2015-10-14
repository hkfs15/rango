from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'project_rango/index.html',{})

def homefiles(request,filename):
    return render(request,filename,{},contenttype="text/plain")