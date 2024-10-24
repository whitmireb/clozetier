# clozetier/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import ClothingItemForm
from .models import ClothingItem
from django.conf import settings
from .model_utils import run_image_through_model

@login_required
def index(request):
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the image
            image = form.cleaned_data['image']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(image.name, image)
            uploaded_image_url = fs.url(filename)
            
            # Run the image through the model
            result = run_image_through_model(fs.path(filename))
            labels = ['blazer','body','buttondown-shirt','dress','hat','hoodie','longsleve','pants','polo-shirt','shoes','shorts','skirt','T-shirt','under-shirt']
            result = labels[result]
            # Save the result to the database
            uploaded_image = ClothingItem(user=request.user, image=filename, cloth_type=result, cloth_color='blue')
            uploaded_image.save()
            
            return render(request, 'index.html', {
                'form': form,
                'uploaded_image_url': uploaded_image_url,
                'result': result,
            })
    else:
        form = ClothingItemForm()

    user_items = ClothingItem.objects.filter(user=request.user)
    return render(request, 'index.html', {'form': form, 'items': user_items})  # Use 'index.html' here
