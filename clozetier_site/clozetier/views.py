# clozetier/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import ClothingItemForm
from .models import ClothingItem
from django.conf import settings
from .model_utils import run_image_through_models  # Ensure this name matches

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
            
            # Run the image through the models
            clothing_result, color_result = run_image_through_models(fs.path(filename))
            clothing_labels = ['blazer', 'body', 'buttondown-shirt', 'dress', 'hat', 'hoodie', 'longsleeve', 'pants', 'polo-shirt', 'shoes', 'shorts', 'skirt', 'T-shirt', 'under-shirt']
            clothing_label = clothing_labels[clothing_result]
            
            # Save to database
            uploaded_image = ClothingItem(user=request.user, image=filename, cloth_type=clothing_label, cloth_color=color_result)
            uploaded_image.save()

            messages.success(request, f'Successfully uploaded image:<br><img src="{uploaded_image_url}" style="width:auto;height:300px;">', extra_tags='safe')
            messages.info(request, f'Clothing type detected: {clothing_label}, Color detected: {color_result}')
            
            return redirect('index')

    else:
        form = ClothingItemForm()

    user_items = ClothingItem.objects.filter(user=request.user)

# Categorize items
    categories = {
        'hats': ['hat'],
        'tops': ['T-shirt', 'longsleeve', 'polo-shirt', 'hoodie', 'buttondown-shirt', 'blazer'],
        'bottoms': ['pants', 'shorts', 'skirt'],
        'shoes': ['shoes'],
    }

    categorized_items = {
        'hats': [item for item in user_items if item.cloth_type in categories['hats']],
        'tops': [item for item in user_items if item.cloth_type in categories['tops']],
        'bottoms': [item for item in user_items if item.cloth_type in categories['bottoms']],
        'shoes': [item for item in user_items if item.cloth_type in categories['shoes']],
    }

    return render(request, 'index.html', {
        'form': form,
        'categorized_items': categorized_items,
        'items': user_items})

@login_required
def outfit_creator_view(request):
    # Retrieve user items
    user_items = ClothingItem.objects.filter(user=request.user)

    # Categorize items as done in the `index` view
    categories = {
        'hats': ['hat'],
        'tops': ['T-shirt', 'longsleeve', 'polo-shirt', 'hoodie', 'buttondown-shirt', 'blazer'],
        'bottoms': ['pants', 'shorts', 'skirt'],
        'shoes': ['shoes'],
    }

    categorized_items = {
        'hats': [item for item in user_items if item.cloth_type in categories['hats']],
        'tops': [item for item in user_items if item.cloth_type in categories['tops']],
        'bottoms': [item for item in user_items if item.cloth_type in categories['bottoms']],
        'shoes': [item for item in user_items if item.cloth_type in categories['shoes']],
    }

    # Pass categorized items to the outfitCreator template
    return render(request, 'outfitCreator.html', {
        'categorized_items': categorized_items
    })