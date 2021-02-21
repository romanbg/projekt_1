from django import forms
from constconv.models import HklDocument

class Jana2006DocumentForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField(label="Select a file with constrains to convert")

class CifForm(forms.Form):
    # title = forms.CharField(max_length=50)
    cif_file = forms.FileField(label="Upload a CIF file")

class HydrogenForm(forms.Form):
    hydrogen_file = forms.FileField(label='Upload a CIF file')

class HklForm(forms.Form):
    hkl_file = forms.FileField(label="Upload a HKL file")

class HklDocumentForm(forms.ModelForm):
    class Meta:
        model = HklDocument
        fields = forms.ALL_FIELDS

class StructureFactorForm(forms.Form):
    hkl_list = forms.CharField(max_length=364, label='Insert list of HKL')
    atoms_list = forms.CharField(max_length=364, label='Insert list of atomic positions')