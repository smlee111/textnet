from http.client import HTTPResponse
from django.forms import JSONField
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Category, CategoryDepth, Entity, Intent, Response, Sentence, Synonym
from .forms import EntityForm, IntentForm
from django.contrib.auth.models import User
from templateloader import xlsxLoader

def home(request, cSub, cdSub):
    """
    데이터레이크 홈
    """
    # 세션 생성
    category = Category.objects.filter(subject=cSub).get()
    categoryDepth = CategoryDepth.objects.filter(subject=cdSub, category_id=category.id).get()
    request.session['cSub'] = category.subject
    request.session['cdSub'] = categoryDepth.subject
    request.session['cVal'] = category.value
    request.session['cdVal'] = categoryDepth.value
    request.session['cId'] = category.id
    request.session['cdId'] = categoryDepth.id
    return render(request, 'datalake/index.html')

def entity_list(request, cSub, cdSub):
    """
    엔티티 목록 등록일순
    """
    entity_list = Entity.objects.filter(CategoryDepth_id=request.session['cdId']).order_by('-create_date')
    page = request.GET.get('page', '1')
    paginator = Paginator(entity_list, 10)
    page_obj = paginator.get_page(page)
    context = {
        'entity_list': page_obj
    }
    return render(request, 'datalake/entity_list.html', context)

def entity_detail(request, cSub, cdSub, entity_id):
    """
    엔티티 상세
    """
    entity = get_object_or_404(Entity, pk=entity_id)
    context = {
        'entity': entity
    }
    return render(request, 'datalake/entity_detail.html', context)

def entity_create(request):
    """
    엔티티 등록
    """
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid(): # 폼이 유효하다면
            entity = form.save(commit=False)  # 임시 저장하여 객체를 리턴받는다.
            entity.CategoryDepth = CategoryDepth.objects.get(subject = request.session['cdSub'])
            entity.author = User.objects.get(username = request.user)
            entity.create_date = timezone.now()   # 실제 저장을 위해 작성일시를 설정한다.
            entity.save() # 데이터를 실제로 저장한다.
            return redirect('datalake:entity_list', request.session['cSub'], request.session['cdSub'])
    else:
        form = EntityForm()
    context = {'form': form}
    return render(request, 'datalake/entity_form.html', context)

def synonym_create(request, entity_id):
    """
    엔티티-동의어 등록
    """
    entity = get_object_or_404(Entity, pk=entity_id)
    entity.synonym_set.create(entry=request.POST.get('entry'), create_date=timezone.now())
    return redirect('datalake:entity_detail', entity_id=entity.id)

def entity_upload(request):
    """
    엔티티 업로드
    """
    entityList = xlsxLoader.xlsxUpload.entity(request.session['cdVal'])
    for entity in entityList:
        Entity.objects.create(
            CategoryDepth = CategoryDepth.objects.get(subject = request.session['cdSub']),
            subject = entity[0],
            entry = entity[1],
            author = User.objects.get(username = request.user),
            create_date = timezone.now()
        )
        synonym_list = entity[2].split('\n')
        for synonym in synonym_list:
            Synonym.objects.create(
                CategoryDepth = CategoryDepth.objects.get(subject = request.session['cdSub']),
                entity = Entity.objects.get(subject = entity[0]),
                entry = synonym,
                author = User.objects.get(username = request.user),
                create_date = timezone.now()
            )
    return redirect('datalake:entity_list', cSub=request.session['cSub'], cdSub=request.session['cdSub'])

def entity_download(request):
    """
    엔티티 다운로드
    """
    entity_list = Entity.objects.filter(CategoryDepth_id=request.session['cdId']).order_by('-create_date')
    synonym_list = Synonym.objects.filter(CategoryDepth_id=request.session['cdId']).order_by('-create_date')
    xlsxLoader.xlsxDownload.entity(request.session['cdVal'], entity_list, synonym_list)
    
    return redirect('datalake:home', cSub=request.session['cSub'], cdSub=request.session['cdSub'])

def intent_list(request, cSub, cdSub):
    """
    인텐트 목록 등록일순
    """
    intent_list = Intent.objects.filter(CategoryDepth_id=request.session['cdId']).order_by('-create_date')
    page = request.GET.get('page', '1')
    paginator = Paginator(intent_list, 10)
    page_obj = paginator.get_page(page)
    context = {
        'intent_list': page_obj
    }
    return render(request, 'datalake/intent_list.html', context)

def intent_detail(request, cSub, cdSub, intent_id):
    """
    인텐트 상세
    """
    intent = get_object_or_404(Intent, pk=intent_id)
    context = {
        'intent': intent
    }
    return render(request, 'datalake/intent_detail.html', context)

def intent_create(request):
    """
    인텐트 등록
    """
    if request.method == 'POST':
        form = IntentForm(request.POST)
        if form.is_valid(): # 폼이 유효하다면
            intent = form.save(commit=False)  # 임시 저장하여 question 객체를 리턴받는다.
            intent.CategoryDepth = CategoryDepth.objects.get(subject = request.session['cdSub'])
            intent.author = User.objects.get(username = request.user)
            intent.create_date = timezone.now()   # 실제 저장을 위해 작성일시를 설정한다.
            intent.save() # 데이터를 실제로 저장한다.
            return redirect('datalake:intent_list', request.session['cSub'], request.session['cdSub'])
    else:
        form = IntentForm()
    context = {'form': form}
    return render(request, 'datalake/intent_form.html', context)

def sentence_create(request, intent_id):
    """
    인텐트-학습문장 등록
    """
    intent = get_object_or_404(Intent, pk=intent_id)
    intent.sentence_set.create(sentence=request.POST.get('sentence'), create_date=timezone.now())
    return redirect('datalake:intent_detail', intent_id=intent.id)

def intent_upload(request):
    """
    인텐트 업로드
    """
    intentList = xlsxLoader.xlsxUpload.intent(request.session['cdVal'])
    for intent in intentList:
        Intent.objects.create(
            CategoryDepth = CategoryDepth.objects.get(subject = request.session['cdSub']),
            subject = intent[0],
            author = User.objects.get(username = request.user),
            create_date = timezone.now()
        )
        sentence_list = intent[1].split('\n')
        for sentence in sentence_list:
            Sentence.objects.create(
                CategoryDepth = CategoryDepth.objects.get(subject = request.session['cdSub']),
                intent = Intent.objects.get(subject = intent[0]),
                phrase = sentence,
                author = User.objects.get(username = request.user),
                create_date = timezone.now()
            )
        Response.objects.create(
            CategoryDepth = CategoryDepth.objects.get(subject = request.session['cdSub']),
            intent = Intent.objects.get(subject = intent[0]),
            phrase = intent[2],
            author = User.objects.get(username = request.user),
            create_date = timezone.now()
        )
    return redirect('datalake:intent_list', cSub=request.session['cSub'], cdSub=request.session['cdSub'])

def intent_download(request):
    """
    인텐트 다운로드
    """
    intent_list = Intent.objects.filter(CategoryDepth_id=request.session['cdId']).order_by('-create_date')
    sentence_list = Sentence.objects.filter(CategoryDepth_id=request.session['cdId']).order_by('-create_date')
    response_list = Response.objects.filter(CategoryDepth_id=request.session['cdId'])
    xlsxLoader.xlsxDownload.intent(request.session['cdVal'], intent_list, sentence_list, response_list)    
    return redirect('datalake:home', cSub=request.session['cSub'], cdSub=request.session['cdSub'])