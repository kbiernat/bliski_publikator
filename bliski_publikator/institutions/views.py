from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import ugettext_lazy as _
from braces.views import (SelectRelatedMixin, LoginRequiredMixin, FormValidMessageMixin,
                          UserFormKwargsMixin)
from django.core.urlresolvers import reverse_lazy
from django_filters.views import FilterView
from atom.views import DeleteMessageMixin
from .models import Institution
from .forms import InstitutionForm
from .filters import InstitutionFilter


class InstitutionListView(SelectRelatedMixin, FilterView):
    filterset_class = InstitutionFilter
    model = Institution
    select_related = ['region', ]
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        qs = super(InstitutionListView, self).get_queryset(*args, **kwargs)
        return qs


class InstitutionDetailView(SelectRelatedMixin, DetailView):
    model = Institution
    select_related = ['region', ]


class InstitutionCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = Institution
    form_class = InstitutionForm

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class InstitutionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserFormKwargsMixin,
                            FormValidMessageMixin, UpdateView):
    model = Institution
    form_class = InstitutionForm
    permission_required = 'institutions.change_institution'

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class InstitutionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteMessageMixin,
                            DeleteView):
    model = Institution
    success_url = reverse_lazy('monitorings:list')
    permission_required = 'institutions.delete_institution'

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)
