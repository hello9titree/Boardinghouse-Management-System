from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "boardinghouse"
urlpatterns = [
    path('', views.index, name="index"),
    
    #boardinghouse/landlords
    path("landlords", views.landlord_list, name="landlord_list"),
    path("landlord_home/<int:landlord_id>/", views.landlord_home, name="landlord_home"),
    path("landlord/new/", views.add_landlord, name="add_landlord"),
    
    path("landlord/<int:landlord_id>/room/add/", views.add_room, name="add_room"),
    path("landlord/<int:landlord_id>/room/edit/<uuid:room_id>/", views.edit_room, name="edit_room"),
    path("landlord/<int:landlord_id>/room/delete/<uuid:room_id>/", views.delete_room, name="delete_room"),
    
    path("landlord/<int:landlord_id>/tenant/add/", views.add_tenant, name="add_tenant"),
    path("landlord/<int:landlord_id>/tenant/edit/<int:tenant_id>/", views.edit_tenant, name="edit_tenant"),
    path("landlord/<int:landlord_id>/tenant/delete/<int:tenant_id>/", views.delete_tenant, name="delete_tenant"),
]
