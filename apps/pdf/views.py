import tempfile
from typing import Any, Dict
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import FormView
from apps.pdf.forms import PdfInput
import PyPDF2
from django.views import View
from .forms import PdfInput,ImageInput
import io
import tabula as tb
from django.contrib import messages
import pandas as pd
from PIL import Image
import pdf2docx

class Merge(FormView):
    template_name = "merge.html"
    form_class = PdfInput
    success_url = "merge"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['button'] = 'Juntar PDF'
        return context
    
    def form_valid(self, form: Any) -> HttpResponse:
        files = self.request.FILES.getlist('files')
        merge = PyPDF2.PdfMerger()
        [merge.append(file) for file in files]
        
            # Criando um buffer para armazenar o PDF gerado
        output_buffer = io.BytesIO()
        merge.write(output_buffer)
        merge.close()
        
        # Configurando a resposta HTTP com o PDF gerado
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="merged_file.pdf"'
        response.write(output_buffer.getvalue())
        
        return response

class Excel(View):
    template_name = "excel.html"
    form_class = PdfInput
    success_url = "excel"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form,
                   'button': 'Converter para Excel'}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            merge = PyPDF2.PdfMerger()
            [merge.append(file) for file in files]
            # Salvar o arquivo temporário PDF
            try:
                with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
                    merge.write(temp_pdf.name)

                        # Converter o PDF para CSV
                    with tempfile.NamedTemporaryFile(suffix=".csv") as temp_csv:
                        tb.convert_into(input_path=temp_pdf.name, output_path=temp_csv.name,
                                        output_format='csv', guess=True, pages='all')
                        df = pd.read_csv(temp_csv.name)
                        with tempfile.NamedTemporaryFile(suffix=".xlsx") as temp_excel:
                            df.to_excel(temp_excel.name, index=False)

                        # Configurar a resposta HTTP com o arquivo Excel gerado
                            with open(temp_excel.name, 'rb') as excel_file:
                                response = FileResponse(open(excel_file.name, 'rb'), filename='Arquivo.xlsx')                    
                                return response
                
            except Exception as e:
                messages.error(request, f'Infelizmente não foi possível converter o arquivo:')
                messages.error(request, f'Possíveis causas: Diferentes formatos de tabelas ou arquivo sem tabelas')
            
                context = {'form': form,
                   'button': 'Converter para Excel'}
                return render(request, self.template_name, context)
            
            
            
            
        context = {'form': form,
                   'button': 'Converter para Excel'}
        return render(request, self.template_name, context)

class Word(FormView):
    template_name = "word.html"
    form_class = PdfInput
    success_url = "word"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['button'] = 'Converter PDF'
        return context
    
    def form_valid(self, form: Any) -> HttpResponse:
            files = self.request.FILES.getlist('files')
            merge = PyPDF2.PdfMerger()
            [merge.append(file) for file in files]
            
             # Criando um buffer para armazenar o PDF gerado
            output_buffer = io.BytesIO()
            merge.write(output_buffer)
            try:
                with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
                    merge.write(temp_pdf.name)
                    with tempfile.NamedTemporaryFile(suffix='.docx') as temp_word:
                        self.convert_pdf_to_word(temp_pdf.name, temp_word.name)
                        with open(temp_word.name, 'rb') as file_word:
                            word_data = file_word.read()
                            # Configurar a resposta HTTP com o arquivo Word gerado
                            response = FileResponse(io.BytesIO(word_data), filename='Arquivo.docx')
                            return response
                
            except Exception as e:
                messages.error(self.request, f'Infelizmente não foi possível converter o arquivo:\n{e}')


    def convert_pdf_to_word(self, pdf_path, docx_path):
        conversor = pdf2docx.Converter(pdf_path)
        conversor.convert(docx_path)
        conversor.close

class ImageFormView(FormView):
    template_name = "image.html"
    form_class = ImageInput
    success_url = "image"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['button'] = 'Transformar em PDF'
        return context
    
    def form_valid(self, form: Any) -> HttpResponse:
            files = self.request.FILES.getlist('file')
            converts = [Image.open(file).convert('RGB') for file in files]
            print(converts)
            try:
                output_buffer = io.BytesIO()
                if len(converts)>1:
                    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:                        
                        converts[0].save(temp_pdf.name, save_all=True, append_images=converts[1:])
                        with open(temp_pdf.name, 'rb') as pdf_file:
                            pdf = pdf_file.read()
                            response = FileResponse(io.BytesIO(pdf), filename='Arquivo.pdf')
                            return response
                else:
                    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:                        
                        converts[0].save(temp_pdf.name)
                        with open(temp_pdf.name, 'rb') as pdf_file:
                            pdf = pdf_file.read()
                            response = FileResponse(io.BytesIO(pdf), filename='Arquivo.pdf')
                            return response
                
                # Configurando a resposta HTTP com o PDF gerado
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] ='attachment; filename="images_file.pdf"'
                response.write(output_buffer.getvalue())
        
                return response
                
            except Exception as e:
                messages.error(self.request, f'Infelizmente não foi possível converter o arquivo:\n{e}')
                return redirect('image')


    def convert_pdf_to_word(self, pdf_path, docx_path):
        conversor = pdf2docx.Converter(pdf_path)
        conversor.convert(docx_path)
        conversor.close



