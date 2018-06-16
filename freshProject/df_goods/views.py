from django.shortcuts import render

# Create your views here.
def index(request):
    context = {'loadin':0}
    return render(request,'df_goods/index.html',context)

def list(request):
    context = {'loadin':0}
    return render(request,'df_goods/list.html',context)

def detail(request):
    context = {'loadin':0}
    return render(request,'df_goods/detail.html',context)