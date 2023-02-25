 # type: ignore

from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView
from ..models import Buffer, Precipitant, Additive, Reservoirsolution, Protein, Plate, Cell, Observation
from django.contrib.auth.decorators import login_required
from django.db import models
from datetime import datetime



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
    


@login_required(login_url='/accounts/login/')
def main(request):
    username = request.user.username
    active_plates = Plate.objects.filter(status='Active', addedby=username).count()
    active_cells = Cell.objects.filter(cellstatus='InObservation', addedby=username).count()
    observation_overdue = Observation.objects.filter(status='InObservation', addedby=username, nextdate__lte=datetime.now()).values('combiname').distinct().count()

    context = {
        'username':username,
        'active_plates':active_plates,
        'active_cells':active_cells,
        'observation_overdue':observation_overdue
    }

    return render(request, "main.html", context)