from django import forms
from django.contrib.auth.forms import UserCreationForm
import accounts.models


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = accounts.models.MyUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

