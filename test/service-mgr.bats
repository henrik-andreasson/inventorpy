
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "service mgr" {
    cd ../utils/
    run ./rest-verify-service-mgr.sh test-service-mgr.csv

    debug

    [ "${lines[2]}" = "ok service mgr service1/user1" ]
    [ "${lines[3]}" = "ok service mgr service2/user1" ]
    [ "${lines[4]}" = "ok service mgr service3/user1" ]
    [ "${lines[5]}" = "ok service mgr service4/user1" ]
    [ "${lines[6]}" = "ok service mgr service5/user1" ]
    [ "${lines[7]}" = "ok service mgr service6/user2" ]

}
