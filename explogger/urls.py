from django.urls import path, include
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
         
    # path('full_plate/<str:plate>', CellListByPlate.as_view(), name='full_plate'),
    # path('update_platecells/<str:plate>', CellsUpdate.as_view(), name='update_platecells'),
    
    path('form_buffer/', BufferFormView.as_view(), name='buffer_form'), 
    path('form_precipitant/', PrecipitantFormView.as_view(), name='precipitant_form'),  
    path('form_additive/', AdditiveFormView.as_view(), name='additive_form'), 
    path('form_rs/', ReservoirSolutionFormView.as_view(), name='reservoirsolution_form'), 
    path('form_protein/', ProteinFormView.as_view(), name='protein_form'), 
    path('form_plate/', PlateFormView.as_view(), name='plate_form'), 
    # path('form_cell/', CellFormView.as_view(), name='cell_form'), 
    # path('form_observation/', ObservationFormView.as_view(), name='observation_form'), 

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


    # path('list_buffers/', BufferListView.as_view(), name='buffer_list'),
    # path('list_buffers/', BufferListView.as_view(), name='buffer_list'),

    path('list_rs/', RsListView.as_view(), name='rs_list'),
                                      
 
    # path('cell_list/', CellListView.as_view(), name='cell_list'),
    path('cells_list/<str:plate>', CellListByPlate.as_view(), name='cells_list'),
    path('cells_update/<str:plate>', CellsUpdate.as_view(), name='cells_update'),

    # path('observation_update/<str:plate>', ObservationUpdate.as_view(), name='observation_update'),              
    path('observation_list/<str:plate>', ObservationListByPlate.as_view(), name='observation_list'),
    path('observation_new/<str:plate>', ObservationNew.as_view(), name='observation_new'),              

    # path('observation_list/', ObservationListView.as_view(), name='observation_list'),
    # path('test11', TestFormSetView.as_view(), name='test11')

    # path('rs_form/', RsFormView.as_view(), name='rs_form'),
    # path('testing/', views.testing, name='testing'),  
    # path('explist/', views.explist, name='explist'),
    # path('buffer_form/', views.buffer_form, name='buffer_form'), 

    # path('accounts/', include('django.contrib.auth.urls')),

    # path('buffer_list/', views.buffer_list, name='buffer_list'),
    # path('buffer_details/<int:id>', views.buffer_details, name='buffer_details'),

    # path('rs_detail/<int:pk>', RsDetailView.as_view(), name='rs_detail'),
    # path('buffer_detail/<int:pk>', BufferDetailView.as_view(), name='buffer_detail'),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)