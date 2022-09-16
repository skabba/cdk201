#!/bin/bash -
#===============================================================================
#
#          FILE: delete-user.sh
#
#         USAGE: ./delete-users.sh [username]
#    LOOP USAGE: for int in $(seq 5); \
#                  do ./delete-users.sh cdk201-user${int}; \
#                done
#
#   DESCRIPTION: Bulk delete workshop users
#
#        AUTHOR: Enri Peters (EP), epeters@schubergphilis.com
#  ORGANIZATION: Schuberg Philis
#       CREATED: 16/09/2022 13:08:04
#      REVISION: 1.0
#===============================================================================

set -o nounset                              # Treat unset variables as an error

WORKSHOP_USER=$1
GROUP="cdk201-group"

aws iam remove-user-from-group --group-name $GROUP --user-name ${WORKSHOP_USER}
aws iam delete-login-profile --user-name ${WORKSHOP_USER}
aws iam delete-user --user-name ${WORKSHOP_USER}