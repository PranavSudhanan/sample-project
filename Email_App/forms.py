from django import forms

# how to convert a form into an html document ?

class regform(forms.Form):
    name = forms.CharField(max_length=20)
    phone = forms.IntegerField()
    image = forms.FileField()

class contactform(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows':3, 'cols': 30}))
