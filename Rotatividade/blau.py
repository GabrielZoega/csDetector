import pandas as pd
from sys import argv

#converte para a devida UTC e a organiza de forma crescente
def timezone(caminhoArquivoTimezones_0):
    timezones = pd.read_csv(caminhoArquivoTimezones_0)
    timezones.sort_values(['Timezone Offset'], inplace = True)
    utcs = [k/3600 for k in timezones['Timezone Offset']]
    grupoUtc = {item: None for item in utcs}
    author_count = timezones['Author Count']
    grupoUtc = {utcs[i]: author_count[i] for i in range(len(utcs))}
    return grupoUtc

#coloca num dicionário a quantidade de membros de cada gênero na planilha dos contribuidores
def generoContribuidores(caminhoArquivoTimeRepo):
    contribuidores = pd.read_csv(caminhoArquivoTimeRepo)
    homens = contribuidores['Homens']
    mulheres = contribuidores['Mulheres']
    indefinidos = contribuidores['Indefinido']
    
    totalHomens = homens.sum()
    totalMulheres = mulheres.sum()
    totalIndefinidos = indefinidos.sum()

    return {'H':totalHomens, 'M':totalMulheres, 'I':totalIndefinidos}

#calcula o índice de diversidade de blau
def calculaIndiceDeDiversidadeDeBlau(caminhoArquivoTimezones_0, caminhoArquivoTimeRepo, timezone, generoContribuidores):
    timeZone = timezone(caminhoArquivoTimezones_0)
    equipe = generoContribuidores(caminhoArquivoTimeRepo)
    
    #encontra a quantidade de membros de cada categoria
    qtdTotalTimeZones = sum(timeZone.values())
    qtdTotalContribuidores = sum(equipe.values())
    
    #calcula a proporção dos elementos para cada categoria
    proporcaoTimeZones = {chave: valor/qtdTotalTimeZones for chave, valor in timeZone.items()}
    proporcaoGeneroEquipe = {chave: valor/qtdTotalContribuidores for chave, valor in equipe.items()}

    #eleva as proporções ao quadrado
    proporcaoTimeZones = {chave: valor ** 2 for chave , valor in proporcaoTimeZones.items()}
    proporcaoGeneroEquipe = {chave: valor ** 2 for chave, valor in proporcaoGeneroEquipe.items()}
    
    #soma o somatório das duas
    somaTimeZone = sum(proporcaoTimeZones.values())
    somaEquipe = sum(proporcaoGeneroEquipe.values())
    
    #subtrai 1
    blau = 1 - (somaTimeZone + somaEquipe)
    return blau;

caminhoArquivos = argv[1].split(",")

flag = 0 #Para calcular somente para gênero

if(len(caminhoArquivos) < 2):
    flag = 1

if flag == 1:
    def calculaIndiceDeDiversidadeDeBlau(caminhoArquivoTimeRepo, generoContribuidores):
        equipe = generoContribuidores(caminhoArquivoTimeRepo)
        qtdTotalContribuidores = sum(equipe.values())
        proporcaoGeneroEquipe = {chave: valor/qtdTotalContribuidores for chave, valor in equipe.items()}
        proporcaoGeneroEquipe = {chave: valor ** 2 for chave, valor in proporcaoGeneroEquipe.items()}
        somaEquipe = sum(proporcaoGeneroEquipe.values())
        blau = 1 - somaEquipe
        return blau
    
    b = calculaIndiceDeDiversidadeDeBlau(caminhoArquivos[0], generoContribuidores)
    print(f"{b:.2f}")

else:
    b = calculaIndiceDeDiversidadeDeBlau(caminhoArquivos[0], caminhoArquivos[1], timezone, generoContribuidores)
    print(f"{b:.2f}")

