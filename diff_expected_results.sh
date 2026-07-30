#!/usr/bin/env bash

jq --help > /dev/null
if [ ${?} -ne 0 ]; then
    echo "install jq (Command-line JSON processor): https://jqlang.org/download/"
    exit 1
fi

echo "diff -- expected_results.json"
diff \
    <(wget -qO- https://raw.githubusercontent.com/nlsandler/writing-a-c-compiler-tests/refs/heads/main/expected_results.json | jq .) \
    <(git show HEAD:expected_results.json | jq .)
if [ ${?} -gt 1 ]; then exit 1; fi
exit 0
