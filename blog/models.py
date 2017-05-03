from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class PostManager(models.Manager):
    def with_documents(self):
        vector = SearchVector('title', weight='A') + \
                 SearchVector('content', weight='C') + \
                 SearchVector('author__name', weight='B') + \
                 SearchVector(StringAgg('tags__name', delimiter=' '), weight='B')
        return self.get_queryset().annotate(document=vector)


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(Author)
    tags = models.ManyToManyField(Tag)
    search_vector = SearchVectorField(null=True)

    objects = PostManager()

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'])
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if 'update_fields' not in kwargs or 'search_vector' not in kwargs['update_fields']:
            instance = self._meta.default_manager.with_documents().get(pk=self.pk)
            instance.search_vector = instance.document
            instance.save(update_fields=['search_vector'])

    def __str__(self):
        return self.title


@receiver(post_save, sender=Author)
def author_changed(sender, instance, **kwargs):
    print("author_changed", sender, instance)
    for post in instance.post_set.with_documents():
        post.search_vector = post.document
        post.save(update_fields=['search_vector'])


@receiver(m2m_changed, sender=Post.tags.through)
def post_tags_changed(sender, instance, action, **kwargs):
    print("post_tags_changed", sender, instance, action)
    if action in ('post_add', 'post_remove', 'post_clear'):
        instance.save()
