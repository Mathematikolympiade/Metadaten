# Zweck dieses Projekts

In diesem Projekt sind erste Versuche zusammengetragen, Metadaten von Aufgben
aus der Mathematikolympiade öffentlich verfügbar zu machen.

## Ontologie 

Das Projekt ist darauf ausgelegt, im Namensraum
<https://www.mathe-wettbewerbe.de/mo/rdf/> alle relevanten Daten als [Linked
Open Data](https://de.wikipedia.org/wiki/Linked_Open_Data) zu sammeln und nach
[allgemein verwendeten RDF-Standards](https://www.w3.org/RDF/) verfügbar zu
machen.

Neben gebräuchlichen allgemeinen Ontologien
* rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
* rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
* owl: <http://www.w3.org/2002/07/owl#> 

wird im Namensraum
* mo: <https://www.mathe-wettbewerbe.de/mo/rdf/Model#>

eine Ontologie zur Beschreibung der relationalen und prozessualen Aspekte rund
um die MO-Aufgaben erstellt, die zu einem späteren Zeitpunkt genauer zu
beschreiben sein wird.

Änderungen an der Ontologie sind ohne weitere Vorwarnung möglich,
Rückwärtskompatibilität kann zum gegenwärtige Zeitpunkt nicht garantiert
werden.

## Daten

Basis für einen ersten Pitch sind die Metadaten der AAG 9/10 der MO 41 bis 55,
die in der Datei `MO-Aufgaben.ttl` zusammengetragen sind und weiter
angereichert werden sollen.

Dabei wird der Namensraum <https://www.mathe-wettbewerbe.de/mo/rdf/Aufgabe/>
sowie ein aus der Aufgabennummer abgeleiteter Bezeichner als URI für die
einzelnen Aufgaben verwendet.

# Web

Dieser Abschnitt muss überarbeitet werden. 

Im Verzeichnis `web` ist der Code eines ersten Pitches enthalten, wie diese
Daten ausgewertet werden können. Der Code verwendet die EasyRDF PHP-Bibliothek
und greift aktuell auf den RDF Triple Store des KoSemNet-Projekts
https://lsgm.uni-leipzig.de/KoSemNet/MetaInformations.php zu.

# Auswertungen

Im Verzeichnis `Auswertungen` sind die pdf-Dateien zusammengetragen, die auf
der Seite https://hg-graebe.de/MO-Auswertung/index.html verlinkt sind.

Vernetzungen mit weiteren Aufgabengruppen sowie eine Erweiterung der
verfügbaren Metadaten ist geplant.