; No need anymore ?? Squeeze the data in the time dimension and transpose
; shift lon from [-178.5, 178.5] to [1.5, 358.5]
; data[nlon, nlat], help_2d[nlon, nlat]
pro rotate_2d, nlon, data, help_2d
  ; tmp_2d = transpose(reform(data))
  help_2d[0:nlon/2-1, *] = data[nlon/2:-1 , *]
  help_2d[nlon/2:-1 , *] = data[0:nlon/2-1, *]
end
