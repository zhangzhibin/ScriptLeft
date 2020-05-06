import os
from os import walk
from sys import stdout
import logging
                    
# def files(path):
#     for file in os.listdir(path):
#         if os.path.isfile(os.path.join(path, file)):
#             yield file

def mergeFile(srcFile, destFile):
    counter = 0
    with open(destFile, 'a') as outFile:
        with open(srcFile, 'r') as inFile:
            for line in inFile.readlines():
                outFile.write(line)
                counter += 1
    return counter

def listAllFiles(srcPath, destFile, fileTypes, excludeFiles):
    counter = 0
    lines = 0
    for (dirpath, dirnames, filenames) in walk(srcPath):
        # f.extend(filenames)
        for f in filenames:
            p = os.path.join(dirpath, f)
            fn, ext = os.path.splitext(f)
            valid = False
            ln = 0
            if not ext:
                # empty extension
                continue
            elif ext.lower() in fileTypes and not(fn.lower() in excludeFiles):
                valid = True
                counter += 1

            if valid:
                ln += mergeFile(p, destFile)
                lines += ln
                logging.info(f'f ==> {p}|{ext}|{ln}')

        for d in dirnames:
            p = os.path.join(dirpath, d)
            if d.lower() in excludeFiles:
                continue
            if d[0] == ".":
                continue
            
            # logging.info(f'd ==> {p}')
            c, l = listAllFiles(p, destFile, fileTypes, excludeFiles)
            counter += c
            lines += l
        break
    return counter,lines

# def writeLog(msg):
#     if not log:
#         print(msg)
#     else:
#         print(msg)
#         log.write(msg)
#         log.write("\n")

def prepareLog(logFile, appendMode):
    logFormatter = logging.Formatter("%(asctime)s %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    if len(logFile)>0:
        if os.path.exists(logFile) and not(appendMode):
            logging.info(f"Removing existing log: {logFile}")
            os.remove(logFile)

        fileHandler = logging.FileHandler(logFile)
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

    # consoleHandler = logging.StreamHandler(stdout)
    # consoleHandler.setFormatter(logFormatter)
    # rootLogger.addHandler(consoleHandler)

    # logging.basicConfig(level=logging.DEBUG, # or other level
    #                 format='%(asctime)s %(message)s',
    #                 datefmt='%m/%d/%Y %I:%M:%S %p',
    #                 )


def main(srcPath, destFile, fileTypes, excludeFiles, appendMode, logFile):
    logging.info(f"Grab scripts from {srcPath} ==> {destFile}, with types: {fileTypes}, exclude: {excludeFiles}")
    if os.path.exists(destFile):
        if appendMode:
            logging.info(f'Appending to existing file: {destFile}')
        else:
            logging.info(f'Removing exsting file: {destFile}')
            os.remove(destFile)

    prepareLog(logFile, appendMode)

    counter, lines = listAllFiles(srcPath, destFile, fileTypes, excludeFiles)

    logging.info(f"total script files: {counter}, lines: {lines}")


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Merge Script Into One File for Software Left')
    parser.add_argument('--src', metavar='path', required=False,
                        dest='srcPath',
                        help='the path to source folder',
                        default='.')
    parser.add_argument('--dest', metavar='path', required=False,
                        dest='destFile',
                        help='the file to output',
                        default='out.txt')

    parser.add_argument('--files', metavar='string', required=False,
                        dest='fileTypes',
                        help='files to include',
                        default='.c,.c++,.cs,.java,.kt,.m,.mm,.js,.ts,.vue,.py,.go'
                        )
    
    parser.add_argument('--exclude', metavar='exclude', required=False,
                        dest='excludeFiles',
                        help='file or directory to exclude',
                        default='node_modules;plugin;plugins;Standard Assets')

    parser.add_argument("--append", type=str2bool, nargs='?',
                            const=True, default=False,
                            help="Activate nice mode.")                        
    
    parser.add_argument("--log", dest="logFile", required=False, help="log files", default="out.log")

    args = parser.parse_args()
    main(args.srcPath, 
        args.destFile, 
        args.fileTypes.lower(), 
        args.excludeFiles.lower(), 
        args.append,
        args.logFile)