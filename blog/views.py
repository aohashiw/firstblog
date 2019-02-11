from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Category,Banner,Tag,Tui,Link,Article
from userprofile.models import Profile
import markdown
# Create your views here.


def global_variable(request):
    allcategory = Category.objects.all()
    remen = Article.objects.filter(tui__id=2)[:6]
    tags =Tag.objects.all()
    return locals()

def index(request):
    banner = Banner.objects.filter(is_active=True)[0:3]
    tui = Article.objects.filter(tui__id=1)[:3]
    allarticle = Article.objects.all().order_by('id')[:10]
    hot = Article.objects.all().order_by('views')[:10]
    link = Link.objects.all()
    user=request.user
    return render(request,'index.html',locals())

def list(request,lid):
    list = Article.objects.filter(category_id=lid)
    cname = Category.objects.get(id=lid)
    page = request.GET.get('page')
    paginator = Paginator(list,5)
    try :
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage :
        list = paginator.page(paginator.num_pages)
    return render(request,'list.html',locals())

def show(request,sid):
    show = Article.objects.get(id=sid)
    hot = Article.objects.all().order_by('?')
    previous_blog = Article.objects.filter(created_time__gt=show.created_time,category=show.category.id).first()
    next_blog = Article.objects.filter(created_time__gt=show.created_time,category=show.category.id).last()
    show.views = show.views + 1
    show.save()
    show.body = markdown.markdown(show.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                  ])
    print(show.body)
    return render(request,'show.html',locals())

def tag(request,tag):
    list = Article.objects.filter(tags__name=tag)
    tname = Tag.objects.get(name=tag)
    page = request.GET.get('page')
    paginator = Paginator(list,5)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request, 'tags.html', locals())

def search(request):
    ss=request.GET.get('search')
    list = Article.objects.filter(title__icontains=ss)
    page = request.GET.get('page')
    paginator = Paginator(list,10)
    try :
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request ,'search.html',locals())


@login_required(login_url='/admin/login/')
def about(request):
    return render(request,'page.html',locals())

def page_not_found(request):
    return render(request, '404.html')

@login_required
def success(request,id):
    list = Article.objects.filter(user__id=id)
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user_id=user.id)
    return render(request, 'userprofile/success.html', locals())

def article_create(requset):
    if requset.user is not None:
        if requset.method == 'POST':
            uname=requset.user
            article_post_form = ArticlePostForm(data=requset.POST)
            if article_post_form.is_valid():
                new_article = article_post_form.save(commit=False)
                new_article.user=User.objects.get(username=uname)
                new_article.save()
            return redirect(reverse('success',args=[User.objects.get(username=uname).id]))
        else:
            article_post_form = ArticlePostForm()
            context = {'article_post_form':article_post_form}
            return render(requset,'add.html',locals())
    else:
        requset.session['uri']=requset.get_raw_uri()
        print('2')
    return render(requset,'add.html',locals())

def article_delete(requset,id):
    article = Article.objects.get(id=id)
    article.delete()
    return redirect(reverse('success', args=[User.objects.get(id=id).id]))





