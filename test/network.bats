
debug(){
  echo "# ${lines[0]}" >&3
  echo "# ${lines[1]}" >&3
  echo "# ${lines[2]}" >&3
  echo "# ${lines[3]}" >&3
  echo "# ${lines[4]}" >&3

}
@test "network" {
    cd ../utils/
    run ./rest-verify-network.sh ./test-networks.csv
#    debug
    [ "${lines[2]}" = "ok network NETWORK1" ]
    [ "${lines[3]}" = "ok network NETWORK2" ]
    [ "${lines[4]}" = "ok network NETWORK3" ]
    [ "${lines[5]}" = "ok network NETWORK4" ]
    [ "${lines[6]}" = "ok network NETWORK5" ]
    [ "${lines[7]}" = "ok network NETWORK6" ]
}
