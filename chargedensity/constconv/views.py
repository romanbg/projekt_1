from django.http import HttpResponse
from django.shortcuts import render
from .forms import Jana2006DocumentForm, CifForm, HydrogenForm, HklForm, StructureFactorForm
import re
import CifFile
from django.template.response import TemplateResponse
from django.views import View
import json
import math


def index(request):
        return TemplateResponse(request, 'constconv/index.html')


class StructureFactorView(View):

    def get(self, request):

        return TemplateResponse(request, 'constconv/structure_factor.html', {
            'form': StructureFactorForm()
        })

    def post(self, request):
        form = StructureFactorForm(data=request.POST)
        ctx = {'form':form}
        if form.is_valid():
            ref = form.cleaned_data['hkl_list']
            atom = form.cleaned_data['atoms_list']
            data_ref = json.loads(ref)
            data_atom = json.loads(atom)

            #ctx['result']= np.sum(np.cos(2. * np.pi * np.
                              #inner(ref, atom)), axis=1)
            F = []
            for j1 in range(len(data_ref)):
                s = 0
                for j2 in range(len(data_atom)):
                    c = 0
                    for i in range(3):
                        c += data_ref[j1][i] * data_atom[j2][i]
                        s += math.cos(2 * math.pi * c)
                F.append(s)
            ctx['result']=F

        return TemplateResponse(request, 'constconv/structure_factor.html', ctx)


def handle_uploaded_file(file):

    dict_one = {'P10':'D0',
                'P11+':'D1+',
                'P11-':'D1-',
                'P20':'Q0',
                'P21+':'Q1+',
                'P21-':'Q1-',
                'P22+':'Q2+',
                'P22-':'Q2-',
                'P30':'O0',
                'P31+':'O1+',
                'P31-':'O1-',
                'P32+':'O2+',
                'P32-':'O2-',
                'P33+':'O3+',
                'P33-':'O3-',
                'P40':'H0',
                'P41+':'H1+',
                'P41-':'H1-',
                'P42+':'H2+',
                'P42-':'H2-',
                'P43+':'H3+',
                'P43-':'H3-',
                'P44+':'H4+',
                'P44-':'H4-',
    }

    data = []
    data_two = []
    data_three =[]
    data_four =[]

    for line in file:
        line = line.decode('utf-8')
        #     import ipdb;ipdb.set_trace()
        search = re.search(r'^\((.*?)\) s',line)
        if search:
            text = search.group(1)
            if text == ' 'or text.startswith(' Symmetry') or text.startswith(' structure'):
                continue
            data.append(text)

    for line in data:
        start_part = 'CON      1 '
        line = start_part + line
        data_two.append(line)

    for line in data_two:
        for k, v in dict_one.items():
            line = line.replace(k, v)

        data_three.append(line)

    for line in data_three:

        line = re.sub(r'\[.*?\]', " ", line)
        data_four.append(line)

    return "\n".join(data_four)


def cif_handler(cif_file, pozycje_atomowe, stale_sieciowe, grupa_przestrzenna, dlugosc_fali):
    my_cif = CifFile.CifFile(cif_file)
    info_1 = my_cif.keys()
    info_2 = []

    if pozycje_atomowe:
        atom_positions = my_cif[info_1[2]].GetLoop('_atom_site_fract_x')
        for item in atom_positions:
            item = item[0:5]
            info_2.append(item)
        return info_2

    if stale_sieciowe:
        a_axis = my_cif[info_1[2]]['_cell_length_a']
        b_axis = my_cif[info_1[2]]['_cell_length_b']
        c_axis = my_cif[info_1[2]]['_cell_length_c']

        wynik = "stałe sieciowe: a={} , b={} , c={}".format(a_axis, b_axis, c_axis)

        return wynik

    if grupa_przestrzenna:
        crystal_system = my_cif[info_1[2]]['_space_group_crystal_system']
        space_group = my_cif[info_1[2]]['_space_group_name_H-M_alt']

        wynik = "układ krystalograficzny: {}; grupa przestrzenna: {}".format(crystal_system, space_group)
        return wynik


    if dlugosc_fali:
        pass


