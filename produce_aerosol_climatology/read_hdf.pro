pro read_hdf
; An example of reading a hdf file


;+++++++++++++++++ Open the file +++++++++++++++++++++++;
; File name
file = '/wrk/putian/tm5mp-run/mhgsrd/rundir/output_20190430-2month_failed_end/mmix_2005010100_2005020100_glb300x200.hdf'

; Open file
file_id = hdf_open(file, /read)

; Get SD id
sd_id = hdf_sd_start(file, /read)

; Extracting the number of attributes and datasets in the file
hdf_sd_fileinfo, sd_id, nr_dataset, nr_attributes

; Print the file info
print, 'file: ', file
print, 'file_id: ', file_id, ' | sd_id: ', sd_id
print, 'nr_dataset: ', nr_dataset, ' | nr_attributes: ', nr_attributes


;+++++++++++++++++ Show the file attribute info +++++++++++++++++++++++;
; All attrs
print, '++++++++++ All file attributes ++++++++++'
for attr_id=0, nr_attributes-1 do begin
  hdf_sd_attrinfo, sd_id, attr_id, name=n, type=t, count=c
  print, 'attr_id: ', attr_id, ' | name: ', n, ' | type: ', t, ' | count: ', c
endfor

; An example of show attr info from its name
; 1. Use hdf_sd_attrfind to find the index from the name
; 2. Use hdf_sd_attrinfo to get its name, type, count, etc.
print, '++++++++++ One file attribute ++++++++++'
attr_name = 'itau'
attr_id = hdf_sd_attrfind(sd_id, attr_name)
hdf_sd_attrinfo, sd_id, attr_id, name=n, type=t, count=c
print, 'attr_id: ', attr_id, ' | name: ', n, ' | type: ', t, ' | count: ', c


;+++++++++++++++++ Show the file dataset info +++++++++++++++++++++++;
; All datasets
for ds_idx=0, nr_dataset-1 do begin
  ; Get dataset ID from its idx (idx is not the same as ID)
  ds_id = hdf_sd_select(sd_id, ds_idx)

  ; Get the dataset info
  hdf_sd_getinfo, ds_id, name=n, natts=na, ndim=nd, dims=d
  print, 'idx: ', ds_idx, ' | id: ', ds_id, ' | name: ', n, ' | natts: ', na, ' | ndim: ', nd, ' | dims: ', d

  ; Get the attr info of dataset
  for ds_attr_id = 0, na-1 do begin
    hdf_sd_attrinfo, ds_id, ds_attr_id, name=n, data=d
    print, 'ds_attr_id: ', ds_attr_id, 'name: ', n, ' | data: ', d
  endfor
endfor

; An example of show dataset info from its name
; 1. Use hdf_sd_nametoindex to find the index from the name
; 2. Use hdf_sd_attrinfo to get its name, type, count, etc.
ds_name = 'SO2'
ds_idx = hdf_sd_nametoindex(sd_id, 'SO2')
ds_id  = HDF_SD_Select(sd_id, ds_idx)
hdf_sd_getinfo, ds_id, name=n, natts=na, ndim=nd, dims=d
print, 'idx: ', ds_idx, ' | id: ', ds_id, ' | name: ', n, ' | natts: ', na, ' | ndim: ', nd, ' | dims: ', d
for ds_attr_id = 0, na-1 do begin
  hdf_sd_attrinfo, ds_id, ds_attr_id, name=n, data=d
  print, 'ds_attr_id: ', ds_attr_id, 'name: ', n, ' | data: ', d
endfor


;+++++++++++++++++ Import the data from datasets +++++++++++++++++++++++;
ds_name = 'SO2'
ds_idx = hdf_sd_nametoindex(sd_id, 'SO2')
ds_id  = HDF_SD_Select(sd_id, ds_idx)
hdf_sd_getdata, ds_id, filedata
; print, filedata


;+++++++++++++++++ Close the file +++++++++++++++++++++++;
hdf_sd_end, sd_id
hdf_close, file_id

end 
