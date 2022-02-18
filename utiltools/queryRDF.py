"""Roger's RDF-store client"""

import rdflib

import logging, sys, os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path, PurePosixPath
from datetime import datetime
from argparse import ArgumentParser

configParams = """
    [DEFAULT]
        logToFile =   True

    #   fixed names & values
    [CONST]
        localDirName = mdRDF
        mathModelFileName = models/math
        moModelFileName = models/mo
        dataFileName = moProbleme.ttl
        remoteURL = http://www.mathematik-olympiaden.de/aufgaben/rdf

    #   specific data

    #   workflow setup
    [WORK]
        source = local
        checkData = False
        queryData = True
"""

#   lib logging

#   environment
inIDE = (os.environ.get('PYCHARM_HOSTED', 0) == '1')
compName = os.environ.get('COMPUTERNAME', 'SHERATAN')
#   control
argParser = ArgumentParser(description="AS user satisfaction: organize data")
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


        #   run

        #   read models
        rdfGraph = rdflib.Graph(identifier="moProbleme")
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
        sys.exit()

        #   check data
        if config.getboolean('WORK', 'checkData'):
            for (subj, pred, obj) in rdfGraph:
                print(subj, pred, obj)

        #   set bindings
        logging.debug('Namespaces\n\t{:s}'.format('\n\t'.join(map(str, rdfGraph.namespaces()))))
        nsDict = dict(rdfGraph.namespaces())
        mo = rdflib.Namespace(nsDict['mo'])

        #   read data
        if config.getboolean('WORK', 'checkData'):
            for (subj, pred, obj) in rdfGraph:
                print(subj, pred, obj)
            # uriRef = rdflib.term.URIRef(value="https://www.mathematik-olympiaden.de/aufgaben/rdf/Problem#MO-511341")
            # print(uriRef)
            # for (pred, obj) in rdfGraph.predicate_objects(subject=uriRef):
            #     print(rdfGraph.label(pred), obj)

        #  query data: MO
        if config.getboolean('WORK', 'queryData'):
            queryStr = 'SELECT $nr $pdfA $oly $rnd $okl \
                        WHERE { \
                            $problem a mo:Problem . \
                            $problem mo:nr $nr . \
                            $problem mo:pdfA $pdfA . \
                            $problem mo:anw $anw . \
                            $anw mo:oly $oly . \
                            $anw mo:rnd $rnd . \
                            $anw mo:okl $okl . \
                        }  \
                        ORDER BY $nr \
                       '
            queryRes = rdfGraph.query(queryStr)
            print(len(queryRes))

            olyLabel = rdfGraph.label(mo.oly)
            rndLabel = rdfGraph.label(mo.rnd)
            oklLabel = rdfGraph.label(mo.okl)
            # for res in queryRes:
            #     resStr = '{:s}\t{:s}\t{:s}\n'.format(res.nr, rdfGraph.label(mo.pdfA), res.pdfA)
            #     resStr += '\t{:s}:'.format(rdfGraph.label(mo.anw))
            #     resStr += '\t{:s} {:s}'.format(olyLabel[3:], res.oly)
            #     resStr += ', {:s} {:s}'.format(rndLabel[3:], res.rnd)
            #     resStr += ', {:s} {:s}'.format(oklLabel[3:], res.okl)
            #     print(resStr)

    #   exceptions
    except Exception:
        logging.exception('General fatal error!')
    finally:
        logging.info('… finished!')
        if not inIDE:
            input("PAUSE …")
