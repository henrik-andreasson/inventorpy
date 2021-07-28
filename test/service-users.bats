
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "service users" {
    cd ../utils/
    run ./rest-verify-service-users.sh test-service-users.csv
    debug
    [ "${lines[2]}" = "ok service user service1/user1" ]
    [ "${lines[3]}" = "ok service user service2/user2" ]
    [ "${lines[4]}" = "ok service user service3/user1" ]
    [ "${lines[5]}" = "ok service user service4/user1" ]
    [ "${lines[6]}" = "ok service user service5/user1" ]
    [ "${lines[7]}" = "ok service user service6/user2" ]
    [ "${lines[8]}" = "ok service user service5/user2" ]
    [ "${lines[9]}" = "ok service user service6/user3" ]

}
