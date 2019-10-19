from blog.models import Post, PostCategory

category_name_all = PostCategory(name="All")


def get_category_and_posts(category_name):

    posts = Post.objects.filter(published=True)

    if category_name == category_name_all.slug():
        category = category_name_all

    else:

        try:
            category = PostCategory.objects.get(name__iexact=category_name)
            posts = posts.filter(category=category)
            print(category)

        except PostCategory.DoesNotExist:
            category = PostCategory(name=category_name)
            posts = Post.objects.none()

    posts = posts.order_by("-created_at")
    return category, posts


def get_categories():
    cateroties = list(PostCategory.objects.all().order_by("name"))
    cateroties.insert(0, category_name_all)
    return cateroties