import csv
import os
import glob
import matplotlib.pyplot as plt

sizes = [153,160,114,117,138,126,50,60,149,51]
folders = ["Coaster","Coaster2","Diving","Drive","Game","Landscape","Pacman","Panel","Ride","Sport"]

for f in range(len(folders)):

    listOfFile = glob.glob("./../Dataset/"+folders[f]+"/Tiles/*.csv")
    listofset = []
    listoflist = []
    stop = False

    #  leggo i vari file e salvo tutti i tiles riga per riga in una lista di set per non avere doppioni.
    #  Valido per qualsiasi tipo di file con le caratteristiche appropiate
    for i in range(len(listOfFile)):
        with open(listOfFile[i], newline="", encoding="ISO-8859-1") as filecsv:
            lettore = csv.reader(filecsv,delimiter=",")
            header = next(lettore)
            l=0
            while True:
                if not stop:
                    listofset.append(set())
                try:
                    riga = next(lettore)
                except:
                    break
                for m in range(1,(len(riga))):
                    listofset[l].add(riga[m])
                l=l+1
            stop = True



    Xpixel = 3840
    Ypixel = 1920
    Ygraphpercentage = []
    Ygraphmoregranularity = []

    # disegno un grafico  x: #frame  y: #percentuale pixel-tiles visti
    for i in range(1800):
        Ygraphpercentage.append ((len(listofset[i]))*192*192/(Xpixel*Ypixel))

    plt.plot(Ygraphpercentage)
    plt.axis([0, 1800, 0, 1])
    plt.title("Percentuale di visualizzazione per frame")
    plt.xlabel("# Frame")
    plt.ylabel("% visualizzato")
    fig = plt.gcf()
    fig.set_size_inches(21, 9)
    fig.savefig("./../Output/"+folders[f]+"/"+folders[f]+"_Tiles_Percentuale-In-Aria-Per-Frame.png", dpi=100)
    plt.close('all')

    # disegno un grafico a granularità maggiore raggruppando i frame di un secondo (30)
    # x: #secondi y: #percentuale pixel-tiles visti
    for i in range(60):
        Ygraphmoregranularity.append(sum(Ygraphpercentage[i*30:i*30+30])/30)

    plt.plot(Ygraphmoregranularity)
    plt.axis([0, 60, 0, 1])
    plt.title("Percentuale di visualizzazione per secondo")
    plt.xlabel("# Secondi")
    plt.ylabel("% visualizzato")
    fig = plt.gcf()
    fig.set_size_inches(21, 9)
    fig.savefig("./../Output/"+folders[f]+"/"+folders[f]+"_Tiles_Percentuale-In-Aria-Per-Secondo.png", dpi=100)
    plt.close('all')

    # Salvo su un file di testo la percentuale totale
    text_file = open("./../Output/" + folders[f] +"/"+folders[f]+"_Tiles_Percentuale-Utilizzo-Totale.txt", "w")
    text_file.write(str(sum(Ygraphpercentage) / 1800))
    text_file.close()


    #  creo il file con numero di frame, percentuale di visione del frame e i tiles visti, l'ultima riga è il totale di
    #  tiles visti nell'insieme del video.
    #  La percentuale non è valida se i tiles per frame sono diversi da 200 in totale.

    with open("./../Output/"+folders[f]+"/"+folders[f]+"_Tiles_Totale-Visti-Per-Frame.csv", 'w', newline='') as filecsv:
        wr = csv.writer(filecsv)
        wr.writerow(["frame","% tiles visti","tiles"])
        totale = 0
        for x in range(1, 1801):
            setToList = list(listofset[x-1])
            setToList.insert(0, x)
            totale = totale + len(listofset[x-1])
            setToList.insert(1, len(listofset[x-1])/200)
            wr.writerow(setToList)
        wr.writerow(["Totale in percentuale " + str(totale/(1800*200))])


    # Calcolo il risparmio di spazio
    text_file = open("./../Output/" + folders[f] +"/"+folders[f]+"_Tiles_DimensionSave.txt", "w")
    text_file.write("%0.2f" % ((sum(Ygraphpercentage) / 1800) * sizes[f]) + " / " + str(sizes[f]))
    text_file.close()


# print (y)
# print(yyy)
# mediay = sum (y) / len(y)
# sumfordev = 0
# for i in range(1800):
#     temp = (y[i] - mediay)
#     sumfordev = sumfordev + temp*temp
# stdev = math.sqrt(sumfordev/1800)
# print(stdev)
# plt.plot(y)
# plt.axis([0, 1800, 0, 225])
# plt.xticks([200*k for k in range (10)])
# x = list(range(1,1801))
# err = [stdev] * 1800
# print(x)
# plt.errorbar(x, y, yerr=(err,err), ecolor="red")
# plt.title("Frame e tiles")
# plt.xlabel("# Frame")
# plt.ylabel("# Tiles visualizzati nel frame")
# plt.show()