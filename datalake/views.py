from django.forms import JSONField
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Category, CategoryDepth, Entity, Intent
from .forms import EntityForm, IntentForm

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
    print(request.session['cSub'])
    return render(request, 'datalake/index.html')

def entity_list(request, cSub, cdSub):
    """
    엔티티 목록 등록일순
    """
    entity_list = Entity.objects.filter(CategoryDepth_id=request.session['cdId']).order_by('create_date')
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
    print(request.session['cdVal'])
    return render(request, 'datalake/entity_detail.html', context)

def entity_create(request):
    """
    엔티티 등록
    """
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid(): # 폼이 유효하다면
            entity = form.save(commit=False)  # 임시 저장하여 question 객체를 리턴받는다.
            entity.create_date = timezone.now()   # 실제 저장을 위해 작성일시를 설정한다.
            entity.save() # 데이터를 실제로 저장한다.
            return redirect('datalake:entity_list')
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

def intent_list(request, cSub, cdSub):
    """
    인텐트 목록 등록일순
    """
    intent_list = Intent.objects.filter(CategoryDepth_id=request.session['cdId']).order_by('create_date')
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
            intent.create_date = timezone.now()   # 실제 저장을 위해 작성일시를 설정한다.
            intent.save() # 데이터를 실제로 저장한다.
            return redirect('datalake:intent_list')
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