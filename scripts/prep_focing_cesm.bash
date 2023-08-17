#!/bin/bash
#
# Script to remap CRUJRA climate data from 0.5° (r720x360)

# 'User' definitions

module load cdo
module load nco

# Time period:
YEARSTART=1850
YEARSTOP=1880 #1880

# Input data:
main=/work/mj0143/b381275/inputdata/atm/datm7/atm_forcing.datm7.MODEL
pin=${main}/RAW_DATA

# Research variables:
uwind=U
vwind=V
wind=WIND

TPHW_var_list="PSL QREFHT TREFHT FLDS WIND"
# ==========================   MAIN PROGRAM    =================================

# Create output folders:
pout_solar=${main}/FORCING/FSDS
rm -r $pout_solar
if [[ ! -e $pout_solar ]]; then
    mkdir $pout_solar
fi

pout_prec=${main}/FORCING/TOTPREC
rm -r $pout_prec
if [[ ! -e $pout_prec ]]; then
    mkdir $pout_prec
fi

pout_tphw=${main}/FORCING/TPHW
rm -r $pout_tphw
if [[ ! -e $pout_tphw ]]; then
    mkdir $pout_tphw
fi

# iterate over the years to be processed:
currentYear=${YEARSTART}
while [[ ${currentYear} -le ${YEARSTOP} ]]; do
    echo ${currentYear}
    # Input data (common for all):
    data_in=${pin}/${currentYear}.nc

    # --- New SOLAR forcing flux:
    echo 'Pre-processing of forcing data for SOLAR flux:'
    var='FSDS'
    ncks -v ${var} ${data_in} ${pout_solar}/foo.nc
    ncatted -O -a _FillValue,${var},o,f,1.e+36 ${pout_solar}/foo.nc
    ncatted -O -a missing_value,${var},o,f,1.e+36 ${pout_solar}/foo.nc
    ncatted -O -a units,${var},o,c,"W/m**2" ${pout_solar}/foo.nc
    ncatted -O -a long_name,${var},o,c,"total incident solar radiation" ${pout_solar}/foo.nc
    # Set global NetCDF attributes:
    ncatted -O -a history,global,d,c,"" ${pout_solar}/foo.nc ${pout_solar}/FSDS_${currentYear}.nc
    ncatted -O -h -a reference,global,c,c,"Initial data were presented by Sebastian Sipple" \
                  -a date,global,c,c,"created on $(date)" \
                  -a created_by,global,c,c,"Evgenii Churiulin, Ana Bastos" \
                  -a contact,global,c,c,"evchur@bgc-jena.mpg.de" \
                  -a institution,global,c,c,"Max Planck Institute for Biogeochemistry" \
                  -a institution_id,global,c,c,"MPI-BGC" \
                  -a model,global,c,c,"b.e212.B1850cmip6.f09_g17.001.nudge-1850-2100-SSP370.1300.linear-weak" \
                  -a model_id,global,c,c,"CESM 2.1.2" ${pout_solar}/FSDS_${currentYear}.nc
    # Delete temporal files:
    rm ${pout_solar}/foo*.nc

    # --- New TOTPREC forcing flux:
    echo 'Pre-processing of forcing data for TOTPREC flux:'
    var='TOTPREC'
    ncks -v ${var} ${data_in} ${pout_prec}/foo.nc
    ncap2 -s 'TOTPREC = TOTPREC * 1e3' ${pout_prec}/foo.nc ${pout_prec}/foo2.nc
    ncatted -O -a _FillValue,${var},o,f,1.e+36 ${pout_prec}/foo2.nc
    ncatted -O -a missing_value,${var},o,f,1.e+36 ${pout_prec}/foo2.nc
    ncatted -O -a units,${var},o,c,"mm H2O / sec" ${pout_prec}/foo2.nc
    ncatted -O -a long_name,${var},o,c,"total precipitation" ${pout_prec}/foo2.nc
    # Set global NetCDF attributes:
    ncatted -O -a history,global,d,c,"" ${pout_prec}/foo2.nc ${pout_prec}/Prec_${currentYear}.nc
    ncatted -O -h -a reference,global,c,c,"Initial data were presented by Sebastian Sipple" \
                  -a date,global,c,c,"created on $(date)" \
                  -a created_by,global,c,c,"Evgenii Churiulin, Ana Bastos" \
                  -a contact,global,c,c,"evchur@bgc-jena.mpg.de" \
                  -a institution,global,c,c,"Max Planck Institute for Biogeochemistry" \
                  -a institution_id,global,c,c,"MPI-BGC" \
                  -a model,global,c,c,"b.e212.B1850cmip6.f09_g17.001.nudge-1850-2100-SSP370.1300.linear-weak" \
                  -a model_id,global,c,c,"CESM 2.1.2" ${pout_prec}/Prec_${currentYear}.nc
    # Delete temporal files:
    rm ${pout_prec}/foo*.nc

    # --- New TPHW forcing flux:
    echo 'Pre-processing of WIND variable for TPHW forcing data:'
    ncks -v ${uwind} ${data_in} ${pout_tphw}/wind.nc
    ncks -A -v ${vwind} ${data_in} ${pout_tphw}/wind.nc
    ncap2 -s 'WIND=sqrt(U*U + V*V)' ${pout_tphw}/wind.nc ${pout_tphw}/wind_full.nc

    echo 'Pre-processing of TPHW forcing data:'
    ncks -v PSL,QREFHT,TREFHT,FLDS ${data_in} ${pout_tphw}/foo.nc
    echo 'Merge TPH data with WIND variable:'
    ncks -A -v WIND ${pout_tphw}/wind_full.nc ${pout_tphw}/foo.nc
    # Set parameters for variables:
    for VAR in $TPHW_var_list ; do
        ncatted -O -a _FillValue,${VAR},o,f,1.e+36 ${pout_tphw}/foo.nc
        ncatted -O -a missing_value,${VAR},o,f,1.e+36 ${pout_tphw}/foo.nc
        if [ ${VAR} == "WIND" ]; then
            ncatted -O -a units,${VAR},o,c,"m/s" ${pout_tphw}/foo.nc
            ncatted -O -a long_name,${VAR},o,c,"wind at the lowest atm level" ${pout_tphw}/foo.nc
        fi
    done
    # Set global NetCDF attributes:
    ncatted -O -a history,global,d,c,"" ${pout_tphw}/foo.nc ${pout_tphw}/TPHW_${currentYear}.nc
    ncatted -O -h -a reference,global,c,c,"Initial data were presented by Sebastian Sipple" \
                  -a date,global,c,c,"created on $(date)" \
                  -a created_by,global,c,c,"Evgenii Churiulin, Ana Bastos" \
                  -a contact,global,c,c,"evchur@bgc-jena.mpg.de" \
                  -a institution,global,c,c,"Max Planck Institute for Biogeochemistry" \
                  -a institution_id,global,c,c,"MPI-BGC" \
                  -a model,global,c,c,"b.e212.B1850cmip6.f09_g17.001.nudge-1850-2100-SSP370.1300.linear-weak" \
                  -a model_id,global,c,c,"CESM 2.1.2"  ${pout_tphw}/TPHW_${currentYear}.nc
    ncatted -O -a history,global,d,c,"" ${pout_tphw}/TPHW_${currentYear}.nc
    # Delete temporal files:
    rm ${pout_tphw}/foo*.nc ${pout_tphw}/wind.nc ${pout_tphw}/wind_full.nc

    echo 'Done'
    (( currentYear = currentYear + 1 ))
done


