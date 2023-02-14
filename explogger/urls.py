from django.urls import path
from . import views
# from .views import BufferListView, RsListView
# from .views import BufferUpdateView
# from .views import BufferFormView, ReservoirSolutionFormView, RsDetailView, PrecipitantFormView
# from .views import BufferDetailView, RsDetailView
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.main, name='main'),
         
    path('form_buffer/', BufferFormView.as_view(), name='buffer_form'), 
    path('form_precipitant/', PrecipitantFormView.as_view(), name='precipitant_form'),  
    path('form_additive/', AdditiveFormView.as_view(), name='additive_form'), 
    path('form_rs/', ReservoirSolutionFormView.as_view(), name='reservoirsolution_form'), 
    path('form_protein/', ProteinFormView.as_view(), name='protein_form'), 
    path('form_plate/', PlateFormView.as_view(), name='plate_form'), 

    path('update_buffer/<int:pk>', BufferUpdateView.as_view(), name='buffer_update'), 
    path('update_precipitant/<int:pk>', PrecipitantUpdateView.as_view(), name='precipitant_update'),  
    path('update_additive/<int:pk>', AdditiveUpdateView.as_view(), name='additive_update'), 
    path('update_rs/<int:pk>', ReservoirSolutionUpdateView.as_view(), name='rs_update'), 
    path('update_protein/<int:pk>', ProteinUpdateView.as_view(), name='protein_update'), 
    path('update_plate/<int:pk>', PlateUpdateView.as_view(), name='plate_update'), 
    path('update_cell/<int:pk>', CellUpdateView.as_view(), name='cell_update'), 
    path('update_observation/<int:pk>', ObservationUpdateView.as_view(), name='observation_update'), 

    path('buffer_list/', BufferListView.as_view(), name='buffer_list'),
    path('precipitant_list/', PrecipitantListView.as_view(), name='precipitant_list'),
    path('additive_list/', AdditiveListView.as_view(), name='additive_list'),
    path('rs_list/', RsListView.as_view(), name='rs_list'),
    path('protein_list/', ProteinListView.as_view(), name='protein_list'),
    path('plate_list/', PlateListView.as_view(), name='plate_list'),
    path('cell_list/', CellPlateListView.as_view(), name='cell_list'),
    path('observation_list/', ObservationPlateListView.as_view(), name='observation_list'),
                                     
    path('cells_list/<path:plate>', CellListByPlate.as_view(), name='cells_list'),
    path('cells_update/<path:plate>', CellsUpdate.as_view(), name='cells_update'),

    path('observation_list/<path:plate>', ObservationListByPlate.as_view(), name='observation_list'),
    path('observation_new/<path:plate>', ObservationNew.as_view(), name='observation_new'),              

]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)