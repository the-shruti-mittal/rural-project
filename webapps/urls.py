"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialnetwork import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('logout', views.logout_action, name='logout'),
    path('request_list', views.request_list, name='request_list'),
    path('inventory_list', views.inventory_list, name='inventory_list'),
    path('inventory_add', views.inventory_add, name='inventory_add'),
    path('order_item', views.order_item, name='order_item'),
    path('get_inventory_item_by_id/<int:id>/', views.get_inventory_item_by_id, name='get_inventory_item_by_id'),
    path('get_inventory_list', views.get_inventory_list, name='get_inventory_list'),
]
