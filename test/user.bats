
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "user" {
    cd ../utils/
    run ./rest-verify-users.sh ./test-users.csv
    debug
    [ "${lines[2]}" = "ok username user1" ]
    [ "${lines[3]}" = "ok username user2" ]
    [ "${lines[4]}" = "ok username user3" ]

}
