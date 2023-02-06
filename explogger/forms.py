# import form class from django
from django import forms
# from django.contrib.admin import widgets                                       
from django.forms.widgets import DateInput

from datetime import datetime, timedelta

# import GeeksModel from models.py
from .models import User, Buffer, Precipitant, Additive, Reservoirsolution, Protein, Plate, Cell, Observation

# create a ModelForm
class UserForm(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = User
        # exclude = ['name'] Will help to exclude fields
		fields = "__all__"


class BufferForm(forms.ModelForm):

	class Meta:
		model = Buffer
		exclude = ["addedby"]
		fields = "__all__"
		
		widgets = {
            'makedate': DateInput(attrs={'type': 'text', 'class':'datepicker', 
					 'value': datetime.now().strftime("%Y-%m-%d")}),
			'expdate' : DateInput(attrs={'type': 'text', 'class':'datepicker', 
				'value': (datetime.now()+timedelta(days = 365)).strftime("%Y-%m-%d")}),
			
		}



class PrecipitantForm(forms.ModelForm):
	class Meta:
		model = Precipitant
		exclude = ["addedby"]
		fields = "__all__"

		widgets = {
            'makedate': DateInput(attrs={'type': 'text', 'class':'datepicker', 
					 'value': datetime.now().strftime("%Y-%m-%d")}),
			'expdate' : DateInput(attrs={'type': 'text', 'class':'datepicker', 
				'value': (datetime.now()+timedelta(days = 365)).strftime("%Y-%m-%d")}),
			
		}

class AdditiveForm(forms.ModelForm):
	class Meta:
		model = Additive
		exclude = ["addedby"]
		fields = "__all__"

		widgets = {
            'makedate': DateInput(attrs={'type': 'text', 'class':'datepicker', 
					 'value': datetime.now().strftime("%Y-%m-%d")}),
			'expdate' : DateInput(attrs={'type': 'text', 'class':'datepicker', 
				'value': (datetime.now()+timedelta(days = 365)).strftime("%Y-%m-%d")}),
			
		}

class ReservoirSolutionForm(forms.ModelForm):
	class Meta:
		model = Reservoirsolution
		exclude = ["addedby"]
		fields = "__all__"

		widgets = {
            'makedate': DateInput(attrs={'type': 'text', 'class':'datepicker', 
					 'value': datetime.now().strftime("%Y-%m-%d")}),
			'expdate' : DateInput(attrs={'type': 'text', 'class':'datepicker', 
				'value': (datetime.now()+timedelta(days = 365)).strftime("%Y-%m-%d")}),
			
		}

class ProteinForm(forms.ModelForm):
	class Meta:
		model = Protein
		exclude = ["addedby"]
		fields = "__all__"

		widgets = {
            'makedate': DateInput(attrs={'type': 'text', 'class':'datepicker', 
					 'value': datetime.now().strftime("%Y-%m-%d")}),
			'expdate' : DateInput(attrs={'type': 'text', 'class':'datepicker', 
				'value': (datetime.now()+timedelta(days = 365)).strftime("%Y-%m-%d")}),
			
		}

class PlateForm(forms.ModelForm):
	class Meta:
		model = Plate
		exclude = ["addedby"]
		fields = "__all__"

		widgets = {
            'makedate': DateInput(attrs={'type': 'text', 'class':'datepicker', 
					 'value': datetime.now().strftime("%Y-%m-%d")}),
			'expdate' : DateInput(attrs={'type': 'text', 'class':'datepicker', 
				'value': (datetime.now()+timedelta(days = 365)).strftime("%Y-%m-%d")}),
			
		}

class CellForm(forms.ModelForm):
	class Meta:
		model = Cell
		exclude = ["addedby"]
		fields = "__all__"

		widgets = {
            'makedate': DateInput(attrs={'type': 'text', 'class':'datepicker', 
					 'value': datetime.now().strftime("%Y-%m-%d")}),
			'expdate' : DateInput(attrs={'type': 'text', 'class':'datepicker', 
					'value': (datetime.now()+timedelta(days = 365)).strftime("%Y-%m-%d")}),
			'remark': forms.Textarea(attrs={'rows':1}),
			
		}


# class CellForm(forms.ModelForm):
# 	def __init__(self, *args, **kwargs):
# 		super(CellForm, self).__init__(*args, **kwargs)
	
# 	class Meta:
# 		model = Cell
# 		fields = "__all__"
	    


class ObservationForm(forms.ModelForm):
	def __init__(self, plate_name, *args, **kwargs):
		super().__init__(*args,**kwargs) # populates the post
		self.fields['platename'].queryset = Plate.objects.filter(plate_name=plate_name)
		self.fields['cellname'].queryset = Cell.objects.filter(plate__plate_name=plate_name)

	class Meta:
		model = Observation
		exclude = ["addedby"]
		fields = "__all__"

		widgets = {
            'observ_date': DateInput(attrs={'type': 'text', 'class':'datepicker', 
					 'value': datetime.now().strftime("%Y-%m-%d")}),
			'nextdate' : DateInput(attrs={'type': 'text', 'class':'datepicker', 
				'value': (datetime.now()+timedelta(days = 5)).strftime("%Y-%m-%d")}),
			'remark': forms.Textarea(attrs={'rows':1}),
        }

		
		
		
# class AdditiveForm(forms.ModelForm):
# 	class Meta:
# 		model = Additive
# 		fields = "__all__"

# class RsForm(forms.ModelForm):
# 	class Meta:
# 		model = Reservoirsolution
# 		fields = "__all__"

# class ProteinForm(forms.ModelForm):
# 	class Meta:
# 		model = Protein
# 		fields = "__all__"

# class PlateForm(forms.ModelForm):
# 	class Meta:
# 		model = Plate
# 		fields = "__all__"

# class CellForm(forms.ModelForm):
# 	class Meta:
# 		model = Cell
# 		fields = "__all__"

# class ObservationForm(forms.ModelForm):
# 	class Meta:
# 		model = Observation
# 		fields = "__all__"
