# CSDETECTOR

Modificações adicionadas tendo em base as alterações feitas anteriormente no projeto [CSDETECTOR Refactory](https://github.com/ViniciusTei/csDetector), que por sua vez usa a versão original da [CSDETECTOR](https://github.com/Nuri22/csDetector).

Aqui vão ser implementadas alterações visando facilitar o uso da CSDETECTOR para pesquisas da equipe [Colminer](http://nupessc.caf.ufv.br/#/home). 

### Sobre a CSDETECTOR

**Módulos Chave e Functionalidades**

- **Módulo de Extração de Métricas:**
  1. **Developer Artifact Extraction:** começa coletando artefatos do sistema de controle de versão.
  2. **Developer Alias Extraction:** Recupera aliases (identificadores) dos desenvolvedores.
  3. **Social Graph Construction:** Usa aliases para criar um gráfico social interconectando desenvolvedores.
  4. **Sentiment-Related Metrics Calculation:** Analiza o conteúdo para calcular métricas de sentimento.
  5. **Socio-Technical Metrics Calculation:** Usa o gráfico social para quantificar a colaboração entre desenvolvedores.

- **Módulo de Detecção de Community Smells:**
  1. **Community Smells Detection:** Utiliza recursos extraídos e métricas calculadas como entrada.
  2. **Pre-Trained Models:** Emprega modelos pré-treinados para identificar possíveis “code smells” na comunidade.
  
Este sistema opera em duas etapas principais: primeiro, extrai informações relacionadas aos desenvolvedores e suas interações na comunidade de desenvolvimento; então, ele utiliza essas informações para detectar possíveis problemas ou "Community Smells".

# Instruções de Uso

Siga as intruções para configurar e usar a ferramenta de forma correta.

## Pré-requisitos

- Python 3.x instalado no seu sistema.
- Git instalado (para clonar o repositório).
- Google Cloud API Key (se usando Perspective API).
- A ferramenta SentiStrength é configurada automaticamente (veja em: [setup](setup.sh)).

## Setup

1. Clone o repositório CSDETECTOR do GitHub:
   
   ```bash
   git clone https://github.com/GabrielZoega/csDetector.git
   cd csDetector
   ```

2. Crie e ative um ambiente virtual (recomendado):
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale os pacotes Python necessários:
   
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o script do setup para instalar componentes adicionais:
   
   ```bash
   sh setup.sh
   ```

## Usando

Navegue até o diretório raiz da ferramenta CSDETECTOR em seu terminal antes de executar os seguintes comandos.

```bash
cd /path/to/csDetector
```

Execute o script main `main.py` com os argumentos necessários:

```bash
python main.py -p <GitHub_PAT> -r <repository_url> -s <sentiStrength_path> -o <output_path>
```

### Argumentos Opcionais:

- `-g, --googleKey`: Google Cloud API Key para Perspective API authentication.
- `-m, --batchMonths`: Número de meses para analizar por batch (o padrão é 9999, i.e., all data).
- `-sd, --startDate`: Data de inicio para começar a análise do projeto (opcional).
- `-ed, --endDate`: Data de término para parar a análise do projeto (opcional).
- `-d, --debug`: Ativa debug logging (opcional, apenas para desenvolvimento).
- `-a, --alias`: Extrai aliases dos autores para o repositório (opcional, se está ativado a ferramenta provavelmente levará mais tempo executando).

**Exemplo:**

```bash
python main.py -p <GitHub_PAT> -g <Google_API_Key> -r <repository_url> -m 6 -s <sentiStrength_path> -o <output_path> -sd 2020-01-01 -d true -a true
```

## Notas

- **GitHub PAT (Personal Access Token)**: Obtenha nas configurações da sua conta GitHub. Vários tokens podem ser usados ​​para melhorar a eficiência da extração de dados.
- **Google Cloud API Key**: Necessário apenas se estiver usando Perspective API.
- **Repository URL**: URL do Repositório do GitHub que você quer analisar.
- **SentiStrength Path**: Caminho para a ferramenta SentiStrength (o padrão é `senti`).
- **Output Path**: Caminho para o diretório onde a saída da analise será colocada. (o padrão é `out`).
- **Planilha de Smells**: Deve ser criado com antecedência um arquivo "smells.xlsx" na pasta de saída escolhida. (Esse arquivo deve ser criado com um programa como o Excel ou o LibreOffice Calc).

Para mais detalhes e uso avançado, consulte o README no [Repositório da CSDETECTOR](https://github.com/Nuri22/csDetector).

