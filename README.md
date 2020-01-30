# Beter dan Baudet
##### Groep IK.13
- Maxime van Munster
- Jesse van der Sluis
- Rowan Duits

## Productvideo
[Klik om te openen](https://drive.google.com/file/d/1CSdl0wol7E4pTuUDefKDdopg7xURSyGS/view?usp=sharing)

## Features
* Via het home scherm kan een kamer aangemaakt worden. De overige gebruikers kunnen vervolgens deze kamer selecteren. Hierdoor wordt een multiplayer spel gestart.
* De gebruikers komen vervolgens in een kamer terecht met een laadscherm. Als iedereen op "spel starten" heeft gedrukt wordt het spel automatisch gestart.
* In het spel heeft iedereen 20 seconde de tijd om de vraag te lezen en het antwoord te kiezen, de persoon met de laagste score mag de categorie van de volgende vraag bepalen.
* Elke speler kan 1x in het spel een joker inzetten, waardoor deze speler het antwoord altijd goed heeft
* In het spel wordt een score bijgehouden. Je krijgt plus punten bij een goed antwoord en min punten bij een onjuist antwoordt. Het aantal punten is gebasseerd op de moeilijkheidsgraad van de vraag.
* De vragen zijn door ons zelf bedacht en opgeslagen in de database in de tabel questions
* De twee spelers met de hoogste score kunnen doorgaan naar een knock-out finale ronde, de verliezers kunnen dit niet en worden gestuurd naar een pagina waar zij een review kunnen schrijven.
* De finale stopt wanneer enkel één speler de vraag goed heeft, deze wint automatisch het spel. Ook de finale spelers kunnen uiteindelijk een review achterlaten.


# Technisch ontwerp

## Controllers
- /index: POST en GET. Hier kun je zien welke rooms al bestaan en een kiezen om in mee te doen. Vanuit hier kun je ook verder naar zelf een room aanmaken.
- Hier hoort een scherm bij (een hmtl) met een link naar de route voor het aanmaken van een room.
- /makeroom: POST en GET. Hier kan een room worden aangemaakt. Hier wordt de roomnaam geregistreerd in een database. Ook wordt het aantal rondes geregistreerd.
- /room: POST en GET. Prompts gebruiker voor gebruikersnaam. Host geeft startsignaal bij 3+ spelers, pagina moet gerefreshed worden.
- /game: POST en GET. Hier wordt het spel gespeeld. Categorieën en vragen worden opgehaald uit de database.
- De score wordt meegenomen over de rondes.
- /ranking: POST en GET. Hier worden de scores bekeken waarbij de top twee kunnen klikken op "play final".
- /final: POST en GET. Hier spelen de twee beste de knock-out finale. Leidt naar eindscherm.
- /end: Eindscherm met score en winnaar.

## Views
- Zie plaatjes toegevoegd in map 'doc'.

## Models/helpers
returns error code
def apology ():
    return ??

takes questions out of db and randomizes them
def get_random_question ():
    return ??

When used question is always right
def joker ():
    return ??

when used 2 wrong answers disappear
def fifty ():
    return ??

when used points will double (even when wrong)
def double ():
    return ??

## Plugin/Frameworks
- Er zal gebruikt gemaakt worden van verschillende frameworks als bootstrap. Wanneer de front end van de site duidelijk wordt zullen we belsuit wel vormgeving deze zal krijgen.
- Als plugin zal er Flask-DebugToolbar gebruikt worden https://flask-debugtoolbar.readthedocs.io/en/latest/,
het downloaden hiervan is uiteindelijk niet gelukt en is deze plugin dus ook niet gebruikt.
