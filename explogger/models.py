# type: ignore

from django.db import models
from django.utils import timezone
# from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal # helps to set min_value=0

# class User(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     email = models.EmailField()
#     phone = models.CharField(max_length=12)
    
#     def __str__(self):
#         return f'{self.username}'

#     def get_fields(self):
#         return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]


# Create your models here.
class Buffer(models.Model):
    UNITS = [('mg', 'mg'), ('ml','ml'), ('%','%'), ('M', 'M')]

    name = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    package = models.CharField(max_length=20, null=False)
    concentration = models.DecimalField(max_digits=5, decimal_places=1)
    concunit = models.CharField(max_length=7, choices=UNITS, default='mg')
    ph = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(14)])
    makedate = models.DateField(null=True)
    expdate = models.DateField(null=True)
    remark = models.TextField(null=True, blank=True)
    # addedby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    addedby = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field='username', related_name='b_addedby',  db_column='b_addedby')
    b_combiname = models.CharField(max_length=20, unique=True)

    # def save(self, *args, **kwargs):
    #     self.b_combiname = self.name[0:3] + '_' + self.make + '_' + self.package
    #     super(Buffer, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.b_combiname}'
    
    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    
''' explog = Buffer(name='SuperBuff',
make='DeltaKing',
package=2022,
concentration=20,
concunit='ml',
ph=4.3,
makedate='2023-01-07',
bcombi_name = 'DK_2022_20_ml_4.3'

) '''



# Create your models here.
class Precipitant(models.Model):
    UNITS = [('M', 'M'), ('%','%')]
    VOLUMES = [('W/V', 'W/V'), ('V/V', 'V/V')]

    name = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    package = models.CharField(max_length=20, null=False)
    concentration = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    concunit = models.CharField(max_length=2, choices=UNITS)
    wv_vv = models.CharField(max_length=3, choices=VOLUMES)
    makedate = models.DateField(null=True)
    expdate = models.DateField(null=True)
    p_combiname = models.CharField(max_length=20, unique=True)
    remark = models.TextField(null=True, blank=True)
    addedby = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field='username', related_name='p_addedby',  db_column='p_addedby')

    def __str__(self):
        # This is for admin display
        # This can also done using admin.py
        return f'{self.p_combiname}'

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]



class Additive(models.Model):
    UNITS = [('M', 'M'), ('%','%')]
    VOLUMES = [('W/V', 'W/V'), ('V/V', 'V/V')]

    name = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    package = models.CharField(max_length=20, null=False)
    concentration = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    concunit = models.CharField(max_length=2, choices=UNITS)
    wv_vv = models.CharField(max_length=3, choices=VOLUMES)
    makedate = models.DateField(null=True)
    expdate = models.DateField(null=True)
    a_combiname = models.CharField(max_length=20, unique=True)
    remark = models.TextField(null=True, blank=True)
    addedby = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field='username', related_name='a_addedby',  db_column='a_addedby')


    def __str__(self):
        return f'{self.a_combiname}'

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]



class Reservoirsolution(models.Model):
    # To_field -- which field needs to be referenced
    buffer = models.ForeignKey(Buffer, on_delete=models.DO_NOTHING, to_field='b_combiname', related_name='buffer',  db_column='buffer')
    b_volume = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=Decimal('0.0'))

    precipitant = models.ForeignKey(Precipitant, on_delete=models.DO_NOTHING, to_field='p_combiname', related_name='precip',  db_column='precip')
    p_volume = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=Decimal('0.0'))

    additive1 = models.ForeignKey(Additive, on_delete=models.DO_NOTHING, to_field='a_combiname', related_name='additive1',  db_column='additive1')
    a1_volume = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=Decimal('0.0'))

    additive2 = models.ForeignKey(Additive, on_delete=models.DO_NOTHING,  blank=True, null=True, to_field='a_combiname', related_name='additive2',  db_column='additive2')
    a2_volume = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=Decimal('0.0'))

    total_volume = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=Decimal('0.0'))
    rs_combinedname = models.CharField(max_length=20, unique=True)
    remark = models.TextField(null=True)
    makedate = models.DateField(default=timezone.now)
    addedby = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field='username', related_name='rs_addedby',  db_column='rs_addedby')


    def save(self, *args, **kwargs):
        self.total_volume = self.b_volume + self.p_volume + self.a1_volume + self.a2_volume #+ self.a3_volume
        return super(Reservoirsolution, self).save(*args, **kwargs)
    
    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    def __str__(self):
        return f'{self.rs_combinedname}'



class Protein(models.Model):
    SOURCES = [('Company','Company'), ('Patient', 'Patient'), ('Volume', 'Volume'), ('Leaf','Leaf')]
    UNITS = [('M', 'M'), ('%','%')]

    name = models.CharField(max_length=50, unique=True)
    puri_method = models.CharField(max_length=255)
    source = models.CharField(max_length=20, choices=SOURCES, default='Company')
    concentration = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    concunit = models.CharField(max_length=2, choices=UNITS, default='M')
    remark = models.TextField(null=True, blank=True)
    addedby = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field='username', related_name='pr_addedby',  db_column='pr_addedby')

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]


    def __str__(self):
        # This is for admin display
        return f'{self.name}'


