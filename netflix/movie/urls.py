from django.contrib import admin
from django.urls import path
from . import views
from .models import Movie, MovieSerializer

urlpatterns = [
    path('', views.index, name="index"),
    path('show/<int:id>', views.show, name="show"),
    path('create', views.create, name="create"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('update/<int:id>', views.update, name="update"),
    path('signup', views.signup, name="signup"),
    # function based
    path('api/index', views.api_index, name="api_index"),
    path('api/show/<int:id>', views.api_show, name="api_show"),
    path('api/create', views.api_create, name="api_create"),
    path('api/update/<int:id>', views.api_update, name="api_update"),
    path('api/delete/<int:id>', views.api_delete, name="api_delete"),
    # class based
    path('api/class/index', views.ApiIndex.as_view(), name="api_class_index"),
    path('api/class/show/<int:id>', views.ApiShow.as_view(), name="api_class_show"),
    path('api/class/create', views.ApiCreate.as_view(), name="api_class_create"),
    path('api/class/update/<int:id>', views.ApiUpdate.as_view(), name="api_class_update"),
    path('api/class/delete/<int:id>', views.ApiDelete.as_view(), name="api_class_delete"),
    # Generics
    path('api/generics/index', views.ApiIndexGenerics.as_view(), name="generics_api_index"),
    path('api/generics/show/', views.ApiShowGenerics.as_view(), name="generics_api_show"),
    path('api/generics/create/', views.ApiCreateGenerics.as_view(), name="generics_api_create"),
    path('api/generics/update/', views.ApiUpdateGenerics.as_view(), name="generics_api_update"),
    path('api/generics/delete/', views.ApiDeleteGenerics.as_view(), name="generics_api_delete"),

    path('api/mixins/index/', views.ApiIndexMixins.as_view(), name="mixins_api_index"),
    path('api/mixins/show/', views.ApiShowMixins.as_view(), name="mixins_api_show"),
    path('api/mixins/create/', views.ApiCreateMixins.as_view(), name="mixins_api_create"),
    path('api/mixins/update/', views.ApiUpdateMixins.as_view(), name="mixins_api_update"),
    path('api/mixins/delete/', views.ApiDeleteMixins.as_view(), name="mixins_api_delete"),
]
