from django.shortcuts import render
from django.views import View, generic
from .models import Product
import requests
# Create your views here.
class product_list(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'product'

    def load_products(request):
        r = requests.get('https://fakestoreapi.com/products')
        for i in r.json():
            product = Product(
                title = i['title'],
                description = i['description'],
                price = i['price'],
                image_url = i['image']
            )
            product.save()

    def get_queryset(self):
        return Product.objects.all()
    
class product_detail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)

        if 'recently_viewed' in request.session:
            if pk in request.session['recently_viewed']:
                request.session['recently_viewed'].remove(pk)
            
            products = Product.objects.filter(pk__in=request.session['recently_viewed'])
            recently_viewed = sorted(
                products, key=lambda x: request.session['recently_viewed'].index(x.id)
            )
            request.session.insert(0, pk)
            if request.session['recently_viewed']>5:
                request.session['recently_viewed'].pop()

        else:
            request.session['recently_viewed'] = [pk]

        request.session.modified = True
        return render(request, 'products.html', {"product": product})


