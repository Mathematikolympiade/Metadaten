"""Roger's RDF-store client"""

import logging
import sys
import os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser

import rdflib

configParams = """
    [DEFAULT]
        logToFile =   True

    #   fixed names & values
    [CONST]
        localDirName = mdRDF
        mathModelFileName = models/math
        moModelFileName = models/mo
        dataFileName = buchThemen.ttl
        remoteURL = http://www.mathematik-olympiaden.de/aufgaben/metadaten

    #   specific data

    #   workflow setup
    [WORK]
        source = local
        checkData = False
"""

#   lib logging

#   environment
inIDE = (os.environ.get('PYCHARM_HOSTED', 0) == '1')
compName = os.environ.get('COMPUTERNAME', 'SHERATAN')
#   control
argParser = ArgumentParser(description=__doc__)
argParser.add_argument('-w', '--workDir', dest='workDirName', default=".", help="working directory")
argParser.add_argument('-i', '--iniFile', dest='iniFileName', default=None, help="param ini file")
cmdLineArgs = f' --workDir={str(Path.home() / "Documents/MO/AA/")}'
# if compName.upper() == 'LONG':
#     cmdLineArgs = ' --workDir=P:/Daten/NewsEye/GT_AS'
# cmdLineArgs += f' --iniFile={PurePosixPath(sys.argv[0]).with_suffix(".ini").name}'

if __name__ == '__main__':
    # noinspection PyBroadException
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
        logBase = Path(sys.argv[0])
        logFilePath = (logBase.parent / 'logs' / logBase.stem).with_suffix('.log')
        if config['DEFAULT'].getboolean('logToFile', None):
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

        #   run

        #   read data
        rdfGraph = rdflib.Graph(identifier="buchProbleme")
        graphSize = len(rdfGraph)
        match src := config.get('WORK', 'source'):
            case 'remote':
                rootURL = config.get('CONST', 'remoteURL')
                for prefix in ['mathModel', 'moModel', 'data']:
                    srcURL = f"{rootURL}/{config.get('CONST', f'{prefix}FileName')}"
                    rdfGraph.parse(srcURL, format='ttl')
                    newGraphSize = len(rdfGraph)
                    logging.info(f'\t{newGraphSize - graphSize} statements read from {srcURL}')
                    graphSize = newGraphSize
            case 'local':
                srcDirPath = workDirPath / config.get('CONST', 'localDirName')
                for prefix in ['mathModel', 'moModel', 'data']:
                    srcFilePath = srcDirPath / config.get('CONST', f'{prefix}FileName')
                    with srcFilePath.open(mode='rt', encoding='utf8') as srcFile:
                        rdfGraph.parse(file=srcFile, format='ttl')
                    newGraphSize = len(rdfGraph)
                    logging.info(f'\t{newGraphSize - graphSize} statements read from {srcFile.name}')
                    graphSize = newGraphSize
            case _:
                raise NotImplementedError(f'source {src} not yet implemented!')
        logging.info(f'data graph now has {len(rdfGraph)} statements')

        #   set prefixes
        logging.debug('Namespaces\n\t{:s}'.format('\n\t'.join(map(str, rdfGraph.namespaces()))))
        nsDict = dict(rdfGraph.namespaces())
        mo = rdflib.Namespace(nsDict['mo'])
        math = rdflib.Namespace(nsDict['math'])

        #   check data
        if config.getboolean('WORK', 'checkData'):
            for (subj, pred, obj) in rdfGraph:
                print(subj, pred, obj)
            # uriRef = rdflib.term.URIRef(value="https://www.mathematik-olympiaden.de/aufgaben/rdf/Problem#MO-511341")
            # print(uriRef)
            # for (pred, obj) in rdfGraph.predicate_objects(subject=uriRef):
            #     print(rdfGraph.label(pred), obj)

        #   work
        replDict = {}
        for subj in rdfGraph.subjects(predicate=rdflib.RDFS.subClassOf, object=math.Gebiet):
            for gebiet in rdfGraph.subjects(predicate=rdflib.RDFS.subClassOf, object=subj):
                replDict[str(rdfGraph.label(subject=gebiet))] = str(gebiet)[62:]

        dstFileName = "buchProblemeGebiete.ttl"
        dstFilePath = srcDirPath / dstFileName
        with dstFilePath.open(mode='wt', encoding='utf8') as dstFile:
            srcFileName = "moBuchProjekt.ttl"
            srcFilePath = srcDirPath / srcFileName
            with srcFilePath.open(mode='rt', encoding='utf8') as srcFile:
                for line in srcFile:
                    if "math:kap" in line:
                        continue
                    newLine = line
                    if "math:typ" in line:
                        replKey = line.split(maxsplit=1)[1][1:-4]
                        print(replDict.get(replKey, replKey))
                    print(newLine, file=dstFile, end='')
            

    #   exceptions
    except Exception:
        logging.exception('General fatal error!')
    finally:
        logging.info('… finished!')
        if not inIDE:
            input("PAUSE …")
