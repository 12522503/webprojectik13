# Projectvoorstel IK13
Triviaspel
- Jesse van der Sluis
- Maxime van Munster
- Rowan Duits
## Samenvatting
We willen een online trivia spel maken, waarbij de politiek centraal staat. Het is een educatief spel zodat jongeren (ong. 15-25 jarigen) iets leren over de politiek, zodat zij deze informatie kunnen gebruiken bij het stemmen e.d. Hierbij kunnen meerdere spelers tegelijkertijd tegen elkaar spelen in een van te voren aangegeven/gekozen aantal rondes. Degene met de laagste score per ronde mag de categorie voor de volgende ronde kiezen. Per vraag zijn er punten te behalen/verliezen (afgestemd op moeilijkheidsgraad). Ook zijn er enkele jokers mogelijk om in te zetten. (bijvoorbeeld een verdubbelaar, dit is geen mvp)
## Features
-  MVP: Het kunnen invoeren van een gebruikersnaam om mee te spelen -> en tijdelijk opslaan hiervan;
-  MVP: Verschillende rooms kunnen hoster, waar elk spel aangemaakt kan worden (niet een room binnenkomen waar het spel al bezig is);
-  MVP: Van te voren aantal rondes kunnen kiezen;
-  MVP: Score kunnen bijhouden;
-  MVP: Finalespel (twee spelers met de hoogste score spelen knock-out);
-  Per ronde een categorie kunnen kiezen (eerste ronde kiest de host, verder kiest de slechtste speler (persoon met laagste score));
-  Het inzetten van jokers per ronde met als doel het halen van een hogere score:
* verdubbelaar (wanneer je zeker weet dat je antwoord goed is kan je de opbrengst verdubbelen, wanneer dit fout is krijg je dubbele aftrek);
* 50/50 (twee foute antwoorden worden verwijderd uit de multiple choice opties);
* joker (1x goed antwoord).

## Afhankelijkheden
Onze webpagina zal afhankelijk zijn van verschillende onderdelen:
### Databronnen
-  Database zoeken, als deze er niet is: zelf maken;
### Externe componenten
-  Bootstrap voor het maken van een website
-  Mogelijke andere CSS bestanden voor een specifieke opmaak
### Concurrentie
Er bestaan natuurlijk al verschillende andere websites waar je games kan spelen. Wij willen echter een website maken waar je nog wat kan leren over de politiek en een knock-out finaleronde kan spelen.
### Moeilijkheden
- Hoe werkt het met het uploaden van je antwoord, naar welke computer/telefoon (device) moet dit, hoe verwerk je verschillende rondes.
- Het starten van het spel, hoe wordt dit gehost?
- Hoe zit de database in elkaar?

# Technisch Ontwerp IK13
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
- Als plugin zal er Flask-DebugToolbar gebruikt worden https://flask-debugtoolbar.readthedocs.io/en/latest/
