
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "switch" {
    cd ../utils/
    run ./rest-verify-switch.sh ./test-switch.csv
    debug

    [ "${lines[2]}" = "ok switch SWITCH-1" ]
    [ "${lines[3]}" = "ok switch SWITCH-2" ]
    [ "${lines[4]}" = "ok switch SWITCH-3" ]
    [ "${lines[5]}" = "ok switch SWITCH-4" ]
    [ "${lines[6]}" = "ok switch SWITCH-5" ]
    [ "${lines[7]}" = "ok switch SWITCH-6" ]
}
