from django import forms

class NewAppointment(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    email = forms.EmailField(label="Email", max_length=254)