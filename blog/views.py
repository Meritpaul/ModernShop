from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post, BlogCategory, Comment
from .forms import CommentForm


def blog_list_view(request):
    posts = Post.objects.filter(is_published=True).select_related('author', 'category')

    cat_slug = request.GET.get('category', '').strip()
    active_cat = None
    if cat_slug:
        active_cat = get_object_or_404(BlogCategory, slug=cat_slug)
        posts = posts.filter(category=active_cat)

    q = request.GET.get('q', '').strip()
    if q:
        posts = posts.filter(title__icontains=q)

    paginator = Paginator(posts, 9)
    page_obj  = paginator.get_page(request.GET.get('page'))
    categories = BlogCategory.objects.all()

    return render(request, 'blog/blog_list.html', {
        'page_obj': page_obj, 'categories': categories,
        'active_cat': active_cat, 'q': q,
    })


def blog_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    Post.objects.filter(pk=post.pk).update(views=post.views + 1)

    comments   = post.comments.filter(is_approved=True)
    recent     = Post.objects.filter(is_published=True).exclude(pk=post.pk)[:4]
    categories = BlogCategory.objects.all()

    initial = {}
    if request.user.is_authenticated:
        initial = {
            'name':  request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }

    form = CommentForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        c = form.save(commit=False)
        c.post = post
        if request.user.is_authenticated:
            c.user = request.user
        c.save()
        messages.success(request, 'Comment posted!')
        return redirect('blog:detail', slug=slug)

    return render(request, 'blog/blog_detail.html', {
        'post': post, 'comments': comments, 'recent': recent,
        'categories': categories, 'form': form,
    })
