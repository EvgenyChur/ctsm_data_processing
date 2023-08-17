#!/bin/bash
#
# Script to remap CRUJRA climate data from 0.5° (r720x360)

# 'User' definitions

module load cdo
module load nco

# Time period:
YEARSTART=1901
YEARSTOP=1920 #1880


# Input data:
main=/work/mj0143/b381275/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516
pout=${main}/PREP_DATA
if [[ ! -e $pout ]]; then
    mkdir $pout
fi

#FOLD_list=("Solar" "Precip" "TPHWL")
#PRF_list=("Solr" "Prec" "TPQWL")
#ycount=2

FOLD_list=("Precip")
PRF_list=("Prec")
ycount=0


fname=clmforc.GSWP3.c2011.0.5x0.5


fformat=nc

# Research variables:
month_list="01 02 03 04 05 06 07 08 09 10 11 12"
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
        # iterate over months:
        for mon in $month_list; do
            # Input data (common for all):
            data_in=${main}/${sub_fld}/${fname}.${sub_prf}.${currentYear}-${mon}.${fformat}
            data_out=$pout/${sub_fld}/${fname}.${sub_prf}.${currentYear}-${mon}_fldmean.${fformat}

            case "$sub_fld" in
                Solar)
                    ncks -v FSDS ${data_in} $pout/${sub_fld}/foo.nc
                    ncwa -a lat,lon -y avg $pout/${sub_fld}/foo.nc ${data_out};;
                Precip)
                    #cdo -L -fldsum -selname,PRECTmms ${data_in} ${data_out};;
                    ncks -v PRECTmms ${data_in} $pout/${sub_fld}/foo.nc
                    #ncwa -a lat,lon -y sum $pout/${sub_fld}/foo.nc ${data_out};;
                    ncwa -a lat,lon -y avg $pout/${sub_fld}/foo.nc ${data_out};;
                TPHWL)
                    ncks -v PSRF,TBOT,WIND,QBOT,FLDS ${data_in} $pout/${sub_fld}/foo.nc
                    ncwa -a lat,lon -y avg $pout/${sub_fld}/foo.nc ${data_out};;
            esac
            rm $pout/${sub_fld}/foo.nc
        done
        echo 'Done'
        (( currentYear = currentYear + 1 ))
    done
    cdo -L -mergetime $pout/${sub_fld}/*.nc $pout/${fname}.${sub_prf}.${YEARSTART}_${YEARSTOP}_fldmean.${fformat}
done
