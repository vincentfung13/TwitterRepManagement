from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(label='password', max_length=20, widget=forms.PasswordInput)
    email = forms.EmailField(label='email')


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=30)
    password = forms.CharField(label='password', max_length=20, widget=forms.PasswordInput)


class AddEntity(forms.Form):
    username = forms.CharField(label='username', max_length=30)
    entity_list = forms.CharField(label='entity_list', max_length=100)
