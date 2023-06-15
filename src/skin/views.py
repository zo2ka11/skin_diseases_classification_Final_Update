from django.shortcuts import render
from django.views.generic import CreateView,TemplateView,FormView
from .models import SkinDiseasesClassification,SkinDiseasesInfo
from keras.models import model_from_json
from keras_preprocessing import image
import numpy as np
from .forms import *
from django.views import View
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

SKIN_CLASSES = {
    0: "Actinic Keratoses",
    1: "Basal Cell Carcinoma",
    2: "Benign Keratosis",
    3: "Dermatofibroma",
    4: "Melanoma",
    5: "Melanocytic Nevi",
    6: "Vascular skin lesion",
}

def get_image_prediction(image_path):
    # reading json file
    model_json_file = open("static\model.json", "r")
    loaded_json_model = model_json_file.read()
    model_json_file.close()
    
    model = model_from_json(loaded_json_model)
    
    model.load_weights("static\model.h5")
    
    img = image.load_img(image_path, target_size=(224, 224))
    img = np.array(img)
    img = img.reshape((1, 224, 224, 3))
    img = img / 255
    prediction = model.predict(img)
    
    pred = np.argmax(prediction)
    disease = SKIN_CLASSES[pred]
    accuracy = round(prediction[0][pred]*100,2)
    
    return disease, accuracy

class HomePageView(FormView):
    template_name = "index.html"
    form_class = SkinDiseasesClassificationForm
    success_url = '/'
    def form_valid(self, form):
        self.object = form.save()
        image_path  = self.object.skin_image
        pred,acc = get_image_prediction(image_path.path)
        try:
            old_records = SkinDiseasesClassification.objects.all()
            for record in old_records:
                record.delete()
            if pred != '' and acc != '':
                skin_class = SkinDiseasesClassification.objects.create(skin_image=image_path,skin_classification=pred,skin_accuracy=acc)
        except SkinDiseasesClassification.DoesNotExist:
            pass
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skin'] = SkinDiseasesClassification.objects.latest('id') if SkinDiseasesClassification.objects.latest('id') else ''
        context['diseas_info'] = SkinDiseasesInfo.objects.get(title = context['skin'].skin_classification)
        return context

class PredictionPageView(TemplateView):
    template_name = "predict.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skin'] = SkinDiseasesClassification.objects.latest('id') if SkinDiseasesClassification.objects.latest('id') else ''
        context['diseas_info'] = SkinDiseasesInfo.objects.get(title = context['skin'].skin_classification)
        return context
    
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        template_path = 'predict.html'
        context = {}
        context['skin'] = SkinDiseasesClassification.objects.latest('id') if SkinDiseasesClassification.objects.latest('id') else ''
        context['diseas_info'] = SkinDiseasesInfo.objects.get(title = context['skin'].skin_classification)
        # Render the template as a string
        html = get_template(template_path).render(context)
        # Generate the PDF
        pdf_file = BytesIO()
        pisa.CreatePDF(BytesIO(html.encode('utf-8')), pdf_file)
        # Set the Content-Disposition header to download the file
        response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{context["diseas_info"].title}-report.pdf"'
        return response