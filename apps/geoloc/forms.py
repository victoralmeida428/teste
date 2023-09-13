from django import forms
import pandas as pd

class ExcelInput(forms.Form):

    busca = forms.CharField(required=True, label='Coluna de Busca', widget=forms.TextInput(attrs={'value':'endereco', 'class': 'form-control mb-3 mt-1'}))
    files = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control mb-3 mt-1'}))
    
    def clean_files(self):
        file = self.cleaned_data.get('files')
        print(self.cleaned_data)
        if 'xlsx' not in file.name or 'xls' not in file.name:
            raise forms.ValidationError(f'O arquivo "{file}" não está no formato excel')
        
        return file
    
