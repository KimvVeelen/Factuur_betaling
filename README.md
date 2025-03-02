# Factuur_betaling
Python project waar facturen aan betalingen worden gekoppeld.

Opgezet in python laad de code twee excel bestanden met de module Pandas (Declaratieoverzicht_dummy.xlsx en Bankbijschriften_dummy.xlsx). Dexlaratieoverzicht_dummy.xlsx bevat een overzicht van de verzonden facturen. Bankbijschriften_dummy.xlsx is een uitdraai van de bankrekening en laat alle betalingen zien. 
<br>
afbeelding
afbeelding
<br>
De twee documenten worden met elkaar vergeleken. Pandas maakt vervolgens een nieuw excel document waar de resultaten van de vergelijking zichtbaar in zijn (definitief_Overzicht<dag>-<maand>-<jaar>_<uur>_<minuut>.xlsx). Er wordt aangegeven of de betalingen zijn betaalt, van elkaar verschillen (indien dit zo is, wordt er aangegeven hoe groot dit verschil is).
<br>
afbeelding
<br>
<br>
Gemiddelde duur betaling per klant:
<br>
Duur_betaling_perklant.ipynb haalt uit het nieuw gegenereerde overzicht een diagram waarin zichtbaar wordt hoe lang elke klant gemiddeld doet over een betaling. Daaronder is een diagram welke de P waarde laat zien (Hoe waarschijnlijk is het dat we het eerste diagram voor waarheid kunnen aanzien). Gezien de dummy bestanden weinig data bezitten, is de P waarde vanzelfsprekend 1. Naarmate de bestanden meer data bevatten, zal deze waarde dalen.
Als vervolg heb ik een vergelijkbaare notebook gemaakt om inzicht te krijgen in de toekomstige omzet per maand, met succes. 
