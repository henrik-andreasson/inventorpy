
debug(){
  for lno in "${lines[@]}" ; do
    echo "# $lno" >&3
  done

}
@test "service" {
    cd ../utils/
    run ./rest-verify-hsm-pcicard.sh test-hsm-pcicard.csv

    debug
    # URL: http://localhost:5000/api
    # User: admin
    [ "${lines[2]}" = "ok hsm-pci-card name HSM-SRV1-CA1" ]
    [ "${lines[3]}" = "ok hsm-pci-card serial 000001" ]
    [ "${lines[4]}" = "ok hsm-pci-card fbno FB000001" ]
    [ "${lines[5]}" = "ok hsm-pci-card name HSM-SRV1-CA2" ]
    [ "${lines[6]}" = "ok hsm-pci-card serial 000002" ]
    [ "${lines[7]}" = "ok hsm-pci-card fbno FB000002" ]
    [ "${lines[8]}" = "ok hsm-pci-card name HSM-SRV1-CA3" ]
    [ "${lines[9]}" = "ok hsm-pci-card serial 000003" ]
    [ "${lines[10]}" = "ok hsm-pci-card fbno FB000003" ]
    [ "${lines[11]}" = "ok hsm-pci-card name HSM-SRV1-FE1" ]
    [ "${lines[12]}" = "ok hsm-pci-card serial 000004" ]
    [ "${lines[13]}" = "ok hsm-pci-card fbno FB000004" ]
    [ "${lines[14]}" = "ok hsm-pci-card name HSM-SRV1-FE2" ]
    [ "${lines[15]}" = "ok hsm-pci-card serial 000005" ]
    [ "${lines[16]}" = "ok hsm-pci-card fbno FB000005" ]
    [ "${lines[17]}" = "ok hsm-pci-card name HSM-SRV1-FE3" ]
    [ "${lines[18]}" = "ok hsm-pci-card serial 000006" ]
    [ "${lines[19]}" = "ok hsm-pci-card fbno FB000006" ]
    [ "${lines[20]}" = "ok hsm-pci-card name HSM-SRV2-CA1" ]
    [ "${lines[21]}" = "ok hsm-pci-card serial 000007" ]
    [ "${lines[22]}" = "ok hsm-pci-card fbno FB000007" ]
    [ "${lines[23]}" = "ok hsm-pci-card name HSM-SRV2-CA2" ]
    [ "${lines[24]}" = "ok hsm-pci-card serial 000008" ]
    [ "${lines[25]}" = "ok hsm-pci-card fbno FB000008" ]
    [ "${lines[26]}" = "ok hsm-pci-card name HSM-SRV2-CA3" ]
    [ "${lines[27]}" = "ok hsm-pci-card serial 000009" ]
    [ "${lines[28]}" = "ok hsm-pci-card fbno FB000009" ]
    [ "${lines[29]}" = "ok hsm-pci-card name HSM-SRV2-FE1" ]
    [ "${lines[30]}" = "ok hsm-pci-card serial 000010" ]
    [ "${lines[31]}" = "ok hsm-pci-card fbno FB000010" ]
    [ "${lines[32]}" = "ok hsm-pci-card name HSM-SRV2-FE2" ]
    [ "${lines[33]}" = "ok hsm-pci-card serial 000011" ]
    [ "${lines[34]}" = "ok hsm-pci-card fbno FB000011" ]
    [ "${lines[35]}" = "ok hsm-pci-card name HSM-SRV2-FE3" ]
    [ "${lines[36]}" = "ok hsm-pci-card serial 000012" ]
    [ "${lines[37]}" = "ok hsm-pci-card fbno FB000012" ]

}
