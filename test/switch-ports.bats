
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "switch-ports" {
    cd ../utils/
    run ./rest-verify-switch-ports.sh test-switch-ports.csv
    debug

    [ "${lines[2]}" = "ok switch port 1/2" ]
    [ "${lines[3]}" = "ok switch SWITCH-1/1" ]
    [ "${lines[4]}" = "ok switch port 1/2" ]
    [ "${lines[5]}" = "ok switch SWITCH-2/2" ]
    [ "${lines[6]}" = "ok switch port 1/2" ]
    [ "${lines[7]}" = "ok switch SWITCH-3/3" ]
    [ "${lines[8]}" = "ok switch port 1/2" ]
    [ "${lines[9]}" = "ok switch SWITCH-4/4" ]
    [ "${lines[10]}" = "ok switch port 1/2" ]
    [ "${lines[11]}" = "ok switch SWITCH-5/5" ]
    [ "${lines[12]}" = "ok switch port 1/2" ]
    [ "${lines[13]}" = "ok switch SWITCH-6/6" ]
}