def cif(request):
    if request.method == 'POST':
        form = CifForm(request.POST, request.FILES)
        if form.is_valid():
            pozycje_atomowe = 'pozycje_atomowe' in request.POST
            stale_sieciowe = 'stale_sieciowe' in request.POST
            grupa_przetrzenna = 'grupa_przestrzenna' in request.POST
            dlugosc_fali = 'dlugosc_fali' in request.POST
            output = cif_handler(form.cleaned_data['cif_file'], pozycje_atomowe, stale_sieciowe, grupa_przetrzenna, dlugosc_fali)
            response = HttpResponse(content=output, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="cif_file.txt"'
            return response
    else:
        form = CifForm()
    return render(request, 'constconv/cif.html', {'form':form})



def hkl_handler(hkl_file):
    data = []
    for line in hkl_file:
        line = line.decode('utf-8')
        data.append(line)
    return "\n".join(data)

def hydrogens(cif_file):

    #out1 = open('capacity','w')
    #out2 = open('formulae','w')

    Molweights = {'H': 1.008, 'D': 1.008, 'He': 4.002, 'Li': 6.94, 'Be': 9.012, 'B': 10.81, 'C': 12.01,
                  'N': 14.01, 'O': 16.00, 'F': 19.00, 'Ne': 20.18, 'Na': 22.99, 'Mg': 24.31, 'Al': 26.98,
                  'Si': 28.09, 'P': 30.97, 'S': 32.06, 'Cl': 35.45, 'Ar': 39.95, 'K': 39.10, 'Ca': 40.08, 'Sc': 44.96,
                  'Ti': 47.87, 'V': 50.94, 'Cr': 52.00, 'Mn': 54.94, 'Fe': 55.85, 'Co': 58.93, 'Ni': 58.69,
                  'Cu': 63.55, 'Zn': 65.38, 'Ga': 69.72, 'Ge': 72.63, 'As': 74.92, 'Se': 78.97, 'Br': 79.90,
                  'Kr': 83.80, 'Rb': 85.47, 'Sr': 87.62, 'Y': 88.91, 'Zr': 91.22, 'Nb': 92.11, 'Mo': 95.95,
                  'Tc': 97.91, 'Ru': 101.07, 'Rh': 102.91, 'Pd': 106.42, 'Ag': 107.87, 'Cd': 112.41, 'In': 114.82,
                  'Sn': 118.71, 'Sb': 121.76, 'Te': 127.60, 'I': 126.90, 'Xe': 131.29, 'Cs': 132.91, 'Ba': 137.33,
                  'La': 138.91, 'Ce': 140.12, 'Pr': 140.91, 'Nd': 144.24, 'Pm': 144.91, 'Sm': 150.36,
                  'Eu': 151.96, 'Gd': 157.25, 'Tb': 158.93, 'Dy': 162.50, 'Ho': 164.93, 'Er': 167.26,
                  'Tm': 168.93, 'Yb': 173.05, 'Lu': 174.97, 'Hf': 178.49, 'Ta': 180.95, 'W': 183.84,
                  'Re': 186.21, 'Os': 190.23, 'Ir': 192.22, 'Pt': 195.08, 'Au': 196.97, 'Hg': 200.59, 'Tl': 204.38,
                  'Pb': 207.2, 'Bi': 208.98, 'Po': 208.98, 'At': 209.99, 'Rn': 222.02, 'Ac': 227.03, 'Th': 232.04,
                  'Pa': 231.04, 'U': 238.03, 'Np': 237.05, 'Pu': 244.06, 'Am': 243.06, 'Cm': 247.07,
                  'Bk': 247.07, 'Cf': 251.08}

    for line in cif_file:
        try:
            if line[-5:-1] != '.cif':
                continue
            Molweight = 0
            Name = line
            try:
                cif = CifFile.ReadCif(Name)
            except:
                continue
            block = re.findall(r'\d+',line)
            print (block[-1])
            datablock = block[-1]

            try:
                CSDnumber = cif[datablock]['_database_code_depnum_ccdc_archive']
                SumFormula = cif[datablock]['_chemical_formula_sum']
                Density = cif[datablock]['_exptl_crystal_density_diffrn']
            except:
                continue
            if Density == '?':
                continue
            SumFormula.replace('\n','').replace('\r','')
            elem = re.findall(r'[a-zA-Z]+',SumFormula)
            boolean = 'H' in elem or 'D' in elem
            if boolean == False:
                continue

            elements = re.findall(r'[a-zA-Z0-9.]+',SumFormula)

            for item in elements:
                elementscount = re.findall(r'[0-9]+',item)[0]
                numbi = elements.index(item)
                element = re.findall(r'[a-zA-Z]+',item)[0]
                elements[numbi] = element
                if not elementscount:
                    elementscount.append(1)
                if element == 'H' or element == 'D':
                    Hcount = elementscount[0]
                boolean = element in Molweights
                if boolean == False:
                    continue
                Molweight = Molweight + Molweights[element]*float(elementscount[0])
            gravcapacity = float(Hcount)*1.008*1000/Molweight
            Dens = re.findall(r'[0-9.]+', Density)
            volcapacity = gravcapacity*float(Dens[0])
            print1 = str(CSDnumber)+''+str(gravcapacity)+''+str(volcapacity)+'\n'
            #out1.write(print1)
            print2 = str(CSDnumber)+'+'+str(SumFormula)+'+\n'
            #out2.write(print2)

        except:
            continue

        return print1 + print2

def upload_file(request):
    if request.method == 'POST':
        form = Jana2006DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            output = handle_uploaded_file(form.cleaned_data['file'])
            response = HttpResponse(content=output, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="newfile.txt"'
            return response
    else:
        form = Jana2006DocumentForm()
    return render(request, 'constconv/upload.html', {'form':form})





def hydrogen(request):
    if request.method == 'POST':
        form = HydrogenForm(request.POST, request.FILES)
        if form.is_valid():
            output = cif_handler(form.cleaned_data['hydrogen_file'])
            response = HttpResponse(content=output, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="hydrogen_file.txt"'
            return response
    else:
        form = CifForm()
    return render(request, 'constconv/hydrogen.html', {'form':form})

def hkl(request):
    if request.method == 'POST':
        form = HklForm(request.POST, request.FILES)
        if form.is_valid():
            output = hkl_handler(form.cleaned_data['hkl_file'])
            response = HttpResponse(content=output, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="hkl_file.txt"'
            return response
    else:
        form = HklForm()
    return render(request, 'constconv/hkl.html', {'form':form})