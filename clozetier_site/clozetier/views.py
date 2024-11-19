from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import ClothingItemForm, EditProfileForm  # Import EditProfileForm
from .models import ClothingItem
from .model_utils import run_image_through_models

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
            clothing_labels = ['blazer', 'body', 'buttondown-shirt', 'dress', 'hat', 'hoodie', 'longsleeve', 'pants', 'polo-shirt', 'shoes', 'shorts', 'skirt', 'T-shirt', 'under-shirt']
            color_labels = ['Black', 'Blue', 'Brown', 'Cream', 'Dark-Blue', 'Dark-Brown',
                            'Dark-Gray', 'Dark-Green', 'Dark-Red', 'Gold', 'Gray', 'Green',
                            'Light-Blue', 'Light-Gray', 'Light-Green', 'Light-Red', 'Orange',
                            'Peach', 'Pink', 'Purple', 'Red', 'White', 'Yellow']
            clothing_label = clothing_labels[clothing_result]
            
            # Save to database (commented out for safety; uncomment to save)
            # uploaded_image = ClothingItem(user=request.user, image=filename, cloth_type=clothing_label, cloth_color=color_result)
            # uploaded_image.save()

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

            # Pass to context directly
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
            messages.error(request, 'Form submission failed. Please check the input.')

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
def save_item(request):
    if request.method == 'POST':
        image = request.POST['image']
        predicted_type = request.POST['predicted_type']
        predicted_color = request.POST.get('predicted_color', 'Unknown')  # Ensure color fallback if missing
        
        # Create and save the ClothingItem instance
        uploaded_image = ClothingItem(user=request.user, image=image, cloth_type=predicted_type, cloth_color=predicted_color)
        uploaded_image.save()

        messages.success(request, 'Item successfully saved!')
        return redirect('index')

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

@login_required
def edit_profile(request):
    """
    View to handle profile editing.
    Allows the user to update their username, email, profile picture, and password.
    """
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            # Save user updates (username, email, etc.)
            updated_user = form.save(commit=False)
            
            # Handle profile picture separately if uploaded
            if 'profile_picture' in request.FILES:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(request.FILES['profile_picture'].name, request.FILES['profile_picture'])
                updated_user.profile_picture = filename
            
            # Update the password if provided
            password = form.cleaned_data.get('password')
            if password:
                updated_user.set_password(password)
            
            updated_user.save()
            messages.success(request, "Your profile has been updated successfully.")

            # Log the user out after password change
            logout(request)
            return redirect('login')  # Redirect to login after password change
        else:
            messages.error(request, "Error updating your profile. Please check the form.")

    else:
        # Prepopulate form with current user data
        form = EditProfileForm(instance=user)

    return render(request, 'edit_profile.html', {
        'form': form,
    })
