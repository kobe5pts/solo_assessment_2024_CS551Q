from . models import Category

# Function to fetch menu links from the Category model
def menu_links(request):
    links = Category.objects.all()
    return {'links': links}

