#!/usr/bin/env bash

####################################################################################################################################################
#  This script replaces all instances of <replace:VARIABLE> with the value stored in the environment variable $VARIABLE (as specified in the tag)  #
#  Please ensure that any variables stored are unique to that file or set of files if they're allowed to share a value                              #
####################################################################################################################################################

folder=${1:-../}

# Find files with the expected replacement flag, e.g.: <replace:VARIABLE>
files_with_secrets=$(grep -Prl "<replace:.+?>" ${folder} | grep -v $0)
if [ -z "${files_with_secrets}" ]; then
    echo "No replacements to be made"
    exit 0
fi

# Set Internal Field Separator so for loop doesn't split on spaces
IFS=$'\n'
for file in ${files_with_secrets}; do
    for replacement in $(grep -P "<replace:.+?>" ${file}); do
        # Extract $VARIABLE from <replace:$VARIABLE> so we can ask gitlab to read it in for us later
        secret=$(echo ${replacement} | grep -Po "(?<=\<replace:)\w+(?=\>)")

        # Prepare command as $secret will become a reference to yet another variable
        cmd="\"s/<replace:${secret}>/\$${secret}/\""

        # Use awk to paste everything neatly together, since sed doesn't like reading commands from elsewhere
        awk -v cmd=$cmd -v file=$file 'BEGIN {print "sed --in-place", cmd, file}' | bash
        retVal=$?
        if [ $retVal -eq 0 ]; then
            echo "Replaced ${secret} in file ${file}"
        else
            >&2 echo "Error replacing ${secret} in file ${file} -- Exit code: ${retVal}"
            exit $retVal
        fi
    done
done

# Reset IFS
unset IFS
