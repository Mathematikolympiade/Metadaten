import logging
import datetime
import sys
from pathlib import Path

import rdflib

#   Konstanten Dateisystem
srcFileNames = ["../Modelle/mo", "../Daten/moProbleme.ttl"]

if __name__ == '__main__':
    #   logging
    logFilePath = Path.cwd().joinpath(Path(sys.argv[0]).stem).with_suffix('.log')
    with logFilePath.open(mode='w', encoding='utf8') as logFile:
        print(datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S'), file=logFile)
    logging.basicConfig(
        level=logging.INFO
        , format='%(levelname)s %(asctime)s %(message)s', datefmt='%H:%M:%S'
        , handlers=[
            logging.FileHandler(logFilePath, mode='a', encoding="utf-8")
            # , logging.StreamHandler()
        ]
    )
    logging.info('started in {:s} …'.format(str(Path().cwd())))

    try:
        #   workBase
        srcPath = Path().cwd()

        #   read sources
        rdfGraph = rdflib.Graph(identifier="moProbleme")
        graphSize = 0
        for srcFileName in srcFileNames:
            srcFilePath = srcPath / srcFileName
            logging.info('reading {:s} …'.format(str(srcFilePath)))
            with srcFilePath.open(encoding='utf8') as srcFile:
                rdfGraph.parse(file=srcFile, format='ttl')
            newGraphSize = len(rdfGraph)
            logging.info('\t… {:d} statements read'.format(newGraphSize - graphSize))
            graphSize = newGraphSize
        logging.info("Final data graph has {:d} statements.".format(len(rdfGraph)))
        logging.debug('Namespaces\n\t{:s}'.format('\n\t'.join([str(ns) for ns in rdfGraph.namespaces()])))
        #   set bindings
        nsDict = dict(rdfGraph.namespaces())
        mo = rdflib.Namespace(nsDict['mo'])

        #   check data
        if False:
            for (subj, pred, obj) in rdfGraph:
                if (subj, pred, obj) not in rdfGraph:
                    raise Exception("It better be!")
                else:
                    print(subj, pred, obj)
            for (pred, obj) in rdfGraph.predicate_objects(subject=rdflib.term.URIRef("MO-511341")):
                print(rdfGraph.label(pred), obj)

        #  query data: MO
        if True:
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
            for res in queryRes:
                resStr = '{:s}\t{:s}\t{:s}\n'.format(res.nr, rdfGraph.label(mo.pdfA), res.pdfA)
                resStr += '\t{:s}:'.format(rdfGraph.label(mo.anw))
                resStr += '\t{:s} {:s}'.format(olyLabel[3:], res.oly)
                resStr += ', {:s} {:s}'.format(rndLabel[3:], res.rnd)
                resStr += ', {:s} {:s}'.format(oklLabel[3:], res.okl)
                print(resStr)


    except Exception:
        logging.exception('General fatal error!')
        raise
    finally:
        logging.info('… finished')
