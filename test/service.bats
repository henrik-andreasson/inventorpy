
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "service" {
    cd ../utils/
    run ./rest-verify-services.sh ./test-services.csv
    debug
    [ "${lines[2]}" = "ok service service1" ]
    [ "${lines[3]}" = "ok service service2" ]
    [ "${lines[4]}" = "ok service service3" ]
    [ "${lines[5]}" = "ok service service4" ]
    [ "${lines[6]}" = "ok service service5" ]
    [ "${lines[7]}" = "ok service service6" ]

}
