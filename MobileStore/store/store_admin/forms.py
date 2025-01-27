from django import forms
from store.models import ShopOwner, Customer, MobilePhone, Laptop, Accessory

class ShopOwnerForm(forms.ModelForm):
    class Meta:
        model = ShopOwner
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class MobilePhoneForm(forms.ModelForm):
    class Meta:
        model = MobilePhone
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'sim': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'os': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'ram': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'battery_capacity': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }
