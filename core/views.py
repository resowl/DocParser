from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pytesseract import pytesseract
from PIL import Image
from django.contrib import messages


@csrf_exempt
def upload(request):
    context = {}
    if request.method == 'POST':

        if not request.FILES:
            messages.error(request, 'Please select file')
            return render(request, 'upload.html')

        uploaded_file = request.FILES['file']
        # Get a searchable PDF
        try:
            pdf = pytesseract.image_to_pdf_or_hocr(Image.open(uploaded_file), extension='pdf')
            response = HttpResponse(pdf)
        except:
            messages.error(request, 'Please upload valid image file')
            return render(request, 'upload.html')
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % (uploaded_file.name.split('.')[0] + '.pdf')
        # Return the response value
        return response
    return render(request, 'upload.html', context)
