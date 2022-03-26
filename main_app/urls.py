from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('products/<str:product_tag>/', views.products_index_by_tag, name='products_index'),
  path('product_detail/<int:id>/', views.products_detail, name='products_detail'),
  path('accounts/signup/', views.signup, name='signup'),
  path('product_detail/<int:id>/add_favorite/<int:user_id>', views.favorite_add, name='favorite_add'),
  path('product_detail/<int:id>/remove_favorite/<int:user_id>', views.favorite_remove, name='favorite_remove'),
  path('favorites/<int:user_id>', views.favorite_list, name='favorite_list'),
  path('looks/', views.looks_list, name='looks_list'),
  path('looks/create', views.LookCreate.as_view(), name='looks_create'),
  path('looks/<int:look_id>/', views.looks_detail, name='looks_detail'),
  path('looks/<int:look_id>/assoc_product/<int:product_id>/', views.assoc_product, name='assoc_product'),
  path('looks/<int:look_id>/unassoc_product/<int:product_id>/', views.unassoc_product, name='unassoc_product'),
  path('looks/edit/<int:pk>/', views.LookEdit.as_view(), name='looks_edit')
]
