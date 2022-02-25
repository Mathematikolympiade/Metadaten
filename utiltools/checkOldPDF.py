"""Roger's RDF store MO old data checker"""
import json
import logging
import os
import sys
import re
from argparse import ArgumentParser
from configparser import ConfigParser, ExtendedInterpolation
from datetime import datetime
from pathlib import Path

from requests import Session, Response
from PyPDF4 import PdfFileReader

configParams = """
    [DEFAULT]
        logToFile =   True

    #   fixed names & values
    [CONST]
        webRootURL = https://www.mathematik-olympiaden.de/aufgaben

    #   specific data

    #   workflow setup
    [WORK]
"""

#   lib logging

#   environment
inIDE = (os.environ.get('PYCHARM_HOSTED', 0) == '1')
compName = os.environ.get('COMPUTERNAME', 'SHERATAN')
#   control
argParser = ArgumentParser(description="Roger's RDF store MO old data checker")
argParser.add_argument('-w', '--workDir', dest='workDirName', default=".", help="working directory")
argParser.add_argument('-i', '--iniFile', dest='iniFileName', default=None, help="param ini file")
cmdLineArgs = f' --workDir={str(Path.home() / "Documents/MO/AA/work")}'
# if compName.upper() == 'LONG':
#     cmdLineArgs = ' --workDir=P:/Daten/NewsEye/GT_AS'
# cmdLineArgs += f' --iniFile={PurePosixPath(sys.argv[0]).with_suffix(".ini").name}'

if __name__ == '__main__':

    try:
        #   cmdLine
        if inIDE and 'cmdLineArgs' in globals():
            sys.argv.extend(cmdLineArgs.split())
        args = argParser.parse_args()

        #   inits
        workDirPath = Path(args.workDirName)
        if not workDirPath.is_absolute():
            workDirPath = (Path.cwd() / workDirPath).absolute()
        if workDirPath.is_dir():
            workDirMsg = f'working in {workDirPath}'
        else:
            raise RuntimeError(f'cannot find {workDirPath}!')

        #   config
        config = ConfigParser(interpolation=ExtendedInterpolation())
        if args.iniFileName is None:
            config.read_string(configParams)
            configMsg = 'using internal parameter config string'
        else:
            iniFilePath = Path(args.iniFileName)
            if not iniFilePath.is_absolute():
                iniFilePath = (workDirPath / iniFilePath).absolute()
            config.read(iniFilePath)
            configMsg = f'using parameter config file {iniFilePath}'

        #   logging
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(logging.Formatter(fmt='%(levelname)s %(message)s'))
        handlerList = [consoleHandler]
        if config['DEFAULT'].getboolean('logToFile', None):
            logBase = Path(sys.argv[0])
            logFilePath = (logBase.parent / 'logs' / logBase.stem).with_suffix('.log')
            with logFilePath.open(mode='w', encoding='utf8') as logFile:
                print(datetime.now().strftime('%y-%m-%d %H:%M:%S'), file=logFile)
            fileHandler = logging.FileHandler(logFilePath, mode='a', encoding="utf-8")
            fileHandler.setLevel(logging.DEBUG)
            handlerList.append(fileHandler)
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(module)s %(levelname)s\n\t%(message)s', datefmt='%H:%M:%S',
            handlers=handlerList
        )
        logging.info(f'running {Path(sys.argv[0])} …')
        logging.info('started in {:s}'.format(str(Path().cwd())))
        logging.info('using arguments {:s}'.format(' '.join(sys.argv[1:])))
        logging.info(workDirMsg)
        logging.info(configMsg)
        if config['DEFAULT'].getboolean('logToFile', None):
            logging.info(f'logging to {logFilePath}')

        #   Konstanten
        webRootURL = config.get('CONST', 'webRootURL')

        #   Daten einlesen
        session = Session()
        resDict = {}
        resFilePath = (workDirPath / "moNr").with_suffix('.txt')
        with resFilePath.open(mode='wt', encoding='utf8') as resFile:
            for oly in range(38, 44):
                olyStr = f'{oly:02d}'
                resDict[olyStr] = {}
                print(file=resFile)
                print(file=resFile)
                print('=' * 40, file=resFile)
                for rnd in range(1, 5):
                    resDict[olyStr][rnd] = {}
                    lenDict = {}
                    print(file=resFile)
                    print('=' * 20, file=resFile)
                    for okl in range(3, 14):
                        text = ''
                        oklLenList = []
                        for tag in ['', 'a', 'b']:
                            fileName = f'A{oly:02d}{okl:02d}{rnd:d}{tag}'
                            actURL = f'{webRootURL}/{oly:02d}/{rnd:d}/{fileName}.pdf'
                            pdfFilePath = (workDirPath / fileName).with_suffix('.pdf')
                            try:
                                logging.debug(f'{actURL}')
                                response: Response = session.get(url=actURL)
                                if response.status_code == 200:
                                    with pdfFilePath.open(mode='wb') as actFile:
                                        actFile.write(response.content)
                                        logging.debug(f'\t… erledigt')
                                else:
                                    logging.debug(f'\t… nicht gefunden')
                            except Exception as ex:
                                logging.debug(ex)
                            if pdfFilePath.exists():
                                with pdfFilePath.open(mode='rb') as actFile:
                                    pdfReader = PdfFileReader(actFile)
                                    for page in pdfReader.pages:
                                        text += page.extractText()
                        logging.debug(f'{oly:02d}-{rnd:d}-{okl:02d}: found text {len(text)}')
                        if len(text) > 0:
                            moNrPattern = f'({oly:02d}{okl:02d}{rnd:1d}\\d)'
                            moNrMatch = re.findall(pattern=moNrPattern, string=text)
                            resList = sorted(list(set(map(''.join, moNrMatch))), reverse=True)
                            print(resList, file=resFile)
                            anz = int(resList[0][-1])
                            oklStr = f'{okl:02d}'
                            resDict[olyStr][rnd][oklStr] = [anz]
                            if rnd > 2 and okl > 5:
                                resDict[olyStr][rnd][oklStr] = [3, 3]
                            oldStart = 0
                            for moNrMatch in re.finditer(pattern=moNrPattern, string=text):
                                newStart = moNrMatch.start()
                                if oldStart > 0:
                                    oklLenList.append(newStart - oldStart)
                                oldStart = newStart
                            oklLenList.append(len(text) - oldStart)
                        if len(oklLenList) > 0:
                            lenDict[okl] = oklLenList
                    resDict[olyStr][rnd].update({"parent": lenDict})

        jsonFilePath = (workDirPath / "moNr").with_suffix('.json')
        with jsonFilePath.open(mode='wt', encoding='utf8') as jsonFile:
            json.dump(resDict, fp=jsonFile, indent=2)

    except Exception:
        logging.exception('General fatal error!')
        raise
    finally:
        logging.info('… finished!')
