#!/usr/bin/env bash

. ./unimelb-COMP90024-2022-grp-8-openrc.sh; ansible-playbook couchdb.yaml -i inventory/hosts.ini