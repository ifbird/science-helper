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
  module load cdo/1.9.7.1
}

# Local/user defaults
# Explanation of colon in the beginning:
# https://stackoverflow.com/questions/32342841/colon-at-the-beginning-of-line-in-docker-entrypoint-bash-script
#
# First set version_name(version name, namely the source folder name), then build_root, 
set_variables () {
  # CSC project name and ece build config file
  export project_name=project_2000652
  export config_build_file=config-build_new.xml

  # subversion: tags, branches or projects
  export subversion=branches/projects/3.3.3.1-aerchemmip

  # version_name: usually the last part of subversion
  export version_name=3.3.3.1-aerchemmip

  # source code folder
  export build_root=/scratch/${project_name}/ece-src

  # exe files folder
  export install_root=/projappl/${project_name}/ece-exe

  # run folder
  export run_root=/scratch/${project_name}/ece-run

  # platform name
  export platform=csc-puhti-intel

  # Others
  # export: ${GRIBEX_TAR_GZ:=${HOME}/gribex_000370.tar.gz
  # export: ${REVNO:=7535
}

updatesources () {
    # [ "$REVNO" ] && local revflag="-r $REVNO"
    mkdir -p $build_root
    cd $build_root
    # svn checkout https://svn.ec-earth.org/ecearth3/$subversion ${build_root}/$version_name
    svn checkout https://svn.ec-earth.org/vendor/gribex/gribex_000370 ${build_root}/vendor/gribex_000370
    cd -
}

ecconfig () {
    cd ${build_root}/${version_name}/sources
    ./util/ec-conf/ec-conf --platform=${platform} ${config_build_file}
    cd -
}

oasis () {
    cd ${build_root}/${version_name}/sources/oasis3-mct/util/make_dir
    FCLIBS=" " make -f TopMakefileOasis3 BUILD_ARCH=ecconf
    cd -
}

lucia() {
    cd ${build_root}/${version_name}/sources/oasis3-mct/util/lucia
    bash lucia -c
    cd -
}

xios () {
    cd ${build_root}/${version_name}/sources/xios-2.5
    ./make_xios --dev --arch ecconf --use_oasis oasis3_mct --netcdf_lib netcdf4_par --job 4
    cd -
}

nemo () {
    cd ${build_root}/${version_name}/sources/nemo-3.6/CONFIG
    ./makenemo -n ORCA1L75_LIM3 -m ecconf -j 4
    cd -
}

oifs () {
    # gribex first
    cd ${build_root}/vendor/gribex_000370
    ./build_library <<EOF
i
y
${build_root}/${version_name}/sources/ifs-36r4/lib
n
EOF
    mv libgribexR64.a ${build_root}/${version_name}/sources/ifs-36r4/lib
    cd -

    # ifs
    cd ${build_root}/${version_name}/sources/ifs-36r4
    #sed -i '666s/STATUS=IRET/IRET/' src/ifsaux/module/grib_api_interface.F90
    make BUILD_ARCH=ecconf -j 8 lib
    make BUILD_ARCH=ecconf master
    cd -
}

tm5 () {
    cd ${build_root}/${version_name}/sources/tm5mp
    # patch -u -p0 < $thisdir/tm5.patch
    sed -i 's/\?//g' base/convection.F90
    PATH=${build_root}/${version_name}/sources/util/makedepf90/bin:$PATH ./setup_tm5 -n -j 4 ecconfig-ecearth3.rc
    cd -
}

runoff-mapper () {
    cd ${build_root}/${version_name}/sources/runoff-mapper/src
    make
    cd -
}

amip-forcing () {
    cd ${build_root}/${version_name}/sources/amip-forcing/src
    make
    cd -
}

lpj-guess () {
    cd ${build_root}/${version_name}/sources/lpjg/build
    cmake .. -DCMAKE_Fortran_FLAGS="-I${HPCX_MPI_INSTALL_ROOT}/lib"
    make # Fails with int <---> MPI_Comm type errors...
    cd -
}

# Install
install_all () {
    mkdir -p ${install_root}/${version_name}/
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
        cp -f ${build_root}/${version_name}/sources/${exe} ${install_root}/${version_name}/
    done
    cp -f ${CDO_INSTALL_ROOT}/bin/cdo ${install_root}/${version_name}/
}

# Create run directory and fix stuff
create_ece_run () {
    mkdir -p ${run_root}/${version_name}
    cd ${run_root}/${version_name}

    # mkdir -p ece-${VERNAME}
    \cp -r ${build_root}/${version_name}/runtime/* ${run_root}/${version_name}
    # \cp ${platform}.cfg.tmpl ${run_root}/classic/platform/
    # \cp ${platform}.xml ${run_root}/classic/platform/
    \cp classic/ece-esm.sh.tmpl classic/ece-ifs+nemo+tm5.sh.tmpl
    # sed "s|THIS_NEEDS_TO_BE_CHANGED|${install_root}/${VERNAME}/${REVNO}|" ${thisdir}/rundir.patch | patch -u -p0
    cd -

    mkdir -p ${run_root}/${version_name}/tm5mp
    cd ${run_root}/${version_name}/tm5mp
    \cp -r ${build_root}/${version_name}/sources/tm5mp/rc .
    \cp -r ${build_root}/${version_name}/sources/tm5mp/bin .
    \cp -r ${build_root}/${version_name}/sources/tm5mp/build .

    # Delete setup_tm5 if it exists
    rm -f setup_tm5
    ln -s bin/pycasso_setup_tm5 setup_tm5
    cd -
}


### Execute all functions if this script is not sourced ###

# if ! ${sourced}; then
#     updatesources
#     ( module -t list 2>&1 ) > ${build_root}/${VERNAME}/modules.log
#     ( ecconfig       2>&1 ) > ${build_root}/${VERNAME}/ecconf.log
#     ( oasis          2>&1 ) > ${build_root}/${VERNAME}/oasis.log    &
#     wait
#     ( lucia          2>&1 ) > ${build_root}/${VERNAME}/lucia.log    &
#     ( xios           2>&1 ) > ${build_root}/${VERNAME}/xios.log &
#     ( tm5            2>&1 ) > ${build_root}/${VERNAME}/tm5.log  &
#     wait
#     ( oifs           2>&1 ) > ${build_root}/${VERNAME}/ifs.log &
#     ( nemo           2>&1 ) > ${build_root}/${VERNAME}/nemo.log &
#     ( runoff-mapper  2>&1 ) > ${build_root}/${VERNAME}/runoff.log &
#     wait
#     ( amip-forcing   2>&1 ) > ${build_root}/${VERNAME}/amipf.log &
#     wait
#     install_all
#     create_ece_run
# fi
