#!/bin/bash

./rest-create-services.sh test-services.csv
./rest-create-users.sh test-users.csv
./rest-create-location.sh test-location.csv
./rest-create-networks.sh test-networks.csv
./rest-create-rack.sh test-rack.csv
./rest-create-servers.sh test-server.csv
./rest-create-firewall.sh test-firewall.csv
./rest-create-safe.sh test-safe.csv
./rest-create-compartment.sh test-compartment.csv
./rest-create-switchs.sh test-switch.csv
./rest-create-switch-ports.sh test-switch-ports.csv
./rest-create-hsm-domain.sh test-hsm-domain.csv
./rest-create-hsm-pcicard.sh test-hsm-pcicard.csv
./rest-create-hsm-ped.sh test-hsm-ped.csv
./rest-create-hsm-pin.sh test-hsm-pin.csv
