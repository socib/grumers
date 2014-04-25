# coding: utf-8
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.http import Http404
from django.shortcuts import redirect
import models


class BasePageView(TemplateResponseMixin):
    """ All pages should inherit this class to get shared components
    """

    def dispatch(self, request, *args, **kwargs):
        # get shared objets between pages
        self.year = datetime.today().year
        self.pages = models.Page.objects.get(url='/').get_descendants()
        return super(BasePageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BasePageView, self).get_context_data(**kwargs)
        # Add shared objects
        context['year'] = self.year
        context['pages'] = self.pages
        return context


class HomePageView(TemplateView, BasePageView):

    template_name = "web/home.html"


class GenericPageView(DetailView, BasePageView):

    template_name = "web/page.html"
    model = models.Page
    context_object_name = 'page'

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(GenericPageView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        # Get page by url
        url = self.kwargs.get('url', None)
        queryset = queryset.filter(url='/' + url)
        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"Page not found"))
        return obj

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.registration_required and not self.user.is_authenticated():
            return redirect('/login/')
        return super(GenericPageView, self).get(*args, **kwargs)
