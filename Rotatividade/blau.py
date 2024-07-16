import pandas as pd
from sys import argv

# Converte para a devida UTC e organiza de forma crescente
def timezone(caminhoArquivoTimezones_0):
    timezones = pd.read_csv(caminhoArquivoTimezones_0)
    timezones.sort_values(['Timezone Offset'], inplace=True)
    utcs = [k / 3600 for k in timezones['Timezone Offset']]
    grupoUtc = {item: None for item in utcs}
    author_count = timezones['Author Count']
    grupoUtc = {utcs[i]: author_count[i] for i in range(len(utcs))}
    return grupoUtc

# Coloca num dicionário a quantidade de membros de cada gênero na planilha dos contribuidores
def generoContribuidores(caminhoArquivoTimeRepo):
    contribuidores = pd.read_csv(caminhoArquivoTimeRepo)
    homens = contribuidores['Homens']
    mulheres = contribuidores['Mulheres']

    totalHomens = homens.sum()
    totalMulheres = mulheres.sum()

    return {'H': totalHomens, 'M': totalMulheres}

# Calcula o índice de Blau para uma única dimensão
def calculaBlau(proporcoes):
    proporcoes = {chave: valor ** 2 for chave, valor in proporcoes.items()}
    somaProporcoes = sum(proporcoes.values())
    blau = 1 - somaProporcoes
    return blau

# Calcula o índice de diversidade de Blau
def calculaIndiceDeDiversidadeDeBlau(caminhoArquivoTimezones_0, caminhoArquivoTimeRepo, timezone, generoContribuidores):
    timeZone = timezone(caminhoArquivoTimezones_0)
    equipe = generoContribuidores(caminhoArquivoTimeRepo)

    # Calcula a proporção dos elementos para cada categoria
    qtdTotalTimeZones = sum(timeZone.values())
    proporcaoTimeZones = {chave: valor / qtdTotalTimeZones for chave, valor in timeZone.items()}

    qtdTotalContribuidores = sum(equipe.values())
    proporcaoGeneroEquipe = {chave: valor / qtdTotalContribuidores for chave, valor in equipe.items()}

    # Calcula os índices de Blau separadamente
    blauTimeZone = calculaBlau(proporcaoTimeZones)
    blauGenero = calculaBlau(proporcaoGeneroEquipe)

    # Combina os índices de Blau (aqui fazemos uma média aritmética)
    blau = (blauTimeZone + blauGenero) / 2
    return blau

# Obtém os caminhos dos arquivos de entrada
caminhoArquivos = argv[1].split(",")

flag = 0  # Para calcular somente para gênero ou somente para timezone

if len(caminhoArquivos) < 2:
    flag = 1

if flag == 1:
    if "timezones_0.csv" in caminhoArquivos[0]:
        def calculaIndiceDeDiversidadeDeBlauTimezone(caminhoArquivoTimezones_0, timezone):
            timeZone = timezone(caminhoArquivoTimezones_0)
            qtdTotalTimeZones = sum(timeZone.values())
            proporcaoTimeZones = {chave: valor / qtdTotalTimeZones for chave, valor in timeZone.items()}
            blau = calculaBlau(proporcaoTimeZones)
            return blau

        b = calculaIndiceDeDiversidadeDeBlauTimezone(caminhoArquivos[0], timezone)
        print(f"{b:.2f}")

    else:
        def calculaIndiceDeDiversidadeDeBlauGenero(caminhoArquivoTimeRepo, generoContribuidores):
            equipe = generoContribuidores(caminhoArquivoTimeRepo)
            qtdTotalContribuidores = sum(equipe.values())
            proporcaoGeneroEquipe = {chave: valor / qtdTotalContribuidores for chave, valor in equipe.items()}
            blau = calculaBlau(proporcaoGeneroEquipe)
            return blau

        b = calculaIndiceDeDiversidadeDeBlauGenero(caminhoArquivos[0], generoContribuidores)
        print(f"{b:.2f}")

else:
    b = calculaIndiceDeDiversidadeDeBlau(caminhoArquivos[0], caminhoArquivos[1], timezone, generoContribuidores)
    print(f"{b:.2f}")

