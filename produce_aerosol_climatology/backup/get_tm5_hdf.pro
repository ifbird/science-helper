pro get_tm5_hdf, mf, tracer=t, data=d, stat=s

; Open file
file_id = hdf_open(mf, /read)

; Get SD id
sd_id = hdf_sd_start(mf, /read)

ds_idx = hdf_sd_nametoindex(sd_id, t)
ds_id  = HDF_SD_Select(sd_id, ds_idx)
hdf_sd_getdata, ds_id, d

s = 0

end
