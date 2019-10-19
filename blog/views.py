from django.shortcuts import render
from blog.models import Post, Comment
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from blog import model_helpers
from blog import navigation
from blog.forms import CreateCommentForm

# Create your views here.


def post_list(request, category_name=model_helpers.category_name_all.slug()):

        category, posts = model_helpers.get_category_and_posts(category_name)
        categories = model_helpers.get_categories()

        context = {
            'navigation_items': navigation.navigation_items(navigation.NAV_POSTS),
            'posts': posts,
            'category': category,
            'categories': categories
        }

        return render(request, 'blog/post_list.html', context)


def post_detail(request, post_id, message=""):
    post = get_object_or_404(Post, pk=post_id)
    other_posts = Post.objects.filter(category=post.category).filter(published=True).exclude(title=post.title)

    comments = post.comments.exclude(status=Comment.STATUS_HIDDEN).order_by('created_at')

    if request.method == "POST":

        comment_form = comment_form = CreateCommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-message',
                                                args=[post.pk, 'Your comment has been posted'],
                                                ) + '#comments')
    else:
        comment_form = CreateCommentForm()

    context = {
        'post': post,
        'navigation_items': navigation.navigation_items(navigation.NAV_POSTS),
        'other_posts': other_posts,
        'comments': comments,
        'comment_form': comment_form,
        'message': message
    }

    return render(request, 'blog/post_detail.html', context)


def about(request):
    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_ABOUT),
    }

    return render(request, 'blog/about.html', context)