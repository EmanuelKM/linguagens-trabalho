import re
import pdb

#expressoes regulares
padraoDados = re.compile(r"(\w+)\=\((\{[^\}]*\}),(\{[^\}]*\}),(\w+),(\{[^\}]*\})\)")
#groups
#1 = nome do afn
#2 = estados
#3 = alfabeto
#4 = estadoInicial
#5 = estadosFinais

padraoFuncaoPrograma = re.compile(r"\(\w(\w),(\w)\)\=(\{[^\}]*\})")
#groups
#1 = indice do estadoAtual
#2 = simbolo lido da fita
#3 = estados a serem atingidos

def leAFN():
    estadoInicial = '' 
    estadosFinais = []
    alfabeto = []

    with open("afn.txt","r") as arquivo:
        linhas = arquivo.readlines()
        dados = linhas[0]
        dadosDoAFN = re.search(padraoDados,dados)

        estadoInicial = dadosDoAFN.group(4)
        estadosFinais = extraiEstadosFinais(dadosDoAFN.group(5))

        alfabeto = extraiAlfabeto(dadosDoAFN.group(3))

        AFN = criaAFN(dadosDoAFN.group(2))
        
        for funcaoPrograma in linhas[2:]:
            funcaoPrograma = re.search(padraoFuncaoPrograma,funcaoPrograma)
            estadoAtual = defineEstadoAtual(funcaoPrograma.group(1), AFN)

            indiceLetraNoAlfabeto = alfabeto.index(funcaoPrograma.group(2))
            AFN[estadoAtual][indiceLetraNoAlfabeto] = extraiConjuntoEstados(funcaoPrograma.group(3))

        return AFN, estadoInicial, estadosFinais, alfabeto

def extraiEstadosFinais(estadosFinais):
    estadosFinais = estadosFinais[1:-1] #remove chaves
    estadosFinais = estadosFinais.split(",")
    return estadosFinais

def extraiAlfabeto(alfabeto):
    alfabeto = alfabeto[1:-1] #remove chaves
    alfabeto = alfabeto.split(",")
    return alfabeto

def criaAFN(estados):
    AFN = []
    for i in range(quantidadeDeEstados(estados)):
        AFN.append(conjuntoDefault())
    return AFN

def defineEstadoAtual(nomeEstado, afn):
    if nomeEstado == 'f':
        return len(afn)-1
    else:
        return int(nomeEstado)

def extraiConjuntoEstados(conjuntoEstados):
    return conjuntoEstados[1:-1].split(',')

def quantidadeDeEstados(estados):
    contador = 0
    for letra in estados[1:-1]:
        if letra == 'q':
            contador += 1

    return contador

def conjuntoDefault():
    return [None,None]

def determinizaAFN(afn, tamanhoAlfabeto):
    afd = []
    afd.append(inicializaAfd(afn))

    estadosVisitados = ['q0']
    iteradorAFD = 0
    
    while len(estadosVisitados) != iteradorAFD: #flag de repeticao de estado no afd

        for possivelEstado in afd[iteradorAFD]:
            if possivelEstado not in estadosVisitados and possivelEstado != None:
                estadosVisitados.append(possivelEstado)

                indicesDasFuncoes = extraiIndices(possivelEstado)

                listaDeEstados = []
                for letra in range(tamanhoAlfabeto):
                    listaDeEstados.append(extraiListaDeEstados(indicesDasFuncoes, afn, letra))

                afd.append(listaDeEstados)

        iteradorAFD += 1

    return afd, estadosVisitados

def inicializaAfd(afn):
    primeiroEstado = []

    for simbolo in afn[0]:
        primeiroEstado.append(unificaEstados(simbolo))

    return primeiroEstado
    
def extraiIndices(estado):
    indices = []

    for letra in estado:
        if letra.isdigit():
            indices.append(int(letra))

        elif letra == 'f':
            indices.append(len(AFN)-1)
            
    return indices

def extraiListaDeEstados(estados, afn, letra):

    if len(estados) == 1 and afn[estados[0]][letra] == None:
        return None

    listaDeEstados = []

    for estado in estados:
        if afn[estado][letra] != None:
            listaDeEstados.append(afn[estado][letra])

    listaDeEstados = simplificaLista(listaDeEstados)
    listaDeEstados = unificaEstados(list(set(listaDeEstados))) #remove estados repetidos
    
    return listaDeEstados

def simplificaLista(lista):
    return [item for listaInterior in lista for item in listaInterior]

def unificaEstados(listaDeEstados):
    if listaDeEstados == None:
        return None

    return ''.join(listaDeEstados)

AFN, estadoInicial, estadosFinais, alfabeto = leAFN()

for estado in AFN:
    print(estado)
print('\n')

AFD, teste = determinizaAFN(AFN, len(alfabeto))

for estado in AFD:
    print(estado)
print(teste)

print("hi")