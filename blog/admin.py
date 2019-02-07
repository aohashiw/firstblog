from django.contrib import admin
from .models import Banner,Category,Tag,Tui,Article,Link
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    #w文章列表显示想要显示的字段
    list_display = ('id','category','title','tui','user','views','created_time')
    #数据满5o条就分页
    list_per_page = 50
    #后台数据排列方式
    ordering = ('-created_time'),
    #设置那些字段可以编辑
    list_display_links = ('id','title')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id','text_info','img','link_url','is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','index')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(Tui)
class TuiAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id','name','linkurl')
