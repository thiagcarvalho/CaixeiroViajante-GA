## Overview

Este repositório contém uma implementação genérica em Python de um Algoritmo Genético para resolver o Problema do Caixeiro Viajante (TSP). As coordenadas das cidades são fornecidas por meio do seguinte link: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/index.html, e essas coordenadas são utilizadas como entrada no código para gerar um grafo ponderado por arestas, onde os pesos representam as distâncias entre as cidades em quilômetros. A base de dados utilizada foi a "berlin52", e outras podem ser encontradas no mesmo link mencionado.

## O Algoritmo Genético

### Indivíduo 

Cada indivíduo na população do algoritmo genético é composto por uma única rota que satisfaz a condição inicial de percorrer exatamente todas as cidades uma única vez. 

O gene de cada indivíduo é uma **cidade**. Em outras palavras são as coordenadas $G = (x, y)$.

### Iniciando a população

A população é criada de forma randômica para garantir uma alta diversidade genética, evitando influências nos resultados que poderiam ocorrer com uma população muito bem definida. O tamanho dessa população é definida pelo usuário.

```python
def pop_inicial(self):
        #Calcula a população inicial
        pop = []
        for i in range(0,self.popsize):
            ind = individuo(self.df)
            ind.gera_aleatorio()
            ind.calc_fitness()
            pop.append(ind)
        return pop
```

### Fitness

O *fitness* é a forma de avaliar o indivíduo. No caso do TSP, pode-se utilizar como *fitness* a distância percorrida. Assim, quanto menor o *fitness*, menor é a distância percorrida. 

A equação de *fitness* pode ser definida pela equação abaixo, no qual o termo $c_{ii+1}$ representa a distância euclidiana de $i$ e a cidade seguinte $i+1$, para todos os valores de $i$ de $0$ a $n$ (número de cidades que um indivíduo possui).

$$ f = \sum_{i=0}^n c_{ii+1} $$

Distância Euclidiana:

$$ d = \sqrt{(x_b-x_a)^2 + (y_b-y_a)^2} $$

```python
def calc_fitness(self):
        #Função que realiza o calculo de fitness do individuo
        self.dist = 0
        for i in range(0, len(self.ind)-1):
            self.dist+=np.linalg.norm(np.asarray(self.df[self.ind[i]])-np.asarray(self.df[self.ind[i+1]]))
        self.dist += np.linalg.norm(np.asarray(self.df[self.ind[0]])-np.asarray(self.df[self.ind[-1]]))
```
É importante salientar que a distância deve considerar a volta à primeira cidade.

### Seleção

A seleção dos indivíduos para realizar o cruzamento é feito através do torneio. O torneio é um método de seleção de indivíduos para reprodução. A ideia é realizar competições entre subconjuntos aleatórios da população, conhecidos como "torneios", e selecionar os indivíduos mais aptos desses torneios para serem pais na próxima geração.

Além disso essa técnica é relativamente simples de implementar e não requer uma classificação completa de toda a população, tornando-o eficiente computacionalmente. Dessa forma, a probabilidade de escolher indivíduos mais aptos é maior, mas ainda há espaço para diversidade genética.

```python
def torneio(self, pop):
        #Seleciona K elementos da população e retorna o individuo com menor fitness
        torn = sample(pop, self.ntoneio)
        i = min(torn, key=lambda indiv: indiv.dist) 
        return i
```


### Cruzamento (*Crossover*)

O cruzamento é o processo de juntar dois indivíduos, combinar seus atributos e gerar um novo indivíduo. Como os indivíduos pais são indivíduos da população, eles podem ser levados para as próximas gerações.

O cruzamento realizado é o *crossover* de ponto de corte.

```python
def crossover(self, pai1:individuo, pai2:individuo):

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
```

### Mutação

A mutação é usada para introduzir de variabilidade genética nos indivíduos da população. Após o cruzamento, ambas o individuo possui uma probabilidade de 5% de sofrer mutação. Se um novo indivíduo entrar no processo de mutação, cada vetor tem uma chance de 5% de passar por uma mutação. A mutação utilizada nessa fase é a de inserção, na qual dois genes aleatórios do indivíduo são selecionados, e então o primeiro gene é movido para seguir o segundo, rearranjando todos os outros genes de acordo.

```python
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
```
### Próxima Geração

Após a aplicação do cruzamento e da mutação, surge uma nova população que, teoricamente, apresentam melhorias em relação à geração anterior. (O elitismo não está funcionando da melhor forma!)

```python
        pop.sort(key=lambda x: x.dist)
        new_pop.sort(key=lambda x: x.dist, reverse=True)
        
        for k in range(0,self.n_elitismo):
          new_pop[k] = pop[k]
          
        self.elite, self.melhor = self.get_elite(new_pop, i)
        pop = new_pop
```
Os novos indivíduos que apresentarem os piores valores de aptidão em comparação com os melhores indivíduos da geração anterior terão seus lugares trocados, seguindo a estratégia de elitismo.

## Resultados

### Berlin 52

* <strong>Melhor resultado (fornecido pela base de dados)</strong>

<div align="center">
<img src="https://github.com/thiagcarvalho/CaixeiroViajante-GA/assets/46302988/e72b1f6c-5d8e-4185-9bab-90db2763f4b9.png" />
<p>Distância: 7544,365</p>
</div>

* <strong>Melhores resultados encontrados pelo GA</strong>

<div align="center">
<img src="https://github.com/thiagcarvalho/CaixeiroViajante-GA/assets/46302988/4eccb376-4464-4be3-8a58-86301c86451d.png" />
<p>Distância: 7800,190</p>
</div>

<div align="center">
<img src="https://github.com/thiagcarvalho/CaixeiroViajante-GA/assets/46302988/331a8805-7a63-49d9-b0d9-2e8601bd6df1.png" />
<p>Distância: 7808,008</p>
</div>









