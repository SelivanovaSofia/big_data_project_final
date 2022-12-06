from parser import Parser
import sys
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

def main():
    parser = Parser()
    if(len(sys.argv) > 1):
        parser.start(sys.argv[1])
    else:
        parser.start('update')
    
if __name__ == "__main__":
    main()
