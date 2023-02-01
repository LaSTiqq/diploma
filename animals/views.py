from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import *
from .forms import AnimalsForm, FamilyForm, UserLoginForm, EditProfileForm, PasswordChangingForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


@staff_member_required
def render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    animals = get_object_or_404(Animals, pk=pk)
    template_path = 'animals/print.html'
    context = {'animals': animals}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="animal.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response, encoding='utf-8')
    return response


class PasswordsChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('home2')
    raise_exception = True


class UserEditForm(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'animals/update_profile.html'
    success_url = reverse_lazy('home2')
    raise_exception = True

    def get_object(self):
        return self.request.user


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Veiksmīga autorizācija')
            return redirect('home2')
        else:
            messages.warning(request, 'Ievadīta nepareiza parole vai lietotājvārds')
    else:
        form = UserLoginForm()
    return render(request, 'animals/login.html', {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Visu labu!')
    return redirect('home')


class HomeAnimals(LoginRequiredMixin, ListView):
    model = Animals
    template_name = 'animals/home_animals_list.html'
    context_object_name = 'animals'
    paginate_by = 3
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'AnimalWiki'
        return context


class AnimalsByFamily(LoginRequiredMixin, ListView):
    model = Animals
    template_name = 'animals/home_animals_list.html'
    context_object_name = 'animals'
    allow_empty = False
    paginate_by = 3
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Family.objects.get(pk=self.kwargs['family_id'])
        return context

    def get_queryset(self):
        return Animals.objects.filter(family_name_id=self.kwargs['family_id']).select_related('family_name')


class ViewAnimals(LoginRequiredMixin, DetailView):
    model = Animals
    context_object_name = 'animals_item'
    raise_exception = True


@method_decorator(staff_member_required, name='dispatch')
class CreateAnimals(LoginRequiredMixin, CreateView):
    form_class = AnimalsForm
    template_name = 'animals/add_animals.html'
    http_method_names = ['get', 'post', 'put']
    raise_exception = True


@method_decorator(staff_member_required, name='dispatch')
class UpdateAnimals(LoginRequiredMixin, UpdateView):
    model = Animals
    form_class = AnimalsForm
    template_name = 'animals/update_animals.html'
    http_method_names = ['get', 'post', 'put']
    success_url = reverse_lazy('home2')
    raise_exception = True


@method_decorator(staff_member_required, name='dispatch')
class DeleteAnimals(LoginRequiredMixin, DeleteView):
    model = Animals
    success_url = reverse_lazy('home2')
    raise_exception = True


@method_decorator(staff_member_required, name='dispatch')
class CreateFamily(LoginRequiredMixin, CreateView):
    form_class = FamilyForm
    template_name = 'animals/add_family.html'
    success_url = reverse_lazy('home2')
    raise_exception = True
