# coding: utf-8
from datetime import datetime
from django.views.generic import TemplateView, FormView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import models
import forms


class BasePageView(TemplateResponseMixin):
    """ All pages should inherit this class to get shared components
    """

    def dispatch(self, request, *args, **kwargs):
        # get shared objets between pages
        self.year = datetime.today().year
        self.pages = models.Page.objects.get(url='/').get_descendants()
        if not request.user.is_superuser:
            # Exclude pages with registration_required and that not include
            # any group from the user
            self.pages = self.pages.exclude(
                ~Q(groups=None),
                ~Q(groups__in=self.request.user.groups.all()),
                registration_required=True)
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


class ChangeProfileView(FormView, BasePageView):

    template_name = "registration/change_profile.html"
    form_class = forms.UserProfileForm
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        return super(ChangeProfileView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ChangeProfileView, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        self.user.first_name = form.cleaned_data['first_name']
        self.user.last_name = form.cleaned_data['last_name']
        self.user.email = form.cleaned_data['email']
        if len(form.cleaned_data['new_password']) > 0:
            self.user.set_password(form.cleaned_data['new_password'])
        self.user.save()
        messages.add_message(self.request, messages.SUCCESS, _('Profile updated'))
        return super(ChangeProfileView, self).form_valid(form)
