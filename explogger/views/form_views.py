 # type: ignore
from django import forms
from django.db.models import Max, Subquery, OuterRef, F
from datetime import datetime, timedelta
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  FormView, ListView
from extra_views import ModelFormSetView
from ..models import Plate, Cell, Observation
from ..forms import BufferForm, PrecipitantForm, AdditiveForm, ReservoirSolutionForm, ProteinForm, PlateForm


class BufferFormView(LoginRequiredMixin, FormView):
    form_class = BufferForm
    template_name = "explogger/form_input.html"
    success_url = "/buffer_list/"
    form_name = 'Buffer'
     
    def form_valid(self, form):
        form = form.save(commit=False)
        form.addedby = self.request.user  
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # This is to pass context name so that single template file can be used
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['form_name'] = self.form_name
        return context
    
class PrecipitantFormView(BufferFormView):
    form_class = PrecipitantForm
    template_name = "explogger/form_input.html"
    success_url = "/precipitant_list/"
    form_name = 'Precipitant'

class AdditiveFormView(BufferFormView):
    form_class = AdditiveForm
    template_name = "explogger/form_input.html"
    success_url = "/additive_list/"
    form_name = 'Additive'

class ReservoirSolutionFormView(BufferFormView):
    form_class = ReservoirSolutionForm
    template_name = "explogger/form_input.html"
    success_url = "/rs_list/"
    form_name = 'ReservoirSolution'

class ProteinFormView(BufferFormView):
    form_class = ProteinForm
    template_name = "explogger/form_input.html"
    success_url = "/protein_list/"
    form_name = 'Protein'

class PlateFormView(LoginRequiredMixin, FormView):
    form_class = PlateForm
    template_name = "explogger/form_input.html"
    # success_url = "/cell_list/"
    form_name = 'Plate'
    plate = None

    def form_valid(self, form):
            form = form.save(commit=False)
            form.addedby = self.request.user  
            form.save()

            plate = Plate.objects.get(id=form.id)
            self.plate = plate
            plate_name = plate.plate_name
            base_rsolution = form.base_rsolution
            base_protein = form.base_protein
            # status = form.status
            # addedby = form.addedby
            rows = ['A', 'B', 'C', 'D']
            cols = [1, 2, 3, 4, 5, 6]
            for row in rows:
                for col in cols:
                    cell = Cell(plate=Plate.objects.get(id=form.id),
                                cell_row=row,
                                cell_column=col,
                                reservoirsolution=base_rsolution,
                                ressol_volume=0,
                                protein=base_protein,
                                protein_volume=0,
                                startdate=datetime.now().strftime("%Y-%m-%d"),
                                cellstatus='InObservation',
                                cell_combiname= plate_name + '_' + row + str(col), 
                                addedby=self.request.user, 
                                remark='')
                    cell.save()
                    observation = Observation(platename=Plate.objects.get(id=form.id),
                                              cellname=Cell.objects.get(id=cell.id),
                                              combiname = plate_name + '_' + row + str(col),
                                              observ_date=datetime.now().strftime("%Y-%m-%d"),
                                              observ_count=0,
                                              crystal_type=None,
                                              crystal_size=None,
                                              photo='test.jpg',
                                              status='InObservation',
                                              nextdate=(datetime.now()+timedelta(days = 5)).strftime("%Y-%m-%d"),
                                              remark='',
                                              addedby=self.request.user)
                    observation.save()
            return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('cells_update', kwargs={'plate':self.plate})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = self.form_name
        return context

class CellsUpdate(ModelFormSetView):
    model = Cell
    template_name = 'explogger/setup_cellmatrix.html'
    fields = ['cell_combiname', 'reservoirsolution', 'ressol_volume', 'protein', 'protein_volume']
    factory_kwargs = {'extra': 0}
    plate = None

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(plate__plate_name=self.kwargs['plate'])
        self.plate = self.kwargs['plate'] 
        qs = qs.filter(addedby=self.request.user)
        qs = qs.order_by("id")
        return qs
    
    def get_success_url(self):
        return reverse('cells_list', kwargs={'plate':self.plate})

class CellListByPlate(LoginRequiredMixin, ListView):
    #tagged url cells_list
    permission_required = 'explogger.view_buffer'
    model = Cell
    plate=None
    # template = 'cell_list.html'
   
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(plate__plate_name=self.kwargs['plate']) 
        self.plate = self.kwargs['plate']
        qs = qs.filter(addedby=self.request.user)
        qs = qs.order_by("id")
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['plate_name'] = self.plate
        return context

class ObservationListByPlate(LoginRequiredMixin, ListView):
    #tagged url observation_list
    permission_required = 'explogger.view_buffer'
    model = Observation
    field = '__all__'
    plate = None
    # template = 'explogger/observation_list.html'
   
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(platename__plate_name=self.kwargs['plate']) 
        self.plate = self.kwargs['plate']
        qs = qs.filter(addedby=self.request.user)
        sq = qs.filter(combiname=OuterRef('combiname')).order_by('-observ_count').values('id')
        qs = qs.annotate(latest=Subquery(sq[:1])).filter(id=F('latest'))
        qs = qs.order_by('combiname')
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plate'] = self.plate
        return context


class MyForm(forms.ModelForm):
    model = Observation

    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget = forms.FileInput()

class ObservationNew(ModelFormSetView):
    model = Observation
    template_name = 'explogger/observation_newfor_cellmatrix.html'
    fields = ['combiname', 'observ_date', 'crystal_type', 'crystal_size', 'photo', 'status', 'nextdate']
    factory_kwargs = {'extra': 0}
    plate = None
    form_class = MyForm

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(platename__plate_name=self.kwargs['plate'])
        self.plate = self.kwargs['plate'] 
        qs = qs.filter(addedby=self.request.user)
        qs = qs.filter(status='InObservation')
        max_counter = qs.aggregate(Max('observ_count'))
        qs = qs.filter(observ_count=max_counter['observ_count__max'])
        qs = qs.order_by("id")
        return qs
    
    def get_success_url(self):
        return reverse('observation_list', kwargs={'plate':self.plate})
    
    def formset_valid(self, formset):
        for form in formset:
            form = form.save(commit=False)
            form.id = None # To ensure new record is created
            form.observ_count = form.observ_count +1
            form.save()

            cell = Cell.objects.get(id=form.cellname_id)
            cell.cellstatus = form.status
            cell.save()

        return super().formset_valid(formset)
    
    # def get_photo_url(self):
    #     if self.photo and hasattr(self.photo, 'url'):
    #         return self.photo.url
    #     else:
    #         return "/static/test.jpg"
