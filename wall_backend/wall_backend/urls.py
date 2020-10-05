from django.contrib import admin
from django.urls import path, include
from wall_api.views import UserView, PostListView, TokenAuthView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', TokenAuthView.as_view(), name='token'),
    path('users/', UserView.as_view(), name='users'),
    path('posts/', PostListView.as_view(), name='posts')
]
