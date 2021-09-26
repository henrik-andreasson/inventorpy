
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "hsm backup unit" {
    cd ../utils/
    run ./rest-verify-hsm-backupunit.sh test-hsm-backup-unit.csv

    debug
    # URL: http://localhost:5000/api
    # User: admin
    [ "${lines[2]}" = "ok hsm-backup-unit fbno FB000001" ]
    [ "${lines[3]}" = "ok hsm-backup-unit model luna6" ]
    [ "${lines[4]}" = "ok hsm-backup-unit fbno FB000002" ]
    [ "${lines[5]}" = "ok hsm-backup-unit model luna6" ]
    [ "${lines[6]}" = "ok hsm-backup-unit fbno FB000003" ]
    [ "${lines[7]}" = "ok hsm-backup-unit model luna6" ]
    [ "${lines[8]}" = "ok hsm-backup-unit fbno FB000004" ]
    [ "${lines[9]}" = "ok hsm-backup-unit model luna6" ]
    [ "${lines[10]}" = "ok hsm-backup-unit fbno FB000005" ]
    [ "${lines[11]}" = "ok hsm-backup-unit model luna6" ]
    [ "${lines[12]}" = "ok hsm-backup-unit fbno FB000006" ]
    [ "${lines[13]}" = "ok hsm-backup-unit model luna6" ]
    [ "${lines[14]}" = "ok hsm-backup-unit fbno FB000007" ]
    [ "${lines[15]}" = "ok hsm-backup-unit model luna6" ]
    [ "${lines[16]}" = "ok hsm-backup-unit fbno FB000008" ]
    [ "${lines[17]}" = "ok hsm-backup-unit model luna6" ]
    [ "${lines[18]}" = "ok hsm-backup-unit fbno FB000009" ]
    [ "${lines[19]}" = "ok hsm-backup-unit model luna6" ]
    [ "${lines[20]}" = "ok hsm-backup-unit fbno FB000010" ]
    [ "${lines[21]}" = "ok hsm-backup-unit model luna6" ]
    [ "${lines[22]}" = "ok hsm-backup-unit fbno FB000011" ]
    [ "${lines[23]}" = "ok hsm-backup-unit model luna6" ]
    [ "${lines[24]}" = "ok hsm-backup-unit fbno FB000012" ]
    [ "${lines[25]}" = "ok hsm-backup-unit model luna6" ]

}