class Plate(models.Model):
    BOOL_CHOICES = (('Active', 'Active'), ('Closed', 'Closed'))

    plate_name = models.CharField(max_length=50, unique=True)
    base_rsolution = models.ForeignKey(Reservoirsolution, on_delete=models.DO_NOTHING)
    base_protein = models.ForeignKey(Protein, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, choices=BOOL_CHOICES, default='Active')
    remark = models.TextField(null=True, blank=True)

    addedby = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field='username', related_name='pl_addedby',  db_column='pl_addedby')

    def __str__(self):
        # This is for admin display
        return f'{self.plate_name}'
    
    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]



class Cell(models.Model):
 
    STATUS = [ ('InObservation', 'InObservation'), ('Stopped', 'Stopped'), ('Characterisation', 'Characterisation')]
    ROWS = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    COLUMNS = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')]

    plate = models.ForeignKey(Plate, on_delete=models.CASCADE, related_name='plate', db_column='plate')
    cell_row = models.CharField(max_length=1, choices=ROWS)
    cell_column = models.CharField(max_length=1, choices=COLUMNS)
    reservoirsolution = models.ForeignKey(Reservoirsolution, on_delete=models.DO_NOTHING, related_name='rs', db_column='rs')
    ressol_volume= models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=Decimal('0.0'))
    protein = models.ForeignKey(Protein, on_delete=models.DO_NOTHING, related_name='protein', db_column='protein')
    protein_volume= models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=Decimal('0.0'))
    startdate = models.DateField()
    cellstatus = models.CharField(max_length=16, choices = STATUS, default='InObservation')
    cell_combiname = models.CharField(max_length=20, unique=True)
    addedby = models.ForeignKey(User, on_delete=models.DO_NOTHING,to_field='username', related_name='c_addedby',  db_column='c_addedby')
    remark = models.TextField(null=True, blank=True)

    # def get_absolute_url(self):
    #     return reverse('full_plate', kwargs={'slug': self.plate.slug, 'pk': self.pk})

    def __str__(self):
            # This is for admin display
            return f'{self.cell_combiname}'

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]


class Observation(models.Model):
 
    STATUS = [ ('InObservation', 'InObservation'), ('Stopped', 'Stopped'), ('Characterisation', 'Characterisation')]

    platename = models.ForeignKey(Plate, on_delete=models.CASCADE, related_name='platename', db_column='platename')
    cellname = models.ForeignKey(Cell, on_delete=models.DO_NOTHING)
    combiname = models.CharField(max_length=20, null=True, blank=True)
    observ_date = models.DateField()
    observ_count = models.PositiveSmallIntegerField(default=0) 
    crystal_type = models.CharField(max_length=20,null=True, blank=True)
    crystal_size = models.CharField(max_length=20,null=True, blank=True)
    photo = models.ImageField(upload_to='images/cells/%Y/%m/%d/', null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUS , default='InObservation')
    nextdate = models.DateField()
    remark = models.TextField(null=True, blank=True)
    addedby = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field='username', related_name='o_addedby',  db_column='o_addedby')

    def __str__(self):
        # This is for admin display
        return f'{self.cellname}'

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]




# class Reservoirsolution(models.Model):

#     buffer = models.ForeignKey(Buffer, on_delete=models.DO_NOTHING, related_name='buffer',  db_column='buffer')
#     b_volume = models.DecimalField(max_digits=5, decimal_places=1, min_value=0, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=0.0)

#     precipitant = models.ForeignKey(Precipitant, on_delete=models.DO_NOTHING, related_name='precip',  db_column='precip')
#     p_volume = models.DecimalField(max_digits=5, decimal_places=1, min_value=0, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=0.0)

#     additive1 = models.ForeignKey(Additive, on_delete=models.DO_NOTHING, related_name='additive1',  db_column='additive1')
#     a1_volume = models.DecimalField(max_digits=5, decimal_places=1, min_value=0, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=0.0)

#     additive2 = models.ForeignKey(Additive, on_delete=models.DO_NOTHING, related_name='additive2',  db_column='additive2')
#     a2_volume = models.DecimalField(max_digits=5, decimal_places=1, min_value=0, validators=[MinValueValidator(0), MaxValueValidator(1000)], default=0.0)

#     total_volume = models.DecimalField(max_digits=5, decimal_places=1, min_value=0)
#     rs_combinedname = models.CharField(max_length=20, unique=True)
#     remark = models.TextField(null=True, blank=True)
#     addedby = models.ForeignKey(User, on_delete=models.DO_NOTHING)





