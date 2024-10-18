from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

User = get_user_model()


# Create your models here.
class Post(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.ImageField(upload_to='media', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']


def create_slug(instance, new_slug=None):
    print(f'0 - {new_slug}')
    slug = slugify(instance.title)
    print(f'1 - {instance.title}')
    print(f'2 - {slug}')
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    print(f'3 - {qs}')
    exists = qs.exists()
    print(f'4 - {exists}')
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        print(f'5 - {new_slug}')
        return create_slug(instance, new_slug=new_slug)
    print(f'6 - {slug}')
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)


class Comment(models.Model):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['created_at']
