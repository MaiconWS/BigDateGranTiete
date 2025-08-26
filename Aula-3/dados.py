import csv # biblioteca para manipulação de arquivos CSV
import random # biblioteca para geração de números aleatórios
from  faker import Faker # biblioteca para geração de dados falsos

faker = Faker('pt_BR')

# Lista de estados brasileiros
estados = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

# 'with' -> garante que o arquivo será fechado após o uso
# 'open' -> abre o arquivo
# "cliente.csv" -> nome do arquivo
# mode="w" -> define o modo escrita
# newline='' -> evita linhas em branco entre os registros
# encoding='utf-8' -> define a codificação do arquivo
with open("cliente.csv",mode="w", newline='', encoding='utf-8') as csvfile:
    arquivo = csv.writer(csvfile)

    arquivo.writerow(["id", "nome", "idade", "sexo","estado, renda_mensal"])

    #random.randint serve para gerar um número inteiro aleatório dentro de um intervalo
    #random.choice serve para escolher um valor aleatório de uma lista
    #random.uniform serve para gerar um número float aleatório dentro de um intervalo
    for i in range(1, 10001):
        nome = faker.name()
        idade = random.randint(18, 100)
        sexo = random.choice(['M', 'F'])
        estado = random.choice(estados)
        renda_mensal = round(random.uniform(1000, 10000), 2)

        arquivo.writerow([i, nome, idade, sexo, estado, renda_mensal])
print("Arquivo cliente.csv criado com sucesso!")