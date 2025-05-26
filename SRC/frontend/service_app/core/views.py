from django.shortcuts import render

# Create your views here.
def home(request):
    """
    Render the home page of the service app.
    """
    return render(request, 'core/home.html')