from django.urls import path
from .views import *

urlpatterns = [
    path('password/', PasswordsChangeView.as_view(template_name='animals/change-password.html'), name='change-password'),
    path('logout/', user_logout, name='logout'),
    path('edit_profile', UserEditForm.as_view(), name='edit_profile'),
    path('animals/', HomeAnimals.as_view(), name='home2'),
    path('', user_login, name='home'),
    path('family/<int:family_id>', AnimalsByFamily.as_view(), name='family'),
    path('animals/<int:pk>', ViewAnimals.as_view(), name='view_animals'),
    path('animals/add-animals', CreateAnimals.as_view(), name='add_animals'),
    path('animals/<int:pk>/update', UpdateAnimals.as_view(), name='update_animals'),
    path('animals/<int:pk>/delete', DeleteAnimals.as_view(), name='delete_animals'),
    path('animals/add-family', CreateFamily.as_view(), name='add_family'),
    path('animals/print/<pk>', render_pdf_view, name='print_animal'),
]