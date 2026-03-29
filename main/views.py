from django.shortcuts import render


def index(request):
    title = 'Gallery'
    ctx = {'title': title}
    return render(request, 'main/index.html', context=ctx)
