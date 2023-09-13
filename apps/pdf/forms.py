from django import forms
from multiupload.fields import MultiFileField

class PdfInput(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            widget_attrs = field.widget.attrs
            widget_attrs['class'] = 'form-control mb-3 mt-1'
            widget_attrs['class'] = 'form-control mb-3 mt-1'

    files = MultiFileField(min_num=1, max_num=200, max_file_size=1024*1024*50)

    def clean_files(self):
        files = self.cleaned_data['files']
        for file in files:
            format = file.name.split('.')
            if 'pdf' not in format:
                raise forms.ValidationError(f'O arquivo "{file}" não está no formato pdf')

class ImageInput(forms.Form):
    file = MultiFileField(min_num=1, max_num=200, max_file_size=1024*1024*50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            widget_attrs = field.widget.attrs
            widget_attrs['class'] = 'form-control mb-3 mt-1'
            widget_attrs['class'] = 'form-control mb-3 mt-1'


