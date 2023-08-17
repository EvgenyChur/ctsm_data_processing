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
main=/work/mj0143/b381275/inputdata/atm/datm7/atm_forcing.datm7.MODEL/FORCING
pout=${main}/PREP_DATA/
if [[ ! -e $pout ]]; then
    mkdir $pout
fi

#FOLD_list=("FSDS" "TOTPREC" "TPHW")
#PRF_list=("FSDS" "Prec" "TPHW")
#ycount=2

FOLD_list=("TOTPREC")
PRF_list=("Prec")
ycount=0

fformat=nc

# ==========================   MAIN PROGRAM    =================================

for (( i=0; i<=ycount ; i++ ));
do
    sub_fld=${FOLD_list[${i}]} # input folder
    sub_prf=${PRF_list[${i}]}  # filename prefix

    # Create output folders:
    rm -r $pout/${sub_fld}
    if [[ ! -e $pout/${sub_fld} ]]; then
        mkdir $pout/${sub_fld}
    fi

    # iterate over the years to be processed:
    currentYear=${YEARSTART}
    while [[ ${currentYear} -le ${YEARSTOP} ]]; do
        echo "${sub_fld}"-"${currentYear}"

        # Input data (common for all):
        data_in=${main}/${sub_fld}/${sub_prf}_${currentYear}.${fformat}

        data_out=$pout/${sub_fld}/${sub_prf}_${currentYear}_fldmean2.${fformat}

        case "$sub_fld" in
            FSDS)
                ncks -v FSDS ${data_in} $pout/${sub_fld}/foo.nc
                ncwa -a lat,lon -y avg $pout/${sub_fld}/foo.nc ${data_out};;
                #cdo -L -fldmean $pout/${sub_fld}/foo.nc ${data_out};;
            TOTPREC)
                ncks -v TOTPREC ${data_in} $pout/${sub_fld}/foo_${currentYear}.nc
                ncwa -a lat,lon -y avg $pout/${sub_fld}/foo_${currentYear}.nc ${data_out};;
                #ncwa -a lat,lon -y sum $pout/${sub_fld}/foo.nc ${data_out};;

            TPHW)
                ncks -v FLDS,PSL,QREFHT,TREFHT,WIND ${data_in} $pout/${sub_fld}/foo.nc
                ncwa -a lat,lon -y avg $pout/${sub_fld}/foo.nc ${data_out};;
                #cdo -L -fldmean $pout/${sub_fld}/foo.nc ${data_out};;
        esac
        rm $pout/${sub_fld}/foo_${currentYear}.nc
        echo 'Done'
        (( currentYear = currentYear + 1 ))
    done
    cdo -L -mergetime $pout/${sub_fld}/*.nc $pout/${sub_prf}.${YEARSTART}_${YEARSTOP}_fldmean3.${fformat}
done


