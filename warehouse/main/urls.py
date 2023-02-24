from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexList.as_view(), name='index'),
    # path('element/<int:element_id>/',
    #      views.element_detail, name='element_detail'),
    path('element/<int:element_id>/',
         views.ElementDetail.as_view(), name='element_detail'),
    # path('create/', views.element_create, name='element_create'),
    path('create/', views.ElementCreate.as_view(), name='element_create'),
    # path('element/<int:element_id>/edit/',
    #      views.element_edit, name='element_edit'),
    path('element/<int:element_id>/edit/',
         views.ElementUpdate.as_view(), name='element_edit'),
    path('element/<int:element_id>/delete/',
         views.ElementDelete.as_view(), name='element_delete'),
]
