from django import forms
from kitty.models import Input, InputTemp

class InputForm(forms.ModelForm):
    class Meta:
        model = Input  #사용할 모델
        fields = ['nickname', 'callnumber', 'keyword', 'max_price'] #모델 속성
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'callnumber': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            'max_price': forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'nickname': '별명',
            'callnumber': '번호',
            'keyword': '단어',
            'max_price': '가격',
        }  


class InputTempForm(forms.ModelForm):
    class Meta:
        model = InputTemp  #사용할 모델
        fields = ['keyword', 'max_price'] #모델 속성
        widgets = {
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            'max_price': forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'keyword': '단어',
            'max_price': '가격',
        }  