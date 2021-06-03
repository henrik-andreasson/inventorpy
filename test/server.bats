
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "server" {
    cd ../utils/
    run ./rest-verify-server.sh ./test-server.csv
    debug
    [ "${lines[2]}" = "ok server server1.tld" ]
    [ "${lines[3]}" = "ok server server2.tld" ]
    [ "${lines[4]}" = "ok server server3.tld" ]
    [ "${lines[5]}" = "ok server server4.tld" ]
    [ "${lines[6]}" = "ok server server5.tld" ]
    [ "${lines[7]}" = "ok server server6.tld" ]
}
