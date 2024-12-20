# clozetier/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from .forms import ClothingItemForm
from .models import ClothingItem
from django.conf import settings
from .model_utils import run_image_through_models
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

categories = {
                'hats': ['hat'],
                'tops': ['T-shirt', 'longsleeve', 'polo-shirt', 'hoodie', 'buttondown-shirt', 'blazer', 'dress', 'body', 'under-shirt'],
                'bottoms': ['pants', 'shorts', 'skirt'],
                'shoes': ['shoes'],
            }

def signup(request):
    if request.method == 'POST':  # Handle form submission
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in after successful signup
            return redirect('index')  # Redirect to the homepage or any desired page
    else:  # Handle GET requests (load the signup form)
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

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
            clothing_result, color_result = run_image_through_models(fs.path(filename))
            
            clothing_labels = ['blazer', 'body', 'buttondown-shirt', 'dress', 'hat', 'hoodie', 'longsleeve', 
                               'pants', 'polo-shirt', 'shoes', 'shorts', 'skirt', 'T-shirt', 'under-shirt']
            
            color_labels = ['Black', 'Blue', 'Brown', 'Cream', 'Dark-Blue', 'Dark-Brown',
                            'Dark-Gray', 'Dark-Green', 'Dark-Red', 'Gold', 'Gray', 'Green',
                            'Light-Blue', 'Light-Gray', 'Light-Green', 'Light-Red', 'Orange',
                            'Peach', 'Pink', 'Purple', 'Red', 'White', 'Yellow']

            clothing_label = clothing_labels[clothing_result]
            
            # Save to database

            user_items = ClothingItem.objects.filter(user=request.user)

            categorized_items = {
                'hats': [item for item in user_items if item.cloth_type in categories['hats']],
                'tops': [item for item in user_items if item.cloth_type in categories['tops']],
                'bottoms': [item for item in user_items if item.cloth_type in categories['bottoms']],
                'shoes': [item for item in user_items if item.cloth_type in categories['shoes']],
            }

            # Pass to context directly (optional)
            context = {
                'predicted_type': clothing_label,
                'predicted_color': color_result,
                'uploaded_image_url': uploaded_image_url,
                'clothing_labels': clothing_labels,
                'color_labels': color_labels,
                'categorized_items': categorized_items,
                'form': form,
            }
            return render(request, 'index.html', context)

    else:
        form = ClothingItemForm()

    user_items = ClothingItem.objects.filter(user=request.user)

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
def save_item(request):
    if request.method == 'POST':
        image = request.POST['image']
        predicted_type = request.POST['predicted_type']
        predicted_color = request.POST['predicted_color']
        
        # Create and save the ClothingItem instance
        uploaded_image = ClothingItem(user=request.user, image=image, cloth_type=predicted_type, cloth_color=predicted_color)
        uploaded_image.save()

        messages.success(request, 'Item successfully saved!')
        return redirect('index')

@login_required
def clozet_view(request):
    # Retrieve user items
    user_items = ClothingItem.objects.filter(user=request.user)

    categorized_items = {
        'hats': [item for item in user_items if item.cloth_type in categories['hats']],
        'tops': [item for item in user_items if item.cloth_type in categories['tops']],
        'bottoms': [item for item in user_items if item.cloth_type in categories['bottoms']],
        'shoes': [item for item in user_items if item.cloth_type in categories['shoes']],
    }

    # Pass categorized items to the clozet template
    return render(request, 'clozet.html', {
        'categorized_items': categorized_items
    })

@login_required
def outfit_creator_view(request):
    # Retrieve user items
    user_items = ClothingItem.objects.filter(user=request.user)

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

def get_item_details(request, item_id):
    # Retrieve the item or return 404 if it doesn't exist
    item = get_object_or_404(ClothingItem, pk=item_id)

    # Return a JSON response if you're using fetch for dynamic content
    return JsonResponse({
        'cloth_type': item.cloth_type,
        'cloth_color': item.cloth_color,
        'image_url': item.image.url
    })

@login_required
def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(ClothingItem, id=item_id, user=request.user)

        # Delete the item
        item.delete()

        messages.success(request, 'Item deleted successfully!')
        return redirect('clozet')  # Redirect back to the outfit creator view

