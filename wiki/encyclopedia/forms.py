from django import forms

class searchForm(forms.Form):
    search = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your query'}),
        )

class newEntry(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Enter the title of the page', 'style': 'width: 100%; height: 50px;', 'class':'form-control'}),
        label=""
    )
    textarea = forms.CharField(
        widget = forms.Textarea(attrs={'placeholder':'Enter the content in Markdown syntax','style': 'width: 100%; height: 480px;', 'class':'form-control'  }),
        label=""
    )

class editEntry(forms.Form):
    textarea = forms.CharField(
        widget = forms.Textarea(attrs={'style': 'width: 100%; height: 480px;', 'class':'form-control'}),
        label=""
    )
    title = forms.CharField(widget=forms.HiddenInput())
