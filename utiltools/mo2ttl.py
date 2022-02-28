"""Roger's RDF store MO data provider module"""

import logging, sys, os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser

import lib.moDataTools as mdt

configParams = """
    [DEFAULT]
        logToFile =   True

    #   fixed names & values
    [CONST]
        minOkl = 5
        maxOkl = 13
        jsonFileName = mdData/moNr_41-43.json
        ttlFileName = moProbleme_41-43.ttl

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
        minOkl = config.getint('CONST', 'minOkl')
        maxOkl = config.getint('CONST', 'maxOkl')

        #   Daten einlesen
        moOlyData = mdt.MoOlyData(minOkl=minOkl, maxOkl=maxOkl)
        jsonFilePath = workDirPath / config.get('CONST', 'jsonFileName')
        moOlyData.loadJSON(jsonFilePath=jsonFilePath)
        moOlyData.procJSON()
        print('\n'.join([prob.info() for prob in sorted(moOlyData)]))
        ttlFilepath = workDirPath / config.get('CONST', 'ttlFileName')
        logging.info(f'writing {ttlFilepath}')
        moOlyData.writeTTL(ttlFilepath=ttlFilepath)

    except Exception:
        logging.exception('General fatal error!')
        raise
    finally:
        logging.info('… finished!')
