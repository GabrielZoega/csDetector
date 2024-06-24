import pandas as pd
from sys import argv

# Lendo os arquivos do csv "commits_per_author"
commits_per_author = pd.read_csv(argv[1])

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
print("Core Devs: ")
print(commits_per_author)