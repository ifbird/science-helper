# Usage:
# $ source setup.sh
# Then use diffferent functions to complete the jobs.

# Environment setup
load_ece3_modules () {
  module purge

  module load intel/19.0.4
  module load hpcx-mpi/2.4.0
  module load intel-mkl/2019.0.4
  module load hdf/4.2.13
  module load hdf5/1.10.4-mpi
  module load netcdf/4.7.0
  module load netcdf-fortran/4.4.4
  module load grib-api/1.24.0
  module load cmake/3.12.3
}

# Local/user defaults
# Explanation of colon in the beginning:
# https://stackoverflow.com/questions/32342841/colon-at-the-beginning-of-line-in-docker-entrypoint-bash-script
#
# First set TAG, then BLDROOT, 
set_variables () {
  export project_name=project_2001025
  export config_build_file=config-build_new.xml

  # tag
  export TAG=3.3.1

  # source code folder
  export BLDROOT=/projappl/${project_name}/ece3

  # exe files folder
  export INSTALLROOT=/projappl/${project_name}/ece3/installs
  export RUNROOT=/scratch/${project_name}/ece3/test_esm
  export PLATFORM=csc-puhti-intel
  # export: ${GRIBEX_TAR_GZ:=${HOME}/gribex_000370.tar.gz
  # export: ${REVNO:=7535
}

updatesources () {
    # [ "$REVNO" ] && local revflag="-r $REVNO"
    mkdir -p $BLDROOT
    cd $BLDROOT
    svn checkout https://svn.ec-earth.org/ecearth3/tags/$TAG $TAG
    svn checkout https://svn.ec-earth.org/vendor/gribex/gribex_000370 gribex_000370
    cd -
}

ecconfig () {
    cd ${BLDROOT}/${TAG}/sources
    ./util/ec-conf/ec-conf --platform=${PLATFORM} ${config_build_file}
    cd -
}

oasis () {
    cd ${BLDROOT}/${TAG}/sources/oasis3-mct/util/make_dir
    FCLIBS=" " make -f TopMakefileOasis3 BUILD_ARCH=ecconf
    cd -
}

lucia() {
    cd ${BLDROOT}/${TAG}/sources/oasis3-mct/util/lucia
    bash lucia -c
    cd -
}

xios () {
    cd ${BLDROOT}/${TAG}/sources/xios-2.5
    ./make_xios --dev --arch ecconf --use_oasis oasis3_mct --netcdf_lib netcdf4_par --job 4
    cd -
}

nemo () {
    cd ${BLDROOT}/${TAG}/sources/nemo-3.6/CONFIG
    ./makenemo -n ORCA1L75_LIM3 -m ecconf -j 4
    cd -
}

oifs () {
    # gribex first
    cd ${BLDROOT}/gribex_000370
    ./build_library <<EOF
i
y
${BLDROOT}/${TAG}/sources/ifs-36r4/lib
n
EOF
    mv libgribexR64.a ${BLDROOT}/${TAG}/sources/ifs-36r4/lib
    cd -

    # ifs
    cd ${BLDROOT}/${TAG}/sources/ifs-36r4
    #sed -i '666s/STATUS=IRET/IRET/' src/ifsaux/module/grib_api_interface.F90
    make BUILD_ARCH=ecconf -j 8 lib
    make BUILD_ARCH=ecconf master
    cd -
}


tm5 () {
    cd ${BLDROOT}/${TAG}/sources/tm5mp
    # patch -u -p0 < $thisdir/tm5.patch
    sed -i 's/\?//g' base/convection.F90
    PATH=${BLDROOT}/${TAG}/sources/util/makedepf90/bin:$PATH ./setup_tm5 -n -j 4 ecconfig-ecearth3.rc
    cd -
}

runoff-mapper () {
    cd ${BLDROOT}/${TAG}/sources/runoff-mapper/src
    make
    cd -
}

amip-forcing () {
    cd ${BLDROOT}/${TAG}/sources/amip-forcing/src
    make
    cd -
}

lpj-guess () {
    cd ${BLDROOT}/${TAG}/sources/lpjg/build
    cmake .. -DCMAKE_Fortran_FLAGS="-I${HPCX_MPI_INSTALL_ROOT}/lib"
    make # Fails with int <---> MPI_Comm type errors...
    cd -
}

# Install
install_all () {
    mkdir -p ${INSTALLROOT}/${TAG}/
    local exes=(
        xios-2.5/bin/xios_server.exe
        nemo-3.6/CONFIG/ORCA1L75_LIM3/BLD/bin/nemo.exe
        ifs-36r4/bin/ifsmaster-ecconf
        runoff-mapper/bin/runoff-mapper.exe
        amip-forcing/bin/amip-forcing.exe
        tm5mp/build/appl-tm5.x
        oasis3-mct/util/lucia/lucia.exe
        oasis3-mct/util/lucia/lucia
        oasis3-mct/util/lucia/balance.gnu)
    for exe in "${exes[@]}"; do
        cp -f ${BLDROOT}/${TAG}/sources/${exe} ${INSTALLROOT}/${TAG}/
    done
    cp -f ${CDO_INSTALL_ROOT}/bin/cdo ${INSTALLROOT}/${TAG}/
}

# Create run directory and fix stuff
create_ece_run () {
    mkdir -p $RUNROOT
    cd $RUNROOT

    # mkdir -p ece-${TAG}
    \cp -r ${BLDROOT}/${TAG}/runtime/* ${RUNROOT}
    # \cp ${PLATFORM}.cfg.tmpl ${RUNROOT}/classic/platform/
    # \cp ${PLATFORM}.xml ${RUNROOT}/classic/platform/
    \cp classic/ece-esm.sh.tmpl classic/ece-ifs+nemo+tm5.sh.tmpl
    # sed "s|THIS_NEEDS_TO_BE_CHANGED|${INSTALLROOT}/${TAG}/${REVNO}|" ${thisdir}/rundir.patch | patch -u -p0
    cd -

    mkdir -p ${RUNROOT}/tm5mp
    cd ${RUNROOT}/tm5mp
    \cp -r ${BLDROOT}/${TAG}/sources/tm5mp/rc .
    \cp -r ${BLDROOT}/${TAG}/sources/tm5mp/bin .
    \cp -r ${BLDROOT}/${TAG}/sources/tm5mp/build .

    # Delete setup_tm5 if it exists
    rm -f setup_tm5
    ln -s bin/pycasso_setup_tm5 setup_tm5
    cd -
}


### Execute all functions if this script is not sourced ###

# if ! ${sourced}; then
#     updatesources
#     ( module -t list 2>&1 ) > ${BLDROOT}/${TAG}/modules.log
#     ( ecconfig       2>&1 ) > ${BLDROOT}/${TAG}/ecconf.log
#     ( oasis          2>&1 ) > ${BLDROOT}/${TAG}/oasis.log    &
#     wait
#     ( lucia          2>&1 ) > ${BLDROOT}/${TAG}/lucia.log    &
#     ( xios           2>&1 ) > ${BLDROOT}/${TAG}/xios.log &
#     ( tm5            2>&1 ) > ${BLDROOT}/${TAG}/tm5.log  &
#     wait
#     ( oifs           2>&1 ) > ${BLDROOT}/${TAG}/ifs.log &
#     ( nemo           2>&1 ) > ${BLDROOT}/${TAG}/nemo.log &
#     ( runoff-mapper  2>&1 ) > ${BLDROOT}/${TAG}/runoff.log &
#     wait
#     ( amip-forcing   2>&1 ) > ${BLDROOT}/${TAG}/amipf.log &
#     wait
#     install_all
#     create_ece_run
# fi
