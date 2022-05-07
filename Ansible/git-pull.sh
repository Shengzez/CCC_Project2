#!/usr/bin/env bash

ansible-playbook -i inventory/hosts.ini -u ubuntu --key-file=/Users/gray/group-8.pem git-pull.yaml