#!/bin/bash

./rest-create-users.sh import-users-cs.csv
./rest-create-services.sh import-services-cs.csv
./rest-create-location.sh import-location-cs.csv
./rest-create-networks.sh import-networks.csv
./rest-create-rack.sh import-rack-cs.csv
./rest-create-compartment.sh import-compartment-cs.csv
./rest-create-safe.sh import-safe-cs.csv
./rest-create-servers.sh import-server-cs.csv
./rest-create-hsm-domain.sh import-hsm-domain-cs.csv
./rest-create-hsm-pcicard.sh import-hsm-pcicard-cs.csv
./rest-create-hsm-ped.sh import-hsm-ped-cs.csv
./rest-create-hsm-pin.sh import-hsm-pin-cs.csv
