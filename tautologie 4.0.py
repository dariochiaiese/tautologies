
"""
Programma per la determinazione delle tautologie
"""

L = ["&","%",">","-","!"] #And, Or, Implica, Se e solo se (bicondizionale), Negazione
F = []
semF = {"&" : [ [False,True],[True,False], [False,False] ],
       "%" : [ [False,False] ],
       ">" : [ [True,False] ],
       "-" : [ [False,True],[True,False] ],
       "!" : [ [True] ]
    } #Dominio delle coppie di valori che danno valori falsi alle cinque funzioni logiche

semV = {"&" : [ [True,True] ],
       "%" : [ [True,False], [False, True], [True,True] ],
       ">" : [ [True,True], [False, True], [False, False] ],
       "-" : [ [True,True], [False,False] ],
       "!" : [ [False] ]
    } #Dominio delle coppie di valori che danno valori falsi alle cinque funzioni logiche

lettereEnunciativeF = []
global checkAssegnamenti
checkAssegnamenti = False

def isLenun(p): #Determina se p è una lettera enunciativa
    for i in L: #Se non vi sono connettori la formula è una lettera enunciativa
        if i in p:
            return False
    return True

def creaAssegnamento(lettere):
    #Crea un assegnamento con tutte le lettere enunciative, di default settate su True
    #Questa funzione serve solitamente per creare un assegnamento qualsiasi per testare se una formula è sempre vera o sempre falsa.
    ass = {}
    for i in lettere:
        ass[i]=True
    return ass

def leggiAssegnamento(ass):
    #Legge un assegnamento che è una stringa del tipo a:0 - b:1 - ecc // 0 è False e 1 è true
    ass = ass.replace(" ", "") #fa il trim
    assegnamento = dict()
    ass = ass.split("-") #trasforma ass in una lista
    for i in ass:
        i = i.split(":")
        assegnamento[i[0]] = bool(int(i[1])) #In Pyton il bool di una stringa è riferito alla sua lunghezza e quindi è sempre True a meno che non sia nulla        
    return assegnamento
        

def lettereEnunciative(p):
    #Crea un assegnamento contenente tutte le lettere enunciative di p
     p = p.replace(" ", "") #Fa un trim sulla stringa
     lenuns = []
     start= 0
     control = False
     for i in range(len(p)):
         print("len p=", len(p))
         print("ciclo ",i, "control = ", control)
         if p[i] in (["(",")"] + L):
            print("Trovato simbolo")
            if control:
                print("lettera enunciativa")
                
                lenuns.append(p[start:i])
                start = i+1
                control = False
            continue
         if not control: start = i
         control = True
     if control: #Se termina senza parentesi lascia fuori l'ultima lettera enunciativa
         lenuns.append(p[start:len(p)])
     return lenuns
        

def checkParentesi(p):
    #Controlla se non ci siano delle parentesi esterne superflue
    barra = 0
    parSup = True
    if not(p.startswith("(") and p.endswith(")") ): return p #se non inizia e finisce con delle parentesi certamente non è chiuso tra partentesi superflue
    test = p[1:len(p)-1] #elimina la prima e l'ultima partentesi e controlla se la formula ha ancora senso
    for i in test:
        if not i in ["(",")"]: continue
        if i == "(":
            barra+=1
        elif i == ")":
            barra-=1
        if barra<0:
            parSup = False
            break

##    if parSup: #Se le parentesi esterne erano superflue, restituisce la versione senza di esse, altrimenti restituisce p
##        print("Parentesi superflue. Versione migliorata: ", test)
##    else:
##        print("Parentesi non superflue. Restituisco ", p)
        
    if parSup: #Se le parentesi esterne erano superflue, restituisce la versione senza di esse, altrimenti restituisce p
        return test
    else:
        return p
        

def computa(p): #p è la formula, f l'insieme delle formule
    counter=0
    start = 0
    index=0
    par =False
    
    f = []

    p = p.replace(" ", "") #Fa un trim sulla stringa
            
    if isLenun(p): #Se la formula è una lettera enunciativa allora ritorna False
        f.append(p)
        if checkAssegnamenti and not p in lettereEnunciativeF :
            lettereEnunciativeF.append(p) #Inserisce la lettera nella lista relativa per il check finale
        return False

    p = checkParentesi(p)
    
    if p[0] == "!": #Se il primo simbolo è la negazione allora si risolve tutto immediatamente
        f.append(p[1:])
        f.append("!")        
        return f
    
    for i in p:
        index+=1
        if i=="(":                           
            if not par: start= index #Se è la prima parentesi aperta allora posiziona lo start in quel punto.
            par = True #Indica che ha trovato parentesi aperte
            counter+=1
        elif i==")":
            counter-=1
        if counter == 0 and par:
            par = False
            counter = 0
            f.append(p[start:index-1]) #Aggiunge la funzione alla lista delle funzioni
            #Se ha appena inserito una formula, significa che subito dopo ci deve essere un operatore, altrimenti la formula non è ben formata
            if len(f)==1:
                if p[index] in L:
                    f.append(p[index]) #Aggiunge l'operatore
                    start = index
                else:
                    print("ERRORE: formula non ben formata")
                    return None
    if len(f)<3:
        f.append(p[start+1:index])
    
    return f        
            

def computaricorsiva(f):
    #f deve essere un vettore di due o tre elementi del tipo (a, operatore binario, b) o (a, negazione)
    x = computa(f[0]) #Primo ramo
    if x != False:
        f[0] = x
        f[0] = computaricorsiva(f[0])
    if len(f)>2: #Se non si tratta di una negazione valuta anche la seconda formula
        x = computa(f[2])
        if x != False:
            f[2] = x
            f[2] = computaricorsiva(f[2])
    return f
    

