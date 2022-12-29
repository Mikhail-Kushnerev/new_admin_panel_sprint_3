from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, PersonFilmwork


class MixinAPI:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Filmwork.objects.prefetch_related('genres', 'persons').values().all().annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=self.__search_role(PersonFilmwork.Role.actor),
            directors=self.__search_role(PersonFilmwork.Role.director),
            writers=self.__search_role(PersonFilmwork.Role.producer),
        )

        return queryset

    @staticmethod
    def __search_role(role):
        return ArrayAgg(
            'persons__full_name',
            filter=Q(personfilmwork__role=role)
        )

    @staticmethod
    def render_to_response(context):
        return JsonResponse(context)


class MoviesListApi(MixinAPI, BaseListView):
    paginate_by = 50

    def get_context_data(self):
        queryset = self.get_queryset()
        paginator, pg, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': pg.previous_page_number() if pg.has_previous() else None,
            'next': pg.next_page_number() if pg.has_next() else None,
            'results': list(queryset)
        }
        return context


class MovieDetailAPI(MixinAPI, BaseDetailView):

    @staticmethod
    def get_context_data(**kwargs):
        context = kwargs['object']

        return context