@login_required
def select_clothing(request, item_id=0):
    clothing_items = ClothingItem.objects.filter(user=request.user).order_by('id')
    clothing_labels = ['blazer', 'body', 'buttondown-shirt', 'dress', 'hat', 'hoodie', 'longsleeve', 
                       'pants', 'polo-shirt', 'shoes', 'shorts', 'skirt', 'T-shirt', 'under-shirt']
    
    if item_id != 0:
        item = get_object_or_404(clothing_items, id=item_id)
        user_items = list(clothing_items)
        user_specific_id = user_items.index(item)
    else:
        user_specific_id = 0

    is_empty = not clothing_items.exists()
    return render(request, 'select_clothing_image.html', {
        'clothing_items': clothing_items,
        'clothing_labels': clothing_labels,
        'item_id': user_specific_id,
        'is_empty': is_empty
    })


def recommendation_view(request):
    # Pass any context data needed for the template
    return render(request, 'AIrecommendation.html', {
        # Add any necessary context here
        'clothing_labels': ['blazer', 'body', 'buttondown-shirt', 'dress', 'hat', 'hoodie', 'longsleeve',
                            'pants', 'polo-shirt', 'shoes', 'shorts', 'skirt', 'T-shirt', 'under-shirt']
    })

from django.http import JsonResponse

def process_selection(request):
    if request.method == "POST":
        selected_item_id = request.POST.get('selected_item_id')
        selected_item_color = request.POST.get('selected_item_color')
        selected_item_type = request.POST.get('selected_item_type')
        clothing_article = request.POST.get('clothing_article')

        # Process the data (store, display, or further logic)
        response_data = {
            'selected_item_id': selected_item_id,
            'selected_item_color': selected_item_color,
            'selected_item_type': selected_item_type,
            'clothing_article': clothing_article,
        }

        return JsonResponse(response_data)  # Or return appropriate respons

COLOR_RECOMMENDATIONS = {
    'Black': ['Black', 'White', 'Cream', 'Dark-Gray', 'Gray', 'Light-Gray', 'Dark-Blue', 'Dark-Brown', 'Dark-Green'],
    'White': ['White', 'Black', 'Cream', 'Gray', 'Light-Gray', 'Peach', 'Light-Blue', 'Light-Red', 'Light-Green'],
    'Dark-Gray': ['Dark-Gray', 'Black', 'Gray', 'White', 'Cream', 'Dark-Blue', 'Dark-Brown', 'Dark-Green', 'Purple'],
    'Gray': ['Gray', 'White', 'Black', 'Light-Gray', 'Dark-Gray', 'Cream', 'Dark-Blue', 'Dark-Brown', 'Red'],
    'Light-Gray': ['Light-Gray', 'Gray', 'White', 'Black', 'Cream', 'Light-Blue', 'Light-Green', 'Peach', 'Pink'],
    'Dark-Blue': ['Dark-Blue', 'White', 'Cream', 'Dark-Gray', 'Black', 'Gray', 'Brown', 'Light-Blue', 'Red'],
    'Blue': ['Blue', 'White', 'Black', 'Cream', 'Gray', 'Light-Gray', 'Dark-Gray', 'Red', 'Pink'],
    'Light-Blue': ['Light-Blue', 'White', 'Gray', 'Light-Gray', 'Blue', 'Cream', 'Peach', 'Light-Green', 'Pink'],
    'Dark-Brown': ['Dark-Brown', 'White', 'Cream', 'Dark-Gray', 'Black', 'Gray', 'Brown', 'Dark-Green', 'Gold'],
    'Brown': ['Brown', 'White', 'Cream', 'Black', 'Gray', 'Dark-Brown', 'Dark-Gray', 'Dark-Green', 'Gold'],
    'Cream': ['Cream', 'White', 'Black', 'Gray', 'Brown', 'Peach', 'Gold', 'Light-Gray', 'Pink'],
    'Dark-Red': ['Dark-Red', 'White', 'Black', 'Dark-Gray', 'Gray', 'Cream', 'Red', 'Pink', 'Dark-Brown'],
    'Red': ['Red', 'White', 'Black', 'Gray', 'Dark-Gray', 'Cream', 'Pink', 'Dark-Red', 'Light-Red'],
    'Light-Red': ['Light-Red', 'White', 'Cream', 'Pink', 'Peach', 'Red', 'Gray', 'Light-Gray', 'Black'],
    'Pink': ['Pink', 'White', 'Cream', 'Light-Gray', 'Gray', 'Red', 'Light-Red', 'Light-Blue', 'Peach'],
    'Purple': ['Purple', 'White', 'Cream', 'Black', 'Gray', 'Dark-Gray', 'Pink', 'Light-Gray', 'Red'],
    'Dark-Green': ['Dark-Green', 'White', 'Cream', 'Dark-Gray', 'Black', 'Gray', 'Green', 'Brown', 'Gold'],
    'Green': ['Green', 'White', 'Black', 'Cream', 'Gray', 'Dark-Green', 'Light-Green', 'Peach', 'Gold'],
    'Light-Green': ['Light-Green', 'White', 'Cream', 'Gray', 'Light-Gray', 'Green', 'Peach', 'Yellow', 'Pink'],
    'Yellow': ['Yellow', 'White', 'Black', 'Gray', 'Cream', 'Light-Gray', 'Light-Green', 'Peach', 'Gold'],
    'Orange': ['Orange', 'White', 'Black', 'Gray', 'Cream', 'Brown', 'Peach', 'Red', 'Gold'],
    'Peach': ['Peach', 'White', 'Cream', 'Gray', 'Light-Gray', 'Pink', 'Light-Blue', 'Light-Red', 'Yellow'],
    'Gold': ['Gold', 'White', 'Black', 'Cream', 'Gray', 'Dark-Green', 'Brown', 'Yellow', 'Dark-Gray']
}

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ClothingItem

