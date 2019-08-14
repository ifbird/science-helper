"""
" File IO
"""
import os
import sys


def set_sysstdout(verb=True, log_file=None):
  """
  " Set the output location to printf
  " verb: 
  "   log_file is None: screen
  "   log_file is not None: file (log_file)
  " not verb:
  "   do not output
  """
  # Set output location
  if verb:
    # To file
    if log_file is not None:
      sys.stdout = open(log_file, 'w')
    # To screen
    else:
      sys.stdout = sys.__stdout__
  else:
    # To nothing (do not output anything)
    sys.stdout = open(os.devnull, 'w')

  return sys.stdout.write


def eol(n=1):
  """
  " Change n new lines.
  " Calling set_sysstdout before eol is recommended.
  " Use eol directly, do not use print(eol).
  """
  # printf("%s" % chr(10) * n)
  sys.stdout.write("%s" % chr(10) * n)
