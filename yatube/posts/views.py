from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from .models import Post, Group, User, Follow
from .forms import PostForm, CommentForm


POST_IN_PAGE = 10


@cache_page(20, key_prefix="index_page")
def index(request):
    """Главная страница."""
    posts = Post.objects.all()
    paginator = Paginator(posts, POST_IN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    # Выполняет указанный шаблон с переданным словарем контекста и возвращает HttpResponse с полученным содержимым.
    return render(request, 'posts/index.html', context)


def groups_posts(request, slug):
    """Страница с постуами группы."""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, POST_IN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, POST_IN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user,
        author=author
    ).exists()
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # ссылаемся на автора использея related_name в Post и считаем сумму его постов
    count = post.author.posts.count()
    comments = post.comments.all()
    form = CommentForm(request.POST or None)
    context = {
        'post': post,
        'count': count,
        'post_id': post.id,
        'form': form,
        'comments': comments
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)
    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'is_edit': is_edit,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'comments': comments,
        'author': request.user
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def follow_index(request):
    # Сначала ищется пользователь с заданным именем.Для него ищутся объекты
    # в таблице Follow, которые на него ссылаются. Далее для всех найденных
    # записей в Follow ищутся связанные с ними авторы.А далее все
    # посты, которые связанны с найденными авторами.
    # https://ru.stackoverflow.com/questions/1194688/%D0%9E%D0%B1%D1%8A%D1%8F%D1%81%D0%BD%D0%B8%D1%82%D0%B5-%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81-%D0%BA-%D0%B1%D0%B0%D0%B7%D0%B5
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, POST_IN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts': posts
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username=author)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follow_delete = Follow.objects.filter(user=request.user, author=author)
    if follow_delete.exists():
        follow_delete.delete()
    return redirect('posts:profile', username=author)
