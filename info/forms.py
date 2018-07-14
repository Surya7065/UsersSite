from django import forms


class UserForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=150)
    email = forms.EmailField(label='Email', max_length=150)
    # password = forms.Passwo