from .fileio import *

from pyhdf.SD import *


def h4dump(hdfFile, verb=True, log_file=None):
  # Dictionnary used to convert from a numeric data type to its symbolic representation
  typeTab = {
             SDC.CHAR:    'CHAR',
             SDC.CHAR8:   'CHAR8',
             SDC.UCHAR8:  'UCHAR8',
             SDC.INT8:    'INT8',
             SDC.UINT8:   'UINT8',
             SDC.INT16:   'INT16',
             SDC.UINT16:  'UINT16',
             SDC.INT32:   'INT32',
             SDC.UINT32:  'UINT32',
             SDC.FLOAT32: 'FLOAT32',
             SDC.FLOAT64: 'FLOAT64'
             }
  
  # Set output location
  printf = set_sysstdout(verb=verb, log_file=log_file)

  # Default values for returned variables
  f, attrList, dsetList = None, [], []
  
  try:  # Catch pyhdf.SD errors
    # Open HDF file named on the command line
    f = SD(hdfFile)

    # Get the numbers of datasets and file attributes in the hdf4 file
    ndsets, nattrs = f.info()

    # Set return attribute list and dataset list
    attrList = []
    dsetList = []
  
    # File name, number of attributes and number of variables.
    printf("FILE INFO"); eol()
    printf("-------------"); eol()
    printf("%-25s%s" % ("File:", hdfFile)); eol()
    printf("%-25s%d" % ("  file attributes:", nattrs)); eol()
    printf("%-25s%d" % ("  datasets:", ndsets)); eol()
    eol();

    # Global attribute table.
    if nattrs > 0:
      printf("File attributes"); eol(2)
      printf("  name                 idx type    len value"); eol()
      printf("  -------------------- --- ------- --- -----"); eol()

      # Get global attribute dictionnary
      # full=1: {attr name: (value, index, type, length)}
      attrs = f.attributes(full=1)

      # Get list of attribute names and sort them lexically
      attNames = list(attrs.keys())
      attNames.sort()
      for name in attNames:
        attrList.append(name)
        # Get the attribute information
        t = attrs[name]
        printf("  %-20s %3d %-7s %3d %s" %
          (name, t[1], typeTab[t[2]], t[3], t[0])); eol()
      eol()

    # Dataset table
    if ndsets > 0:
      printf("Datasets (idx:index num, na:n attributes, cv:coord var)"); eol(2)
      printf("  name                 idx type    na cv dimension(s)"); eol()
      printf("  -------------------- --- ------- -- -- ------------"); eol()
      for idx in range(ndsets):
        # Get dataset instance from the dataset index
        ds = f.select(idx)

        # Retrieve the dictionary of dataset attributes so as to display their number
        dsInfo = ds.info()  # (name, rank, shape, data type, number of attributes)
        dsDim  = ds.dimensions()  # {dim name: dim length}
        dsetList.append(dsInfo[0])
        printf("  %-20s %3d %-7s %2d %-2s " %
          (dsInfo[0], idx, typeTab[dsInfo[3]], dsInfo[4],
          ds.iscoordvar() and 'X' or ''))

        # Display dimension info
        n = 0
        for k, v in dsDim.items():
          printf("%s%s(%d)" % (n > 0 and ', ' or '', k, v))
          n += 1
        eol()
      eol()

    # Dataset info
    if ndsets > 0:
      printf("DATASET INFO"); eol()
      printf("-------------"); eol(2)
      for idx in range(ndsets):
        # Access the dataset
        ds = f.select(idx)

        # Get dataset information
        # info: (name, rank, shape, data type, number of attributes)
        dsInfo = ds.info()

        # Get dataset attribute dictionary
        # attribute dictionary: {attr name: (value, index, type, length)}
        dsAttr = ds.attributes(full=1)
        if len(dsAttr) > 0:
          printf("%s attributes" % dsInfo[0]); eol(2)
          printf("  name                 idx type    len value"); eol()
          printf("  -------------------- --- ------- --- -----"); eol()
          # Get the list of attribute names and sort them alphabetically.
          attNames = list(dsAttr.keys())
          attNames.sort()
          for nm in attNames:
            t = dsAttr[nm]
            printf("  %-20s %3d %-7s %3d %s" %
              (nm, t[1], typeTab[t[2]], t[3], t[0])); eol()
          eol()

        # Get dataset dimension dictionnary
        # full = 0: {dim name: length}
        # full = 1: {dim name: (length, index, unlimited (1) or not (0), scale type (0 if no scale), number of attributs)}
        dsDim = ds.dimensions(full=1)
        if len(dsDim) > 0:
          printf ("%s dimensions" % dsInfo[0]); eol(2)
          printf("  name                 idx len   unl type    natt");eol()
          printf("  -------------------- --- ----- --- ------- ----");eol()
          # Get the list of dimension names and sort them alphabetically.
          dimNames = list(dsDim.keys())
          dimNames.sort()
          for nm in dimNames:
            t = dsDim[nm]
            printf("  %-20s %3d %5d  %s  %-7s %4d" %
              (nm, t[1], t[0], t[2] and "X" or " ",
              t[3] and typeTab[t[3]] or "", t[4])); eol()
          eol()
  
  except HDF4Error as msg:
    print("HDF4Error", msg)

  # Reset output location to screen
  set_sysstdout(verb=True)

  return f, attrList, dsetList


if __name__ == '__main__':
  # Get first command line argument as the input hdf4 file name
  hdfFile = sys.argv[1]

  # Print the hdf4 file info on the screen
  h4dump(hdfFile, verb=True)
