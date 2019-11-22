# Zweck dieses Projekts

In diesem Projekt sind erste Versuche zusammengetragen, Metadaten von Aufgaben
der Mathematikolympiade öffentlich in einem RDF-Format verfügbar zu machen.

## Allgemeine Bedingungen

Dieses Projekt ist auf github als Projekt *Metadaten* im
**github Organisationsaccount Mathematikolympiade** gehostet und damit
**öffentlich sichtbar**.

Dies ist einerseits intentional, da wir diese Metadaten der Allgemeinheit zur
weiteren Verwendung zur Verfügung stellen wollen.

Dies ist andererseits durch die am Projekt Beteiligten bei der Auswahl der zur
Verfügung gestellten Informationen zu berücksichtigen.

## Grundsätzliches

Für ein RDF-Projekt sind zwei grundsätzliche Fragen zu klären:
* Welche Namensräume sollen belegt werden?
* In welcher Weise sollen die Daten verfügbar gemacht werden?

### Namensraum

Namensräume sind vergleichbar den Verzeichnisnamen im Dateisystem hierarchisch
angeordnet und erlauben eine inhaltliche Strukturierung der zur Verfügung
gestellten Daten.  Über Namensraumpräfixe können hier weitere baumartige
Gruppierungen vorgenommen werden, wobei insbesondere der Namensraum der Wurzel
dieses Baumes, also das globale Namensraumpräfix, mit Bedacht gewählt werden
muss.

Die Wahl des globalen Namensraumspräfixes hängt stark davon ab, wer final die
Oberhoheit über die Weiterentwicklung der Daten in den Händen halten soll, da
auf die Daten über HTTP zugegriffen wird. Entsprechende Anfragen schlagen also
auf dem Server auf, welcher der Basisdomäne zugeordnet ist, so dass der
Inhaber dieser Domäne die Art der Präsentation und der Verwendung der Daten
weitgehend kontrollieren kann.

Da der MO e.V. die Oberhoheit über die Aufgaben hat und das auch so
bleiben soll, wurde als Basisadresse 

$base = https://www.mathematik-olympiaden.de/aufgaben/rdf

gewählt. 

### Datenhaltung

Ein RDF-Projekt kann seine Daten als **Dateien im Netz** zur Verfügung stellen
oder einen **RDF-Store** betreiben, welcher die Daten ausliefert.  Letzteres
hat den Vorteil, dass dieser in der Regel zugleich einen SPARQL-Endpunkt zur
Verfügung stellt, über den flexible Anfragen an den Datenbestand ausgeführt
werden können.  Dies ist vergleichbar zu einem klassischen SQL-Datenbankserver
und der Anfragesprache SQL.

Mischformen zwischen beiden Formen sind möglich, es sollte allerdings ein
klares Datenmanagement (was sind Primärdaten, was Sekundärdaten, wie
funktioniert ein Update der Datenbestände, wie deren Synchronisierung)
vereinbart sein.

Wie bei Datenbankservern auch können sich Webserver (Präsentationsmanagement)
und RDF-Store (Datenmanagement) auf unterschiedlichen Rechnern befinden, was
aber zusätzlichen technischen Aufwand mit sich bringt.

* [Mehr dazu](https://symbolicdata.github.io/LocalSparqlEndpoint)

Im aktuellen Ausbauzustand sind die Primärdaten im Turtle-Format in
verschiedenen Dateien im Verzeichnis `Daten` abgelegt.  

Näheres hierzu ist unter `Daten/README.md` zu finden.

Weiterhin wurde ein RDF-Store aufgesetzt, in dem einige Datenbestände einer
früheren Version eingespielt sind.  
* [SPARQL Endpunkt](http://pcai003.informatik.uni-leipzig.de:8893/sparql)

## Inhalt dieses Verzeichnisses

* Auswertungen - enthält die pdf-Dateien der Auswertungen der einzelnen
  Olympiaden, die unter [https://hg-graebe.de/MO-Auswertung/index.html] zum
  Download angeboten werden.
* Daten - enthält die aktuell zusammengetragenen Daten in mehreren
  Turtle-Dateien. Siehe dazu `Daten/README.md`.
* Queries.txt - Einige Beispiele für SPARQL-Anfragen an den RDF-Store. Zu
  überarbeiten.
* README.md - Diese Datei.
* utiltools - Python-Werkzeuge von Roger Labahn.
* web - Code einer Webpräsenz zur prototypischen Präsentation von
  Möglichkeiten.
* workbench - Werkbank von Hans-Gert Gräbe.
