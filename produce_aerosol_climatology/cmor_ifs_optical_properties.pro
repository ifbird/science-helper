PRO cmor_ifs_optical_properties
; Program for converting TM5 output from aerocom3 and budget/mmix files to CMOR format. 
; used for producing a pre-industrial aerosol climatology for EC-Earth 3.2.

compile_opt idl2
; Set this to find out where underflow/overflow happens
; Usually the 'underflow' can be ignored
!EXCEPT=2

;outputdir = '/nobackup_1/users/noije/TM5/AEROCOM/AP3-INSITU/CMOR_AEROCOM/MONTHLY/'
;outputdir = '/nobackup_1/users/noije/TM5/EC-Earth3.2/v1.2/'
;outputdir = '/nobackup_1/users/noije/TM5/EC-Earth3.2/v2.0/'
;outputdir = '/nobackup_1/users/noije/TM5/EC-Earth3.2/v3.0/'
;outputdir = '/nobackup_1/users/noije/TM5/EC-Earth3.2/v3.0-pd/'
;outputdir = '/nobackup_1/users/noije/TM5/EC-Earth3.2/v4.0-salter15/'
;outputdir = '/nobackup_1/users/noije/TM5/EC-Earth3.2/v5.0-salter15-enh3/'
;outputdir = '/nobackup_1/users/noije/TM5/EC-Earth3.2/v5.0-salter15-enh5/'
;outputdir = '/nobackup_1/users/noije/TM5/EC-Earth3.2/v5.0-salter15-enh7/'
;outputdir = '/nobackup_1/users/noije/TM5/EC-Earth3.2/v5.0-salter-enh3/'
;outputdir = '/nobackup_1/users/noije/TM5/EC-Earth3.2/v5.0-salter-enh5/'
;outputdir = '/nobackup_1/users/noije/TM5/EC-Earth3.2/v5.0-salter-enh7/'
outputdir = '/wrk/putian/DONOTREMOVE/tm5mp/ifs_aerosol_climatology/mhgsrd_200501/'

nbnds=2
nlon=120
nlat=90
nlev_tm5=34 ; 34 (out 60)
nlev_ece=62 ; 62, 91, 137 (previously 34, out of 91)
nwav=14

nmonth=12

dlon=360./nlon
dlat=180./nlat

ae=6.371e6 ; earth radius
dxx=dlon*!dtor
dyy=dlat*!dtor
xlat=-90.*!dtor

dxyp=dblarr(nlat)
area=dblarr(nlon,nlat)

;tot_area=0.
for ilat=0,nlat-1 do begin
  dxyp[ilat]=dxx*(sin(xlat+dyy)-sin(xlat))*ae*ae
  xlat=xlat+dyy
  ;tot_area=tot_area+dxyp[ilat]
  area[*,ilat]=dxyp[ilat]
endfor
;print,tot_area*nlon

;read hybrid coordinates from 34/60 griddef file
; ncdf_read, grid, file='/nobackup/users/noije/TM5/TM5_griddef_glb300x200_L34_L60.nc',/all
ncdf_read, grid, file='/wrk/putian/tm5mp-run/mhgsrd/rundir/output_20190426/TM5_tropomi_griddef.nc',/all

lev=dblarr(nlev_tm5)
a=dblarr(nlev_tm5)
ap=dblarr(nlev_tm5)
b=dblarr(nlev_tm5)
a_bnds=dblarr(nbnds,nlev_tm5)
ap_bnds=dblarr(nbnds,nlev_tm5)
b_bnds=dblarr(nbnds,nlev_tm5)

p0=1.e5
a=grid.a/p0
ap=grid.a
b=grid.b
lev=a+b
for ilev=0,nlev_tm5-1 do begin
  a_bnds[0,ilev]=grid.a_bnds[ilev]/p0
  a_bnds[1,ilev]=grid.a_bnds[ilev+1]/p0
  ap_bnds[0,ilev]=grid.a_bnds[ilev]
  ap_bnds[1,ilev]=grid.a_bnds[ilev+1]
  b_bnds[0,ilev]=grid.b_bnds[ilev]
  b_bnds[1,ilev]=grid.b_bnds[ilev+1]
endfor

wav=dblarr(nwav)
wav_bnds=dblarr(nbnds,nwav)
;wav=[0.2316,0.3040,0.3932,0.5332,0.7016,1.0101,1.2705,1.4625,1.7840,2.0460,2.3250,2.7885,3.4615,8.0205] ; v1
wav=[0.257,0.313,0.398,0.530,0.697,0.973,1.269,1.447,1.767,2.040,2.308,2.752,3.407,5.254] ; v2 and later
wav_bnds[0,*]=[0.2000,0.2632,0.3448,0.4415,0.6250,0.7782,1.2420,1.2990,1.6260,1.9420,2.1500,2.5000,3.0770,3.8460]
wav_bnds[1,0:nwav-2]=wav_bnds[0,1:nwav-1]
wav_bnds[1,nwav-1]=12.1950

surfpres=dblarr(nlon,nlat,nmonth)
;mass_air=dblarr(nlon,nlat,nlev_tm5,nmonth)
aerod4d=dblarr(nlon,nlat,nlev_tm5,nwav,nmonth)
aerabs4d=dblarr(nlon,nlat,nlev_tm5,nwav,nmonth)
aersasy4d=dblarr(nlon,nlat,nlev_tm5,nwav,nmonth)
;aerod550=dblarr(nlon,nlat,nmonth)
;aerabs550=dblarr(nlon,nlat,nmonth)
;aerasy=dblarr(nlon,nlat,nmonth)

;nus_nconc=dblarr(nlon,nlat,nlev_tm5,nmonth)
;nus_so4mmr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;
;ais_nconc=dblarr(nlon,nlat,nlev_tm5,nmonth)
;ais_so4mmr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;ais_bcmmr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;ais_oammr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;
;acs_nconc=dblarr(nlon,nlat,nlev_tm5,nmonth)
;acs_so4mmr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;acs_bcmmr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;acs_oammr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;acs_ssmmr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;acs_dummr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;
;cos_nconc=dblarr(nlon,nlat,nlev_tm5,nmonth)
;cos_so4mmr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;cos_bcmmr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;cos_oammr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;cos_ssmmr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;cos_dummr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;
;aii_nconc=dblarr(nlon,nlat,nlev_tm5,nmonth)
;aii_bcmmr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;aii_oammr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;
;aci_nconc=dblarr(nlon,nlat,nlev_tm5,nmonth)
;aci_dummr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;
;coi_nconc=dblarr(nlon,nlat,nlev_tm5,nmonth)
;coi_dummr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;
;no3_ammr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;nh4_mmr=dblarr(nlon,nlat,nlev_tm5,nmonth)
;;msa_mmr=dblarr(nlon,nlat,nlev_tm5,nmonth)

help_3d=dblarr(nlon,nlat,nlev_tm5)
help_2d=dblarr(nlon,nlat)

surfpres[*,*,*]=0.
;mass_air[*,*,*,*]=0.
aerod4d[*,*,*,*,*]=0.
aerabs4d[*,*,*,*,*]=0.
aersasy4d[*,*,*,*,*]=0.
;aerod550[*,*,*]=0.
;aerabs550[*,*,*]=0.
;aerasy[*,*,*]=0.

;nus_nconc[*,*,*,*]=0.
;nus_so4mmr[*,*,*,*]=0.
;
;ais_nconc[*,*,*,*]=0.
;ais_so4mmr[*,*,*,*]=0.
;ais_bcmmr[*,*,*,*]=0.
;ais_oammr[*,*,*,*]=0.
;
;acs_nconc[*,*,*,*]=0.
;acs_so4mmr[*,*,*,*]=0.
;acs_bcmmr[*,*,*,*]=0.
;acs_oammr[*,*,*,*]=0.
;acs_ssmmr[*,*,*,*]=0.
;acs_dummr[*,*,*,*]=0.
;
;cos_nconc[*,*,*,*]=0.
;cos_so4mmr[*,*,*,*]=0.
;cos_bcmmr[*,*,*,*]=0.
;cos_oammr[*,*,*,*]=0.
;cos_ssmmr[*,*,*,*]=0.
;cos_dummr[*,*,*,*]=0.
;
;aii_nconc[*,*,*,*]=0.
;aii_bcmmr[*,*,*,*]=0.
;aii_oammr[*,*,*,*]=0.
;
;aci_nconc[*,*,*,*]=0.
;aci_dummr[*,*,*,*]=0.
;
;coi_nconc[*,*,*,*]=0.
;coi_dummr[*,*,*,*]=0.
;
;no3_ammr[*,*,*,*]=0.
;nh4_mmr[*,*,*,*]=0.
;;msa_mmr=[*,*,*,*]=0.

