from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///webproject.db")

q = [["Welke fractievoorzitter is het jongste?", "Fractievoorzitters & Ministers", "Rob Jetten (D66)", "Jesse Klaver (GroenLinks)", "Lilian Marijnissen (SP)", "Thierry Baudet (FvD)", 30, -60],
["Wie is de fractievoorzitter van DENK?", "Fractievoorzitters & Ministers", "Tunahan Kuzu", "Esther Ouwehand", "Gert-Jan Segers", "Klaas Dijkhoff", 30, -60],
["Wie is Nederlands huidige Minister van Buitenlandse Zaken (BuZa)?", "Fractievoorzitters & Ministers", "Stef Blok", "Ank Bijleveld", "Carola Schouten", "Wopke Hoekstra", 60, -30],
["Sinds welk jaar is Mark Rutte premier van Nederland?", "Fractievoorzitters & Ministers", "2010", "2012", "2014", "2016", 60, -30],
["Van welke partij is Kees van der Staaij fractievoorzitter?", "Fractievoorzitters & Ministers", "SGP", "ChristenUnie", "50Plus", "PVV", 60, -30],
["GroenLinks is een linkse partij, dit wil zeggen dat…", "Politiek spectrum", "... deze partij veel waarde hecht aan gelijkheid en voorstander is van het toepassen van overheidsingrijpen",
"… deze partij veel waarde hecht aan traditionele regels", "… deze partij veel waarde hecht aan de vrije marktwerking en het bedrijfsleven", "… deze partij links in de tweede kamer zit", 30, -60],
["Welk van deze partijen bevinden zich veelal rechts in het politiek spectrum?", "Politiek spectrum", "VVD, CDA en PVV", "50Plus, GroenLinks en SP", "VVD, SP en Partij van de Dieren",
"PvdA, SP en D66", 30, -60],
["Naast de links/rechts oriëntatie zegt het politiek spectrum iets over…", "Politiek spectrum", "… in hoeverre de partijen progressief en conservatief zijn",
"… in hoeverre de partijen met elkaar samenwerken", "… in hoeverre de partijen macht hebben", "… in hoeverre de partijen zetels in de tweede kamer hebben", 60, -30],
["De links/rechts schaalverdeling is grotendeels gebaseerd op…", "Politiek spectrum", "… de standpunten van partijen m.b.t. thema’s als economie, zorg en belastingen",
"… de standpunten van partijen m.b.t. thema’s als klimaat, zorg en migratie", "… de standpunten van partijen m.b.t. thema’s als economie, belastingen en internationale samenwerking",
"… de standpunten van partijen m.b.t. thema’s als klimaat, migratie en internationale samenwerking", 60, -30],
["Welke zin is waar?", "Politiek spectrum", "	Meestal zijn linkse partijen progressief en rechtse partijen conservatief, maar dat hoeft niet altijd",
"Het politiek spectrum is zo ingedeeld dat alle linkse partijen progressief zijn en alle rechtse partijen conservatief zijn",
"Meestal zijn linkse partijen conservatief en rechtse partijen progressief, maar dat hoeft niet altijd",
"Het politiek spectrum is zo ingedeeld dat alle linkse partijen conservatief zijn en alle rechtse partijen progressief zijn", 60, -30],
["In welk land ontstond de bestuursvorm ‘democratie’?", "Geschiedenis", "Griekenland", "Italie", "Spanje", "Duitsland", 30, -60],
["In welk jaar werd de politicus Pim Fortuyn vermoord?", "Geschiedenis", "2002", "2001", "2004", "2003", 60, -30],
["Welke filosoof bedacht de verdeling genaamd ‘trias politica’?", "Geschiedenis", "Montesquieu", "John Locke", "Rene Descartes", "Thomas Hobbes", 30, -60],
["Wat is de oudste partij van Nederland?", "Geschiedenis", "SGP", "VVD", "CDA", "SP", 60, -30],
["Vanaf welk jaar hebben vrouwen actief kiesrecht?", "Geschiedenis", "1919", "1917", "1912", "1915", 60, -30],
["Van wie is de uitspraak ,Ik heb zestien miljoen bazen.'?", "Uitspraken", "Mark Rutte (VVD)", "Geert Wilders (PVV)", "Alexander Pechtold (D66)", "Jesse Klaver (GroenLinks)", 60, -30],
["Van wie is de uitspraak ,Ik zou het liefst allemaal persoonlijk in elkaar willen slaan die lui die dat doen. Maar dat gaat niet.’?", "Uitspraken", "Mark Rutte (VVD)", "Geert Wilders (PVV)",
"Tunahan Kuzu (DENK)", "Thierry Baudet (FvD)", 30, -60],
["Van wie is de uitspraak ,Meer CO2 heeft geweldig positief effect op plantengroei.’?", "Uitspraken", "Thierry Baudet (FvD)", "Mark Rutte (VVD)", "Geert Wilders (PVV)", "Sybrand Buma (CDA)", 60, -30],
["Van wie is de uitspraak ,Caroliene, ik ben het even kwijt. Help!’ ?", "Uitspraken", "Mark Rutte (VVD)", "Thierry Baudet (FvD)", "Alexander Pechtold (D66)", "Sybrand Buma (CDA)", 60, -30],
["Van wie is de uitspraak ,Willen we meer of minder Marokkanen?’?", "Uitspraken", "Geert Wilders (PVV)", "Thierry Baudet (FvD)", "Sylvana Simons (BIJ1)", "Emile Roemer (SP)", 30, -60]]


# Insert questions into database
for question in q:
    db.execute("INSERT INTO questions (question, category, correctanswer, answer2, answer3, answer4, pointscorrect, pointsincorrect) VALUES(:q, :c, :correct, :a2, :a3, :a4, :yes, :no)",
                q=question[0], c=question[1], correct=question[2], a2=question[3], a3=question[4], a4=question[5], yes=question[6], no=question[7])
