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
- Als plugin zal er Flask-DebugToolbar gebruikt worden https://flask-debugtoolbar.readthedocs.io/en/latest/, 
het downloaden hiervan is uiteindelijk niet gelukt en is deze plugin dus ook niet gebruikt.
