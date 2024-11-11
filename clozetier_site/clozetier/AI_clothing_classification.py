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

from .models import ClothingItem

def get_recommended_clothing(selected_item, target_cloth_type):
    selected_color = selected_item.cloth_color
    
    # Get the prioritized color list
    color_priority_list = COLOR_RECOMMENDATIONS.get(selected_color, [])
    
    recommended_items = []
    
    # Loop through colors in priority order to find matching items
    for color in color_priority_list:
        matching_items = ClothingItem.objects.filter(cloth_color=color, cloth_type=target_cloth_type)
        
        # Add all items of this color/type combination to recommendations
        if matching_items.exists():
            recommended_items.extend(matching_items)
    
    if not recommended_items:
        print("You have no drip... Go shopping little bro!")
        return []
    
    return recommended_items
