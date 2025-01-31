from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function 
    # name the URL
    path(route='', view=views.index, name='index'),
    # path for about view
    path('dealer/about/', views.about, name='about'),
    # path for contact us view
    path('dealer/contact/', views.contact, name='contact'),
    #path for Sign Up
    path(route='signup/', view=views.signup, name='signup'),
    # path for registration
    path('registration/', views.registration_request, name='registration'), 
    # path for login
    path('login/', views.login_request, name='login'),
    # path for logout
    path('logout/', views.logout_request, name='logout'),
    # path for dealer
    path(route='dealer/', view=views.get_dealerships, name='index'),
    path(route='dealer/signup/', view=views.signup, name='signup'),
    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    # path for add a review view
    path(route='dealer/<int:dealer_id>/review/', view=views.add_review, name='add_review'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)