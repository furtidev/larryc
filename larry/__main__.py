from larry.app import *
import sys

obj = App()

if len(sys.argv) == 2:
	obj.run(sys.argv[1])
else:
	obj.err(ErrorType.NO_ARG)
