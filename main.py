import math
import random

#mendefinisikan panjang gen dan maks populasi
nPopulasi = 20
lengthChromosome = 12 #berbentuk biner
lajuCrossover = 0.7
lajuMutasi = 0.2

parent1 = []
parent2 = []
isiPopulasi = []


#representasi genetik
def gen(panjangGen):
    genX = random.choices([0,1], k = lengthChromosome)
    genY = random.choices([0,1], k = lengthChromosome)
    hasilX = decode(5,-5,genX)
    hasilY = decode(5,-5,genY)

    hasilF = fitnes(hasilX,hasilY)
    return{
        "gen X" : genX,
        "gen Y" : genY,
        "hasil X" : hasilX,
        "hasil Y" : hasilY,
        "kromosom" : genX + genY,
        "hasil fitness" : hasilF
    }

#fitness function
def h(x,y):
    hasilH = (((math.cos(x)) + math.sin(y)) ** 2) / (
    x ** 2 + y ** 2)  # x dan y yang dimasukkan mempunyai inteval -5 sampai 5
    return hasilH

def fitnes(x,y):
    a = random.uniform(0, 0.000000000000000001) #a digunakan untuk random bilangan kecil agar tidak terjadi null exception error
    hasilF = 1 / (h(x,y) + a)
    return  hasilF


#fungsi decode merubah biner menjadi bil real
def decode(upperInt, lowerInt, nGen): #nGen adalah sebuah array
    minSquare = [2**-i for i in range (1, len(nGen) + 1)]
    minSquareMul = [nGen[i] * minSquare[i] for i in range(len(nGen))]
    mainOperation = lowerInt + (((upperInt - lowerInt) / sum(minSquare)) * sum(minSquareMul))
    return mainOperation

#ini adalah fungsi buat dipakai di built in function sort di function population
def myFunc(based):
    return based["hasil fitness"]

def population(max):
    #proses memasukkan ke populasi yang kosong
    while len(isiPopulasi) < max:
        isiPopulasi.append(gen(lengthChromosome))
        #lalu kita sort populasi yang ada di populasiKosong
        #sorted(1, key=operator.itemgetter("hasil fitness"))
        isiPopulasi.sort( key = myFunc,reverse = True) #reverse = true maka diurutkan secara descending dan key adalah field yang akan disort

    return isiPopulasi

#fungsi untuk menyeleksi orang tua
def seleksi():
    for i in range (5):
        angka1 = random.randint(0, nPopulasi-1)
        hasil1 = isiPopulasi[angka1]
        parent1.append(hasil1)
        #int(parent1[i]["kromosom"])
    parent1.sort(key = myFunc,reverse = True)
    final1 = parent1[0]

    for i in range (5):
        angka2 = random.randint(0, nPopulasi-1)
        hasil2 = isiPopulasi[angka2]
        parent2.append(hasil2)
    parent2.sort(key = myFunc,reverse = True)
    final2 = parent2[0]

    return final1, final2

def crossover(p1, p2):
    p = random.randint(1, 2*lengthChromosome-1)
    campuran1 = p2["kromosom"][:p] + p1["kromosom"][p:]
    campuran2 = p2["kromosom"][:p] + p1["kromosom"][p:]

    child1 = dict(p1)
    child2 = dict(p2)

    lenGen = len(campuran2)//2
    child1["gen X"] = campuran1[:lenGen]
    child1["gen Y"] = campuran1[lenGen:]
    child1["hasil X"] = decode(5, -5, child1["gen X"])
    child1["hasil Y"] = decode(5, -5, child1["gen Y"])
    child1["kromosom"] = child1["gen X"] + child1["gen Y"]
    child1["hasil fitness"] = fitnes(child1["hasil X"], child1["hasil Y"])

    child2["gen X"] = campuran2[:lenGen]
    child2["gen Y"] = campuran2[lenGen:]
    child2["hasil X"] = decode(5, -5, child2["gen X"])
    child2["hasil Y"] = decode(5, -5, child2["gen Y"])
    child2["kromosom"] = child2["gen X"] + child2["gen Y"]

    return child1, child2

def mutation(lajuMutasi, c1, c2):
    child1 = dict(c1)
    child2 = dict(c2)
    for i in range(len(child1["kromosom"])):
        if ((random.uniform(0,1)) <= lajuMutasi):
            if child1["kromosom"][i]  == 1:
                child1["kromosom"][i] = 0
            else:
                child1["kromosom"][i] = 1

    for i in range(len(child2["kromosom"])):
        if ((random.uniform(0,1)) <= lajuMutasi):
            if child2["kromosom"][i]  == 1:
                child2["kromosom"][i] = 0
            else:
                child2["kromosom"][i] = 1

    return child1,  child2

def regeneration(populasi, child1, child2):
    populasi = sorted(populasi, key=lambda x: x['hasil fitness'], reverse = True)
    if populasi[-1]["hasil fitness"] < child1["hasil fitness"]:
        populasi[-1] = child1


    populasi = sorted(populasi, key=lambda x: x['hasil fitness'], reverse=True)
    if populasi[-1]["hasil fitness"] < child2["hasil fitness"]:
        populasi[-1] = child2

    return populasi

def main():
    isiPopulasi = population(nPopulasi)
    isiPopulasi.sort(key=myFunc, reverse=False)
    for i in range(1000):
        a, b = seleksi()
        if ((random.uniform(0, 1)) <= lajuCrossover):
            c1, c2 = crossover(a, b)
            m1, m2 = mutation(lajuMutasi, c1, c2)
        else:
            m1 , m2 = mutation(lajuMutasi, a, b)
        isiPopulasi = regeneration(isiPopulasi, m1, m2)
        isiPopulasi.sort(key = myFunc,reverse = False)
        b = isiPopulasi[-1]["hasil fitness"]
        print("Generasi         : ", i)
        print("Kromosom         : ", isiPopulasi[-1]["kromosom"])
        print("Gen X            : ", isiPopulasi[-1]["gen X"])
        print("Gen Y            : ", isiPopulasi[-1]["gen X"])
        print("hasil fitness    : ", b)


main()
































