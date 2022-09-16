#!/bin/bash -
#===============================================================================
#
#          FILE: create-users.sh
#
#         USAGE: ./create-users.sh [username] [account_id] [account_alias]
#    LOOP USAGE: for int in $(seq 5); \
#                  do ./create-users.sh cdk201-user${int} 803120882800 obsessedbyaws; \
#                done
#
#   DESCRIPTION: Bulk create workshop users
#
#        AUTHOR: Enri Peters (EP), epeters@schubergphilis.com
#  ORGANIZATION: Schuberg Philis
#       CREATED: 16/09/2022 13:07:30
#      REVISION: 1.0
#===============================================================================

set -o nounset                              # Treat unset variables as an error


WORKSHOP_USER=$1
ACCOUNT_ID=$2
ACCOUNT_ALIAS=$3
PASSWORD=$(pwgen -c -n -s -B -1 12)
GROUP="cdk201-group"
URL="https://${ACCOUNT_ALIAS}.signin.aws.amazon.com/console"

export AWS_PAGER=""

aws iam create-user --user-name ${WORKSHOP_USER}

aws iam create-login-profile \
  --user-name ${WORKSHOP_USER} \
  --password $PASSWORD

aws iam add-user-to-group \
  --group-name $GROUP \
  --user-name ${WORKSHOP_USER}

# It takes a few seconds before Cloud9 can see the user
sleep 15

aws cloud9 create-environment-ec2 \
  --name ${WORKSHOP_USER} \
  --instance-type t3.small \
  --image-id amazonlinux-2-x86_64 \
  --subnet-id subnet-032aa0ff01791bb25 \
  --automatic-stop-time-minutes 60 \
  --owner-arn arn:aws:iam::${ACCOUNT_ID}:user/${WORKSHOP_USER}

echo "Login URL: ${URL}" >> cdk-workshop-users.txt
echo "Username: ${WORKSHOP_USER}" >> cdk-workshop-users.txt
echo "Password: ${PASSWORD}" >> cdk-workshop-users.txt
echo "-----------------------" >> cdk-workshop-users.txt
