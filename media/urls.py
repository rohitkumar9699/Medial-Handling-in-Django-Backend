from django.urls import path
from .views import UploadView, ListMediaView, ViewView, DeleteView, UpdateView

urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload'),
    path('list/', ListMediaView.as_view(), name='media-list'),
    path('list/<int:file_id>/', ViewView.as_view(), name='media-detail'),
    path('update/', UpdateView.as_view(), name='update'),  # ✅ Update endpoint
    path('delete/', DeleteView.as_view(), name='delete'),

]
