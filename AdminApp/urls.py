from django.urls import path
from AdminApp import views

urlpatterns=[
    path('dashboard/',views.dashboard,name="dashboard"),
    path('add_anime/',views.add_anime,name="add_anime"),
    path('save_anime/',views.save_anime,name="save_anime"),
    path('view_anime/',views.view_anime,name="view_anime"),
    path('edit_anime/<int:Anime_ID>/',views.edit_anime,name="edit_anime"),
    path('update_anime/<int:Anime_ID>/',views.update_anime,name="update_anime"),
    path('delete_anime/<int:A_ID>/',views.delete_anime,name="delete_anime"),

    path('admin_login_page/',views.admin_login_page,name="admin_login_page"),
    path('admin_login/',views.admin_login,name="admin_login"),
]