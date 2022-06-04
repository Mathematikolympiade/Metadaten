"""Roger's RDF store: subject handling tools"""
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class TocConverter:

    def readTXT(self, txtFilePath: Path) -> None:
        with txtFilePath.open(mode='rt', encoding='utf8') as txtFile:
            for line in txtFile:
                print(line.rstrip())