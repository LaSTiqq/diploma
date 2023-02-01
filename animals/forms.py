from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Lietotājvārds', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Parole', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(label='E-pasts', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Vārds', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Uzvārds', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
        )


class AnimalsForm(forms.ModelForm):
    class Meta:
        model = Animals
        fields = [
            'animal_name',
            'family_name',
            'latin_name',
            'text',
            'image',
        ]
        widgets = {
            'animal_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dzīvnieka nosaukums'}),
            'family_name': forms.Select(attrs={'class': 'form-select'}),
            'latin_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Dzīvnieka pilnais latīņu nosaukums'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                          'placeholder': 'Tekstuāls apraksts par dzīvnieku'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = [
            'name',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Dzīvnieka dzimta (daudzskaitlī, ģenitīva locījumā)'}),
        }


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(label='Vecā parole', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                          'type': 'password'}))
    new_password1 = forms.CharField(label='Jaunā parole', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                            'type': 'password'}))
    new_password2 = forms.CharField(label='Jaunā parole atkārtoti', widget=forms.PasswordInput(attrs={
                                                                                                'class': 'form-control',
                                                                                                'type': 'password'}))

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password1',
            'new_password2',
        )