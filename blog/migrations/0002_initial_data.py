# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 17:56
from __future__ import unicode_literals

from django.db import migrations


def load_initial_data(apps, schema_editor):
    Author = apps.get_model('blog', 'Author')
    Tag = apps.get_model('blog', 'Tag')
    Post = apps.get_model('blog', 'Post')

    jim = Author.objects.create(name="Jim Blogwriter")
    nancy = Author.objects.create(name="Nancy Blogaday")

    databases = Tag.objects.create(name="Databases")
    programming = Tag.objects.create(name="Programming")
    python = Tag.objects.create(name="Python")
    postgres = Tag.objects.create(name="Postgres")
    django = Tag.objects.create(name="Django")

    django_post = Post.objects.create(
        title="Django, the western character",
        content="Django is a character who appears in a number of spaghetti western films.",
        author=jim
    )
    django_post.tags.add(django)

    python_post = Post.objects.create(
        title="Python is a programming language",
        content="Python is a programming language created by Guido van Rossum and first released "
                "in 1991. Django is written in Python. Python can connect to databases.",
        author=nancy
    )
    python_post.tags.add(django, programming, python)

    postgres_post = Post.objects.create(
        title="What is Postgres",
        content="PostgreSQL, commonly Postgres, is an open-source, object-relational database (ORDBMS).",
        author=nancy
    )
    postgres_post.tags.add(databases, postgres)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, migrations.RunPython.noop)
    ]
