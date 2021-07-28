
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "rack" {
    cd ../utils/
    run ./rest-verify-rack.sh ./test-rack.csv
    debug
    [ "${lines[2]}" = "ok rack RACK-1" ]
    [ "${lines[3]}" = "ok rack location_long_name Stockholm / Solna / dc1 / Floor 1" ]
    [ "${lines[4]}" = "ok rack RACK-2" ]
    [ "${lines[5]}" = "ok rack location_long_name Stockholm / Kista / HQ / Floor 1" ]
    [ "${lines[6]}" = "ok rack RACK-3" ]
    [ "${lines[7]}" = "ok rack location_long_name Stockholm / Solna / dc1 / Floor 1" ]
    [ "${lines[8]}" = "ok rack RACK-4" ]
    [ "${lines[9]}" = "ok rack location_long_name Stockholm / Kista / HQ / Floor 1" ]
    [ "${lines[10]}" = "ok rack RACK-5" ]
    [ "${lines[11]}" = "ok rack location_long_name Stockholm / Solna / dc1 / Floor 1" ]
    [ "${lines[12]}" = "ok rack RACK-6" ]
    [ "${lines[13]}" = "ok rack location_long_name Stockholm / Kista / HQ / Floor 1" ]
}
