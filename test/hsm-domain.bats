
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "service" {
    cd ../utils/
    run ./rest-verify-hsm-domain.sh test-hsm-domain.csv

    debug
    [ "${lines[2]}" = "ok hsm-domain name hsmdom1" ]
    [ "${lines[3]}" = "ok hsm-domain service service1" ]
    [ "${lines[4]}" = "ok hsm-domain name hsmdom2" ]
    [ "${lines[5]}" = "ok hsm-domain service service2" ]
    [ "${lines[6]}" = "ok hsm-domain name hsmdom3" ]
    [ "${lines[7]}" = "ok hsm-domain service service3" ]
    [ "${lines[8]}" = "ok hsm-domain name hsmdom4" ]
    [ "${lines[9]}" = "ok hsm-domain service service4" ]
    [ "${lines[10]}" = "ok hsm-domain name hsmdom5" ]
    [ "${lines[11]}" = "ok hsm-domain service service5" ]
    [ "${lines[12]}" = "ok hsm-domain name hsmdom6" ]
    [ "${lines[13]}" = "ok hsm-domain service service6" ]
}
