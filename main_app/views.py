from django.shortcuts import redirect, render
from .models import Product, Color, Look, ProductFavorite
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def products_index_by_tag(request, product_tag):
  if product_tag == 'Vegan':
      products_list = Product.objects.filter(tags__icontains=product_tag)
  elif product_tag == 'cruelty-free' or product_tag == 'cruelty free':
      sanitized_product_tag = product_tag.replace('-', ' ')
      products_list = Product.objects.filter(tags__icontains=sanitized_product_tag)
  elif product_tag == 'natural':
      products_list = Product.objects.filter(tags__icontains=product_tag)
  else: 
    return redirect('home')
  return render(request, 'products_index.html', {'product': products_list})

def products_detail(request, product_id):
  product = Product.objects.get(id=product_id)
  colors = Color.objects.filter(product_id=product_id)
  return render(request, 'products/detail.html', {'product': product, 'colors': colors})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid Sign Up - Please Try Again'
  form = UserCreationForm()
  context = { 'form': form, 'error': error_message }
  return render(request, 'registration/signup.html', {'form': form, 'error': error_message})

def favorite_add(request, product_id, user_id):
    product_favorite = ProductFavorite()
    product = Product.objects.get(id=product_id)
    user = User.objects.get(id=user_id)
    product_favorite.product_id = product
    product_favorite.user_id = user
    product_favorite.save()
    return redirect(request.META['HTTP_REFERER'])

def favorite_remove(request, product_id, user_id):
    ProductFavorite.objects.get(product_id=product_id).delete()
    return redirect(request.META['HTTP_REFERER'])

def favorite_list(request, user_id):
  favorite_product_ids = ProductFavorite.objects.filter(user_id=request.user)
  # loop over the above collection and do Product.objects.get() for all those
  favorites = []
  for product in favorite_product_ids:
    favorites.append(Product.objects.get(id=product.product_id.id))
  # where theid is the id from favorite_product_ids
  return render(request, 'favorites/index.html', {'favorites': favorites})

def looks_list(request):
  looks = Look.objects.filter(user=request.user)
  return render(request, 'looks/index.html', {'looks':looks})

class LookCreate(CreateView):
  model = Look
  fields = ('name','description')

  template_name = 'looks/look_form.html'
  success_url = '/looks/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

def looks_detail(request, look_id):
  look = Look.objects.get(id=look_id)
  products_look_doesnt_have = ProductFavorite.objects.filter(user_id=request.user).exclude(id__in = ProductFavorite.objects.all().values_list('product_id'))
  looks_favorites = []
  for product in products_look_doesnt_have:
    looks_favorites.append(ProductFavorite.objects.get(id=product.id))
  return render(request, 'looks/detail.html', {
    'look':look,
    'products': products_look_doesnt_have
  })

def assoc_product(request, look_id, product_id):
  look = Look.objects.get(id=look_id).products.add(product_id)
  return redirect('looks_detail', look_id=look_id)

def unassoc_product(request, look_id, product_id):
  look = Look.objects.get(id=look_id).products.remove(product_id)
  return redirect('looks_detail', look_id=look_id)

class LookEdit(UpdateView):
  model = Look
  fields = ('name', 'description')
  template_name = 'looks/look_form.html'
  success_url = '/looks/'