from . import views
from django.urls import path

app_name = 'datalake'

urlpatterns = [
    path('<str:cSub>/<str:cdSub>/home', views.home, name='home'),
    path('<str:cSub>/<str:cdSub>/entity', views.entity_list, name='entity_list'),
    path('<str:cSub>/<str:cdSub>/entity/<int:entity_id>/', views.entity_detail, name='entity_detail'),
    path('entity/create', views.entity_create, name='entity_create'),
    path('synonym/create/<int:entity_id>', views.synonym_create, name='synonym_create'),
    path('<str:cSub>/<str:cdSub>/intent', views.intent_list, name='intent_list'),
    path('<str:cSub>/<str:cdSub>/intent/<int:intent_id>/', views.intent_detail, name='intent_detail'),
    path('intent/create', views.intent_create, name='intent_create'),
    path('sentence/create/<int:intent_id>', views.sentence_create, name='sentence_create'),
]