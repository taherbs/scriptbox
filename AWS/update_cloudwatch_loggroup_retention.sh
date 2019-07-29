#!/bin/bash

# By default CloudWatch Logs are kept indefinitely and never expire.
# This script should allow you to change retention period for multiple log groups at once.

# Set retention to 2years (731 days)
declare -r retention="731"

# Get all log groups with indefinit retention period
for L in $(aws logs describe-log-groups \
    --query 'logGroups[?!not_null(retentionInDays)] | [].logGroupName' \
    --output text)
do
   # Set new retention period
   aws logs  put-retention-policy --log-group-name ${L} \
   --retention-in-days ${retention}
done
