; Now the data from get_tm5_hdf has the same shape as help_3d, so rotate_3d is not needed
; shift lon from [-178.5, 178.5] to [1.5, 358.5]
; data[nlon, nlat, nlev_tm5], help_3d[nlon, nlat, nlev_tm5]
pro rotate_3d, nlon, data, help_3d
  help_3d[0:nlon/2-1, *, *] = data[nlon/2:-1 , *, *]
  help_3d[nlon/2:-1 , *, *] = data[0:nlon/2-1, *, *]
end