def isTautologia(f, val): #f è la funzione da valutare, val il valore che deve avere, dominio è l'insieme dei valori necessari delle lettere enunciative
    #La funzione ritorna True se è una tautologia, o il dominio se non lo è
    
    if isLenun(f): #Se è una lettera enunciativa l'unico assegnamento è il suo valore        
        return [ {f : val} ]

    assegnamenti = []
    condizione = []
    if val:
        condizione = semV[f[1]]
    else:
        condizione = semF[f[1]]

    print("\nLe condizioni per ", (f,val), " sono: ", condizione)

    for cond in condizione: #Cond è una lista di coppie ordinate di True, False e None. None sta ad indicare che non importa il valore di quell'assegnamento
        print("\nEsamino la condizione: ", cond, " per ", f)
        x = isTautologia(f[0], cond[0])
        if x == []: #Se x è un insieme vuoto allora f[0] è una tautologia o una formula sempre falsa. Questo implica che non è nemmeno necessario valutare l'altra formula. f non può sostenere questa configurazione
            continue

        if len(f) <= 2 or cond[1] == None: #Se la funzione è solo una negazione, allora non possiede un altro ramo da valutare. Anche se non è necessario valoutare il ramo (cond = None) si passa avanti
            assegnamenti += x #Inserisce direttamente l'assegnamento tra quelli coerenti
            continue
        y = isTautologia(f[2], cond[1])
        if y == []: #Se y è un insieme vuoto allora f[0] è una tautologia o una formula sempre falsa.
            continue

        print("\nConfronto assegnamenti per", f, "\nGli assegnamenti sono:",x,y)
        ass = confrontaAssegnamenti([x,y])

        assegnamenti += ass
        print("\nAssegnamenti coerenti: ", ass)
    
    print("\nAssegnamenti: ", assegnamenti)
    #Infine si passa a valutare la compatibilità degli assegnamenti
    
    return assegnamenti
    

def confrontaAssegnamenti(d):
    #Da una lista di due classi di assegnamenti, d, opera un confronto e restituisce soltanto gli assegnameti compatibili tra loro
    # d è composto da assegnamenti parziali, che non ricopriono tutti i valori delle lettere enunciative
    ass = []

    if d[0] == []: #E' possibile che uno dei due tronconi sia completamente vuoto. In questo caso restituisce direttamente gli assegnamenti
        return d[1]
    elif d[1] == []:
        return d[0]
    
    for a1 in d[0]:
        for a2 in d[1]:
            assegnamento = dict()
            incompatibile = False
            
            for i in a1:
                #print(i, a1[i], a2[i])
                if (not(i in a2)) or (a1[i] == a2[i]): #Se in a2 non c'è la lettera enunciativa, o se ha lo stesso valore                    
                    assegnamento[i] = a1[i]
                else: #Se vi è una contraddizione tra i valori necessari allora i due assegnamenti a1 e a2 sono incompatibili
                    incompatibile = True
                    break #Passa al prossimo dizionario da confrontare

            if not incompatibile: #Esamina anche gli elementi di a2, che potrebbero non essere nell'assegnamento
                for i in a2:
                    if (not(i in a1)): #Se in a1 non c'è la lettera enunciativa                        
                        assegnamento[i] = a2[i]                
            if not incompatibile:
                ass.append(assegnamento)
    return ass
                    

def Valuta(f, ass): #valuta una formula usando l'assegnamento dato

    if isLenun(f):
        return ass[f]
    
    #Primo ramo
    A = Valuta(f[0], ass)

    if len(f) <=2:  #Se è una negazione, il suo valore sarà necessariamente il contrario valore di A
        return not A
    
    #Secondo ramo
    B = Valuta(f[0],ass)

    #Valuta il valore finale. f[1] è il connettivo
    if [A,B] in semV[f[1]]:
        return True
    else:
        return False

# FUNZIONI DI TEST

def testcomputa():
    frase = input("Frase: ")
    formule = computaricorsiva(computa(frase))
    #formule = computa(frase, [])
    print(formule)

def testvalore():
     global checkAssegnamenti
     checkAssegnamenti = True
     frase = input("Frase: ")
     formule = computaricorsiva(computa(frase))
     print ("L'albero è: ", formule)
     print("Le lettere enunciative sono", lettereEnunciativeF)
     x = isTautologia(formule, False)
     if len(x)>0:
         print("I contromodelli sono: ", x, "\nNon è una tautologia")
     else:         
         if Valuta(formule, creaAssegnamento(lettereEnunciativeF)):             
             print("\nNon ci sono contromodelli: ", x, "\nE' una tautologia")
         else:
             print("\nNon ci sono modelli che la rendano vera: ", x, "\nE' sempre falsa")
     
def testparentesi():
    frase = input("Frase: ")
    checkParentesi(frase)

def testvaluta():
    global checkAssegnamenti
    checkAssegnamenti = True
    frase = input("Frase: ")
    ass = input("Scrivere l'assegnamento rispettando la seguente forma: a:1 - b:0 - ecc\nRicorda che 0 è False e 1 è True\n Assegnamento: ")
    ass = leggiAssegnamento(ass)
    print("L'assegnamento è ", ass)
    formule = computaricorsiva(computa(frase))
    x = Valuta(formule, ass)
    print("\nIl valore finale è ", x)

def main():
    while(True):
        global checkAssegnamenti
        checkAssegnamenti = False
        #testparentesi()
        testvalore()
        #testcomputa()
        #testvaluta()
        if input("Continua? y/n") !="y": break
    

main()
    
