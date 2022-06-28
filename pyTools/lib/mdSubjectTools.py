"""Roger's RDF store: subject handling tools"""
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class TocDict(dict[str: str]):
    ttlHeader: str = '''
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

@prefix math: <https://www.mathematik-olympiaden.de/aufgaben/rdf/models/math#> .

math:Gebiet a rdfs:Class ;
	rdfs:comment	"Basis-Klasse für Gebiete" ;
	rdfs:label "Gebiet" .
'''

    def __init__(self):
        super(TocDict, self).__init__()
        self._labelPrefix = ''

    def readTXT(self, txtFilePath: Path) -> None:
        with txtFilePath.open(mode='rt', encoding='utf8') as txtFile:
            for line in txtFile:
                (nr, titel) = line.rstrip().split(' ', maxsplit=1)
                self[nr] = titel

    @staticmethod
    def normLabel(label: str) -> str:
        return label.replace('.', '-')

    @staticmethod
    def parentLabel(label: str) -> str:
        return label[:label.rfind('.')]

    def subjectLabel(self, label: str) -> str:
        return f'math:{self._labelPrefix}_T_{self.normLabel(label)}'

    def writeTTL(self, ttlFilePath: Path = None, labelPrefix: str = '') -> str:
        self._labelPrefix = labelPrefix
        ttlStr: str = self.ttlHeader
        for (label, thema) in self.items():
            ttlStr += f'\n{self.subjectLabel(label)} a math:Thema ;'
            ttlStr += f'\n\trdfs:label\t"{thema}" ;'
            subClassOfStr = self.subjectLabel(self.parentLabel(label)) \
                if len(label) > 1 else 'math:Gebiet'
            ttlStr += f'\n\trdfs:subClassOf\t{subClassOfStr} .\n'
        if ttlFilePath is not None:
            with ttlFilePath.open(mode='wt', encoding='utf8') as ttlFile:
                print(ttlStr, file=ttlFile)
                logger.info(f'wrote {ttlFile.name}')
        return ttlStr


class MoSubjData:

    def __init__(self, moNr: str):
        self.moNr: str = moNr
        self.thm: str = ''
        self.aut: str = ''

class TtlWriter:
    nrFmt = ':MO-{:s} a mo:Problem ;'
    autFmt = '\tmath:aut\t"{:s}" ;'

    def __init__(self, thmFmt: str):
        self.thmFmt = f'\tmath:thm\t{thmFmt} ;'

    def write(self, subj: MoSubjData):
        ttlList = [self.nrFmt.format(subj.moNr)]
        ttlList.append(self.thmFmt.format(subj.thm))
        ttlList.append(self.autFmt.format(subj.aut))
        ttlList.append(".\n")
        return '\n'.join(ttlList)

if __name__ == '__main__':
    print(TocDict.parentLabel('1.1.5'))
