from django.shortcuts import redirect, render
from .models import Product, Color, Look

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

def products_detail(request, id):
  product = Product.objects.get(id=id)
  colors = Color.objects.filter(product=id)
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

def favorite_add(request, id, user_id):
  Product.objects.get(id=id).favorites.add(request.user)
  return redirect(request.META['HTTP_REFERER'])

def favorite_remove(request, id, user_id):
  Product.objects.get(id=id).favorites.remove(request.user)
  return redirect(request.META['HTTP_REFERER'])

def favorite_list(request, user_id):
  favorites = Product.objects.filter(favorites=request.user)
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
  products_look_doesnt_have = Product.objects.filter(favorites=request.user).exclude(id__in = look.products.all().values_list('id'))
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