;ece_mass_air=dblarr(nlon,nlat,nlev_ece,nmonth)
ece_aerod4d=dblarr(nlon,nlat,nlev_ece,nwav,nmonth)
ece_aerabs4d=dblarr(nlon,nlat,nlev_ece,nwav,nmonth)
ece_aersasy4d=dblarr(nlon,nlat,nlev_ece,nwav,nmonth)

;ece_nus_nconc=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_nus_so4mmr=dblarr(nlon,nlat,nlev_ece,nmonth)
;
;ece_ais_nconc=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_ais_so4mmr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_ais_bcmmr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_ais_oammr=dblarr(nlon,nlat,nlev_ece,nmonth)
;
;ece_acs_nconc=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_acs_so4mmr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_acs_bcmmr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_acs_oammr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_acs_ssmmr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_acs_dummr=dblarr(nlon,nlat,nlev_ece,nmonth)
;
;ece_cos_nconc=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_cos_so4mmr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_cos_bcmmr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_cos_oammr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_cos_ssmmr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_cos_dummr=dblarr(nlon,nlat,nlev_ece,nmonth)
;
;ece_aii_nconc=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_aii_bcmmr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_aii_oammr=dblarr(nlon,nlat,nlev_ece,nmonth)
;
;ece_aci_nconc=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_aci_dummr=dblarr(nlon,nlat,nlev_ece,nmonth)
;
;ece_coi_nconc=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_coi_dummr=dblarr(nlon,nlat,nlev_ece,nmonth)
;
;ece_no3_ammr=dblarr(nlon,nlat,nlev_ece,nmonth)
;ece_nh4_mmr=dblarr(nlon,nlat,nlev_ece,nmonth)
;;ece_msa_mmr=dblarr(nlon,nlat,nlev_ece,nmonth)

;ece_mass_air[*,*,*,*]=0.
ece_aerod4d[*,*,*,*,*]=0.
ece_aerabs4d[*,*,*,*,*]=0.
ece_aersasy4d[*,*,*,*,*]=0.

;ece_nus_nconc[*,*,*,*]=0.
;ece_nus_so4mmr[*,*,*,*]=0.
;
;ece_ais_nconc[*,*,*,*]=0.
;ece_ais_so4mmr[*,*,*,*]=0.
;ece_ais_bcmmr[*,*,*,*]=0.
;ece_ais_oammr[*,*,*,*]=0.
;
;ece_acs_nconc[*,*,*,*]=0.
;ece_acs_so4mmr[*,*,*,*]=0.
;ece_acs_bcmmr[*,*,*,*]=0.
;ece_acs_oammr[*,*,*,*]=0.
;ece_acs_ssmmr[*,*,*,*]=0.
;ece_acs_dummr[*,*,*,*]=0.
;
;ece_cos_nconc[*,*,*,*]=0.
;ece_cos_so4mmr[*,*,*,*]=0.
;ece_cos_bcmmr[*,*,*,*]=0.
;ece_cos_oammr[*,*,*,*]=0.
;ece_cos_ssmmr[*,*,*,*]=0.
;ece_cos_dummr[*,*,*,*]=0.
;
;ece_aii_nconc[*,*,*,*]=0.
;ece_aii_bcmmr[*,*,*,*]=0.
;ece_aii_oammr[*,*,*,*]=0.
;
;ece_aci_nconc[*,*,*,*]=0.
;ece_aci_dummr[*,*,*,*]=0.
;
;ece_coi_nconc[*,*,*,*]=0.
;ece_coi_dummr[*,*,*,*]=0.
;
;ece_no3_ammr[*,*,*,*]=0.
;ece_nh4_mmr[*,*,*,*]=0.
;;ece_msa_mmr=[*,*,*,*]=0.

xmh     = 1.0079
xmc     = 12.01115
xmch4   = xmc + xmh*4.
xmo     = 15.9994

xms     = 32.064
xmso4   = xms+xmo*4.
xmmsa   = xms+xmc+xmh*4.+xmo*3.
;xmh2so4 = xms+xmh*2.+xmo*4.

xmn     = 14.0067
xmno3_a = xmn+xmo*3.
xmnh4   = xmn+xmh*4.

xmair=28.94
xmbc=xmc
xmpom=xmair
xmdust=xmair
xmnumb=xmair

xmna=22.990
xmcl=35.453
xmnacl=xmna+xmcl

Navog=6.02205e23

grav=9.80665
Rgas=8.3144/(28.964e-3)

nyear=1
;nyear=1
year_start=2005
year_end=year_start+nyear-1
for year = year_start,year_end do begin

print,'year: ',year
cyear = string(year,  FORMAT='(I4.4)')
;inputdir = '/nobackup/users/noije/TM5/ap3-insitu/monthly/'
;inputdir = '/nobackup/users/noije/TM5/ecearth-pi/'
;inputdir = '/nobackup/users/noije/TM5/ecearth-pi-v2/'
;inputdir = '/nobackup/users/noije/TM5/ecearth-pi-vcmip6/'
;inputdir = '/nobackup/users/noije/TM5/ecearth-pd-vcmip6/'
;inputdir = '/nobackup/users/noije/TM5/ecearth-pi-v4-salter15/'
;inputdir = '/nobackup/users/noije/TM5/ecearth-pi-v5-salter15-enh3/'
;inputdir = '/nobackup/users/noije/TM5/ecearth-pi-v5-salter15-enh5/'
;inputdir = '/nobackup/users/noije/TM5/ecearth-pi-v5-salter15-enh7/'
;inputdir = '/nobackup/users/noije/TM5/ecearth-pi-v5-salter-enh3/'
;inputdir = '/nobackup/users/noije/TM5/ecearth-pi-v5-salter-enh5/'
;inputdir = '/nobackup/users/noije/TM5/ecearth-pi-v5-salter-enh7/'
; inputdir = '/wrk/putian/tm5mp-run/mhgsrd/rundir/output_20190426/'
inputdir = '/wrk/putian/tm5mp-run/mhgsrd/rundir/output_20190503-1month_fail_end/'
;simulation_id='AP3-PI'
;simulation_id='PI-V2'
;simulation_id='CMIP6'
;simulation_id='PI-V4'
simulation_id='aerocom'
modelname='TM5'
 
print, inputdir

days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
if ( (year mod 4) eq 0 and year ne 1900 and year ne 2100) then begin
  days_in_month[1]=29
endif

time=dblarr(nmonth)
time_bnds=dblarr(nbnds,nmonth)
time[0]=days_in_month[0]/2.
time_bnds[0,0]=0.
time_bnds[1,0]=days_in_month[0]
for imonth=1,nmonth-1 do begin
 time[imonth]=time[imonth-1]+days_in_month[imonth-1]/2.+days_in_month[imonth]/2.
 time_bnds[0,imonth]=time_bnds[1,imonth-1]
 time_bnds[1,imonth]=time_bnds[0,imonth]+days_in_month[imonth]
endfor

year_ref=1850
ndays_ref=0
if year lt year_ref or year gt 2100 then begin
  print, 'Chosen year is outside 1850-2100'
  stop
endif
if year gt year_ref then begin
  for yy=year_ref,year-1 do begin
    if ( (yy mod 4) eq 0 and yy ne 1900 and yy ne 2100) then begin
      ndays_ref=ndays_ref+366
    endif else begin
      ndays_ref=ndays_ref+365
    endelse
  endfor
