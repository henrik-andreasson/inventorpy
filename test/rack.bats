
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
    [ "${lines[3]}" = "ok rack RACK-2" ]
    [ "${lines[4]}" = "ok rack RACK-3" ]
    [ "${lines[5]}" = "ok rack RACK-4" ]
    [ "${lines[6]}" = "ok rack RACK-5" ]
    [ "${lines[7]}" = "ok rack RACK-6" ]
}