# views.py
from django.http import JsonResponse

import logging

logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ClothingItem  # Import your ClothingItem model
import logging

logger = logging.getLogger(__name__)

def get_clothing_recommendations(request):
    if request.method == "POST":
        selected_item_id = request.POST.get('selected_item_id')
        selected_item_color = request.POST.get('selected_item_color')
        selected_item_type = request.POST.get('selected_item_type')
        clothing_article = request.POST.get('clothing_article')

        logger.debug(f"Received POST data: ID={selected_item_id}, Color={selected_item_color}, Type={selected_item_type}, Article={clothing_article}")

        if not all([selected_item_id, selected_item_color, selected_item_type, clothing_article]):
            return JsonResponse({"success": False, "error": "Missing data fields"}, status=400)

        # Get recommendations using recommend_clothing function
        recommendations = recommend_clothing(selected_item_color, clothing_article, selected_item_type, request.user)
        # Save recommendations to the session to access them in /recommendations/
        request.session['recommendations'] = [item.id for item in recommendations]  # Store IDs or serialize items as needed
        request.session['prev_image'] = selected_item_id

        data = {
            "success": True,
            "redirect_url": "/clozetier/recommendations/"  # Adjust if necessary
        }
        return JsonResponse(data)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def recommend_clothing(selected_color, clothing_article, selected_item_type, active_user):
    matching_colors = COLOR_RECOMMENDATIONS.get(selected_color, [])
    recommended_items = []

    # Get clothing items that match the color and type

    if (clothing_article == "No-Selection"):
        clothing_items = ClothingItem.objects.filter(user=active_user)
    else:
        clothing_items = ClothingItem.objects.filter(cloth_type=clothing_article, user=active_user)
    
    if clothing_article != selected_item_type:
        clothing_items = clothing_items.exclude(cloth_type=selected_item_type)

    for item in clothing_items:
        if item.cloth_color in matching_colors:
            recommended_items.append(item)

    return recommended_items

from django.core.serializers import serialize
from django.http import JsonResponse

import json
from django.shortcuts import render
from .models import ClothingItem

def show_recommendations(request):
    # Retrieve recommendations from session
    recommendation_ids = request.session.get('recommendations', [])
    prev_image_id = request.session.get('prev_image')
    recommendations = ClothingItem.objects.filter(id__in=recommendation_ids).exclude(id=prev_image_id)
    prev_image = ClothingItem.objects.filter(id=prev_image_id)[0]
    print(prev_image.image.url)

    # Serialize recommendations into a JSON-friendly format
    serialized_recommendations = [
        {
            "id": item.id,
            "image": {"url": item.image.url},
            "cloth_color": item.cloth_color,
            "cloth_type": item.cloth_type,
        }
        for item in recommendations
    ]
    
    # Convert Python data to JSON string for proper JavaScript usage
    recommendations_json = json.dumps(serialized_recommendations)

    # Pass serialized recommendations to the template
    return render(request, 'recommendations.html', {
        'recommendations_json': recommendations_json,  # Pass to JavaScript
        'recommendations': recommendations,  # For rendering in HTML
        'prev_image': prev_image.image,
    })