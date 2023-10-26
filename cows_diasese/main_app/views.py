from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# mensagens nos templates
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .models import Consulta

from .forms import UserForm
from django.forms.widgets import HiddenInput

import os

""" KERAS """
from PIL import Image
from keras.models import load_model
from flask import Flask, render_template, request, send_file
from keras.utils import load_img, img_to_array

# Create your views here.

# Dicionário de doenças com números como chaves e descrições
doencas = {
    0: {
        'nome': 'Ceratoconjuntivite Infecciosa Bovina',
        'descricao': 'A asma é uma doença crônica das vias respiratórias que pode causar dificuldade para respirar, chiado no peito e tosse.',
        'factor_risco': [
            'História familiar de asma',
            'Exposição a alérgenos ambientais',
            'Fumo passivo durante a infância',
            'Infecções respiratórias frequentes durante a infância'
        ],
        'tratamento': [
            'Inalador',
            'Mepolizumabe',
            'itraconazol',
            'Omalizumabe',
            'Corticosteroides inalados para controle a longo prazo',
            'Evitar gatilhos da asma, como alérgenos e poluentes do ar'
        ]
    },
    1: {
        'nome': 'Doença de Casco Bovina',
        'descricao': 'A bronquiectasia é uma condição em que as vias aéreas dos pulmões se dilatam e se tornam inflamadas, levando a infecções frequentes.',
        'factor_risco': [
            'Infecções respiratórias recorrentes',
            'Fibrose cística',
            'Síndrome de imunodeficiência',
            'Exposição a substâncias irritantes no local de trabalho'
        ],
        'tratamento': [
            'Antibióticos',
            'Solução Salina Hipertônica',
            'Ventilação Percussiva Intrapulmonar',
            'Fisioterapia respiratória',
            'Controle de muco com medicamentos'
        ]
    },
    2: {
        'nome': 'Febre Aftosa',
        'descricao': 'A bronquiolite é uma infecção respiratória comum em bebês e crianças pequenas, causada frequentemente pelo Vírus Sincicial Respiratório (VSR).',
        'factor_risco': [
            'Infecção pelo vírus sincicial respiratório (VSR), comum em bebês e crianças pequenas'
        ],
        'tratamento': [
            'Inalador',
            'Consultar um médico especialista',
            'Gotas Salinas no Nariz',
            'Tratamento de suporte para bebês, incluindo oxigenoterapia e hidratação'
        ]
    },
    3: {
        'nome': 'Doença da Pele Grumosa',
        'descricao': 'A bronquite é a inflamação das vias aéreas principais (brônquios) dos pulmões, geralmente causada por infecções virais ou bacterianas.',
        'factor_risco': [
            'Tabagismo activo e passivo',
            'Exposição a poluentes do ar',
            'Exposição a irritantes químicos no ambiente de trabalho'
        ],
        'tratamento': [
            'Antibióticos se a causa for bacteriana',
            'Repouso',
            'Hidratação',
            'Medicamentos para aliviar sintomas, como antitussígenos e analgésicos'
        ]
    },
    4: {
        'nome': 'Olhos Saudáveis',
        'descricao': 'A bronquite crônica é uma forma de doença pulmonar obstrutiva crônica (DPOC) caracterizada por tosse crônica e produção excessiva de muco.',
        'factor_risco': [
            'Tabagismo activo e passivo',
            'Exposição a poluentes do ar',
            'Exposição a irritantes químicos no ambiente de trabalho'
        ],
        'tratamento': [
            'Oxigênio',
            'Inalador',
            'Raio-X',
            'Esteroides para reduzir a inflamação',
            'Medicamentos broncodilatadores',
            'Parar de fumar e evitar irritantes'
        ]
    },
    5: {
        'nome': 'Cascos Saudáveis',
        'descricao': 'A DPOC é uma doença pulmonar progressiva que dificulta a respiração devido a danos nos pulmões.',
        'factor_risco': [
            'Tabagismo é o principal factor de risco',
            'Exposição a poluição do ar',
            'Exposição ocupacional a poeira e produtos químicos'
        ],
        'tratamento': [
            'Oxigênio',
            'Reabilitação Pulmonar',
            'Consultar um médico especialista',
            'Inalador',
            'Cirurgia',
            'Broncodilatadores',
            'Parar de fumar e evitar irritantes'
        ]
    },
    6: {
        'nome': 'Sem Febre Aftosa',
        'descricao': 'O mesotelioma é um tipo raro de câncer que afecta o revestimento dos órgãos internos, como os pulmões e o coração.',
        'factor_risco': [
            'Exposição ao amianto (asbestos) é o fator de risco mais importante',
            'Exposição ocupacional em indústrias que utilizam amianto'
        ],
        'tratamento': [
            'Tratamento varia com base no estágio, mas pode incluir cirurgia, radioterapia e quimioterapia',
            'Consultar um médico especialista',
        ]
    },
    7: {
        'nome': 'Pele Saudável',
        'descricao': 'A pneumonia é uma infecção dos pulmões que causa sintomas como febre, tosse e dificuldade para respirar.',
        'factor_risco': [
            'Infecção por bactérias, vírus ou fungos',
            'Sistema imunológico enfraquecido',
            'Idade avançada',
            'Tabagismo crônico'
        ],
        'tratamento': [
            'Aspirina',
            'Antibióticos (se a causa for bacteriana)',
            'Repouso',
            'Hidratação',
            'Medicamento para tosse',
            'Medicamentos para febre e dor',
            'Hospitalização em casos graves'
        ]
    },
}


