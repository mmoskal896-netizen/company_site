from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import News, Comment
from .forms import CommentForm

def index(request):
    """Главная страница с последними 3 новостями"""
    latest_news = News.objects.all()[:3]
    return render(request, 'news/index.html', {'latest_news': latest_news})

def contacts(request):
    """Страница контактов"""
    return render(request, 'news/contacts.html')

def news_list(request):
    """Страница со списком всех новостей, поиском и сортировкой"""
    news_list_all = News.objects.all()
    
    # Поиск по названию или содержанию
    search_query = request.GET.get('search', '')
    if search_query:
        news_list_all = news_list_all.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    
    # Сортировка по дате
    sort_order = request.GET.get('sort', 'desc')
    if sort_order == 'asc':
        news_list_all = news_list_all.order_by('created_date')
    else:
        news_list_all = news_list_all.order_by('-created_date')
    
    # Пагинация (по 5 новостей на страницу)
    paginator = Paginator(news_list_all, 5)
    page_number = request.GET.get('page')
    news_list_all = paginator.get_page(page_number)
    
    return render(request, 'news/news_list.html', {
        'news_list': news_list_all,
        'search_query': search_query,
        'sort_order': sort_order,
    })

def news_detail(request, pk):
    """Полная страница отдельной новости с комментариями"""
    news = get_object_or_404(News, pk=pk)
    comments = news.comments.filter(is_active=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.author = request.user
            comment.save()
            return redirect('news_detail', pk=pk)
    else:
        form = CommentForm()
    
    return render(request, 'news/news_detail.html', {
        'news': news,
        'comments': comments,
        'form': form,
    })