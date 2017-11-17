import dbInteraction
import random

class Evolution:
    DB = dbInteraction.DBInteraction()
    fitness=[0]*4
    isTried=[False]*4
    generation=[]
    howManyToBreed=2
    howManyfunctions=4
    currentFunction=-1

    def __init__(self):
        res=self.DB.query("select count(*) from strategies")
        if res[0][0]==0:
            self.generation=self.getFirstGeneration()
        else:
            tmp=self.DB.query("select strategy,fitness from strategies")
            self.generation=[0]*len(tmp)
            for i in range(0,len(tmp)):
                self.generation[i]= tmp[i][0].split()
                for j in range(0,len(self.generation[i])):
                    self.generation[i][j]=float(self.generation[i][j].strip(','))
                if tmp[i][1]=='':
                    self.fitness[i]=None
                    self.isTried[i]=False
                else:
                    self.fitness[i] =int(tmp[i][1])
                    self.isTried[i]=True
            print("LOL")


    def addToDB(self,generation,fitness,isTried):
        #self.DB.DML("delete from strategies")
        s=[]
        s.append("delete from strategies")
        tmp=None
        for i in range(0,len(generation)):
            if isTried[i]==False:
                tmp=""
            else:
                tmp=fitness[i]
            s.append("insert into strategies(strategy,fitness) values('"+', '.join(map(str,generation[i]))+"','"+str(tmp)+"')")
            #self.DB.DML("insert into strategies(strategy,fitness) values('"+', '.join(map(str,generation[i]))+"','"+str(tmp)+"')")
        self.DB.DML(s)


    def getFirstGeneration(self):
        generation_l = [0] * 4

        for i in range(0,len(generation_l)):
            generation_l[i]=[]

        for i in range(0, len(generation_l)):
            for j in range(0, 59, 1):
                generation_l[i].append(random.random())
        return generation_l

    def getFirstGenerationFitness(self,generation_l):
        fitness_l=[0]*4

        for i in range(0,len(fitness_l)):
            fitness_l[i]=[]

        for i in range(0, len(generation_l)):
            for j in range(0, 59, 1):
                fitness_l[i].append(random.random())
        return fitness_l

    def chooseForBreeding(self,fitness_l):
        chosen=[]
        for i in range(0,self.howManyToBreed):
            max=0
            for j in range(1,len(fitness_l)):
                if fitness_l[j]>=fitness_l[max] and j not in chosen:
                    max=j
            chosen.append(max)
        return chosen

    def getDistribution(self,generation_l,fitness_l):
        distr=[0]*2
        for i in range(0,len(distr)):
            distr[i]=[]

        for i in range(0,len(generation_l[0])):
            tmp=random.randint(0,1)
            distr[tmp].append(i)
        return distr


    def breed(self,generation_l,fitness_l):
        chosen_l=self.chooseForBreeding(fitness_l)
        gen=[0]*self.howManyfunctions

        for i in range(0,len( gen)):
            gen[i]=[]

        for i in range(0,self.howManyfunctions):
            distr = self.getDistribution(generation_l, fitness_l)
            for j in range(0,len(generation_l[0])):
                ind=-1
                for k in range(0,len(distr)):
                    if j in distr[k]:
                        ind=k
                        break
                gen[i].append(generation_l[chosen_l[ind]][j])
        for i in range(0,len(self.isTried)):
            self.isTried[i]=False
        return gen

    def setFitness(self,result):
        self.fitness[self.currentFunction]=result
        self.isTried[self.currentFunction]=True
        self.addToDB(self.generation,self.fitness,self.isTried)

    def chooseFunction(self):
        for i in range(0,len(self.isTried)):
            if self.isTried[i]==False:
                return i
        return -1

    def getFunction(self):
        fun=self.chooseFunction()
        if fun==-1:
            self.generation = self.breed(self.generation, self.fitness)
        fun=self.chooseFunction()
        self.currentFunction=fun
        return self.generation[fun]
