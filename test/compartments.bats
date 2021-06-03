
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}

@test "compartment" {
    cd ../utils/
    run ./rest-verify-compartment.sh ./test-compartment.csv
    debug
    [ "${lines[2]}" = "ok compartment TEST-COMP-KISTA-1" ]
    [ "${lines[3]}" = "ok compartment username user1" ]
    [ "${lines[4]}" = "ok compartment safe TEST-SAFE-STHLM-1" ]
    [ "${lines[5]}" = "ok compartment TEST-COMP-KISTA-2" ]
    [ "${lines[6]}" = "ok compartment username user2" ]
    [ "${lines[7]}" = "ok compartment safe TEST-SAFE-STHLM-1" ]
    [ "${lines[8]}" = "ok compartment TEST-COMP-KISTA-3" ]
    [ "${lines[9]}" = "ok compartment username user3" ]
    [ "${lines[10]}" = "ok compartment safe TEST-SAFE-STHLM-1" ]
    [ "${lines[11]}" = "ok compartment TEST-COMP-SOLNA-1" ]
    [ "${lines[12]}" = "ok compartment username user1" ]
    [ "${lines[13]}" = "ok compartment safe TEST-SAFE-STHLM-4" ]
    [ "${lines[14]}" = "ok compartment TEST-COMP-SOLNA-2" ]
    [ "${lines[15]}" = "ok compartment username user2" ]
    [ "${lines[16]}" = "ok compartment safe TEST-SAFE-STHLM-4" ]
    [ "${lines[17]}" = "ok compartment TEST-COMP-SOLNA-3" ]
    [ "${lines[18]}" = "ok compartment username user3" ]
    [ "${lines[19]}" = "ok compartment safe TEST-SAFE-STHLM-4" ]
  }
