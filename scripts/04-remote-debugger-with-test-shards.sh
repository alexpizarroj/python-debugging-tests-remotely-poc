#!/usr/bin/env bash
set -e -o pipefail

run_test_shard() {
    remote_debugger_port="$1"
    docker run \
        --rm \
        --mount type=bind,source="$(pwd)",target=/app \
        --mount type=bind,source="$(pwd)"/remote-debugger-events.log,target=/tmp/remote-debugger-events.log \
        --mount type=bind,source="$(pwd)"/remote-debugger-events.log.lockfile,target=/tmp/remote-debugger-events.log.lockfile \
        --env PYTHON_REMOTE_DBG_PORT="$remote_debugger_port" \
        --publish "$remote_debugger_port":"$remote_debugger_port" \
        python-remote-debugging-poc \
        pytest --pdb --pdbcls=remote_dbg:RemotePdb tests/
}

: >./remote-debugger-events.log          # empty file
: >./remote-debugger-events.log.lockfile # empty file

declare -A shard_pids_by_shard_id
for ((shard_id = 1; shard_id <= 3; shard_id++)); do
    ((remote_debugger_port = 7200 + $shard_id - 1))

    echo "Starting test shard #${shard_id}"
    run_test_shard "$remote_debugger_port" &>"./test-shard-${shard_id}.log" &

    shard_pids_by_shard_id["$shard_id"]=$!
done

docker run \
    --rm \
    --mount type=bind,source="$(pwd)",target=/app \
    --mount type=bind,source="$(pwd)"/remote-debugger-events.log,target=/tmp/remote-debugger-events.log \
    --mount type=bind,source="$(pwd)"/remote-debugger-events.log.lockfile,target=/tmp/remote-debugger-events.log.lockfile \
    python-remote-debugging-poc \
    python -u -m remote_dbg.commands.monitor_debug_events &
monitor_debug_events_pid=$!

for shard_id in "${!shard_pids_by_shard_id[@]}"; do
    pid=${shard_pids_by_shard_id[$shard_id]}
    echo "Waiting for test shard #${shard_id} to finish..."

    wait $pid || true

    echo "Done."
done

kill "${monitor_debug_events_pid}"
wait "${monitor_debug_events_pid}"

rm -f ./remote-debugger-events.log
rm -f ./remote-debugger-events.log.lockfile
