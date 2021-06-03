
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "firewall" {
    cd ../utils/
    run ./rest-verify-firewall.sh ./test-firewall.csv
    debug
    [ "${lines[2]}" = "ok firewall fw-1" ]
    [ "${lines[3]}" = "ok firewall fw-2" ]
    [ "${lines[4]}" = "ok firewall fw-3" ]
    [ "${lines[5]}" = "ok firewall fw-4" ]
    [ "${lines[6]}" = "ok firewall fw-5" ]
    [ "${lines[7]}" = "ok firewall fw-6" ]
}
