class Tm5Output:

  def __init__(self, folder):
    self.folder = folder


  def get_file_name(self, otype, year, month):
    if otype == 'aerocom':
      file_name = 'aerocom3_TM5_aerocom_global_{0:4d}{1:02d}_monthly.nc'.format(year, month)
    elif otype == 'general':
      file_name = 'general_TM5_general_output_{0:4d}{1:02d}_monthly.nc'.format(year, month)
    else:
      print('Wrong output type.')
      file_name = None

    return file_name


  def get_file_full_path(self, otype, year, month):
    file_name = self.get_file_name(otype, year, month)
    if file_name is None:
      file_full_path = None
    else:
      file_full_path = self.folder + '/' + self.get_file_name(otype, year, month)

    return file_full_path
