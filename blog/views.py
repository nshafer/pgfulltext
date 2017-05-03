from django.db.models import F
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.shortcuts import render
from django.views.generic import ListView

from blog.models import Post


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            query = SearchQuery(q)
            qs = qs.annotate(rank=SearchRank(F('search_vector'), query))\
                .filter(search_vector=query) \
                .order_by('-rank')

        return qs

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            q=self.request.GET.get('q', "")
        )
