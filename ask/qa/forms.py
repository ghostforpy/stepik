from django import forms
from django.contrib.auth.forms import UserCreationForm

class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    author = forms.CharField()
    def cleaned_data(self):
        pass
        return 1



class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
#    question = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField()
    author = forms.CharField()

class MyUserCreationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)