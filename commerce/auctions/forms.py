from django import forms


class ListingForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Enter the title of your listing', 'style': 'width: 100%; height: 50px;', 'class':'form-control'}),
        label="Title"
    )
    details = forms.CharField(
        widget = forms.Textarea(attrs={'placeholder':'Enter the Description','style': 'width: 100%; height: 250px;', 'class':'form-control'  }),
        label="Description"
    )
    category = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Category of the listing (Optional)', 'style': 'width: 40%; height: 50px;', 'class':'form-control'}),
        label="Category",
        required = False
    )
    image = forms.URLField(
        max_length=400,
        required = False,
        widget = forms.TextInput(attrs={'placeholder':'Enter the url of an image (Optional)', 'style': 'width: 30%; height: 50px;', 'class':'form-control'})
    )
    price = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        label="Starting Bid",
        widget = forms.TextInput(attrs={'placeholder':'$','class':'form-control', 'style': 'width: 150px;'})
    )

class BidForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        label="",
        widget = forms.TextInput(attrs={'placeholder':'Bid ','class':'form-control', 'style': 'width: 90%; height: 40px;'})
    )

class CommentForm(forms.Form):
    comment = forms.CharField(
        widget = forms.Textarea(attrs={'placeholder':'Add a comment','style': 'width: 100%; height: 100px;', 'class':'form-control'}),
        label=""
    )
