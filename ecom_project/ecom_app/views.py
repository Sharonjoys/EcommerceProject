from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from.models import Category,products
from django.core.paginator import Paginator,EmptyPage,InvalidPage

# Create your views here.


def allprodcat(request,c_slug=None):
    c_page=None
    product_list=None
    if c_slug!=None:
        c_page=get_object_or_404(Category,slug=c_slug)
        product_list=products.objects.all().filter(category=c_page,available=True)
    else:
        product_list=products.objects.all().filter(available=True)
    paginator=Paginator(product_list,6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        product=paginator.page(page)
    except (EmptyPage,InvalidPage):
        product=paginator.page(paginator.num_pages)
    return render(request,'category.html',{'category':c_page,'product':product})

def prodetail(request,c_slug,p_slug):
    try:
        product=products.objects.get(category__slug=c_slug,slug=p_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':product})