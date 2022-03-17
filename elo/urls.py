from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<genre>', views.index, name="ratings"),
    path('results/<genre>', views.ResultListView.as_view(), name='results'),
    path('team/<int:pk>', views.TeamInfoView.as_view(), name='team-info'),
]
