"""helper functions"""

import re

nrSplit = re.compile('(?P<oly>\d{2})(?P<okl>\d{2})(?P<rnd>\d)(?P<itm>\d)')
htmlBase = "https://www.mathematik-olympiaden.de/aufgaben"


def nr2link(nummer: str) -> str:
    nrMatch = nrSplit.match(nummer)
    oly = int(nrMatch['oly'])
    rnd = int(nrMatch['rnd'])
    htmlAdr = f"{htmlBase}/{oly}/{rnd}"

    wahl = ''
    if oly > 34:
        if rnd == 4 or (rnd == 3 and int(nrMatch['okl']) > 7):
            if int(nrMatch['itm']) < 4:
                wahl = "a"
            else:
                wahl = "b"
    aufgBlatt = f'A{nummer[:-1]}{wahl}.pdf'

    return f'{htmlAdr}/{aufgBlatt}'

if __name__ == '__main__':
    print(nr2link("611214"))
    print(nr2link("561243"))
