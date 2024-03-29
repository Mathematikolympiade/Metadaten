"""Roger's RDF store MO data provider module"""

import logging, sys, os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser
from csv import DictReader

import lib.mdSubjectTools as mst

configParams = """
    [DEFAULT]
        logToFile =   True

    #   fixed names & values
    [CONST]
        csvFileName = mdData/Buch300_aufgList.csv
        ttlFileName = mdRDF/buchProblemeGebiete.ttl

    #   specific data

    #   workflow setup
    [WORK]
"""

#   lib logging

#   environment
inIDE = (os.environ.get('PYCHARM_HOSTED', 0) == '1')
compName = os.environ.get('COMPUTERNAME', 'SHERATAN')
#   control
argParser = ArgumentParser(description="Roger's RDF store MO data provider")
argParser.add_argument('-w', '--workDir', dest='workDirName', default=".", help="working directory")
argParser.add_argument('-i', '--iniFile', dest='iniFileName', default=None, help="param ini file")
cmdLineArgs = f' --workDir={str(Path.home() / "Documents/MO/AA/")}'
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

        #   CSV einlesen
        subjList = []
        csvFilePath = workDirPath / config.get('CONST', 'csvFileName')
        with csvFilePath.open(mode='rt', encoding='utf8') as csvFile:
            logging.info(f'reading from {csvFile.name}')
            subjReader = DictReader(csvFile, delimiter=';')
            for dataRow in subjReader:
                subjData = mst.MoSubjData(dataRow["OJM"])
                subjData.aut = "BuchProjekt (Roger Labahn)"
                subjData.thm = dataRow["SekNummer"].replace('.', '-')
                subjList.append(subjData)

        #   TTL schreiben
        ttlWriter = mst.TtlWriter("math:buch_G_{:s}")
        ttlFilepath = workDirPath / config.get('CONST', 'ttlFileName')
        logging.info(f'writing to {ttlFilepath}')
        with ttlFilepath.open(mode='wt', encoding='utf8') as ttlFile:
            for subjData in subjList:
                print(ttlWriter.write(subjData), file=ttlFile)

    except Exception:
        logging.exception('General fatal error!')
        raise
    finally:
        logging.info('… finished!')
