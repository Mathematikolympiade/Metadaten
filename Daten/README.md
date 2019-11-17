# Datenverzeichnis des Projekts

## Inhalt dieses Verzeichnisses

* AAG9-Intern.ttl - RDF-Datei mit Metadaten (u.a. Gebiete, Schwierigkeit) aus
  dem Aufgabenschatz der AAG 9/10, wie er dort zur Klassifizierung von
  Aufgaben seit vielen Jahren verwendet wird.  Die Daten sind aus den
  AAG-internen Klassifizierungsdaten ("Aufgaben-Kopf") extrahiert, enthalten
  aber auch weitere Informationen zur Geschichte und zum Verwendungsstand der
  einzelnen Aufgaben, die früher in einer History-Datei der AAG
  zusammengetragen wurden.
* Cube.ttl - Transformation einer Zuarbeit von Roger in das Format des [RDF
  Data Cube](https://www.w3.org/TR/vocab-data-cube/).  Noch sehr
  experimentell.
* MO-AufgabenTexte.ttl - Übernahme einer nicht konsolidierten Version der
  Aufgabentexte aus den Arbeiten von Manuela Kugel, die auf deren Seiten für
  eine Volltextsuche verwendet wurde.
* MO-Aufgaben.ttl - konsolidierte Version der Datei `AAG-9-Intern.ttl`, welche
  nur die Gebiete und Schwierigkeiten bereits publizierter MO-Aufgaben enthält
  und diese konkreten Aufgabennummern zuordnet.
* Modell.ttl - RDF-Datei, die eine Beschreibung des verwendeten Datenmodells
  enthält.
* moProbleme.ttl - Ursprüngliche Daten von Roger, die in den RDF Cube
  `Cube.ttl` verwandelt wurde.

## Allgemeines

### Ontologie 

Das Projekt ist darauf ausgelegt, im Namensraum
<https://www.mathematik-olympiaden.de/aufgaben/rdf/> alle relevanten Daten als
[Linked Open Data](https://de.wikipedia.org/wiki/Linked_Open_Data) zu sammeln
und nach [allgemein verwendeten RDF-Standards](https://www.w3.org/RDF/)
verfügbar zu machen.

Neben gebräuchlichen allgemeinen Ontologien
* rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
* rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
* owl: <http://www.w3.org/2002/07/owl#> 
* qb:  <http://purl.org/linked-data/cube#>

wird im Namensraum ($base = https://www.mathematik-olympiaden.de/aufgaben/rdf) 
* mo: $base/Model#

eine Ontologie zur Beschreibung der relationalen und prozessualen Aspekte rund
um die MO-Aufgaben erstellt, deren aktueller Stand weiter unten genauer
beschrieben ist. Ein erster Beschreibungsansatz ist auch im RDF-Format in der
Datei Modell.ttl enthalten (Zuarbeit von Roger), der weiter auszubauen ist.

Änderungen an der Ontologie sind ohne weitere Vorwarnung möglich,
Rückwärtskompatibilität kann zum gegenwärtige Zeitpunkt nicht garantiert
werden.

### Weitere standardisierte Namensraum-Konzepte

Für Aufgaben
* RDF-Typ mo:Problem
* Namensraumpräfix mop: $base/Aufgabe/
* Namensgebungsregel: mop:MO-<Aufgabennummer>
* Beispiel: mop:MO-450731

Für Aufgabengebiete
* RDF-Type mo:Kategorie
* Namensraumpräfix mog: $base/Gebiet/
* Namensgebungsregel: mog:<String>
* Beispiel: mog:Kombinatorik

Für Aufgabenvorschläge (nur `AAG9-Intern.ttl`)
* RDF-Typ mo:Aufgabenvorschlag
* Namensraumpräfix moa: $base/AufgabenVorschlag/
* Namensgebungsregel: moa:MO-<InterneKennung>
* Beispiel: moa:MO-bey-00-01

Für den RDF Data Cube (nur `Cube.ttl`)
* RDF-Typ qb:Observation 
* Namensraumpräfix : moo: $base/Observation/
* Namensgebungsregel: moo:o<Laufendenummer> (Einige Werkzeuge haben Probleme
  mit Kennungen, die mit einem numerischen Zeichen beginnen)
* Beispiel: moo:o236

## Daten. Allgemeines

Basis für einen ersten Pitch sind die Metadaten der AAG 9/10 der MO 41 bis 55,
die in der Datei `MO-Aufgaben.ttl` zusammengetragen sind und weiter
angereichert werden sollen.  Dabei wird der Namensraumpräfix `$base/Aufgabe/`
sowie ein aus der Aufgabennummer abgeleiteter Bezeichner als URI für die
einzelnen Aufgaben verwendet.

Aus den Aufgabenvorschlägen der AAG 9/10 wurden weiter Kategorien und
Schwierigkeitsgrade extrahiert, die dort bei der Vorsortierung der Aufgaben
seit Längerem verwendet werden.

Roger Labahn hat in `moProbleme.ttl` eine Reihe von Aufgabeninformationen
zusammengetragen. Hier ist eine Trennung zwischen den Informationen zu
konkreten Aufgaben und der Zuordnung zu Olympiaden (die im Prinzip auch aus
den Aufgabennummern inferiert werden kann) sinnvoll, wobei die relationalen
Informationen in einen RDF-Cube ausgelagert werden sollten, wie dies
prototypisch in `Cube.ttl` geschehen ist. Das ist noch nicht ausdiskutiert,
siehe unten.

Schließlich wurden aus einem Projekt von Manuela Kugel Aufgabentexte
übernommen, die dort mit klassischen Werkzeugen aus den Aufgaben-pdf
extrahiert und prototypisch zur Suche in den Aufgabentexten verwendet wurden.
Die Aufgabentexte sind weiter zu konsolidieren, da die Extraktionswerkzeuge
insbesondere mit mathematischen Formeln ihre Probleme haben.

Das aktuelle Datenmodell ist im Weiteren genauer beschrieben.

## Datenmodell

### AAG9-Intern.ttl

Aus dem Datenbestand der AAG 9/10 wurden von bereits gestellten Aufgaben und
Aufgaben im Schatz (ich halte diese Informationen, selbst wenn sie sich auf
Aufgaben beziehen, die noch nicht gestellt wurden, nicht für kritisch) die
verwendeten Gebietseinordnungen und Schwierigkeitsgrade extrahiert.  Außerdem
wurden Informationen zur Historie der Aufgabenvorschläge aufgenommen, wenn sie
aus dem Schatz aussortiert wurden, ohne für eine Olympiade verwendet worden zu
sein.

Struktur der Datensätze:

mo:AufgabenVorschlag
* mo:hasSubtype Literal - noch genauere thematische Einordnung der Aufgabe
* mo:hasType Literal - genauere thematische Einordnung der Aufgabe
* mo:hatSchwierigkeit Integer - Wert im Bereich 1..5, entspricht grob der
  Stufe, in welcher die Aufgaben gestellt werden könnte. In älteren Aufgaben
  auch eine verbale Angabe (niedrig/mittl/hoch)
* mo:hatStatus Literal - Status der Aufgabe (Stand aber nicht aktuell)
* mo:zumGebiet Literal - Komma getrennte standardisierte Angabe von Gebieten 
* owl:sameAs URI - Ein oder mehrere (wenn in beiden Klassenstufen gestellt)
  Verweise auf eine mo:Aufgabe (aktuell noch rdf/AufgabenVorschlag)

Nicht alle Prädikate wurden über die ganze Zeit vergeben. 

### Cube.ttl

In diesem RDF-Graphen sollen subjektive Informationen zu den einzelnen
Aufgaben zusammengetragen werden. Dazu soll das Format des RDF Data Cube
verwendet werden, das mit dem Datentyp qb:Observation gut geeignet ist,
derartige Informationen systematisch zu erfassen.

Datentyp qb:Observation;
* qb:dataSet qb:DataSetDefinition - diese enthält die Metainformationen über
  die Struktur der in der Observation zusammengetragenen Information.  In der
  aktuellen Ausprägung wird hier einfach mit einer nicht weiter untersetzten
  URI gearbeitet.  Die entsprechende Metainformationen kann zunächst informell
  erfasst werden. Eine Konsolidierung als formale Information ist nur
  erforderlich, wenn die Daten automatisiert weiterverarbeitet werden sollen.
  Über diesen Mechanismus lassen sich auch Observationen zu *mehreren*
  DataSetDefinitions miteinander kombinieren.
* mo:Aufgabe mo:Problem - Verweis auf die Aufgabe, die in der Observation
  adressiert wird. Beispiel: mop:MO-450731. Dies ist eine qb:attributeProperty. 
* mo:okl Literal - Olympiadeklasse
* mo:oly Literal - Olympiade
* mo:rnd Literal - Runde 

Die letzten drei Properties sind vom Typ qb:dimensionProperty und hier nur zur
Erläuterung des Konzepts extrahiert, da diese Information zu den "objektiven"
Informationen gehört, die einem mo:Problem zugeordnet werden sollten und
keiner Observation.

Observation könnten zum Beispiel verwendet werden, um die verschiedenen
Erfolgsdaten einzelner Aufgaben in verschiedenen Regionen zu erfassen - hier
wäre das Anlegen mehrerer Observations zu einer Aufgabe sinnvoll. Es handelt
sich dann um eine Information, die Aufgabe und konkrete Bedingungen des Lösens
zueinander in Relation setzt.

Der RDF Data Cube setzt strukturell bekannte Data Warehouse Ansätze um, die
für die Auswertung entsprechender Informationen zur Performanz der einzelnen
aufgaben sinnvoll wären.

### MO-AufgabenTexte.ttl

Struktur der Datensätze: Ergänzt MO-Aufgaben
* mo:hatAufgabentext Literal

### MO-Aufgaben.ttl

In diesem RDF-Graphen sollen die relevanten "objektiven" Informationen über
einzelne Aufgaben zusammengetragen werden.

Datentyp mo:Problem
* mo:nr Literal - die Aufgabennummer. Beispiel: "441035" 
* mo:hasA9Tag mo:Kategorie - Beispiel: mog:Algebra
* mo:hatSchwierigkeit Literal - verschiedene Schemata, zuletzt 1..5

Datentyp mo:Kategorie
* rdfs:label Literal - Bezeichnung des Themengebiets

Hier sollten die Grunddaten zu den einzelnen Aufgaben zusammengetragen werden,
also insbesondere auch noch die Einträge 
* mo:okl Literal - Olympiadeklasse
* mo:oly Literal - Olympiade
* mo:rnd Literal - Runde

Unklar ist, wie modelliert werden kann, dass eine gleiche Aufgabe in
verschiedenen Klassenstufen gestellt wurde, denn diese Information geht vom
mo:Aufgabenvorschlag zum mo:Problem verloren. 

Offen ist weiterhin, ob diese Grundinformationen und das angestrebte Tagging
in einer RDF-Datei zusammengeführt werden sollen oder hierfür eine eigene
RDF-Datei angelegt wird wie für die Aufgabentexte. Das kann aber später
entschieden werden, da das Auftrennen nach verschiedenen Prädikaten kein
großes Problem ist.

### Modell.ttl

In dieser Datei sind perspektivisch die im Datenmodell definierten Klassen
genauer zu beschreiben. Aktuell ist diese Datei die Referenzdatei für
derartige Beschreibungen. 

### moProbleme.ttl

Von Roger Labahn extrahierte Daten.