endif
;print,ndays_ref
; january 2000 starts at 54876.0
; january 2006 starts at 56978.0 days (http://calendarhome.com)

; comment lines below, because the climatology is for the year 1850
;time[*]=time[*]+double(ndays_ref)
;time_bnds[*,*]=time_bnds[*,*]+double(ndays_ref)

;time_string=cyear+'01-'+cyear+'12'
;time_string=cyear
time_string=string(year_ref,  FORMAT='(I4.4)')

for month = 1,nmonth do begin
  print,'month: ',month
  cmonth = string(month,  FORMAT='(I2.2)')
  next_year=year
  next_month=month+1
  if next_month eq 13 then begin
    next_year=year+1
    next_month=1
  endif
  cnext_year = string(next_year,  FORMAT='(I4.4)')
  cnext_month = string(next_month,  FORMAT='(I2.2)')

  cnext_year = '2005'
  cmonth = '01'
  cnext_month = '02'

af=inputdir+'aerocom3'+'_'+modelname+'_'+simulation_id+'_global_'+cyear+cmonth+'_monthly.nc'
;bf=inputdir+'budget_'+cyear+cmonth+'0100_'+cnext_year+cnext_month+'0100_global.hdf'
mf=inputdir+'mmix_'+cyear+cmonth+'0100_'+cnext_year+cnext_month+'0100_glb300x200.hdf'

ncdf_read, data, file=af,/all

for iwav=0,nwav-1 do begin
  rotate_3d, nlon, data.od4daer[*,*,*,iwav], help_3d
  aerod4d[*,*,*,iwav,month-1]=aerod4d[*,*,*,iwav,month-1]+help_3d
  
  rotate_3d, nlon, data.abs4daer[*,*,*,iwav], help_3d
  aerabs4d[*,*,*,iwav,month-1]=aerabs4d[*,*,*,iwav,month-1]+help_3d
  
  rotate_3d, nlon, data.sasy4daer[*,*,*,iwav], help_3d
  aersasy4d[*,*,*,iwav,month-1]=aersasy4d[*,*,*,iwav,month-1]+help_3d
endfor

;rotate_3d, nlon, data.airmass, help_3d
;mass_air[*,*,*,month-1]=mass_air[*,*,*,month-1]+help_3d

rotate_2d, nlon, data.ps, help_2d
surfpres[*,*,month-1]=surfpres[*,*,month-1]+help_2d

;rotate_2d, nlon, data.od550aer, help_2d
;aerod550[*,*,month-1]=aerod550[*,*,month-1]+help_2d
;
;rotate_2d, nlon, data.abs550aer, help_2d
;aerabs550[*,*,month-1]=aerabs550[*,*,month-1]+help_2d
;
;rotate_2d, nlon, data.asyaer, help_2d
;aerasy[*,*,month-1]=aerasy[*,*,month-1]+help_2d

;get_tm5_hdf, mf, tracer="presm", data=data, lonC=lon, latC=lat, stat=rc
;if (rc lt 0) then begin
;  print,'Error reading ', mf
;  stop
;endif else begin
;  rotate_2d, nlon, data, help_2d
;  surfpres[*,*,month-1]=surfpres[*,*,month-1]+help_2d[*,*]
;  for ilev=0,nlev_tm5-1 do begin
;    mass_air[*,*,ilev,month-1]=mass_air[*,*,ilev,month-1]+( grid.a_bnds[ilev]-grid.a_bnds[ilev+1] + (grid.b_bnds[ilev]-grid.b_bnds[ilev+1])* help_2d[*,*])/grav
;  endfor
;endelse

; fields in the the mmix file are mmr times fscale(i) = xmair/xm(i)
; for gases this would be volume mixing ratio
; for the mass concentrations of pom and dust, the ratio xmair/xm is equal to unity.
; for so4, bc and sea salt we need to multiply by xm(i)/xmair, to convert to the mass mixing ratios.

; for number concentrations the ratio xmair/xm is also equal to unity.
; the field in the file is therefore in units #particles/kg air.

;get_tm5_hdf, mf, tracer="NUS_N", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;nus_nconc[*,*,*,month-1]=nus_nconc[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="SO4NUS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;nus_so4mmr[*,*,*,month-1]=nus_so4mmr[*,*,*,month-1]+help_3d[*,*,*]*xmso4/xmair
;
;get_tm5_hdf, mf, tracer="AIS_N", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;ais_nconc[*,*,*,month-1]=ais_nconc[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="SO4AIS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;ais_so4mmr[*,*,*,month-1]=ais_so4mmr[*,*,*,month-1]+help_3d[*,*,*]*xmso4/xmair
;
;get_tm5_hdf, mf, tracer="BCAIS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;ais_bcmmr[*,*,*,month-1]=ais_bcmmr[*,*,*,month-1]+help_3d[*,*,*]*xmbc/xmair
;
;get_tm5_hdf, mf, tracer="POMAIS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;ais_oammr[*,*,*,month-1]=ais_oammr[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="ACS_N", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;acs_nconc[*,*,*,month-1]=acs_nconc[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="SO4ACS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;acs_so4mmr[*,*,*,month-1]=acs_so4mmr[*,*,*,month-1]+help_3d[*,*,*]*xmso4/xmair
;
;get_tm5_hdf, mf, tracer="BCACS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;acs_bcmmr[*,*,*,month-1]=acs_bcmmr[*,*,*,month-1]+help_3d[*,*,*]*xmbc/xmair
;
;get_tm5_hdf, mf, tracer="POMACS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;acs_oammr[*,*,*,month-1]=acs_oammr[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="SSACS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;acs_ssmmr[*,*,*,month-1]=acs_ssmmr[*,*,*,month-1]+help_3d[*,*,*]*xmnacl/xmair
;
;get_tm5_hdf, mf, tracer="DUACS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;acs_dummr[*,*,*,month-1]=acs_dummr[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="COS_N", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;cos_nconc[*,*,*,month-1]=cos_nconc[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="SO4COS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;cos_so4mmr[*,*,*,month-1]=cos_so4mmr[*,*,*,month-1]+help_3d[*,*,*]*xmso4/xmair
;
;get_tm5_hdf, mf, tracer="BCCOS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;cos_bcmmr[*,*,*,month-1]=cos_bcmmr[*,*,*,month-1]+help_3d[*,*,*]*xmbc/xmair
;
;get_tm5_hdf, mf, tracer="POMCOS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;cos_oammr[*,*,*,month-1]=cos_oammr[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="SSCOS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;cos_ssmmr[*,*,*,month-1]=cos_ssmmr[*,*,*,month-1]+help_3d[*,*,*]*xmnacl/xmair
;
;get_tm5_hdf, mf, tracer="DUCOS", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;cos_dummr[*,*,*,month-1]=cos_dummr[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="AII_N", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;aii_nconc[*,*,*,month-1]=aii_nconc[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="BCAII", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;aii_bcmmr[*,*,*,month-1]=aii_bcmmr[*,*,*,month-1]+help_3d[*,*,*]*xmbc/xmair
;
;get_tm5_hdf, mf, tracer="POMAII", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;aii_oammr[*,*,*,month-1]=aii_oammr[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="ACI_N", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;aci_nconc[*,*,*,month-1]=aci_nconc[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="DUACI", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;aci_dummr[*,*,*,month-1]=aci_dummr[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="COI_N", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;coi_nconc[*,*,*,month-1]=coi_nconc[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="DUCOI", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;coi_dummr[*,*,*,month-1]=coi_dummr[*,*,*,month-1]+help_3d[*,*,*]
;
;get_tm5_hdf, mf, tracer="NO3_A", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;no3_ammr[*,*,*,month-1]=no3_ammr[*,*,*,month-1]+help_3d[*,*,*]*xmno3_a/xmair
;
;get_tm5_hdf, mf, tracer="NH4", data=data, stat=rc
;rotate_3d, nlon, data, help_3d
;nh4_mmr[*,*,*,month-1]=nh4_mmr[*,*,*,month-1]+help_3d[*,*,*]*xmnh4/xmair
;
;;get_tm5_hdf, mf, tracer="MSA", data=data, stat=rc
;;rotate_3d, nlon, data, help_3d
;;msa_mmr[*,*,*,month-1]=msa_mmr[*,*,*,month-1]+help_3d[*,*,*]*xmmsa/xmair

endfor

endfor ; year

surfpres=surfpres/double(nyear)
;mass_air=mass_air/double(nyear)
aerod4d=aerod4d/double(nyear)
aerabs4d=aerabs4d/double(nyear)
aersasy4d=aersasy4d/double(nyear)
;aerod550=aerod550/double(nyear)
;aerabs550=aerabs550/double(nyear)
;aerasy=aerasy/double(nyear)

;nus_nconc=nus_nconc/double(nyear)
;nus_so4mmr=nus_so4mmr/double(nyear)
;
;ais_nconc=ais_nconc/double(nyear)
;ais_so4mmr=ais_so4mmr/double(nyear)
;ais_bcmmr=ais_bcmmr/double(nyear)
;ais_oammr=ais_oammr/double(nyear)
;
;acs_nconc=acs_nconc/double(nyear)
;acs_so4mmr=acs_so4mmr/double(nyear)
;acs_bcmmr=acs_bcmmr/double(nyear)
;acs_oammr=acs_oammr/double(nyear)
;acs_ssmmr=acs_ssmmr/double(nyear)
;acs_dummr=acs_dummr/double(nyear)
;
;cos_nconc=cos_nconc/double(nyear)
;cos_so4mmr=cos_so4mmr/double(nyear)
;cos_bcmmr=cos_bcmmr/double(nyear)
;cos_oammr=cos_oammr/double(nyear)
;cos_ssmmr=cos_ssmmr/double(nyear)
;cos_dummr=cos_dummr/double(nyear)
;
;aii_nconc=aii_nconc/double(nyear)
;aii_bcmmr=aii_bcmmr/double(nyear)
;aii_oammr=aii_oammr/double(nyear)
;
;aci_nconc=aci_nconc/double(nyear)
;aci_dummr=aci_dummr/double(nyear)
;
;coi_nconc=coi_nconc/double(nyear)
;coi_dummr=coi_dummr/double(nyear)
;
;no3_ammr=no3_ammr/double(nyear)
;nh4_mmr=nh4_mmr/double(nyear)
;;msa_mmr=msa_mmr/double(nyear)

; shift longitudes by 180 degrees
lon=findgen(nlon)*dlon+dlon/2.
lat=findgen(nlat)*dlat-90.+dlat/2.

lon_bnds=dblarr(nbnds,nlon)
lat_bnds=dblarr(nbnds,nlat)
for ilon=0,nlon-1 do begin
  lon_bnds[0,ilon]=lon[ilon]-dlon/2.
  lon_bnds[1,ilon]=lon[ilon]+dlon/2.
endfor
for ilat=0,nlat-1 do begin
  lat_bnds[0,ilat]=lat[ilat]-dlat/2.
  lat_bnds[1,ilat]=lat[ilat]+dlat/2.
endfor

ece_lev=dblarr(nlev_ece)
ece_a=dblarr(nlev_ece)
ece_ap=dblarr(nlev_ece)
ece_b=dblarr(nlev_ece)
ece_a_bnds=dblarr(nbnds,nlev_ece)
ece_ap_bnds=dblarr(nbnds,nlev_ece)
ece_b_bnds=dblarr(nbnds,nlev_ece)

if (nlev_ece eq 34) then begin
  levels_id1 = 'L34'
  levels_id2 = 'L34/L91'
  levels_id3 = 'L34_L91'
endif else if (nlev_ece eq 60) then begin
  levels_id1 = 'L60'
  levels_id2 = levels_id1
  levels_id3 = levels_id1
endif else if (nlev_ece eq 62) then begin
  levels_id1 = 'L62'
  levels_id2 = levels_id1
  levels_id3 = levels_id1
endif else if (nlev_ece eq 91) then begin
  levels_id1 = 'L91'
  levels_id2 = levels_id1
  levels_id3 = levels_id1
endif else if (nlev_ece eq 137) then begin
  levels_id1 = 'L137'
  levels_id2 = levels_id1
  levels_id3 = levels_id1
endif else begin
  print, 'Target vertical grid not implemented'
  stop
endelse

;read hybrid coordinates from 34/91 griddef file
; ncdf_read, grid, file='/nobackup/users/noije/TM5/TM5_griddef_glb300x200_'+levels_id3+'.nc',/all
get_grid, levels_id1, grid=grid

ece_a=grid.a/p0
ece_ap=grid.a
ece_b=grid.b
ece_lev=ece_a+ece_b
for ilev=0,nlev_ece-1 do begin
  ece_a_bnds[0,ilev]=grid.a_bnds[ilev]/p0
  ece_a_bnds[1,ilev]=grid.a_bnds[ilev+1]/p0
  ece_ap_bnds[0,ilev]=grid.a_bnds[ilev]
  ece_ap_bnds[1,ilev]=grid.a_bnds[ilev+1]
  ece_b_bnds[0,ilev]=grid.b_bnds[ilev]
  ece_b_bnds[1,ilev]=grid.b_bnds[ilev+1]
endfor

phalf_in=dblarr(nlev_tm5+1)
field_in=dblarr(nlev_tm5)

phalf_out=dblarr(nlev_ece+1)
field_out=dblarr(nlev_ece)

for imonth=0,nmonth-1 do begin
 for ilon=0,nlon-1 do begin
  for ilat=0,nlat-1 do begin
    
      for ilev=0,nlev_tm5-1 do begin
        phalf_in[ilev]=ap_bnds[0,ilev] + b_bnds[0,ilev]*surfpres[ilon,ilat,imonth]
        ;phalf_in[ilev]=ap_bnds[0,ilev] + b_bnds[0,ilev]*101325.
        ;print,ilev+1,phalf_in[ilev]
      endfor
      phalf_in[nlev_tm5]=0.
      for ilev=0,nlev_ece-1 do begin
        phalf_out[ilev]=ece_ap_bnds[0,ilev] + ece_b_bnds[0,ilev]*surfpres[ilon,ilat,imonth]
        ;phalf_out[ilev]=ece_ap_bnds[0,ilev] + ece_b_bnds[0,ilev]*101325.
        ;print,ilev+1,phalf_out[ilev]
      endfor
      phalf_out[nlev_ece]=0.

      for ilev=0,nlev_tm5-1 do begin
        ;find overlapping levels on target grid
        ;these run from kmin to kmax
        for klev=0,nlev_ece-1 do begin
          if phalf_out[klev+1] lt phalf_in[ilev] then begin
            kmin=klev
            break
          endif
        endfor

        for klev=nlev_ece-1,0,-1 do begin
          if phalf_out[klev] gt phalf_in[ilev+1] then begin
            kmax=klev
            break
          endif
        endfor

        for klev=kmin,kmax do begin

          if klev eq kmin then begin
            pbot_out=phalf_in[ilev]
          endif else begin
            pbot_out=phalf_out[klev]
          endelse

          if klev eq kmax then begin
            ptop_out=phalf_in[ilev+1]
          endif else begin
            ptop_out=phalf_out[klev+1]
          endelse

          ; extensive fields
          ;ece_mass_air[ilon,ilat,klev,imonth]=ece_mass_air[ilon,ilat,klev,imonth]+mass_air[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)/(phalf_in[ilev]-phalf_in[ilev+1])
          ece_aerod4d[ilon,ilat,klev,*,imonth]=ece_aerod4d[ilon,ilat,klev,*,imonth]+aerod4d[ilon,ilat,ilev,*,imonth]*(pbot_out-ptop_out)/(phalf_in[ilev]-phalf_in[ilev+1])
          ece_aerabs4d[ilon,ilat,klev,*,imonth]=ece_aerabs4d[ilon,ilat,klev,*,imonth]+aerabs4d[ilon,ilat,ilev,*,imonth]*(pbot_out-ptop_out)/(phalf_in[ilev]-phalf_in[ilev+1])
          ece_aersasy4d[ilon,ilat,klev,*,imonth]=ece_aersasy4d[ilon,ilat,klev,*,imonth]+aersasy4d[ilon,ilat,ilev,*,imonth]*(pbot_out-ptop_out)/(phalf_in[ilev]-phalf_in[ilev+1])
          ; intensive fields
;          ece_nus_nconc[ilon,ilat,klev,imonth]=ece_nus_nconc[ilon,ilat,klev,imonth]+nus_nconc[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_nus_so4mmr[ilon,ilat,klev,imonth]=ece_nus_so4mmr[ilon,ilat,klev,imonth]+nus_so4mmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_ais_nconc[ilon,ilat,klev,imonth]=ece_ais_nconc[ilon,ilat,klev,imonth]+ais_nconc[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_ais_so4mmr[ilon,ilat,klev,imonth]=ece_ais_so4mmr[ilon,ilat,klev,imonth]+ais_so4mmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_ais_bcmmr[ilon,ilat,klev,imonth]=ece_ais_bcmmr[ilon,ilat,klev,imonth]+ais_bcmmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_ais_oammr[ilon,ilat,klev,imonth]=ece_ais_oammr[ilon,ilat,klev,imonth]+ais_oammr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_acs_nconc[ilon,ilat,klev,imonth]=ece_acs_nconc[ilon,ilat,klev,imonth]+acs_nconc[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_acs_so4mmr[ilon,ilat,klev,imonth]=ece_acs_so4mmr[ilon,ilat,klev,imonth]+acs_so4mmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_acs_bcmmr[ilon,ilat,klev,imonth]=ece_acs_bcmmr[ilon,ilat,klev,imonth]+acs_bcmmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_acs_oammr[ilon,ilat,klev,imonth]=ece_acs_oammr[ilon,ilat,klev,imonth]+acs_oammr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_acs_ssmmr[ilon,ilat,klev,imonth]=ece_acs_ssmmr[ilon,ilat,klev,imonth]+acs_ssmmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_acs_dummr[ilon,ilat,klev,imonth]=ece_acs_dummr[ilon,ilat,klev,imonth]+acs_dummr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_cos_nconc[ilon,ilat,klev,imonth]=ece_cos_nconc[ilon,ilat,klev,imonth]+cos_nconc[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_cos_so4mmr[ilon,ilat,klev,imonth]=ece_cos_so4mmr[ilon,ilat,klev,imonth]+cos_so4mmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_cos_bcmmr[ilon,ilat,klev,imonth]=ece_cos_bcmmr[ilon,ilat,klev,imonth]+cos_bcmmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_cos_oammr[ilon,ilat,klev,imonth]=ece_cos_oammr[ilon,ilat,klev,imonth]+cos_oammr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_cos_ssmmr[ilon,ilat,klev,imonth]=ece_cos_ssmmr[ilon,ilat,klev,imonth]+cos_ssmmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_cos_dummr[ilon,ilat,klev,imonth]=ece_cos_dummr[ilon,ilat,klev,imonth]+cos_dummr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_aii_nconc[ilon,ilat,klev,imonth]=ece_aii_nconc[ilon,ilat,klev,imonth]+aii_nconc[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_aii_bcmmr[ilon,ilat,klev,imonth]=ece_aii_bcmmr[ilon,ilat,klev,imonth]+aii_bcmmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_aii_oammr[ilon,ilat,klev,imonth]=ece_aii_oammr[ilon,ilat,klev,imonth]+aii_oammr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_aci_nconc[ilon,ilat,klev,imonth]=ece_aci_nconc[ilon,ilat,klev,imonth]+aci_nconc[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_aci_dummr[ilon,ilat,klev,imonth]=ece_aci_dummr[ilon,ilat,klev,imonth]+aci_dummr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_coi_nconc[ilon,ilat,klev,imonth]=ece_coi_nconc[ilon,ilat,klev,imonth]+coi_nconc[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_coi_dummr[ilon,ilat,klev,imonth]=ece_coi_dummr[ilon,ilat,klev,imonth]+coi_dummr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_no3_ammr[ilon,ilat,klev,imonth]=ece_no3_ammr[ilon,ilat,klev,imonth]+no3_ammr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ece_nh4_mmr[ilon,ilat,klev,imonth]=ece_nh4_mmr[ilon,ilat,klev,imonth]+nh4_mmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
;          ;ece_msa_mmr[ilon,ilat,klev,imonth]=ece_msa_mmr[ilon,ilat,klev,imonth]+msa_mmr[ilon,ilat,ilev,imonth]*(pbot_out-ptop_out)
        endfor

        ;print,ilev+1,phalf_in[ilev]
        ;print,'     ',kmin+1,' - ',kmax+1
        ;print,'     ',phalf_out[kmin],' - ',phalf_out[kmax+1]
      endfor ; ilev
      
      ; normalize intensive fields
;      for klev=0,nlev_ece-1 do begin
;        ece_nus_nconc[ilon,ilat,klev,imonth]=ece_nus_nconc[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_nus_so4mmr[ilon,ilat,klev,imonth]=ece_nus_so4mmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_ais_nconc[ilon,ilat,klev,imonth]=ece_ais_nconc[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_ais_so4mmr[ilon,ilat,klev,imonth]=ece_ais_so4mmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_ais_bcmmr[ilon,ilat,klev,imonth]=ece_ais_bcmmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_ais_oammr[ilon,ilat,klev,imonth]=ece_ais_oammr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_acs_nconc[ilon,ilat,klev,imonth]=ece_acs_nconc[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_acs_so4mmr[ilon,ilat,klev,imonth]=ece_acs_so4mmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_acs_bcmmr[ilon,ilat,klev,imonth]=ece_acs_bcmmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_acs_oammr[ilon,ilat,klev,imonth]=ece_acs_oammr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_acs_ssmmr[ilon,ilat,klev,imonth]=ece_acs_ssmmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_acs_dummr[ilon,ilat,klev,imonth]=ece_acs_dummr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_cos_nconc[ilon,ilat,klev,imonth]=ece_cos_nconc[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_cos_so4mmr[ilon,ilat,klev,imonth]=ece_cos_so4mmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_cos_bcmmr[ilon,ilat,klev,imonth]=ece_cos_bcmmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_cos_oammr[ilon,ilat,klev,imonth]=ece_cos_oammr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_cos_ssmmr[ilon,ilat,klev,imonth]=ece_cos_ssmmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_cos_dummr[ilon,ilat,klev,imonth]=ece_cos_dummr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_aii_nconc[ilon,ilat,klev,imonth]=ece_aii_nconc[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_aii_bcmmr[ilon,ilat,klev,imonth]=ece_aii_bcmmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_aii_oammr[ilon,ilat,klev,imonth]=ece_aii_oammr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_aci_nconc[ilon,ilat,klev,imonth]=ece_aci_nconc[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_aci_dummr[ilon,ilat,klev,imonth]=ece_aci_dummr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_coi_nconc[ilon,ilat,klev,imonth]=ece_coi_nconc[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_coi_dummr[ilon,ilat,klev,imonth]=ece_coi_dummr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_no3_ammr[ilon,ilat,klev,imonth]=ece_no3_ammr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ece_nh4_mmr[ilon,ilat,klev,imonth]=ece_nh4_mmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;        ;ece_msa_mmr[ilon,ilat,klev,imonth]=ece_msa_mmr[ilon,ilat,klev,imonth]/(phalf_out[klev]-phalf_out[klev+1])
;      endfor

  endfor
 endfor
endfor

;sum_in=0.
;for ilev=0,nlev_tm5-1 do begin
;  sum_in=sum_in+aerod4d[0,0,ilev,0,0]
;  ;sum_in=sum_in+nus_nconc[0,0,ilev,0]*(phalf_in[ilev]-phalf_in[ilev+1])
;  ;sum_in=sum_in+mass_air[0,0,ilev,0]
;endfor
;sum_out=0.
;for ilev=0,nlev_ece-1 do begin
;  sum_out=sum_out+ece_aerod4d[0,0,ilev,0,0]
;  ;sum_out=sum_out+ece_nus_nconc[0,0,ilev,0]*(phalf_out[ilev]-phalf_out[ilev+1])
;  ;sum_out=sum_out+ece_mass_air[0,0,ilev,0]
;endfor
;print,sum_in, sum_out
;stop

iwrite=1
if (iwrite eq 1) then begin


  var_filenames=['od4daer','abs4daer','sasy4daer'] ;,'nconc_nus','mmrso4_nus',$
;      'nconc_ais','mmrso4_ais','mmrbc_ais','mmroa_ais',$
;      'nconc_acs','mmrso4_acs','mmrbc_acs','mmroa_acs','mmrss_acs','mmrdust_acs',$
;      'nconc_cos','mmrso4_cos','mmrbc_cos','mmroa_cos','mmrss_cos','mmrdust_cos',$
;      'nconc_aii','mmrbc_aii','mmroa_aii',$
;      'nconc_aci','mmrdust_aci',$
;      'nconc_coi','mmrdust_coi',$
;      'mmr_no3','mmr_nh4'] ;,'mmr_msa']
      
  vertical='ModelLevel'
 ;outputfile=outputdir+'ecearth3.2'+'_'+modelname+'_'+simulation_id+'_'+vertical+'_'+time_string+'_monthly_v1.2_L34.nc'
 ;outputfile=outputdir+'ecearth3.2'+'_'+modelname+'_'+simulation_id+'_'+vertical+'_'+time_string+'_monthly_v1.2_'+levels_id1+'_aerosol-optical-properties.nc'
 ;outputfile=outputdir+'tm5_clim_pi_aerosol_opt_v1.2_'+levels_id1+'.nc'
 ;outputfile=outputdir+'tm5_clim_pi_aerosol_opt_v2.0_'+levels_id1+'.nc'
 ;outputfile=outputdir+'tm5_clim_pi_aerosol_opt_v3.0_'+levels_id1+'.nc'
 ;outputfile=outputdir+'tm5_clim_pd_aerosol_opt_v3.0_'+levels_id1+'.nc'
 ;outputfile=outputdir+'tm5_clim_pi_aerosol_v1.2_'+levels_id1+'.nc'
 ;outputfile=outputdir+'tm5_clim_pi_aerosol_opt_v4.0_'+levels_id1+'.nc'
 ;outputfile=outputdir+'tm5_clim_pi_aerosol_opt_v5.0_153'+levels_id1+'.nc'
 ;outputfile=outputdir+'tm5_clim_pi_aerosol_opt_v5.0_155'+levels_id1+'.nc'
 ;outputfile=outputdir+'tm5_clim_pi_aerosol_opt_v5.0_157'+levels_id1+'.nc'
 ;outputfile=outputdir+'tm5_clim_pi_aerosol_opt_v5.0_203'+levels_id1+'.nc'
 ;outputfile=outputdir+'tm5_clim_pi_aerosol_opt_v5.0_205'+levels_id1+'.nc'
 ;outputfile=outputdir+'tm5_clim_pi_aerosol_opt_v5.0_207'+levels_id1+'.nc'
 outputfile=outputdir+'tm5_clim_mh2_aerosol_opt_'+levels_id1+'.nc'
 print, outputfile
 cdfid=ncdf_create(outputfile,/clobber)
 
 NCDF_ATTPUT, cdfid, /GLOBAL, 'institution', 'Royal Netherlands Meteorological Institute, De Bilt, The Netherlands'
 NCDF_ATTPUT, cdfid, /GLOBAL, 'institute_id', 'KNMI'
 NCDF_ATTPUT, cdfid, /GLOBAL, 'source', 'TM5-mp: CTM ERA-Interim 3x2 L34/L60, processed to '+levels_id2+' for EC-Earth'
 NCDF_ATTPUT, cdfid, /GLOBAL, 'model_id', modelname
 NCDF_ATTPUT, cdfid, /GLOBAL, 'references', 'Van Noije, T.P.C., et al. (Geosci. Model Dev., 7, 2435-2475, 2014); Van Noije, T.P.C., et al. (manuscript in preparation)' 
 NCDF_ATTPUT, cdfid, /GLOBAL, 'experiment_id', simulation_id
 ;NCDF_ATTPUT, cdfid, /GLOBAL, 'project_id', 'Pre-industrial aerosol climatolology for EC-Earth 3.2 (v1.2, based on CMIP5 emissions)'
 ;NCDF_ATTPUT, cdfid, /GLOBAL, 'project_id', 'Pre-industrial aerosol climatolology for EC-Earth 3.2 (v2.0, based on CMIP6 emissions)'
 ;NCDF_ATTPUT, cdfid, /GLOBAL, 'project_id', 'Pre-industrial aerosol climatolology for EC-Earth 3.2 (v3.0, based on latest CMIP6 emissions and TM5 model version)'
 ;NCDF_ATTPUT, cdfid, /GLOBAL, 'project_id', 'Present-day aerosol climatolology for EC-Earth 3.2 (v3.0, based on latest CMIP6 emissions and TM5 model version)'
 ;NCDF_ATTPUT, cdfid, /GLOBAL, 'project_id', 'Pre-industrial aerosol climatolology for EC-Earth 3.2 (v4.0, based on latest CMIP6 emissions and TM5 model version)'
 NCDF_ATTPUT, cdfid, /GLOBAL, 'project_id', 'Pre-industrial aerosol climatolology for EC-Earth 3.2 (v5.0, based on latest CMIP6 emissions and TM5 model version)'
 NCDF_ATTPUT, cdfid, /GLOBAL, 'title', 'TM5 model output prepared for EC-Earth'
 NCDF_ATTPUT, cdfid, /GLOBAL, 'Conventions', 'CF-1.6'
 ;NCDF_ATTPUT, cdfid, /GLOBAL, 'cmor_version', '2.6.0'
 NCDF_ATTPUT, cdfid, /GLOBAL, 'contact', 'Twan van Noije (noije@knmi.nl)'
 
 ;varnames_2d=['lon','lat','area']
 varnames_2d=['lon','lon_bnds','lat','lat_bnds'] 
 varnames_3d=['lev','a','a_bnds','b','b_bnds','p0','ps']
 ;varnames_3d=['lev','ap','ap_bnds','b','b_bnds','p0','ps'] 
 varnames_4d=['wav','wav_bnds'] 

 dim_lon=ncdf_dimdef(cdfid,'lon',nlon)
 dim_lat=ncdf_dimdef(cdfid,'lat',nlat)
 dim_lev=ncdf_dimdef(cdfid,'lev',nlev_ece)
 dim_wav=ncdf_dimdef(cdfid,'wav',nwav)
 dim_time=ncdf_dimdef(cdfid,'time',nmonth)
 dim_bnds=ncdf_dimdef(cdfid,'bnds',nbnds)
 varnames=[varnames_2d,'time','time_bnds',varnames_3d,varnames_4d,var_filenames]
 
 nvar=N_ELEMENTS(varnames)
 varid=intarr(nvar)
 for ivar=0,nvar-1 do begin
  varname=varnames[ivar]
  case varname of
    'lon': begin
      varid[ivar]=ncdf_vardef(cdfid,varname,dim_lon,/double)
      ncdf_attput,cdfid,varid[ivar],'units','degrees_east'
      ncdf_attput,cdfid,varid[ivar],'standard_name','longitude'
      ncdf_attput,cdfid,varid[ivar],'long_name','longitude'
      ncdf_attput,cdfid,varid[ivar],'axis','X'
      ncdf_attput,cdfid,varid[ivar],'bounds','lon_bnds'
    end
    'lon_bnds' : begin
      varid[ivar]=ncdf_vardef(cdfid,varname,[dim_bnds,dim_lon],/double)
    end
    'lat': begin
      varid[ivar]=ncdf_vardef(cdfid,varname,dim_lat,/double)
      ncdf_attput,cdfid,varid[ivar],'units','degrees_north'
      ncdf_attput,cdfid,varid[ivar],'standard_name','latitude'
      ncdf_attput,cdfid,varid[ivar],'long_name','latitude'
      ncdf_attput,cdfid,varid[ivar],'axis','Y'
      ncdf_attput,cdfid,varid[ivar],'bounds','lat_bnds'
    end
    'lat_bnds' : begin
      varid[ivar]=ncdf_vardef(cdfid,varname,[dim_bnds,dim_lat],/double)
    end
    'time': begin
      varid[ivar]=ncdf_vardef(cdfid,varname,dim_time,/double)
      ncdf_attput,cdfid,varid[ivar],'units','days since 1850-01-01 00:00'
      ncdf_attput,cdfid,varid[ivar],'standard_name','time'
      ncdf_attput,cdfid,varid[ivar],'long_name','time'
      ncdf_attput,cdfid,varid[ivar],'calendar','julian'
      ncdf_attput,cdfid,varid[ivar],'axis','T'
      ncdf_attput,cdfid,varid[ivar],'bounds','time_bnds'
    end
    'time_bnds' : begin
      varid[ivar]=ncdf_vardef(cdfid,varname,[dim_bnds,dim_time],/double)
    end
    'lev' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,dim_lev,/double)
        ncdf_attput,cdfid,varid[ivar],'units','1'
        ncdf_attput,cdfid,varid[ivar],'standard_name','atmosphere_hybrid_sigma_pressure_coordinate'
        ncdf_attput,cdfid,varid[ivar],'long_name','hybrid sigma pressure coordinate'
        ncdf_attput,cdfid,varid[ivar],'axis','Z'
        ncdf_attput,cdfid,varid[ivar],'positive','down'
        ncdf_attput,cdfid,varid[ivar],'stored_direction','decreasing'
        ncdf_attput,cdfid,varid[ivar],'valid_min','0.0'
        ncdf_attput,cdfid,varid[ivar],'valid_max','1.0'
        ncdf_attput,cdfid,varid[ivar],'formula','p(n,k,j,i) = a(k)*p0 + b(k)*ps(n,j,i)'
        ncdf_attput,cdfid,varid[ivar],'formula_terms','a: a b: b ps: ps p0: p0'
        ;ncdf_attput,cdfid,varid[ivar],'formula','p(n,k,j,i) = ap(k) + b(k)*ps(n,j,i)'
        ;ncdf_attput,cdfid,varid[ivar],'formula_terms','ap: ap b: b ps: ps p0: p0'
    end
    'wav' : begin
      varid[ivar]=ncdf_vardef(cdfid,varname,dim_wav,/double)
      ncdf_attput,cdfid,varid[ivar],'units','um'
      ncdf_attput,cdfid,varid[ivar],'standard_name','wavelength'
      ncdf_attput,cdfid,varid[ivar],'long_name','wavelength'
      ncdf_attput,cdfid,varid[ivar],'axis','W'
      ncdf_attput,cdfid,varid[ivar],'bounds','wav_bnds'
    end
    'wav_bnds' : begin
      varid[ivar]=ncdf_vardef(cdfid,varname,[dim_bnds,dim_wav],/double)
    end
    'a' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,dim_lev,/double)
        ncdf_attput,cdfid,varid[ivar],'units','1'
        ncdf_attput,cdfid,varid[ivar],'long_name','vertical coordinate formula term: a(k)'
    end
    'a_bnds' : begin
      varid[ivar]=ncdf_vardef(cdfid,varname,[dim_bnds,dim_lev],/double)
      ncdf_attput,cdfid,varid[ivar],'units','1'
      ncdf_attput,cdfid,varid[ivar],'long_name','vertical coordinate formula term: a(k+1/2)'      
    end
    'ap' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,dim_lev,/double)
        ncdf_attput,cdfid,varid[ivar],'units','Pa'
        ncdf_attput,cdfid,varid[ivar],'long_name','vertical coordinate formula term: ap(k)'
    end
    'ap_bnds' : begin
      varid[ivar]=ncdf_vardef(cdfid,varname,[dim_bnds,dim_lev],/double)
      ncdf_attput,cdfid,varid[ivar],'units','Pa'
      ncdf_attput,cdfid,varid[ivar],'long_name','vertical coordinate formula term: ap(k+1/2)'
    end
    'b' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,dim_lev,/double)
        ncdf_attput,cdfid,varid[ivar],'units','1'
        ncdf_attput,cdfid,varid[ivar],'long_name','vertical coordinate formula term: b(k)'
    end
    'b_bnds' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_bnds,dim_lev],/double)
        ncdf_attput,cdfid,varid[ivar],'units','1'
        ncdf_attput,cdfid,varid[ivar],'long_name','vertical coordinate formula term: b(k+1/2)'
    end
    'p0' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,/double)
        ncdf_attput,cdfid,varid[ivar],'units','Pa'
        ;ncdf_attput,cdfid,varid[ivar],'standard_name','reference_pressure_for_hybrid_sigma_pressure_coordinate'
        ;ncdf_attput,cdfid,varid[ivar],'long_name','reference pressure for hybrid sigma pressure coordinate
        ncdf_attput,cdfid,varid[ivar],'long_name','vertical coordinate formula term: reference pressure'
    end
    'area' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat],/float)
        ncdf_attput,cdfid,varid[ivar],'units','m2'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','area: sum'
        ncdf_attput,cdfid,varid[ivar],'standard_name','cell_area'
        ncdf_attput,cdfid,varid[ivar],'long_name','grid-cell area'
    end
    'areacella' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat],/float)
        ncdf_attput,cdfid,varid[ivar],'units','m2'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','area: sum'
        ncdf_attput,cdfid,varid[ivar],'standard_name','cell_area'
        ncdf_attput,cdfid,varid[ivar],'long_name','Atmosphere Grid-Cell Area'
    end
    'airmass' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg m-2'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','area: mean lev: sum time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','atmosphere_mass_content_of_air'
        ;ncdf_attput,cdfid,varid[ivar],'long_name','mass content of air'
        ncdf_attput,cdfid,varid[ivar],'long_name','Vertically Integrated Mass Content of Air in Layer'
    end 
    'ps': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','Pa'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','surface_air_pressure'
        ncdf_attput,cdfid,varid[ivar],'long_name','Surface Air Pressure'
      end
     'od4daer' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_wav,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','area: mean lev: sum wav time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','atmosphere_optical_depth_due_to_ambient_aerosol'
        ncdf_attput,cdfid,varid[ivar],'long_name','Ambient Aerosol Optical Depth'
      end
      'abs4daer' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_wav,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','area: mean lev: sum wav time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','atmosphere_absorption_due_to_ambient_aerosol'
        ncdf_attput,cdfid,varid[ivar],'long_name','Ambient Aerosol Absorption'
      end
      'sasy4daer' : begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_wav,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','area: mean lev: sum wav time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','atmosphere_asymmetry_parameter_of_ambient_aerosol_times_scattering_optical_depth'
        ncdf_attput,cdfid,varid[ivar],'long_name','Ambient Asymmetry Parameter Times Scattering Aerosol Optical Depth'
      end
      'od550aer': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','atmosphere_optical_thickness_due_to_ambient_aerosol'
        ;ncdf_attput,cdfid,varid[ivar],'standard_name','atmosphere_optical_thickness_due_to_ambient_aerosol'
        ncdf_attput,cdfid,varid[ivar],'long_name','Ambient Aerosol Optical Thickness at 550 nm'
      end
      'abs550aer': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','atmosphere_absorption_optical_thickness_due_to_ambient_aerosol'
        ncdf_attput,cdfid,varid[ivar],'long_name','Ambient Absorption Aerosol Optical Thickness at 550 nm'
      end
      'asyaer': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','atmosphere_asymmetry_parameter_of_ambient_aerosol'
        ncdf_attput,cdfid,varid[ivar],'long_name','Aerosol Asymmetry Parameter at 550 nm'
      end
      'nconc_nus': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','particles/kg(air)'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','particle_number_concentration_in_the_nucleation_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Nucleation Mode Particle Number Concentration'
      end
      'mmrso4_nus': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_sulfate_dry_aerosol_in_air_in_the_nucleation_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Nucleation Mode Sulfate Aerosol Mass Mixing Ratio'
      end
      'nconc_ais': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','particles/kg(air)'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','particle_number_concentration_in_the_soluble_Aitken_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Aitken Mode Particle Number Concentration'
      end
      'mmrso4_ais': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_sulfate_dry_aerosol_in_air_in_the_soluble_Aitken_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Aitken Mode Sulfate Aerosol Mass Mixing Ratio'
      end
      'mmrbc_ais': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_black_carbon_dry_aerosol_in_air_in_the_soluble_Aitken_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Aitken Mode BC Mass Mixing Ratio'
      end
      'mmroa_ais': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_particulate_organic_matter_dry_aerosol_in_air_in_the_soluble_Aitken_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Aitken Mode POM Mass Mixing Ratio'
      end
      'nconc_acs': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','particles/kg(air)'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','particle_number_concentration_in_the_soluble_accumulation_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Accumulation Mode Particle Number Concentration'
      end
      'mmrso4_acs': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_sulfate_dry_aerosol_in_air_in_the_soluble_accumulation_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Accumulation Mode Sulfate Aerosol Mass Mixing Ratio'
      end
      'mmrbc_acs': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_black_carbon_dry_aerosol_in_air_in_the_soluble_accumulation_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Accumulation Mode BC Mass Mixing Ratio'
      end
      'mmroa_acs': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_particulate_organic_matter_dry_aerosol_in_air_in_the_soluble_accumulation_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Accumulation Mode POM Mass Mixing Ratio'
      end
      'mmrss_acs': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_seasalt_dry_aerosol_in_air_in_the_soluble_accumulation_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Accumulation Mode Sea Salt Mass Mixing Ratio'
      end
      'mmrdust_acs': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_dust_dry_aerosol_in_air_in_the_soluble_accumulation_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Accumulation Mode Dust Mass Mixing Ratio'
      end
      'nconc_cos': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','particles/kg(air)'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','particle_number_concentration_in_the_soluble_coarse_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Coarse Mode Particle Number Concentration'
      end
      'mmrso4_cos': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_sulfate_dry_aerosol_in_air_in_the_soluble_coarse_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Coarse Mode Sulfate Aerosol Mass Mixing Ratio'
      end
      'mmrbc_cos': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_black_carbon_dry_aerosol_in_air_in_the_soluble_coarse_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Coarse Mode BC Mass Mixing Ratio'
      end
      'mmroa_cos': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_particulate_organic_matter_dry_aerosol_in_air_in_the_soluble_coarse_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Coarse Mode POM Mass Mixing Ratio'
      end
      'mmrss_cos': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_seasalt_dry_aerosol_in_air_in_the_soluble_coarse_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Coarse Mode Sea Salt Mass Mixing Ratio'
      end
      'mmrdust_cos': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_dust_dry_aerosol_in_air_in_the_soluble_coarse_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Soluble Coarse Mode Dust Mass Mixing Ratio'
      end
      'nconc_aii': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','particles/kg(air)'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','particle_number_concentration_in_the_insoluble_Aitken_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Insoluble Aitken Mode Particle Number Concentration'
      end
      'mmrbc_aii': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_black_carbon_dry_aerosol_in_air_in_the_insoluble_Aitken_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Insoluble Aitken Mode BC Mass Mixing Ratio'
      end
      'mmroa_aii': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_particulate_organic_matter_dry_aerosol_in_air_in_the_insoluble_Aitken_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Insoluble Aitken Mode POM Mass Mixing Ratio'
      end
      'nconc_aci': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','particles/kg(air)'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','particle_number_concentration_in_the_insoluble_accumulation_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Insoluble Accumulation Mode Particle Number Concentration'
      end
      'mmrdust_aci': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_dust_dry_aerosol_in_air_in_the_insoluble_accumulation_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Insoluble Accumulation Mode Dust Mass Mixing Ratio'
      end
      'nconc_coi': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','particles/kg(air)'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','particle_number_concentration_in_the_insoluble_coarse_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Insoluble Coarse Mode Particle Number Concentration'
      end
      'mmrdust_coi': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_dust_dry_aerosol_in_air_in_the_insoluble_coarse_mode'
        ncdf_attput,cdfid,varid[ivar],'long_name','Insoluble Coarse Mode Dust Mass Mixing Ratio'
      end
      'mmr_no3': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_nitrate_dry_aerosol_in_air'
        ncdf_attput,cdfid,varid[ivar],'long_name','Nitrate Aerosol Mass Mixing Ratio'
      end
      'mmr_nh4': begin
        varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
        ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
        ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
        ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_ammonium_dry_aerosol_in_air'
        ncdf_attput,cdfid,varid[ivar],'long_name','Ammonium Mass Mixing Ratio'
      end
      ;    'mmr_msa': begin
      ;      varid[ivar]=ncdf_vardef(cdfid,varname,[dim_lon,dim_lat,dim_lev,dim_time],/float)
      ;      ncdf_attput,cdfid,varid[ivar],'units','kg kg-1'
      ;      ncdf_attput,cdfid,varid[ivar],'cell_methods','lon: lat: lev: point time: mean'
      ;      ncdf_attput,cdfid,varid[ivar],'standard_name','mass_fraction_of_methanesulfonic_acid_dry_aerosol_in_air'
      ;      ncdf_attput,cdfid,varid[ivar],'long_name','MSA Mass Mixing Ratio'
      ;    end
     
    else: begin
        print,'Unknown varname ', varname
        stop
      end
  endcase
 endfor
  
 ncdf_control, cdfid,/endef
 
 for ivar=0,nvar-1 do begin
  varname=varnames[ivar]
  case varname of
    'lon' : begin
      ncdf_varput,cdfid,varid[ivar],lon
    end
    'lon_bnds' : begin
      ncdf_varput,cdfid,varid[ivar],lon_bnds
    end
    'lat' : begin
      ncdf_varput,cdfid,varid[ivar],lat
    end
    'lat_bnds' : begin
      ncdf_varput,cdfid,varid[ivar],lat_bnds
    end
    'time' : begin
      ncdf_varput,cdfid,varid[ivar],time  
    end
    'time_bnds' : begin
      ncdf_varput,cdfid,varid[ivar],time_bnds
    end
    'lev' : begin
      ncdf_varput, cdfid, varid[ivar],ece_lev
    end
    'wav' : begin
      ncdf_varput, cdfid, varid[ivar],wav
    end
    'wav_bnds' : begin
      ncdf_varput, cdfid, varid[ivar],wav_bnds
    end
    'a' : begin
       ncdf_varput,cdfid,varid[ivar],ece_a
    end
    'a_bnds' : begin
      ncdf_varput,cdfid,varid[ivar],ece_a_bnds
    end
    'ap' : begin
       ncdf_varput,cdfid,varid[ivar],ece_ap
    end
    'ap_bnds' : begin
      ncdf_varput,cdfid,varid[ivar],ece_ap_bnds
    end
    'b' : begin
       ncdf_varput,cdfid,varid[ivar],ece_b
    end
    'b_bnds' : begin
       ncdf_varput,cdfid,varid[ivar],ece_b_bnds
    end
    'p0' : begin
       ncdf_varput,cdfid,varid[ivar],p0
    end
    'area' : begin
       ncdf_varput,cdfid,varid[ivar],area
    end
    'areacella' : begin
       ncdf_varput,cdfid,varid[ivar],area 
    end
    'airmass' : begin
      ncdf_varput,cdfid,varid[ivar],ece_mass_air
    end
    'ps' : begin
      ncdf_varput,cdfid,varid[ivar],surfpres
    end
    'od4daer' : begin
      ncdf_varput,cdfid,varid[ivar],ece_aerod4d
    end
    'abs4daer' : begin
      ncdf_varput,cdfid,varid[ivar],ece_aerabs4d
    end
    'sasy4daer' : begin
      ncdf_varput,cdfid,varid[ivar],ece_aersasy4d
    end
    'od550aer': begin
      ncdf_varput,cdfid,varid[ivar],aerod550
    end
    'abs550aer': begin
      ncdf_varput,cdfid,varid[ivar], aerabs550
    end
    'asyaer': begin
      ncdf_varput,cdfid,varid[ivar], aerasy
    end
    'nconc_nus': begin
      ncdf_varput,cdfid,varid[ivar],ece_nus_nconc
    end
    
    'mmrso4_nus': begin
      ncdf_varput,cdfid,varid[ivar],ece_nus_so4mmr
    end
    'nconc_ais': begin
      ncdf_varput,cdfid,varid[ivar],ece_ais_nconc
    end
    'mmrso4_ais': begin
      ncdf_varput,cdfid,varid[ivar],ece_ais_so4mmr
    end
    'mmrbc_ais': begin
      ncdf_varput,cdfid,varid[ivar],ece_ais_bcmmr
    end
    'mmroa_ais': begin
      ncdf_varput,cdfid,varid[ivar],ece_ais_oammr
    end
    'nconc_acs': begin
      ncdf_varput,cdfid,varid[ivar],ece_acs_nconc
    end
    'mmrso4_acs': begin
      ncdf_varput,cdfid,varid[ivar],ece_acs_so4mmr
    end
    'mmrbc_acs': begin
      ncdf_varput,cdfid,varid[ivar],ece_acs_bcmmr
    end
    'mmroa_acs': begin
      ncdf_varput,cdfid,varid[ivar],ece_acs_oammr
    end
    'mmrss_acs': begin
      ncdf_varput,cdfid,varid[ivar],ece_acs_ssmmr
    end
    'mmrdust_acs': begin
      ncdf_varput,cdfid,varid[ivar],ece_acs_dummr
    end
    'nconc_cos': begin
      ncdf_varput,cdfid,varid[ivar],ece_cos_nconc
    end
    'mmrso4_cos': begin
      ncdf_varput,cdfid,varid[ivar],ece_cos_so4mmr
    end
    'mmrbc_cos': begin
      ncdf_varput,cdfid,varid[ivar],ece_cos_bcmmr
    end
    'mmroa_cos': begin
      ncdf_varput,cdfid,varid[ivar],ece_cos_oammr
    end
    'mmrss_cos': begin
      ncdf_varput,cdfid,varid[ivar],ece_cos_ssmmr
    end
    'mmrdust_cos': begin
      ncdf_varput,cdfid,varid[ivar],ece_cos_dummr
    end
    'nconc_aii': begin
      ncdf_varput,cdfid,varid[ivar],ece_aii_nconc
    end
    'mmrbc_aii': begin
      ncdf_varput,cdfid,varid[ivar],ece_aii_bcmmr
    end
    'mmroa_aii': begin
      ncdf_varput,cdfid,varid[ivar],ece_aii_oammr
    end
    'nconc_aci': begin
      ncdf_varput,cdfid,varid[ivar],ece_aci_nconc
    end
    'mmrdust_aci': begin
      ncdf_varput,cdfid,varid[ivar],ece_aci_dummr
    end
    'nconc_coi': begin
      ncdf_varput,cdfid,varid[ivar],ece_coi_nconc
    end
    'mmrdust_coi': begin
      ncdf_varput,cdfid,varid[ivar],ece_coi_dummr
    end
    'mmr_no3': begin
      ncdf_varput,cdfid,varid[ivar],ece_no3_ammr
    end
    'mmr_nh4': begin
      ncdf_varput,cdfid,varid[ivar],ece_nh4_mmr
    end
    ;'mmr_msa': begin
    ;ncdf_varput,cdfid,varid[ivar],ece_msa_mmr
    ;end

    else: begin
        print,'Unknown varname', varname
        stop
    end
  endcase
 endfor

 NCDF_CLOSE, cdfid

endif

END

