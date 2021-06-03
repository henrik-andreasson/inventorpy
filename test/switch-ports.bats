
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "switch" {
    cd ../utils/
    run ./rest-verify-switch.sh ./test-switch.csv
    debug

    [ "${lines[2]}" = "ok switch port 1/2" ]
    [ "${lines[2]}" = "ok switch SWITCH-1/1" ]
    [ "${lines[2]}" = "ok switch port 1/2" ]
    [ "${lines[2]}" = "ok switch SWITCH-2/2" ]
    [ "${lines[2]}" = "ok switch port 1/2" ]
    [ "${lines[2]}" = "ok switch SWITCH-3/3" ]
    [ "${lines[2]}" = "ok switch port 1/2" ]
    [ "${lines[2]}" = "ok switch SWITCH-4/4" ]
    [ "${lines[2]}" = "ok switch port 1/2" ]
    [ "${lines[2]}" = "ok switch SWITCH-5/5" ]
    [ "${lines[2]}" = "ok switch port 1/2" ]
    [ "${lines[2]}" = "ok switch SWITCH-6/6" ]
}
