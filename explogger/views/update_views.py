from datetime import datetime
# from django import forms
from django.urls import reverse
# from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import  FormView, UpdateView, ListView, DetailView
from extra_views import ModelFormSetView
from ..models import User, Buffer, Precipitant, Additive, Reservoirsolution, Protein, Plate, Cell, Observation
from ..forms import BufferForm, PrecipitantForm, AdditiveForm, ReservoirSolutionForm, ProteinForm, PlateForm, CellForm, ObservationForm




# *************************************
# Update View
# *************************************

class BufferUpdateView(LoginRequiredMixin, UpdateView):
    model = Buffer
    fields = '__all__'
    exclude = ['addedby']
    template_name = "explogger/form_update.html"
    success_url = "/buffer_list/"
    form_name = 'Buffer'
     
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # This is to pass context name so that single template file can be used
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['form_name'] = self.form_name
        return context

class PrecipitantUpdateView(BufferUpdateView):
    model = Precipitant
    template_name = "explogger/form_update.html"
    success_url = "/precipitant_list/"
    form_name = 'Precipitant'

class AdditiveUpdateView(BufferUpdateView):
    model = Additive
    template_name = "explogger/form_update.html"
    success_url = "/additive_list/"
    form_name = 'Additive'

class ReservoirSolutionUpdateView(BufferUpdateView):
    model = Reservoirsolution
    template_name = "explogger/form_update.html"
    success_url = "/rs_list/"
    form_name = 'ReservoirSolution'

class ProteinUpdateView(BufferUpdateView):
    model = Protein
    template_name = "explogger/form_update.html"
    success_url = "/protein_list/"
    form_name = 'Protein'

class PlateUpdateView(BufferUpdateView):
    model = Plate
    template_name = "explogger/form_update.html"
    success_url = "/plate_list/"
    form_name = 'Plate'

class CellUpdateView(BufferUpdateView):
    model = Cell
    template_name = "explogger/form_update.html"
    success_url = "/cell_list/"
    form_name = 'Cell'

class ObservationUpdateView(BufferUpdateView):
    model = Observation
    template_name = "explogger/form_update.html"
    success_url = "/observation_list/"
    form_name = 'Observation'

