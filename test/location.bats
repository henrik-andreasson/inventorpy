
debug(){
  echo "# ${lines[0]}" >&3
  echo "# ${lines[1]}" >&3
  echo "# ${lines[2]}" >&3
  echo "# ${lines[3]}" >&3
  echo "# ${lines[4]}" >&3

}
@test "location" {
    cd ../utils/
    run ./rest-verify-location.sh ./test-location.csv
#    debug
    [ "${lines[2]}" = "ok place Stockholm" ]
    [ "${lines[3]}" = "ok facillity Kista" ]
    [ "${lines[4]}" = "ok area HQ" ]
    [ "${lines[5]}" = "ok type dc" ]
    [ "${lines[6]}" = "ok place Stockholm" ]
    [ "${lines[7]}" = "ok facillity Solna" ]
    [ "${lines[8]}" = "ok area dc1" ]
    [ "${lines[9]}" = "ok type dc" ]
    [ "${lines[10]}" = "ok place US" ]
    [ "${lines[11]}" = "ok facillity New York" ]
    [ "${lines[12]}" = "ok area ny office" ]
    [ "${lines[13]}" = "ok type office" ]
    [ "${lines[14]}" = "ok place UK" ]
    [ "${lines[15]}" = "ok facillity London" ]
    [ "${lines[16]}" = "ok area HQ" ]
    [ "${lines[17]}" = "ok type office" ]

}
