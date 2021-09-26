
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "hsm ped" {
    cd ../utils/
    run ./rest-verify-hsm-ped.sh test-hsm-ped.csv

    debug
    # URL: http://localhost:5000/api
    # User: admin
    [ "${lines[2]}" = "ok hsm-ped sn 1" ]
    [ "${lines[3]}" = "ok hsm-ped type blue" ]
    [ "${lines[4]}" = "ok hsm-ped sn 2" ]
    [ "${lines[5]}" = "ok hsm-ped type blue" ]
    [ "${lines[6]}" = "ok hsm-ped sn 3" ]
    [ "${lines[7]}" = "ok hsm-ped type blue" ]
    [ "${lines[8]}" = "ok hsm-ped sn 4" ]
    [ "${lines[9]}" = "ok hsm-ped type blue" ]
    [ "${lines[10]}" = "ok hsm-ped sn 5" ]
    [ "${lines[11]}" = "ok hsm-ped type blue" ]
    [ "${lines[12]}" = "ok hsm-ped sn 6" ]
    [ "${lines[13]}" = "ok hsm-ped type blue" ]
    [ "${lines[14]}" = "ok hsm-ped sn 7" ]
    [ "${lines[15]}" = "ok hsm-ped type blue" ]
    [ "${lines[16]}" = "ok hsm-ped sn 8" ]
    [ "${lines[17]}" = "ok hsm-ped type blue" ]
    [ "${lines[18]}" = "ok hsm-ped sn 9" ]
    [ "${lines[19]}" = "ok hsm-ped type red2" ]
    [ "${lines[20]}" = "ok hsm-ped sn 10" ]
    [ "${lines[21]}" = "ok hsm-ped type red2" ]
    [ "${lines[22]}" = "ok hsm-ped sn 11" ]
    [ "${lines[23]}" = "ok hsm-ped type red" ]
    [ "${lines[24]}" = "ok hsm-ped sn 12" ]
    [ "${lines[25]}" = "ok hsm-ped type red" ]
    [ "${lines[26]}" = "ok hsm-ped sn 13" ]
    [ "${lines[27]}" = "ok hsm-ped type red" ]
    [ "${lines[28]}" = "ok hsm-ped sn 14" ]
    [ "${lines[29]}" = "ok hsm-ped type red" ]
    [ "${lines[30]}" = "ok hsm-ped sn 15" ]
    [ "${lines[31]}" = "ok hsm-ped type red" ]
    [ "${lines[32]}" = "ok hsm-ped sn 16" ]
    [ "${lines[33]}" = "ok hsm-ped type red" ]
    [ "${lines[34]}" = "ok hsm-ped sn 17" ]
    [ "${lines[35]}" = "ok hsm-ped type red" ]
    [ "${lines[36]}" = "ok hsm-ped sn 18" ]
    [ "${lines[37]}" = "ok hsm-ped type red" ]
    [ "${lines[38]}" = "ok hsm-ped sn 19" ]
    [ "${lines[39]}" = "ok hsm-ped type black" ]
    [ "${lines[40]}" = "ok hsm-ped sn 20" ]
    [ "${lines[41]}" = "ok hsm-ped type black" ]
    [ "${lines[42]}" = "ok hsm-ped sn 21" ]
    [ "${lines[43]}" = "ok hsm-ped type black" ]
    [ "${lines[44]}" = "ok hsm-ped sn 22" ]
    [ "${lines[45]}" = "ok hsm-ped type black" ]
    [ "${lines[46]}" = "ok hsm-ped sn 23" ]
    [ "${lines[47]}" = "ok hsm-ped type black" ]
    [ "${lines[48]}" = "ok hsm-ped sn 24" ]
    [ "${lines[49]}" = "ok hsm-ped type black" ]
    [ "${lines[50]}" = "ok hsm-ped sn 25" ]
    [ "${lines[51]}" = "ok hsm-ped type black" ]
    [ "${lines[52]}" = "ok hsm-ped sn 26" ]
    [ "${lines[53]}" = "ok hsm-ped type black" ]
    [ "${lines[54]}" = "ok hsm-ped sn 27" ]
    [ "${lines[55]}" = "ok hsm-ped type black" ]
    [ "${lines[56]}" = "ok hsm-ped sn 28" ]
    [ "${lines[57]}" = "ok hsm-ped type black" ]
    [ "${lines[58]}" = "ok hsm-ped sn 29" ]
    [ "${lines[59]}" = "ok hsm-ped type orange" ]
    [ "${lines[60]}" = "ok hsm-ped sn 30" ]
    [ "${lines[61]}" = "ok hsm-ped type orange" ]
}
