from django.shortcuts import render

def custom_500(request):
    return render(request, '505.html', status=500)
