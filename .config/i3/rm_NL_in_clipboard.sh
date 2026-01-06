#!/bin/bash

xclip -o -selection clipboard | awk '
{
    # Remove leading and trailing spaces from each line
    gsub(/^[ \t]+|[ \t]+$/, "", $0);
    if (NR == 1) {
        # Initialize result with the first line
        result = $0;
    } else {
        if (result ~ /[a-zA-Z]-$/ && $1 ~ /^[a-zA-Z]/) {
            # If the previous line ends with a hyphen and the current line starts with a letter
            result = substr(result, 1, length(result) - 1) $0;
        } else {
            # Otherwise, add a space and append the current line
            result = result " " $0;
        }
    }
}
END {
    # Print the final result
    print result;
}' | xclip -selection clipboard