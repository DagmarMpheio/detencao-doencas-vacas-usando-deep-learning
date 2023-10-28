from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# mensagens nos templates
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .models import Consulta, User

from .forms import UserForm
from django.forms.widgets import HiddenInput

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

""" KERAS """
from PIL import Image
from keras.models import load_model
from flask import Flask, render_template, request, send_file
from keras.utils import load_img, img_to_array

import numpy as np
from io import BytesIO

# para graficos
from collections import Counter
from django.db.models.functions import TruncMonth
from django.db.models import Count
import json
import random
from datetime import datetime

# Create your views here.

# Dicionário de doenças com números como chaves e descrições
doencas = {
    0: {
        'nome': 'Ceratoconjuntivite Infecciosa Bovina',
        'descricao': 'A Ceratoconjuntivite Infecciosa Bovina (CIB), também conhecida como "olho rosa" ou "olho de água" em bovinos, é uma doença ocular infecciosa que afeta o gado, em particular bovinos, causando inflamação da córnea e da conjuntiva. A conjuntiva é a membrana mucosa fina que cobre a parte branca do olho e a parte interna das pálpebras.',
        'sintomas': [
            'Olhos lacrimejantes (epífora)',
            'Inchaço e vermelhidão da conjuntiva',
            'Descarga ocular purulenta',
            'Fotofobia (sensibilidade à luz)',
            'Ulceração da córnea, que pode levar a lesões graves e perda de visão se não for tratada adequadamente',
        ],
        'factor_risco': [
            'Superlotação: Manter bovinos em espaços confinados e superlotados aumenta o contato próximo entre os animais, facilitando a disseminação da infecção',
            'Condições de higiene inadequadas: A falta de limpeza nas instalações do rebanho e a água suja ou contaminada podem contribuir para a propagação da doença',
            'Estresse ambiental: Ambientes estressantes, como exposição excessiva à luz solar, poeira, vento forte ou variações climáticas extremas, podem tornar os olhos dos bovinos mais suscetíveis à infecção',
            'Moscas e outros insetos: Moscas e outros insetos podem transmitir a bactéria Moraxella bovis de um animal infectado para outro, o que aumenta o risco de propagação da doença',
            'Falta de vacinação: A vacinação contra a CIB é uma medida eficaz de prevenção. A falta de vacinação ou a não adesão a programas de vacinação adequados aumentam o risco de surtos da doença',
            'Raça e genética: Alguns bovinos podem ser geneticamente mais suscetíveis à CIB do que outros. Além disso, raças com características faciais distintas, como olhos proeminentes, podem ser mais vulneráveis',
            'Idade dos animais: Bezerros e animais jovens são mais suscetíveis à CIB do que os animais mais velhos, uma vez que podem ter menos imunidade natural',
            'Introdução de animais infectados: A introdução de bovinos infectados em um rebanho saudável é uma forma comum de disseminação da CIB',
            'Falta de manejo sanitário adequado: Práticas inadequadas de manejo, como a falta de isolamento de animais doentes, podem permitir que a infecção se espalhe rapidamente',
            'Outras condições de saúde subjacentes: Bovinos com outras condições de saúde, como conjuntivite não infecciosa, podem ser mais vulneráveis à CIB',
        ],
        'tratamento': [
            'Antibióticos: O tratamento com antibióticos é uma parte fundamental do controle da CIB. Antibióticos tópicos, como pomadas ou colírios, são aplicados diretamente nos olhos afetados para combater a infecção bacteriana. A escolha do antibiótico dependerá da susceptibilidade do agente causador (geralmente Moraxella bovis) à medicação. A aplicação dos antibióticos deve ser realizada de acordo com a prescrição do veterinário',
            'Anti-inflamatórios: Em casos graves de CIB, pode ser necessário administrar anti-inflamatórios para reduzir a inflamação ocular e aliviar o desconforto do animal',
            'Proteção dos olhos: Em casos avançados, pode ser necessário proteger os olhos dos bovinos do ambiente, luz solar intensa e poeira, o que pode agravar a condição. Isso pode ser feito com o uso de óculos de proteção ocular',
            'Isolamento e separação de animais doentes: Para evitar a propagação da doença para outros animais no rebanho, os bovinos afetados devem ser isolados dos animais saudáveis até que estejam recuperados',
            'Vacinação: Embora a vacinação não seja uma forma de tratamento direto, ela desempenha um papel importante na prevenção da CIB. A vacinação regular pode ser recomendada como parte das medidas de controle em rebanhos com histórico da doença',
            'Manejo ambiental: Melhorar as condições de higiene nas instalações do rebanho, reduzir o estresse ambiental (como superlotação e exposição a condições climáticas extremas) e controlar insetos que podem transmitir a bactéria Moraxella bovis são medidas importantes para prevenir surtos de CIB',
            'Monitoramento: É importante que um veterinário acompanhe de perto a progressão do tratamento e faça ajustes conforme necessário. A recuperação pode levar semanas, e o acompanhamento regular é fundamental',
        ]
    },
    1: {
        'nome': 'Doença de Casco Bovina',
        'descricao': 'A Doença de Casco Bovina, também conhecida como laminite ou pododermatite, é uma condição de saúde que afeta os cascos dos bovinos, causando dor e claudicação. Ela é mais comum em bovinos leiteiros, mas pode ocorrer em bovinos de corte e outros tipos de gado. A doença envolve inflamação e danos nas estruturas internas do casco, incluindo o laminar, a sola e a parede do casco.',
        'sintomas': [
            'Claudicação',
            'Dificuldade em caminhar',
            'Sensibilidade ao toque na região do casco e possível deformação dos cascos',
            'Em casos graves, os bovinos podem não ser capazes de se levantar',
        ],
        'factor_risco': [
            'Alimentação inadequada: Uma dieta desequilibrada, com excesso de grãos ou outros alimentos de alto teor energético, pode aumentar o risco de laminite em bovinos',
            'Obesidade: Bovinos obesos têm maior probabilidade de desenvolver laminite, já que o excesso de peso coloca mais pressão sobre os cascos',
            'Excesso de consumo de carboidratos: O consumo excessivo de carboidratos, especialmente aqueles rapidamente fermentáveis, pode levar à acidose ruminal, o que pode contribuir para a laminite',
            'Estresse físico: Ficar de pé por longos períodos em superfícies duras e desconfortáveis, como concreto, pode aumentar a pressão sobre os cascos e contribuir para a laminite',
            'Infecções: Infecções bacterianas ou fúngicas nos cascos podem causar inflamação e contribuir para a doença',
        ],
        'tratamento': [
            'Manejo nutricional Ajustes na dieta para evitar o excesso de carboidratos ou energia, bem como o controle do consumo de grãos, são comuns',
            'Medicação O tratamento com anti-inflamatórios e analgésicos pode ser prescrito para aliviar a dor e a inflamação',
            'Cuidados com os cascos É importante manter os cascos limpos e bem cuidados. Isso pode incluir a limpeza regular dos cascos e, em alguns casos, o uso de talas especiais',
            'Alívio do estresse Fornecer áreas de descanso macias e evitar a sobrecarga nos cascos dos bovinos é importante para a recuperação',
        ]
    },
    2: {
        'nome': 'Febre Aftosa',
        'descricao': 'A Febre Aftosa é uma doença viral altamente contagiosa que afeta principalmente os animais de casco fendido, como bovinos, ovinos, suínos e cervídeos, bem como outros animais ungulados. A doença é causada pelo vírus da Febre Aftosa, que pertence à família Picornaviridae.',
        'sintomas': [
            'Febre',
            'Salivação excessiva,',
            'Lesões vesiculares na boca, cascos e tetos',
            'Claudicação (dificuldade de locomoção)',
            'Perda de apetite',
            'Diminuição na produção de leite ou ganho de peso',
        ],
        'factor_risco': [
            'Movimentação de animais: O transporte de animais entre fazendas, regiões ou países pode facilitar a propagação da doença. Movimentar animais de áreas onde a Febre Aftosa é endêmica para áreas onde a doença está controlada é particularmente arriscado',
            'Falta de vacinação: A não vacinação de rebanhos suscetíveis contra a Febre Aftosa deixa os animais vulneráveis à infecção. A vacinação adequada é uma medida fundamental para prevenir a doença',
            'Introdução de animais infectados: A introdução de animais infectados em rebanhos saudáveis pode ser uma fonte significativa de propagação da doença',
            'Contato com animais selvagens: Aproximação de animais selvagens, que podem carregar o vírus da Febre Aftosa, aumenta o risco de exposição aos animais de criação',
            'Condições de manejo inadequadas: Práticas de manejo de animais que não seguem boas práticas de biossegurança, como a falta de quarentena para animais recém-chegados, higiene inadequada e acesso irrestrito a estranhos em fazendas, podem aumentar o risco de infecção',
            'Comércio internacional de animais e produtos: O comércio de animais, carne, leite e outros produtos de origem animal entre países pode ser um veículo de propagação do vírus da Febre Aftosa se medidas de controle rigorosas não forem implementadas',
            'Falta de detecção precoce: A ausência de sistemas de vigilância eficazes para detectar casos precoces de Febre Aftosa pode resultar em atrasos na resposta e na disseminação da doença',
            'Proximidade geográfica a áreas endêmicas: A localização geográfica de uma fazenda em relação a áreas onde a Febre Aftosa é endêmica ou onde ocorrem surtos pode aumentar o risco de introdução da doença',
            'Falta de conscientização e educação: A falta de conscientização e educação dos agricultores, trabalhadores de fazendas e profissionais do setor pecuário sobre a Febre Aftosa e suas medidas de prevenção pode levar a práticas de manejo inadequadas',
            'Condições climáticas e ambientais: As condições climáticas, como ventos fortes, chuvas e inundações, podem desempenhar um papel na disseminação do vírus, pois podem transportar o vírus para áreas distantes',
        ],
        'tratamento': [
            'Vacinação A vacinação dos rebanhos é uma estratégia fundamental para prevenir a Febre Aftosa. Os animais são vacinados regularmente para criar imunidade e proteger contra a infecção',
            'Controle de movimentação de animais:** Restrições são frequentemente colocadas na movimentação de animais de regiões onde a Febre Aftosa é endêmica ou onde ocorrem surtos',
            'Higiene e biossegurança Boas práticas de manejo, como manter instalações limpas e evitar a entrada de visitantes não autorizados em fazendas, ajudam a reduzir o risco de introdução da doença',
            'Detecção precoce e relato Identificar casos suspeitos e relatar imediatamente às autoridades veterinárias é essencial para conter surtos',
            'Quarentena Animais suspeitos de estarem infectados devem ser isolados e submetidos a quarentena até que a presença da doença seja confirmada ou descartada',
        ]
    },
    3: {
        'nome': 'Doença da Pele Grumosa',
        'descricao': 'A "Doença da Pele Grumosa" (Lumpy Skin Disease, em inglês) é uma doença viral específica que afeta o gado bovino e se caracteriza pela formação de nódulos ou caroços na pele. Ela é causada por um poxvírus conhecido como "Vírus da Doença da Pele Grumosa" (Lumpy Skin Disease Virus, ou LSDV, em inglês). Essa doença afeta principalmente o gado, mas também pode infectar búfalos d\'água e outras espécies relacionadas.',
        'sintomas': [
            'Nódulos na Pele: A característica mais marcante da Doença da Pele Grumosa é o desenvolvimento de nódulos ou caroços na pele. Esses nódulos podem variar em tamanho e são tipicamente firmes e indolores',
            'Febre: Bovinos infectados podem desenvolver febre alta',
            'Perda de Apetite: Bovinos com a Doença da Pele Grumosa podem apresentar redução no apetite e menor consumo de alimentos',
            'Redução na Produção de Leite: Em bovinos leiteiros, a produção de leite pode diminuir',
            'Depressão: Os animais infectados podem parecer letárgicos ou deprimidos',
        ],
        'factor_risco': [
            'Movimentação de animais: O transporte de bovinos entre fazendas, regiões ou países pode facilitar a propagação da doença. Movimentar animais de áreas onde a Doença da Pele Grumosa é endêmica para áreas onde a doença está controlada é particularmente arriscado',
            'Falta de vacinação: A não vacinação de rebanhos suscetíveis contra a Doença da Pele Grumosa deixa os animais vulneráveis à infecção. A vacinação adequada é uma medida fundamental para prevenir a doença',
            'Introdução de animais infectados: A introdução de bovinos infectados em rebanhos saudáveis pode ser uma fonte significativa de propagação da doença',
            'Contato com vetores de insetos: A presença de insetos vetores da doença, como moscas picadoras e mosquitos, pode aumentar o risco de transmissão da Doença da Pele Grumosa',
            'Proximidade geográfica a áreas endêmicas: A localização geográfica de uma fazenda em relação a áreas onde a Doença da Pele Grumosa é endêmica ou onde ocorrem surtos pode aumentar o risco de introdução da doença',
            'Movimentação de equipamentos contaminados: Equipamentos agrícolas ou de transporte que estiveram em contato com animais infectados podem transportar o vírus para novas áreas',
            'Falta de conscientização e educação: A falta de conscientização e educação dos agricultores, trabalhadores de fazendas e profissionais do setor pecuário sobre a Doença da Pele Grumosa e suas medidas de prevenção pode levar a práticas de manejo inadequadas',
            'Falta de medidas de controle: A ausência de medidas de controle adequadas, como quarentena de animais recém-chegados, pode permitir a propagação da doença',
        ],
        'tratamento': [
            'Quarentena: Isolamento de bovinos infectados para evitar a propagação da doença',
            'Controle de Insetos: Redução das populações de insetos por meio do uso de inseticidas ou outros métodos de controle',
            'Vacinação: A vacinação é uma ferramenta importante para o controle da Doença da Pele Grumosa em áreas endêmicas',
            'Higiene Rigorosa: Manter boas práticas de higiene e desinfecção na fazenda',
            'Monitoramento: Monitoramento regular e notificação de casos suspeitos às autoridades veterinárias',
        ]
    },
    4: {
        'nome': 'Olhos Saudáveis',
        'descricao': 'Este gado não possui Ceratoconjuntivite Infecciosa Bovina (CIB). Portanto, é fundamental monitorar a saúde ocular do gado e adotar práticas de manejo adequadas para prevenir a propagação dessa doença infecciosa.',
        'sintomas': [
        ],
        'factor_risco': [
        ],
        'tratamento': [
            'A prevenção e o tratamento da CIB envolvem medidas de manejo sanitário e o uso de antibióticos tópicos para tratar as infecções oculares. Além disso, a vacinação pode ser usada como parte das estratégias de controle em rebanhos com histórico recorrente da doença.',
        ]
    },
    5: {
        'nome': 'Cascos Saudáveis',
        'descricao': 'Este gado não possui a doença dos cascos. Portanto, é fundamental monitorar a saúde do mesmo.',
        'sintomas': [
        ],
        'factor_risco': [
        ],
        'tratamento': [
            'A prevenção é fundamental na Doença de Casco Bovina e envolve a implementação de boas práticas de manejo, controle da dieta e monitoramento constante da saúde dos cascos do gado. Manter um ambiente limpo e seguro para os bovinos também é crucial para evitar essa condição dolorosa.',
        ]
    },
    6: {
        'nome': 'Sem Febre Aftosa',
        'descricao': 'Este gado não possui a febre aftosa. Portanto, é fundamental monitorar a saúde do mesmo, implementar medidas rigorosas de controle e biossegurança, incluindo a vacinação regular dos rebanhos, quarentena de animais recém-chegados, controle de movimentação de animais e vigilância ativa. A conscientização, educação e cooperação internacional também desempenham um papel crucial na prevenção da doença. É importante observar que a Febre Aftosa é uma doença sujeita a notificação obrigatória às autoridades veterinárias em muitos países para permitir a resposta rápida e eficaz a qualquer surto.',
        'sintomas': [
        ],
        'factor_risco': [
        ],
        'tratamento': [
            'A Febre Aftosa é uma preocupação significativa para a indústria pecuária, uma vez que pode causar grandes perdas econômicas, devido à redução na produção e às medidas de controle, como a eliminação de animais infectados e a vacinação em massa.',
        ]
    },
    7: {
        'nome': 'Pele Saudável',
        'descricao': 'Este gado não possui a doença da pele grumosa. Portanto, é fundamental monitorar a saúde do mesmo, implementar medidas rigorosas de controle e biossegurança, incluindo a vacinação regular dos rebanhos, quarentena de animais recém-chegados, controle de insetos vetores e vigilância ativa. A conscientização, educação e cooperação internacional também desempenham um papel crucial na prevenção da doença. É importante observar que a Doença da Pele Grumosa é uma doença sujeita a notificação obrigatória às autoridades veterinárias em muitos países para permitir a resposta rápida e eficaz a qualquer surto.',
        'sintomas': [
        ],
        'factor_risco': [
        ],
        'tratamento': [
            'A Doença da Pele Grumosa pode ter impactos econômicos significativos devido à redução na produção de leite, ganho de peso reduzido e restrições comerciais sobre o gado afetado e produtos derivados. Portanto, a detecção precoce e o manejo adequado são cruciais em regiões onde a doença está presente. Veterinários e autoridades de saúde animal locais devem estar envolvidos no diagnóstico, controle e prevenção de surtos de Doença da Pele Grumosa.',
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
def consultaCreate(request):
    if request.method == 'POST':

        # obter dados do formulario
        raca = request.POST.get("raca")
        # Obter a imagem como BytesIO
        imagem = request.FILES.get('imagem')
        if imagem:
            image_data = BytesIO(imagem.read())
            print(f"Imagem recebida com sucesso.")
            # Resto do código...
        else:
            print("Nenhuma imagem recebida no formulário.")

        print(f"raca {raca}")
        print(f"imagem {imagem}")

        # Caminho para a pasta onde você deseja copiar a imagem
        destino = os.path.join(settings.STATIC_ROOT, 'static', 'detencao-img')

        # Verifique se a pasta de destino existe, caso contrário, crie-a
        if not os.path.exists(destino):
            os.makedirs(destino)

        # Crie um sistema de arquivos para lidar com o armazenamento da imagem
        fs = FileSystemStorage(location=destino)

        # Salve a imagem no sistema de arquivos
        fs.save(imagem.name, imagem)

        # carregar a imagem com as devidas dimensoes
        img = load_img(image_data, target_size=(150, 150))
        # transformar a imagem em array
        img = img_to_array(img)
        # redimencionar a imagem
        img = img.reshape(1, 150, 150, 3)

        # transformar o array sob forma de imagens em float
        img = img.astype('float32')
        img = img/255.0

        # Carregar o modelo treinado
        model = load_model(
            'main_app/static/model/cow-diseases-20-epochs-mobilenet.h5')
        # classificar a imagem
        result = model.predict(img)
        # Obter o índice da classe com maior probabilidade
        prediction = np.argmax(result)
        # Obter a probabilidade da classe predita
        prob = result[0][prediction]
        prob = prob*100

        image_data.close()

        # nome da doenca
        doenca_nome = doencas[prediction]["nome"]

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

        # GUARDAR PREVISAO NA BASE DE DADOS

        consulta = Consulta.objects.create(
            veterinario=request.user, raca=raca, imagem=imagem, doenca=doenca_nome,
            probabilidade=round(prob, 2), status=status)

        messages.success(request, 'Previsão Efectuado com Sucesso')

        # return redirect('consultas')
        return redirect('/consulta-details/{}'.format(consulta.id))

    return render(request, 'system/consulta-create.html')


@login_required(login_url='/login')
def consultaDetails(request, idConsulta):
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
    sintomas = doencas[posicao_doenca]['sintomas']
    factores = doencas[posicao_doenca]['factor_risco']
    tratamentos = doencas[posicao_doenca]['tratamento']

    return render(request, 'system/consulta-detalhe.html', {"consulta": consulta,
                                                            "descricao": descricao, "sintomas": sintomas, "factores": factores, "tratamentos": tratamentos})


@login_required(login_url='/login')
def consultaDelete(request, idConsulta):
    consulta = Consulta.objects.get(id=idConsulta)
    try:
        consulta.delete()
    except Exception as e:
        return redirect('consultas', {'error_message': 'Algo ocorreu mal\nErro: {}'.format(e)})

    messages.success(request, 'Consulta excluída com sucesso!')

    return redirect('consultas')


# relatorio graficos
@login_required(login_url='/login')
def reports(request):
    # Obter os dados das consultas
    veterinario = request.user
    consultas = Consulta.objects.filter(veterinario_id=veterinario)

    """ Gráfico de Quantidade de Detenções por Raça """
    # Extrair as raças das consultas
    racas = [consulta.raca for consulta in consultas]

    # Contar a quantidade de detenções por raça
    contador_racas = Counter(racas)

    # Separar as raças e contagens
    racas = list(contador_racas.keys())
    quantidades = list(contador_racas.values())

    # Crie uma lista de datasets com rótulos e dados correspondentes
    datasets = []

    for i, raca in enumerate(racas):
        #cores
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        alpha_point = 0.2  # Valor de alfa para pointBackgroundColor
        alpha_legend = 0.1  # Valor de alfa para backgroundColor
        cor = cor_aleatoria()
        
        dataset = {
            'label': f'{raca}',
            'borderColor': cor,  # Cor do gráfico
            'pointBackgroundColor': cor_aleatoria_rgba(r, g, b, alpha_point),
            'pointRadius': 0,
            'backgroundColor': cor_aleatoria_rgba(r, g, b, alpha_legend),
            'legendColor': cor,
            'fill': True,
            'borderWidth': 2,
            'data': quantidades  # Usar o valor correspondente à raça
        }
        datasets.append(dataset)

    # Converter a lista de datasets em uma string JSON para ser usada no JavaScript
    datasets_json = json.dumps(datasets)

    """ Gráfico de Quantidade de Detecções por Mês """
    # Anotar a data das consultas por mês
    consultas_mes = consultas.annotate(month=TruncMonth('created_at'))

    # Conte a quantidade de detenções por mês
    contador_meses = consultas_mes.values('month').annotate(count=Count('id'))

    # Separar os meses e contagens
    meses = [str(entry['month'].strftime('%Y-%m')) for entry in contador_meses]

    nomes_meses = [datetime.strptime(mes, '%Y-%m').strftime('%b') for mes in meses]

    quantidades_meses = [entry['count'] for entry in contador_meses]


    """ Gráfico de Quantidade de Detenções por Doenças """

    # Extrair as doenças das consultas
    doencas = [consulta.doenca for consulta in consultas]

    # Contar a quantidade de detenções por doença
    contador_doencas = Counter(doencas)

    # Separar as doenças e contagens
    doencas = list(contador_doencas.keys())
    quantidades_doencas = list(contador_doencas.values())

    print(f"doencas: {doencas}")
    print(f"quantidades: {quantidades_doencas}")

    return render(request, 'system/reports.html',{
        "datasets_json":datasets_json,
        "racas":json.dumps(racas),
        "quantidades":json.dumps(quantidades),
        "nomes_meses":json.dumps(nomes_meses),
        "quantidades_meses":json.dumps(quantidades_meses),
        "doencas":json.dumps(doencas),
        "quantidades_doencas":json.dumps(quantidades_doencas),
    })


# metodo auxiliar
def encontrar_chave_valor(dicionario, valor_procurado):
    for chave, valor in dicionario.items():
        if valor.get('nome') == valor_procurado:
            return chave
    return None

# Função para gerar uma cor hexadecimal aleatória
def cor_aleatoria():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Função para gerar uma cor RGBA aleatória com um valor de alfa específico
def cor_aleatoria_rgba(r, g, b, alpha):
    return f'rgba({r}, {g}, {b}, {alpha})'

