"""Roger's MO RDF store builder"""

import logging
import sys
import os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser

# import rdflib, rdflib.resource
from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics
from rdflib import Graph, Literal

configParams = """
    [DEFAULT]
        logToFile =   True

    #   fixed names & values
    [CONST]
        remoteURL = http://www.mathematik-olympiaden.de/aufgaben/metadaten

    #   specific data
    [SOURCES]
        1 = models/math
        2 = models/mo
        3 = buchThemen.ttl
        4 = buchProbleme.ttl
    
    [LOCAL]
        srcDir = mdRDF

    #   workflow setup
    [WORK]
        srcDir = local
        dstFileBase =   buch300
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

        #   read models
        rdfGraph = Graph(identifier="buch300")
        graphSize = len(rdfGraph)
        srcDirPath = workDirPath / config.get(config.get('WORK', 'srcDir').upper(), 'srcDir')
        for srcFileName in config['SOURCES'].values():
            srcFilePath = srcDirPath/srcFileName
            if srcFilePath.is_file():
                rdfGraph.parse(srcFilePath, format='ttl')
                newGraphSize = len(rdfGraph)
                logging.info(f'{newGraphSize - graphSize} statements read from {srcFilePath}')
                graphSize = newGraphSize
        logging.info(f'data graph now has {len(rdfGraph)} statements')

        rdfsClosure = DeductiveClosure(closure_class=RDFS_Semantics, rdfs_closure=False, improved_datatypes=False)
        rdfsClosure.expand(rdfGraph)
        logging.info(f'closure graph has {len(rdfGraph)} statements')

        for triple in rdfGraph:
            if isinstance(triple[0], Literal):
                rdfGraph.remove(triple)

        logging.info(f'reduced closure graph now has {len(rdfGraph)} statements')

        #   write rdf
        for suffix in ['ttl', 'xml']:
            dstFilePath = (srcDirPath / config.get('WORK', 'dstFileBase')).with_suffix(f'.{suffix}')
            rdfGraph.serialize(destination=dstFilePath, format=suffix)
            logging.info(f'wrote graph to {dstFilePath}')

        #   test
        # nsDict = dict(rdfGraph.namespaces())
        # mo = rdflib.Namespace(nsDict['mo'])
        # math = rdflib.Namespace(nsDict['math'])
        # prob = rdflib.Namespace(nsDict[''])
        # uriRef = rdflib.term.URIRef(value="https://www.mathematik-olympiaden.de/aufgaben/rdf/Problem#MO-511341")

    #   exceptions
    except Exception:
        logging.exception('General fatal error!')
    finally:
        logging.info('… finished!')
        if not inIDE:
            input("PAUSE …")
