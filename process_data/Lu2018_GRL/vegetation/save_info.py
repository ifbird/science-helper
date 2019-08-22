#==============================================================================#
#
# Write the important information of the data
#
#==============================================================================#

#
# Import header
#

import local_functions as lfunc

#==============================================================================#
#
# Read LPJ-GUESS veg data obtained from Lu2018 (GRL)
#
# Lu2018:
#   They simulated three cases with different climate forcing.
#   PI: preindustrial with standard CMIP5 (Taylor2012)
#   MH: insolation, greenhouse gas in MH
#   MHgsrd: MH case with green Sahara and 80% reduced dust concentration (Pausata2016)
#
#==============================================================================#

# Lu2018 lpjg veg data folder
dir_lu2018_data = '../data/lu2018_lpjg_monthly_veg'

# Read data
print('Reading Lu2018 data for PI ...')
lu2018_pi     = lfunc.read_Lu2018_lpjg_data(dir_lu2018_data + '/LPJ-GUESS_monthlyoutput_PI.txt'    )
print('Reading Lu2018 data for MH ...')
lu2018_mh     = lfunc.read_Lu2018_lpjg_data(dir_lu2018_data + '/LPJ-GUESS_monthlyoutput_MH.txt'    )
print('Reading Lu2018 data for MHgsrd ...')
lu2018_mhgsrd = lfunc.read_Lu2018_lpjg_data(dir_lu2018_data + '/LPJ-GUESS_monthlyoutput_MHgsrd.txt')

#
# At some grid cells the vegetation type will change with time during 10 years.
# So here we record the altering history of these grids, including:
# grid number, grid id, lon, lat, vegetation type for 10 years, dominant veg type
#
# Low vegetation types: 2, 7, 9, 13
# High vegetation types: 3, 4, 5, 6, 18
#

# Output folder
dir_info = lfunc.set_dir('./info')

print('Writing the vegetation type change history during 10 years for PI ...')
lfunc.write_veg_change_history(lu2018_pi    , dir_info+'/veg_type_change_pi.txt'    )
print('Writing the vegetation type change history during 10 years for MH ...')
lfunc.write_veg_change_history(lu2018_mh    , dir_info+'/veg_type_change_mh.txt'    )
print('Writing the vegetation type change history during 10 years for MHgsrd ...')
lfunc.write_veg_change_history(lu2018_mhgsrd, dir_info+'/veg_type_change_mhgsrd.txt')
