
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}

@test "safe" {
    cd ../utils/
    run ./rest-verify-safe.sh ./test-safe.csv
    debug
    [ "${lines[2]}" = "ok safe name TEST-SAFE-STHLM-1" ]
    [ "${lines[3]}" = "ok safe location 1" ]
    [ "${lines[4]}" = "ok safe name TEST-SAFE-STHLM-2" ]
    [ "${lines[5]}" = "ok safe location 1" ]
    [ "${lines[6]}" = "ok safe name TEST-SAFE-STHLM-3" ]
    [ "${lines[7]}" = "ok safe location 1" ]
    [ "${lines[8]}" = "ok safe name TEST-SAFE-STHLM-4" ]
    [ "${lines[9]}" = "ok safe location 2" ]
    [ "${lines[10]}" = "ok safe name TEST-SAFE-STHLM-5" ]
    [ "${lines[11]}" = "ok safe location 2" ]
    [ "${lines[12]}" = "ok safe name TEST-SAFE-STHLM-6" ]
    [ "${lines[13]}" = "ok safe location 2" ]
}
