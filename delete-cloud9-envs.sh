#!/bin/bash -
#===============================================================================
#
#          FILE: delete-cloud9-envs.sh
#
#         USAGE: ./delete-cloud9-envs.sh
#
#   DESCRIPTION: Bulk delete Cloud9 environments
#
#        AUTHOR: Enri Peters (EP), epeters@schubergphilis.com
#  ORGANIZATION: Schuberg Philis
#       CREATED: 16/09/2022 14:33:09
#      REVISION: 1.0
#===============================================================================

set -o nounset                              # Treat unset variables as an error


for CLOUD9ENV in $(aws cloud9 list-environments | jq -r '.environmentIds[]')
do
    aws cloud9 delete-environment --environment-id ${CLOUD9ENV}
done
