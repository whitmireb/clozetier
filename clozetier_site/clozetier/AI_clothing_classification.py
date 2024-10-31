color_selection_comparison_dictionary = {
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


#assuming that we are taking into account that there is only pizza that is only considered to be a pizza not inclusing hot pockets adn shit
#now we are assuming the population and assuming that children under 3 are not eating pizza
#now the school system. pizza is servered to alot of studetns in the system.
#and pizza is cheap so alot of people are considered eating
#now we are assumign the stardard pizza is 8 inches wide which we will configure to be about .75 sq feet per pizza.
#now we are saying that the average family will eat 50 standard 8 inch pizzas per year exclusing edge cases of people with lactose intolerance, too young to digest pizza and other stuff
#finally we will assume there are 350 million people in teh united states. and we will do 350 million * 50 = 1.7 billion *.75 sq feet = 1.35 billion sqfeet


# for i in range(1, 101):
#     if i % 3 == 0 and i % 5 == 0:
#         print("baby yoda")
#     elif i % 3 == 0:
#         print("baby")
#     elif i % 5 == 0:
#         print("yoda")
#     else:
#         print(i)


# list = [1,2,4,3,5,6]
# smallest_num, largest_num = min(list), max(list)
# print(largest_num - smallest_num)