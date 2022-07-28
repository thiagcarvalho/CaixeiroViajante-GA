import pandas as pd
from random import shuffle, sample, uniform, random, randrange
from pprint import pprint
import numpy as np
from copy import copy, deepcopy
import matplotlib.pyplot as plt

class individuo:
    def __init__(self, df:dict) -> None:
        self.ind = []
        self.df = df
        self.dist = 0
        #self.gera_aleatorio()
        #self.calc_fitness()
    def gera_aleatorio(self):
        self.ind = list(self.df.keys())
        shuffle(self.ind)
    def calc_fitness(self):
        #Função que realiza o calculo de fitness do individuo
        self.dist = 0
        for i in range(0, len(self.ind)-1):
            self.dist+=np.linalg.norm(np.asarray(self.df[self.ind[i]])-np.asarray(self.df[self.ind[i+1]]))
        self.dist += np.linalg.norm(np.asarray(self.df[self.ind[0]])-np.asarray(self.df[self.ind[-1]]))
    def __str__(self) -> None:
        return str(self.dist)


class ga:
    def __init__(self, popsize, ngeneration, df, ntoneio, taxa_cruzamento, taxa_mutacao, n_elitismo) -> None:
        self.popsize = popsize
        self.ngeneration = ngeneration
        self.df = df
        self.ntoneio = ntoneio
        self.taxa_cruzamento=taxa_cruzamento
        self.taxa_mutacao = taxa_mutacao
        self.n_elitismo = n_elitismo
        self.melhor = 0
        self.curva =[]
        self.elite = []

    def pop_inicial(self):
        #Calcula a população inicial
        pop = []
        for i in range(0,self.popsize):
            ind = individuo(self.df)
            ind.gera_aleatorio()
            ind.calc_fitness()
            pop.append(ind)
        return pop

    def run(self):
        #Função na qual geramos a nova população, realizamos cruzamento e mutações
        pop = self.pop_inicial()
        self.elite, self.melhor = self.get_elite(pop)
        print("Distância Inicial: ", self.melhor)

        for i in range(0, self.ngeneration):
            new_pop = []
            for j in range(0, int(len(pop)/2)):
                ind1 = deepcopy(self.torneio(pop))
                ind2 = deepcopy(self.torneio(pop))
                aux = uniform(0, 1)
                if aux < self.taxa_cruzamento:
                    aux1 = self.crossover(ind1, ind2)
                    aux2 = self.crossover(ind2, ind1)
                    ind1 = aux1
                    ind2 = aux2
                ind1 = self.mutacao(ind1)
                ind2 = self.mutacao(ind2)
                ind1.calc_fitness()
                ind2.calc_fitness()
                new_pop.append(ind1)
                new_pop.append(ind2)
            pop.sort(key=lambda x: x.dist)
            new_pop.sort(key=lambda x: x.dist, reverse=True)
            for k in range(0,self.n_elitismo):
                new_pop[k] = pop[k]
            self.elite, self.melhor = self.get_elite(new_pop)
            pop = new_pop
        
    def torneio(self, pop):
        #Seleciona K elementos da população e retorna o individuo com menor fitness
        torn = sample(pop, self.ntoneio)
        i = min(torn, key=lambda indiv: indiv.dist) 
        return i

    def mutacao(self, ind:individuo):
        for i in range(0, len(ind.ind)):
            aux = uniform(0, 1)
            if aux < self.taxa_mutacao:
                gene = int(random() * len(ind.ind))
                city1 = ind.ind[i]
                city2 = ind.ind[gene]    
                ind.ind[i] = city2
                ind.ind[gene] = city1
        return ind

    def elitismo(self, pop, newpop):
        for i in range(0,self.n_elitismo):
            newpop[i] = pop[i]

    def get_elite(self, pop):
        #Função que coleta o melhor fitness da atual geração
        pop.sort(key=lambda x: x.dist, reverse=True)
        self.curva.append(pop[-1].dist)
        return pop[-1].ind, pop[-1].dist

    def crossover(self, pai1:individuo, pai2:individuo):
        #Função que realiza a mutação
            ind_filho = individuo(self.df)
            childP1 = []
            childP2 = []
            geneA = int(random() * len(pai1.ind))
            geneB = int(random() * len(pai1.ind))
            startGene = min(geneA, geneB)
            endGene = max(geneA, geneB)
            for i in range(startGene, endGene):
                childP1.append(pai1.ind[i])
            childP2 = [item for item in pai2.ind if item not in childP1]
            ind_filho.ind = childP1 + childP2
            ind_filho.calc_fitness()
            return ind_filho

    def print_pop(self, pop):
        for i in pop:
            print(i)


#Lê a base de dados
dados = pd.read_csv('./dados/berlin52.tsp', sep='\s', skiprows=6,
                    skipfooter=2, header=None, index_col=None, engine='python')

dados.rename({0: 'cidade', 1: 'coordenada_x',
             2: 'coordenada_y'}, axis=1, inplace=True)


dados.set_index('cidade', inplace=True)

#Armazena a base de dados em um dicionário
base = {}
for i, row in dados.iterrows():
    base[i] = (row['coordenada_x'], row['coordenada_y'])

#Iniciar o Algoritmo Genético
GA = ga(popsize=200, ngeneration=500, df=base, ntoneio=5, taxa_cruzamento=0.85, taxa_mutacao=0.005, n_elitismo=5)
GA.run()

#Variaveis que irão coletar o melhor individuo e o melhor fitness obtido depois das gerações
ind = GA.elite
dist = GA.melhor
print("Distância Final: ", dist)

#Plotagem do grafico de convergência e da melhor rota
f, ax = plt.subplots(figsize=(12, 12))
ax.scatter(dados['coordenada_x'], dados['coordenada_y'])
x = []
y = []
for i in ind:
    x.append(base[i][0])
    y.append(base[i][1])
x.append(base[ind[0]][0])
y.append(base[ind[0]][1])

ax.plot(x, y, '-', c='k', label='Melhor Caminho Encontrado')

f, ax = plt.subplots(figsize=(12, 12))
ax.plot(GA.curva)
plt.show()
plt.savefig('curva.png')