import pandas as pd
from sys import argv

def coreDevs (path):
    commits_per_author = pd.read_csv(path)

    # Somando todos os commits do csv
    commits_total = commits_per_author["Commit Count"].sum()

    # Calculando a porcentagem de cada dev
    commits_per_author = commits_per_author.assign (dev_percentage = (commits_per_author["Commit Count"] * 100) / commits_total)
    commits_per_author = commits_per_author.sort_values(["dev_percentage"], ascending = False)
    commits_per_author = commits_per_author.reset_index(drop = True)

    # Selecionando os maiores autores até chegar a 80% dos commits
    sum = 0    
    for i in range(commits_per_author["dev_percentage"].size):
        sum += commits_per_author.loc[i][2]
        if (sum >= 80):
            index = i
            break
            
    # Retirando aqueles abaixo de 5%
    commits_per_author = commits_per_author.loc[0:index]
    commits_per_author = commits_per_author[commits_per_author["dev_percentage"] > 5]


    # Exibindo os Core Devs
    core_devs_number = commits_per_author["dev_percentage"].size
    print("Core Devs: {}".format(core_devs_number))
    #print(commits_per_author)   Caso queira saber quem são os CoreDevs descomente esta linha
    return core_devs_number
    
# Lendo os arquivos do csv "commits_per_author"
paths = argv[1].split(",")

# Calculando a Taxa de Rotatividade:
SetA = coreDevs(paths[0])
SetB = coreDevs(paths[1])

# Calculando a Core Dev Leaver Rate (CDLrate)
CDL = SetA - SetB
CDLrate = (abs(CDL) / abs(SetA)) * 100

#Calculando a Core Developer Turnover (CDTrate)
CDTrate = (abs(CDL) / ((abs(SetA) + abs(SetB)) / 2)) * 100

# Exibindo o resultado:
print("CDL: {}".format(CDL))
print("CDLrate: {}".format(CDLrate))
print("CDTrate: {}".format(CDTrate))