"""MO data handling tools"""
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class MoProbData:

    def __init__(self, oly: str, rnd: str, okl: str, itm: str):
        self.oly: str = f'{oly:02s}'
        self.rnd: str = rnd
        self.okl: str = f'{okl:02s}'
        self.itm: str = itm
        self.tag: str = ''
        self.anw: list[tuple[str, str, str]] = [(self.oly, self.rnd, self.okl)]

    def moNr(self) -> str:
        return f'{self.oly}{self.okl}{self.rnd}{self.itm}'

    def _compStr(self):
        return f'{self.oly}{self.rnd}{self.okl}{self.itm}'

    def __lt__(self, other):
        return self._compStr() < other._compStr()

    def info(self) -> str:
        infoStr = self.moNr()
        if len(self.tag) > 0:
            infoStr += f' @{self.tag}'
        if len(self.anw) > 1:
            infoStr += f' » {" ".join(map(str, self.anw[1:]))}'
        return infoStr


class MoOlyData(list[MoProbData]):

    def __init__(self):
        super(MoOlyData, self).__init__([])
        self.jsonData: dict = {}
        self._isOK: bool = False

    def loadJSON(self, jsonFilePath: Path):
        with jsonFilePath.open(mode='rt') as jsonFile:
            logger.info(f'lade Daten aus {jsonFile.name}')
            self.jsonData.update(json.load(fp=jsonFile))

    def procOldJSON(self):
        for oly in self.jsonData:
            for (rnd, rndData) in self.jsonData[oly].items():
                logger.info(f'verarbeite MO {oly}-{rnd}')
                oklList = [key for key in rndData.keys() if not key.endswith('Links')]
                for okl in oklList:
                    for itm in range(sum(rndData[okl])):
                        prob = MoProbData(oly, rnd, okl, str(itm + 1))
                        moNr = prob.moNr()
                        if moNr not in rndData['texLinks']:
                            if len(rndData[okl]) > 1:
                                if itm < rndData[okl][0]:
                                    prob.tag = 'a'
                                else:
                                    prob.tag = 'b'
                            if moNr in rndData['texLinks'].values():
                                for (anw, moNr) in rndData['texLinks'].items():
                                    if prob.moNr() == moNr:
                                        prob.anw.append((oly, rnd, anw[2:4]))
                            self.append(prob)

    def procJSON(self):
        for oly in self.jsonData:
            for (rnd, rndData) in self.jsonData[oly].items():
                logger.info(f'verarbeite MO {oly}-{rnd}')
                oklList = [key for key in rndData.keys() if key not in ['parent','AB']]
                for okl in oklList:
                    for itm in range(sum(rndData[okl])):
                        prob = MoProbData(oly, rnd, okl, str(itm + 1))
                        moNr = prob.moNr()
                        if moNr not in rndData['parent']:
                            if len(rndData[okl]) > 1:
                                if itm < rndData[okl][0]:
                                    prob.tag = 'a'
                                else:
                                    prob.tag = 'b'
                            match okl:
                                case '06' | '08' | '10' | '12':
                                    childOkl = f'{int(okl) - 1:02d}'
                                    if childOkl not in rndData:
                                        prob.anw.append((oly, rnd, childOkl))
                                case '13':
                                    for dist in [1,2]:
                                        childOkl = f'{int(okl) - dist:02d}'
                                        if childOkl not in rndData:
                                            prob.anw.append((oly, rnd, childOkl))
                            if moNr in rndData['parent'].values():
                                for (anw, moNr) in rndData['parent'].items():
                                    if prob.moNr() == moNr:
                                        prob.anw.append((oly, rnd, anw[2:4]))
                            self.append(prob)

    def writeTTL(self, ttlFilepath: Path):
        if not self._isOK:
            self.procJSON()
        ttlWriter = TtlWriter()
        with ttlFilepath.open(mode='wt', encoding='utf8') as ttlFile:
            rnd = 0
            okl = 0
            for prob in self:
                if prob.rnd != rnd:
                    rnd = prob.rnd
                    print(ttlWriter.writeRndHeader(prob), file=ttlFile)
                if prob.okl != okl:
                    okl = prob.okl
                    print(ttlWriter.writeOklHeader(prob), file=ttlFile)
                print(ttlWriter.write(prob), file=ttlFile)


class TtlWriter:
    minOkl = 5
    maxOkl = 13
    webRoot = 'https://www.mathematik-olympiaden.de/aufgaben'

    oklSep = '#' * 30
    rndSep = '#' * 60
    # rndSep = f'{oklSep}\n{oklSep}'

    aLineFmt = ':MO-{:s} a mo:Problem ;'
    nrLineFmt = '\tmo:nr\t\t"{:s}" ;'
    pdfALineFmt = '\tmo:pdfA\t{0:s}/{1:s}/{2:s}/A{1:s}{3:s}{2:s}{4:s}.pdf ;'
    anwFmt = 'anw:MO-{:s}-{:s}-{:s}'
    anwLineFmt = '\tmo:anw\t{:s}'

    anwHeaderFmt = 'anw:MO-{0:s}-{1:s}-{2:s} a mo:Verwendung ;\n\tmo:oly "{0:s}";\tmo:rnd "{1:s}";\tmo:okl "{2:s}"\n.'

    def write(self, prob: MoProbData):
        moNr = prob.moNr()
        ttlList = [self.aLineFmt.format(moNr)]
        ttlList.append(self.nrLineFmt.format(moNr))
        ttlList.append(self.pdfALineFmt.format(self.webRoot, prob.oly, prob.rnd, prob.okl, prob.tag))
        anwStr = ', '.join([self.anwFmt.format(*anw) for anw in prob.anw])
        ttlList.append(self.anwLineFmt.format(anwStr))
        ttlList.append(".\n")
        return '\n'.join(ttlList)

    def writeOklHeader(self, prob: MoProbData):
        ttlList = [self.oklSep]
        return '\n'.join(ttlList)

    def writeRndHeader(self, prob: MoProbData):
        ttlList = [self.rndSep]
        for oklStr in [f'{okl:02d}' for okl in range(self.minOkl, self.maxOkl + 1)]:
            ttlList.append(self.anwHeaderFmt.format(prob.oly, prob.rnd, oklStr))
        ttlList.append("\n")
        return '\n'.join(ttlList)
