from django.shortcuts import render,HttpResponse,get_object_or_404
from article.models import Article
from django.http import HttpResponseRedirect
from django.urls import reverse
from article.forms import ArticleForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from article.models import Article
from django.contrib import messages
from .search_indexes import search_articles
from django.core.cache import cache
from django.conf.urls import handler500





def index(request):
    return render (request, 'index.html', {'title': 'Home Page'})


def about(request):
    return render(request, 'about.html', {'title': 'About Page'})

def contact(request):
    return render(request, 'contact.html', {'title': 'Contact Page'})

def dashboard (request):
    return render(request, 'dashboard.html', {'title': 'Dashboard Page'})

def articles_list(request):
    articles = Article.objects.all().order_by('-created_at')  # ən son yazılanlar yuxarda
    return render(request, 'articles_list.html', {'articles': articles})

# Məqalə detayı
def articles_detail(request, pk):
    cache_key = f"article_{pk}"  # hər məqaləyə unikal açar
    article = cache.get(cache_key)

    if not article:
        # Cache-də yoxdursa DB-dən götürürük
        article = get_object_or_404(Article, pk=pk)
        cache.set(cache_key, article, timeout=60*5)  # 5 dəqiqəlik cache

    return render(request, 'articles_detail.html', {
        'title': article.title,
        'article': article,
    })

@login_required
def addArticle(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)  # commit=False ilə model obyektini yarat, amma DB-ə yazma
            article.author = request.user      # author-u təyin et
            article.save()                     # indi DB-ə yaz
            messages.success(request, "Article added successfully!")
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ArticleForm()

    return render(request, 'addarticle.html', {'form': form})
@login_required
def dashboard_view(request):
    user = request.user

    # İstifadəçinin məqalələri
    user_articles = Article.objects.filter(author=user)

    # Statistikalar
    total_articles = user_articles.count()
    pending_reviews = user_articles.filter(status='pending').count()
    

    context = {
        'user_articles': user_articles,
        'total_articles': total_articles,
        'pending_reviews': pending_reviews,
        
    }

    return render(request, 'dashboard.html', context)

@login_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)  # yalnız müəllif
    if request.method == 'POST':
        form = ArticleForm(request.POST,request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('article:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ArticleForm(instance=article)

    return render(request, 'edit_article.html', {'form': form, 'article': article})


@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)  # yalnız müəllif
    if request.method == 'POST':
        article.delete()
        messages.success(request, "Article deleted successfully!")
        return redirect('article:dashboard')
    return render(request, 'delete_article.html', {'article': article})


def search_view(request):
    query = request.GET.get('q', '')
    results = search_articles(query) if query else []
    return render(request, 'search_results.html', {'query': query, 'results': results})


