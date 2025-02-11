
# resume/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact_success/', views.contact_success, name='contact_success'),
    path('course/', views.select_template, name='select_template'),
    path('edit_resume/<int:template_id>/', views.edit_resume, name='edit_resume'),
    path('preview_template/<int:resume_id>/', views.preview_resume, name='preview_resume'),
    path('place_order/<int:resume_id>/', views.place_order, name='place_order'),
    path('resumes/download_resume/<int:order_id>/', views.download_resume, name='download_resume'),
    path('my_account/',views.my_account,name='my_account'),
    path('thank_you/',views.thank_you,name='thank_you'),
    path('resume/<int:resume_id>/checkout/', views.checkout_page, name='checkout_page'),
    path('resume/<int:resume_id>/initiate-checkout/', views.initiate_checkout, name='initiate_checkout'),

]
