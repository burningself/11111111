# -*- coding: utf-8 -*-
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.decorators import login_required
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework import filters


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class SelfPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'perPage'


class CustomOrderingFilter(filters.OrderingFilter):
    def __init__(self):
        super(CustomOrderingFilter, self).__init__()

    def filter_queryset(self, request, queryset, view):
        custom_ordering = getattr(view, 'custom_ordering', None)
        ordering = self.get_ordering(request, queryset, view)

        print custom_ordering
        if ordering:
            newcol = {}
            custom_list = []
            order_list = []
            for each in ordering:
                if each in custom_ordering or each[1:] in custom_ordering:
                    if each.startswith("-"):
                        newcol["new_"+each[1:]] = 'CONVERT(%s USING gbk)' % each[1:]
                        custom_list.append("-new_"+each[1:])
                    else:
                        newcol["new_"+each] = 'CONVERT(%s USING gbk)' % each
                        custom_list.append("new_"+each)
                else:
                    order_list.append(each)
                    
            queryset = queryset.order_by(*order_list).extra(select=newcol).extra(order_by = custom_list)

        return queryset