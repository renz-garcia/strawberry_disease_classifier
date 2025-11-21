import os
from django.shortcuts import render
from django.conf import settings
from .forms import ImageUploadForm
from classifier.utils.inference import load_model, predict
from classifier.model_architecture import ResNet50

MODEL_PATH = os.path.join(settings.BASE_DIR, 'classifier/model/best_model.pth')

model = load_model(MODEL_PATH, ResNet50)

def upload_view(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            image_file = form.cleaned_data["image"]
            temp_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
            with open(temp_path, "wb+") as file:
                for chunk in image_file.chunks():
                    file.write(chunk)

            label, idx = predict(temp_path, model)

            context = {
                "label": label,
                "index": idx,
                "image_url": settings.MEDIA_URL + image_file.name
            }

            return render(request, "classifier/result.html", context)
    else:
        form = ImageUploadForm()

    context = {
        "form": form
    }

    return render(request, "classifier/upload.html", context)