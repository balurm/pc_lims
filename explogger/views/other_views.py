 # type: ignore

# from datetime import datetime
# from django import forms
# from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import  FormView, UpdateView, ListView, DetailView
from extra_views import ModelFormSetView
from ..models import User, Buffer, Precipitant, Additive, Reservoirsolution, Protein, Plate, Cell, Observation
from ..forms import BufferForm, PrecipitantForm, AdditiveForm, ReservoirSolutionForm, ProteinForm, PlateForm, CellForm, ObservationForm
from django.contrib.auth.decorators import login_required
from django.db import models



class BufferListView(PermissionRequiredMixin, ListView):
    permission_required = 'explogger.view_buffer'
    model = Buffer
    template_name = "explogger/list_view.html"
    list_name = 'buffer'
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        # qs = qs.filter(addedby=self.request.user)
        qs = qs.order_by("-id")
        return qs
    
    def get_context_data(self, **kwargs):
        # This is to pass context name so that single template file can be used
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['list_name'] = self.list_name
        return context

    def get_fields(self):
        return [
            (field, str(getattr(self, field.name)))
            if isinstance(field, models.ForeignKey)
            else (field, field.value_to_string(self))
            for field in self._meta.fields
        ]

class PrecipitantListView(BufferListView):
    model = Precipitant
    template_name = "explogger/list_view.html"
    list_name = 'precipitant'

class AdditiveListView(BufferListView):
    model = Additive
    template_name = "explogger/list_view.html"
    list_name = 'additive'

class RsListView(BufferListView):
    model = Reservoirsolution
    template_name = "explogger/list_view.html"
    list_name = 'rs'

class ProteinListView(BufferListView):
    model = Protein
    template_name = "explogger/list_view.html"
    list_name = 'protein'

class PlateListView(BufferListView):
    model = Plate
    template_name = "explogger/list_view.html"
    list_name = 'plate'

class CellPlateListView(BufferListView):
    model = Plate
    template_name = "explogger/platelist_for_cellmatrix.html"
    list_name = 'cell'
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.values('id', 'plate_name')
        qs = qs.order_by("-id")
        return qs

class ObservationPlateListView(BufferListView):
    model = Plate
    template_name = "explogger/platelist_for_observation.html"
    list_name = 'observation'
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.values('id', 'plate_name')
        qs = qs.order_by("-id")
        return qs
    




# class BufferDetailView(LoginRequiredMixin, DetailView):
#     permission_required = 'explogger.view_buffer'
#     model = Buffer


# class CellListView(LoginRequiredMixin, ListView):
#     permission_required = 'explogger.view_buffer'
#     model = Cell
#     def get_queryset(self, *args, **kwargs):
#         qs = super().get_queryset(*args, **kwargs)
#         # qs = qs.filter(addedby=self.request.user)
#         qs = qs.order_by("-id")
#         return qs


# class CellListByPlate(LoginRequiredMixin, ListView):
#     permission_required = 'explogger.view_buffer'
#     model = Cell
#     def get_queryset(self, *args, **kwargs):
#         qs = super().get_queryset(*args, **kwargs)
#         # self.plate = 
#         # qs = qs.filter(addedby=self.request.user)
#         qs = qs.order_by("-id")
#         return qs



# class RsFormView(FormView):
#      form_class = RsForm
#      template_name = "explogger/reservoirsolution_form.html"
#      success_url = "/rs_list/"
     
#      def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)









# def rs_list(request):
#     entries = Reservoirsolution.objects.all().values()
#     template = loader.get_template('rs_list.html')
#     context = {
#         'entries': entries,
#     }
#     return HttpResponse(template.render(context, request))











def testing(request):
    mybuffers = Buffer.objects.all()
    template = loader.get_template('test_template.html')
    context = {
        'mybuffers': mybuffers,
    }
    return HttpResponse(template.render(context, request))



@login_required(login_url='/accounts/login/')
def main(request):
    return render(request, "main.html",{
        "username": request.user.username # don't overwriting user
    })


# # Create your views here.
# def explist(request):
#     template = loader.get_template('explist.html')
#     return HttpResponse(template.render())
# 
# def buffer_list(request):
#     mybuffers = Buffer.objects.all().values()
#     template = loader.get_template('buffer_list.html')
#     context = {
#         'mybuffers': mybuffers,
#     }
#     return HttpResponse(template.render(context, request))
# 
# 
# def buffer_form(request):
#     context = {}
#     # create object of form
#     form = BufferForm(request.POST or None)
#     # check if form data is valid
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect(reverse('buffers'))
# 
#     context['form'] = form
#     return render(request, "buffer_form.html", context)
# 
# def buffer_details(request, id):
#     mybuffer = Buffer.objects.get(id=id)
#     template = loader.get_template('buffer_details.html')
#     context = {
#         'mybuffer': mybuffer,
#     }
#     return HttpResponse(template.render(context, request))



# from extra_views import UpdateWithInlinesView
# from extra_views.generic import GenericInlineFormSet


