from django.shortcuts import render

def index(request):
    """
    프로젝트 메인
    """
    return render(request, 'project/index.html')