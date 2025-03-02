import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import re
from datetime import datetime

def factuurnrvinden(text):
    match = re.findall(r"A\d{7}", text)
    return match if match else None

def factuurgegevens_opzoeken(facturatiebestand):
    
    #Lijst van gebruikte rijen
    used_indices = []

    #Dit is de lijst waar we de uiteindelijke gegevens in willen plaatsen.
    gegevens = []

    #We gaan door het facturatie bestand heen itereren. Omdat het met Pandas is ingeladen kunnen we hier iterrows() voor gebruiken. We pakken
    #dan per rij de index (het rij nummer) en de rijen.
    for index, row in facturatiebestand.iterrows():
    
    #Als de index in used_indices voorkomt dan slaan we hem over.
        if index in used_indices:
            continue

    #Hier slaan we het factuur nr en het eerste bedrag, de factuur datum en de status op in variabelen.
        factnr = row["Factuur nummer"]
        bedrag = float(row["Bedrag"])
        klant = row["Ontvangende Partij"]

    #De factuur datum wordt hier omgezet in een datetime object, dit is voor mij magie.
        factdatum = row["Factuur datum"].to_pydatetime().date()
    #De status wordt later toegekent.
        status = ""
    #We voegen de index toe aan used_indices zodat deze niet opnieuw wordt gebruikt.
        used_indices.append(index)

    #We starten een nieuwe loop om met de bovenstaande waardes, vergelijkbare factuur nrs te vinden.
        for index2, row2 in facturatiebestand.iterrows():

    #We controleren of index2 niet gelijk is aan index, ook moet de index niet voorkomen in used_indices. Het factuur nr moet dan overeen komen 
    #met het eerder opgeslagen factuur nr in factnr. 
            if index2 != index and index2 not in used_indices and row2["Factuur nummer"] == factnr:

                #Als er aan de bovenstaande voorwaarden wordt voldaan, dan mag het bedrag in row2 bedrag opgeteld 
                #worden bij het bedrag in variabel bedrag.
                bedrag += float(row2["Bedrag"])

                #Om aan te geven dat deze regel is gebruikt en overgeslagen moet worden, wordt deze ook toegevoegd
                #aan de lijst met gebruikte rijen.
                used_indices.append(index2)

    #Als alles bij elkaar is opgeteld dan plaatsen we de gegevens in de lijst gegevens. Per entry creeren we een aparte lijst zodat we deze makkelijk
    #omzetten in een dataframe.
        gegevens.append([factnr, bedrag, factdatum, status, klant])
    return gegevens

def betalingen_opzoeken(bankbestand):
    gegevens = []
    used_indices = []
    for index, row in bankbestand.iterrows():
        if index in used_indices:
            continue
        factnr = factuurnrvinden(row["Mededelingen"])
        bedrag = float(row["Bedrag (EUR)"])
        betaaldatum = datetime.strptime(str(row["Datum"]), "%Y%m%d")
        indice = index +2
        gegevens.append([factnr, bedrag, betaaldatum, indice])
        used_indices.append(index)
    return gegevens

def optellen(lijst_met_factnr, factuurdata):
    bedrag = 0
    used_indices = []
    for nummer in lijst_met_factnr:
        for index, row in factuurdata.iterrows():
            if nummer == row["Factuurnr"]:
                used_indices.append(index)
                bedrag += row["Bedrag"]
    return bedrag, used_indices

def crossreverance(betalingen, factuurgegevens):
    used_indices = []
    gegevens = []
    tolerance = 0.01
    for index, row in factuurgegevens.iterrows():
        
        if index in used_indices:
            continue
        
        factuurnr_factuur = row["Factuurnr"]
        betaling_factuur = row["Bedrag"]
        datum_factuur = row["Fact datum"]
        status_factuur = "Komt niet voor in betalingen"
        betalingsbedrag = 0
        regel_in_betalingsdocument = 0
        datum_betaling = None
        klant = row["Klant"]
        
        for index2, row2 in betalingen.iterrows():
            
            factuurnr_betaling = row2["Factuurnr"]
            betaling_bank = row2["Bedrag"]
                        
            if factuurnr_betaling != None and factuurnr_factuur in factuurnr_betaling:
                used_indices.append(index)
                 
                if len(factuurnr_betaling) == 1:
                     if abs(betaling_factuur - betaling_bank) <= tolerance:
                         status_factuur = "Betaald"
                         datum_betaling = row2["Betaaldatum"]
                         betalingsbedrag = row2["Bedrag"]
                     else:
                         status_factuur = "Bedrag komt niet overeen"
                         regel_in_betalingsdocument = row2["Regel in document"]
                         datum_betaling = row2["Betaaldatum"]
                         betalingsbedrag = row2["Bedrag"]
                                
                else:
                    indices = []
                    betaling_factuur, indices = optellen(factuurnr_betaling, factuurgegevens)
                    used_indices.extend(indices)
                    if abs(betaling_factuur - betaling_bank) <= tolerance:
                        status_factuur = "Betaald"
                        datum_betaling = row2["Betaaldatum"]
                        betalingsbedrag = row2["Bedrag"]
                    else:
                        status_factuur = "Bedrag komt niet overeen"
                        regel_in_betalingsdocument = row2["Regel in document"]
                        used_indices.append(index)
                        datum_betaling = row2["Betaaldatum"]
                        betalingsbedrag = row2["Bedrag"]
            
        gegevens.append([factuurnr_factuur, betaling_factuur, betalingsbedrag, klant, datum_factuur, datum_betaling, status_factuur, regel_in_betalingsdocument])
    return gegevens