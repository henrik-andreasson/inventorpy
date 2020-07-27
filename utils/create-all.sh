#!/bin/bash

./rest-create-services.sh test-services.csv
./rest-create-users.sh test-users.csv
./rest-create-location.sh test-location.csv
./rest-create-networks.sh test-networks.csv
./rest-create-rack.sh test-rack.csv
./rest-create-servers.sh test-server.csv
./rest-create-firewall.sh test-firewall.csv
#./rest-create-compartment.sh import-compartment.csv
#./rest-create-safe.sh import-safe.csv
#./rest-create-hsm-domain.sh import-hsm-domain.csv
#./rest-create-hsm-pcicard.sh import-hsm-pcicard.csv
#./rest-create-hsm-ped.sh import-hsm-ped.csv
#./rest-create-hsm-pin.sh import-hsm-pin.csv
