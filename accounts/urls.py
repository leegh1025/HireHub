from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
   path('', landing, name='landing'),
   path('initialInterviewer/', initialInterviewer, name='initialInterviewer'),
   path('signup/', signup, name='signup'),
   path('login/', login, name='login'),
   path('logout/', logout, name='logout'),  
   path("mainboard/<int:pk>/", mainboard, name="mainboard"),
]