
debug(){
  echo "# ${lines[0]}" >&3
  echo "# ${lines[1]}" >&3
  echo "# ${lines[2]}" >&3
  echo "# ${lines[3]}" >&3
  echo "# ${lines[4]}" >&3

}
@test "user" {
    cd ../utils/
    run ./rest-verify-users.sh ./test-users.csv
#    debug
    [ "${lines[2]}" = "ok username user1" ]
    [ "${lines[3]}" = "ok username user2" ]
    [ "${lines[4]}" = "ok username user3" ]

}
