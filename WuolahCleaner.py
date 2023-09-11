from gulagcleaner.extract import clean_pdf
import sys

class Log:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
    @staticmethod
    def Success(msg: str):
        print(f"{Log.OKGREEN}[OK]{Log.ENDC} {msg}'")

    @staticmethod
    def Warning(msg: str):
        print(f'{Log.WARNING}[WARNING]{Log.ENDC} {msg}')

    @staticmethod
    def Error(msg: str):
        print(f"{Log.FAIL}[ERROR]{Log.ENDC} {msg}")


class Cleaner:
    '''See Cleaner.help for usage'''
    @staticmethod
    def clean(argv: str) -> bool:
        '''@param argv: Command line parameters
        @return: success'''
        if (len(argv) < 2 or "-h" in argv or argv[1][0] == '-'):
            Cleaner.logHelp()
            exit(0)

        file = argv[1]
        output = ""

        # Process parameters
        if ('-r' in argv):
            output = file
            if ('-o' in argv):
                Log.Warning("-r specified, output path will be ignored")
        elif ("-o" in argv):
            output_idx = argv.index("-o") + 1
            if (output_idx >= len(argv)):
                Log.Error("output_file not specified!")
                exit(0)
            output = argv[output_idx]
        elif("wuolah-free-" in file):
            output = file.replace("wuolah-free-", "")

        # Force output to be .pdf
        if (output != "" and not output.endswith(".pdf")):
            output += ".pdf"
        
        # Execute clean
        return_msg = clean_pdf(file, output)
        success = return_msg["Success"]

        # Output status
        if (success):
            Log.Success(f"Removing ads from '{file}' to '{return_msg['return_path']}")
        else:
            Log.Error(f"{return_msg['Error']}")

        return success

    @staticmethod
    def logHelp():
        print("""Usage: python3 cleanWuolahAds.py <filename> [-o <output_path>] [-r] [-h]
    [-h]
        Show help
    [-o <output_path>] 
        Creates a new cleaned file in the specified path
    [-r]
        Replaces the original file with the cleaned one (if -o is specified too, output path will be ignored)""")

Cleaner.clean(sys.argv)
