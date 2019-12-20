;+
; NAME:
;	GET_TM5_HDF
;
; PURPOSE:
;       general HDF reader for TM5 hdf output files.
;
;       (This is "dirty"....Should have been an object for multiple
;       calls on the same file... to avoid too many i/o open/close,
;       and easier to maintain, particularly with the pointers! ...but
;       time is missing)
;
;
; CATEGORY:
;
;
;
; CALLING SEQUENCE:
;	GET_TM5_HDF, filename [, keywords]
;
;
; INPUTS:
;	Filename : HDF file to read
;
;
; OUTPUT KEYWORDS :
;	          NSDS   : number of datasets
;	          NATTR  : number of global attributes
;	          SNAME  : vector holding name of all SDS datasets
;                 ANAME  : vector holding name of all global ATTRIBUTES
;                 
;                 LONC/LATC : vectors of lon & lat CENTERS from general
;                             attributes in TM5 hdf files. If not found then
;                             return NaN.
;
;                 LONE/LATE : vectors of lon & lat EDGES from general
;                             attributes in TM5 hdf files. If not found then
;                             return NaN.
;
;                 PRESS : pressure from general attributes (A's and B's),
;                         assuming a surface pressure of 1000 hPa. If not
;                         found then return NaN.
;
;                 DATA    : output data
;                 SATTR   : attributes of requested SDS dataset (if any). This is
;                            an array of structures {name:'', data:ptr}. You
;                            should call Clean_TM5_ptr when done with these
;                            output.
;                 UNIT, LABEL, RANGE : SDS information if available. If UNIT
;                                       information is empty, it is looked for
;                                       in attributes as *unit*.
;
;                 SDATE, EDATE, WDATE : start, end, and writing date. Use the
;                            later for instantaneous fields, and the other two
;                            for average fields.
;                 
;                 VERBOSE : print additional information
;                 
;                 STATUS  : return code. 0 or positive =success, negative =
;                           failure. Filled with index of SDS or global
;                           attribute if any requested and found. Do not apply
;                           for LON/LAT/DATE retrievals.
;                 
; INPUT KEYWORDS :
; 	To select which data to return in "DATA" output keyword, you can use:
; 	
;                 ATTR   : name of global attribute to read
;                 AINDEX : index of global attribute to read
;                 
;                 TRACER : name of SDS set to read
;                 IND    : index of SDS set to read (output if not defined, is
;                                  filled with TRACER's index)
;                 NOTFORMAT : set to **NOT** format the S/E/WDATE output. 
;                         Default is to format them into YYYY/MM/DD. If set,
;                         you get: [year, month, day, hh, mm, ss] vector.
;                 
; RESTRICTIONS:
;	works with other HDF files for most of the general/common
;	request. But you probably will not get LON/LAT output, which
;	is unusually carried with TM5-hdf...
;
; EXAMPLE:
;
;       TO GET INFORMATION:
;       ===================
;
;       ; To get and print list of SDS names, and how many there are:
;       
;          GET_TM5_HDF, file, Sname=names, nsds=ns, /verb
;          
;          print, ns, n_elements(names) 
;
;
;       ; To get info about one SDS (example O3), including its Attributes :
;       
;          GET_TM5_HDF, file, tracer="O3",  /verb
;
;         ; or using an index
;
;          GET_TM5_HDF, file, ind=0,  /verb
;
;
;
;       ; To get and print list of Global Attributes name:
;       
;          GET_TM5_HDF, file, Aname=names, /verb
;
;
;       ; To get info about one Global Attribute :
;       
;          GET_TM5_HDF, file, Attr="dx",  /verb
;
;         ; or using an index
;
;          GET_TM5_HDF, file, Aind=0,  /verb
;
;
;
;       TO GET DATA:
;       ============
;
; 	; To get data from the first SDS in file, and its name return in
; 	; variable "name":
; 	
;	   GET_TM5_HDF, file, data=data, ind=0, tr=name
;	   
;	   print, name
;	   help, data
;
;
;       ; To get a data set, and the corresponding lon/lat/press:
;       
;          GET_TM5_HDF, file, tracer="O3", data=data, lonC=lon, latC=lat, $
;                                          press=press, stat=rc
;          
;          IF rc lt 0 THEN message, "no O3 data!"
;          
;          CONTOUR, data[*,*,0], lon, lat
;
;
;
;       ; To get a data set, and its attributes:
;       
;          GET_TM5_HDF, file, tracer="O3", data=data, Sattr=att, stat=rc
;          
;          IF rc lt 0 then  message, "no O3 data!"
;          
;          help, att, /struct
;          help, *att[0].data    ; to get the data of the 1st attribute
;
;          ; when you don't need them anymore, you must free their pointers if
;          ; you request SDS attributes:
;          
;          clean_tm5_ptr, att
;
;
;       ; To get one Global Attribute :
;       
;          GET_TM5_HDF, file, Attr="dx", data=data, /verb
;
;         ; or using an index
;
;          GET_TM5_HDF, file, Aind=0,  data=data,/verb;
;
;
;
; MODIFICATION HISTORY:
;    8 Nov 2010 - P. Le Sager - first documented version.
;   12 Nov 2010 - P. Le Sager - Added UNIT, LABEL, and RANGE output
;                    keyword. UNIT is search in the SDS attributes if not
;                    directly available. RANGE is gathered directly from DATA,
;                    if not directly available in the HDF file. 
;    1 Dec 2010 - P. Le Sager - Remove RANGE (always missing in TM5 hdf
;                 files!) output. Now distinguish between CENTER and EDGE
;                 LON/LAT.
;   11 Feb 2011 - P. Le Sager - return dates (start, end, ..)
;                             - fix for file with datasets without attributes
;   27 Apr 2011 - P. Le Sager - minor fixes for dates output and for
;                               checking hdf input 
;   30 Jun 2011 - P. Le Sager - NOTFORMAT keyword
;                             - tuned verbosity
;
;-

;------------------------------------------------------------------
FUNCTION gth_get_attr, fId, att, data=data, verb=verb
   
   ; get global attribute from file-ID and attribute name
   
   attId = HDF_SD_AttrFind( fId, att)
   
   if attId[0] lt 0 then begin
        if verb then message, 'cannot find attribute '+ att, /info
   endif else begin
        HDF_SD_ATTRINFO, fID, attId, data=data   
   endelse
   
   return, attId[0]
   
end
;------------------------------------------------------------------

PRO CLEAN_TM5_PTR, sds_attr
   
   ; free ptrs in the input (which must be an array of SdsAttr structure)
   
   on_error,  2
   
   for j=0L, n_elements(sds_attr)-1L do begin
        if ptr_valid(sds_attr[j].data) then ptr_free, sds_attr[j].data
   endfor
   
   return
end

;------------------------------------------------------------------

PRO GET_TM5_HDF, infilename,                           $  ; [in]
                 nSDS=nsds, nAttr=nattr, sname=name,   $  ; [out] global info
                 aname=aname,                          $  ;
                 lonC=lonC, latC=latC, press=press,    $  ; [out] global info
                 lonE=lonE, latE=latE,                 $  ; [out] global info
                 tracer=tr, ind=index, sattr=sds_attr, $  ; [in] to select SDS data to output
                 attr=attr, aind=aindex,               $  ; [in] to select Global Attr to output
                 data=data,                            $  ; [out] data
                 verbose=verb,                         $
                 status=stat,                          $
                 unit=units, label=label, range=range, $
                 sdate=sdate, edate=edate, wdate=wdate, notformat=notformat
   
   compile_opt idl2, logical_predicate
   on_error, 2

   ; --- On Error
   catch, bug
   if bug then begin
        catch, /cancel
        if n_elements(thissdsid) then HDF_SD_ENDACCESS, thissdsid      
        if n_elements(newfileid) then HDF_SD_END, newfileid
        if n_elements(sds_attr)  then clean_tm5_ptr, sds_attr
        if verb then print, "GET_TM5_HDF : cleanup"
        message, /reissue_last
   endif
   
   ; --- Init
   stat = -1
   verb = keyword_set(verb)
   if n_elements(index) && index lt 0 then $
      message, 'Requested Index cannot be negative. Returning...'
   clean = ~arg_present(sds_attr) 

   ; --- Check file
   if n_params() ne 1 then message, 'You must provide an HDF file as argument'
   filename=infilename[0]
   if ~hdf_ishdf(filename) then message, '"'+filename+'" is not an HDF file'
   
   ; --- Open file
   if verb then print, 'Opening "' + filename + '"'   
   newfileid = hdf_sd_start(filename, /read)
   hdf_sd_fileinfo, newfileid, nSDS, nAttr
   npal = hdf_dfp_npals(filename)
   
   ; --- Get list of data sets names (if requested)
   if arg_present(name) then begin   
        for klm=0L, nsds-1L do begin
             sds_id = HDF_SD_SELECT( newfileid, klm )
             HDF_SD_GETINFO, sds_id, name=oname;, ndim=ndim, natts=natts
             name = klm eq 0 ? oname :[name, oname]
             stat = 0
        endfor
        if verb then print, transpose([[sindgen(nSDS)], [name]])
   endif
   
   ; --- Get list of global attributes' name (if requested)
   if arg_present(aname) then begin
      if nAttr ne 0 then begin
         for klm=0L, nAttr-1L do begin
            HDF_SD_AttrINFO, newfileid, klm, name=oname
            aname = klm eq 0 ? oname :[aname, oname]
            stat = 0
         endfor
         if verb then print, transpose([[sindgen(nattr)], [aname]])
      endif else print, "There is 0 attribute."
   endif

   stat = 0
   
   ; --- Get a GLOBAL ATTRIBUTE
   ;------------------------------------------------
   if n_elements(attr) OR n_elements(aindex) then begin
        
        if n_elements(aindex) then begin
             if aindex lt 0 or aindex ge nAttr then $
                message, "requested index of Global Attribute is out of range!"
             HDF_SD_ATTRINFO, newfileid, aindex, data=data, name=oname
             attr = oname
             stat = aindex
        endif else $
           stat = gth_get_attr( newfileid, attr[0], data=data, verb=verb)
        
        ; information
        if verb then begin
             print, "Gl. Attr. Name : " + attr
             print, "    with index : " + strtrim(stat, 2)
             help, data
        endif
        
   endif else begin
        
        ; --- ... OR a SDS
        ;------------------------------------------------
        if ( n_elements(tr) ne 0 ) OR ( n_elements(index) ne 0 ) then begin
             
             stat = -1  ; reset rc
             
             ; get index, then id, then data and attr of the SDS.
             if n_elements(index) eq 0 then begin
                index = hdf_sd_nametoindex(newfileid, tr)
                ;PRINT,  'PLSPLS',  index
             endif
             
             if index lt 0 or index ge nSDS then $
                  message, 'Out-of-range SDS index requested: '+strtrim(index, 2) $
             else thissdsid = hdf_sd_select(newfileid, index)
             
             ; print the names of the gridded data attributes.
             hdf_sd_getinfo, thissdsid, natts=numattributes, ndim=ndim, $
                             dims=dims, name=snm, unit=units, label=label;, range=range
             
             ; the missing "else" could be a check:
             if n_elements(tr) eq 0 then tr = snm
             
             ; SDS attribute
             hasAtt = numattributes gt 0
             if hasAtt then begin
                Sds_Attr = REPLICATE({SdsAttr, name:'', data:ptr_new()}, numattributes)
                for j=0, numattributes-1 do begin
                   hdf_sd_attrinfo, thissdsid, j, name=thisattr, data=dd
                   sds_attr[j].name = thisattr
                   sds_attr[j].data = ptr_new(dd)
                endfor
             endif
             
             ; check for units in sds attributes
             if strlen(units) eq 0 then begin
                count = 0
                if hasAtt then $
                   uu = where(stregex(sds_attr.name, 'unit', /boolean, /fold), count)
                case count of
                   0 : if verb then print, "no units..."
                   1 : units = *sds_attr[uu].data
                   else : if verb then print, "More than one unit! Do " + $
                                              "not know how to choose.."  
                endcase
             endif 
                          
             ; get the data.
             hdf_sd_getdata, thissdsid, data

             ; Check for range
             if n_elements(range) eq 0 then range = [min(data, max=mm), mm]

             ; talker
             if verb then begin
                  print, ''
                  print, " Retrieve...."
                  print, "SDS name : ", snm
                  print, "   ndims : ", ndim
                  print, "    dims : ", dims
                  print, "   units : ", units
                  print, "   range : ", range
                  print, "   label : ", label
                  print, '  -----'
                  print, '  number of gridded data attributes: ', strtrim(numattributes, 2)
                  if hasAtt then begin
                     for j=0, numattributes-1 do begin
                        sz = size(sds_attr[j].data)
                        print, '   sds attribute no. ', + strtrim(j, 2), ': ', sds_attr[j].name
                        help,  *sds_attr[j].data
                     endfor
                  endif
             endif
             
             ; clean pointers if attributes are not returned to caller
             if clean and hasAtt then clean_tm5_ptr, sds_attr
             
             ; get the gridded dimension data. NOT AVAILABLE IN TM5 design....
             ;
             ;        longitudedimid = hdf_sd_dimgetid(thissdsid, 0)
             ;        latitudedimid = hdf_sd_dimgetid(thissdsid, 1)
             
             ;        hdf_sd_dimget, longitudedimid, name=name, count=count;label=lonlable, $
             ;                  unit=lonunits
             ;        print,  name, count
             ;        hdf_sd_dimget, latitudedimid, name=name, count=count;label=latlable, $
             ;unit=latunits
             ;        print, name, count
             
             ; close sd interface
             Hdf_Sd_Endaccess, thissdsid & undefine, thissdsid
             
             ; succes
             stat = index
        endif
   endelse
   
   
   ; get the lon/lat vectors from the global attrs:
   ;------------------------------------------------
   if arg_present(lonC) or arg_present(latC) or $
      arg_present(lonE) or arg_present(latE) then begin
        
        res = gth_get_attr( newfileid, 'xbeg', data=xbeg, verb=verb)   
        res = gth_get_attr( newfileid, 'ybeg', data=ybeg, verb=verb)  < res
        res = gth_get_attr( newfileid,   'dx', data=dx  , verb=verb)  < res
        res = gth_get_attr( newfileid,   'dy', data=dy  , verb=verb)  < res
        res = gth_get_attr( newfileid,   'im', data=im  , verb=verb)  < res
        res = gth_get_attr( newfileid,   'jm', data=jm  , verb=verb)  < res
        
        if res lt 0 then begin
             if verb then message,  "one or more global attributes that define LON/LAT is missing!", /info
             if verb then message,  "LON and LAT are set to NAN. ", /info
             lonC = ( latC = !values.f_nan )
             lonE = ( latE = !values.f_nan )
        endif else begin
             lonC = xbeg[0] + findgen(im[0])*dx[0] + dx[0]/2.
             latC = ybeg[0] + findgen(jm[0])*dy[0] + dy[0]/2.
             lonE = xbeg[0] + findgen(im[0])*dx[0]
             latE = ybeg[0] + findgen(jm[0])*dy[0]
        endelse
   endif
   
   
   ; Pressure (vertical dimension) from hybrid coeff
   ;------------------------------------------------
   if arg_present(press) then begin
        res = gth_get_attr( newfileid, 'at', data=hyam, verb=verb)   
        res = gth_get_attr( newfileid, 'bt', data=hybm, verb=verb) < res
        
        if res lt 0 then begin
             if verb then message,  "A and/or B hybrid coeff is missing!", /info
             if verb then message,  "PRESS is set to NAN. ", /info
             press = !values.f_nan
        endif else begin
             ps_surf = 1.0e5          ; constant [but we should use sthg better]
             zz = hyam + hybm*ps_surf ; Pa
             zz = zz/100.0            ; hPa
        endelse
   endif
   
   
   ; get time range (only if requested, since not always available)
   ;------------------------------------------------
   dateF = "(i4,'/',i2.2,'/',i2.2)"
   ft = ~keyword_set(notformat)
   six = intarr(6)

   if arg_present(sdate) then begin
      res = gth_get_attr( newfileid, 'idatei', data=sdate, verb=verb)
      if res ge 0 then begin
         if ft then sdate = string( sdate[0:2], format=dateF)
      endif else $
         sdate = ft ? '0000/00/00' : six
      if verb then print, "Run starts at "+sdate
   endif

   if arg_present(edate) then begin
      res = gth_get_attr( newfileid, 'idatee', data=edate, verb=verb)
      if res ge 0 then begin
         if ft then edate = string( edate[0:2], format=dateF)
      endif else $
         edate = ft ? '0000/00/00' : six
      if verb then print, "Run   ends at "+edate
   endif

   if arg_present(wdate) then begin
      res = gth_get_attr( newfileid, 'idatet', data=wdate, verb=verb)
      if res ge 0 then begin
         if ft then wdate = string( wdate[0:2], format=dateF)
      endif else $
         wdate = ft ? '0000/00/00' : six
   endif
   

   ; Done
   ; --------
   HDF_SD_END, newfileid & undefine, newfileid
   return
end
