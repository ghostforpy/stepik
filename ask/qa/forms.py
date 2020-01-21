from django import forms


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