def login_view(request):
    if request.method == "POST":
        # Tentar login
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # verficar se o usuario foi autenticdo com sucesso
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auth/login.html", {
                "message": "Email ou Passowrd inválida."
            })
    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required(login_url='/login')
def index(request):
    return render(request, "system/index.html")


@login_required(login_url='/login')
def profile(request):
    user = request.user
    numConsultas = 0

    if user.consultas.all().count() > 0:
        numConsultas = user.consultas.all().count()

    return render(request, "user/profile.html", {'numConsultas': numConsultas})


@login_required(login_url='/login')
def update_profile(request):
    user = request.user
    form = UserForm(initial={'first_name': user.first_name,
                    'last_name': user.last_name, 'email': user.email})

    if request.method == "POST":

        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            try:
                form.save()
                model = form.instance

                messages.success(request, 'Usuário actualizado com sucesso!')
                return redirect('/profile')

            except Exception as e:
                messages.error(request, 'Algo ocorreu mal\nErro: {}'.format(e))
                return redirect('/profile')
    return render(request, "user/edit-profile.html", {'form': form})

# metodo de pesquisa


@login_required(login_url='/login')
def search_view(request):
    query = request.GET.get('q')

    user = request.user
    consultas = user.consultas.all()

    results = consultas.filter(raca__icontains=query)
    resultTotal = results.count()

    return render(request, "system/search-results.html", {'results': results, 'resultTotal': resultTotal})


""" Extensões permitidas """
ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

"""CONSULTAS"""
@login_required(login_url='/login')
def consultas(request):
    if request.method == "GET":
        try:
            veterinario = request.user
            consultas = Consulta.objects.filter(veterinario_id=veterinario)

            """ # paginacao de 5 elementos por paginas
            paginator = Paginator(consultas, 5)
            page_number = request.GET.get("page")
            pag_obj = paginator.get_page(page_number)

            context_consultas = {'consultas': consultas, 'page_obj': pag_obj} """

        except Exception as e:
            return render(request, "system/consulta-list.html", {
                "error_message": "Não possivel carregar os dados.\nErro: {}".format(e)
            })
    return render(request, "system/consulta-list.html", {'consultas': consultas})

@login_required(login_url='/login')
def consultaCreate(request, paciente):
    if request.method == 'POST':

        # obter dados do formulario
        raca = request.POST.get("raca")
        imagem = request.POST.get("imagem")

        # carregar a imagem com as devidas dimensoes
        img = load_img(imagem, target_size=(150, 150))
        # transformar a imagem em array
        img = img_to_array(img)
        # redimencionar a imagem
        img = img.reshape(1, 150, 150, 3)

        # transformar o array sob forma de imagens em float
        img = img.astype('float32')
        img = img/255.0

        # Carregar o modelo treinado
        model = load_model('main_app/static/model/cow-diseases-20-epochs-mobilenet.h5')
        # classificar a imagem
        result = model.predict(img)
        print(result[0])


        # traduzir o nome da doenca
        """ doenca_nome = doencas[prediction]["nome"]

        print("Doenca: ", doenca_nome, " prob: ",
              prob, "pos: ", prediction)

        # customizar o status de acordo com as probalidade
        status = None
        if prob >= 0 and prob <= 33:
            status = "Baixa"
        elif prob >= 34 and prob <= 66:
            status = "Moderado"
        else:
            status = "Muito Grave"

        #GUARDAR PREVISAO NA BASE DE DADOS

        consulta = Consulta.objects.create(
            veterinario=request.user, raca=raca, imagem=imagem, doenca=doenca_nome,
            probabilidade=round(100, 2), status=status) """

        messages.success(request, 'Previsão Efectuado com Sucesso')

        return redirect('consultas')
        #return redirect('/consulta-details/{}'.format(consulta.id))

    return render(request, 'system/consulta-create.html')


@login_required(login_url='/login')
def consultaDetails(request, paciente, idConsulta):
    consulta = Consulta.objects.get(id=idConsulta)

    if request.method == 'POST':
        prescricao = request.POST.get("prescricao")
        consultaResult = Consulta.objects.filter(id=idConsulta)
        consultaResult.update(prescricao=prescricao)

        messages.success(request, 'Obversão inserida com sucesso!')

        return redirect('/consulta-details/{}'.format(consulta.id))

    # se a requisicao for GET, faca:
    posicao_doenca = encontrar_chave_valor(doencas, consulta.doenca)

    descricao = doencas[posicao_doenca]['descricao']
    factores = doencas[posicao_doenca]['factor_risco']
    tratamentos = doencas[posicao_doenca]['tratamento']

    return render(request, 'system/consulta-detalhe.html', {"consulta": consulta,
                                                            "descricao": descricao, "factores": factores, "tratamentos": tratamentos})


@login_required(login_url='/login')
def consultaDelete(request, idConsulta):
    consulta = Consulta.objects.get(id=idConsulta)
    try:
        consulta.delete()
    except Exception as e:
        return redirect('consultas', {'error_message': 'Algo ocorreu mal\nErro: {}'.format(e)})

    messages.success(request, 'Consulta excluída com sucesso!')

    return redirect('consultas')


# metodo auxiliar
def encontrar_chave_valor(dicionario, valor_procurado):
    for chave, valor in dicionario.items():
        if valor.get('nome') == valor_procurado:
            return chave
    return None
