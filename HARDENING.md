<!-- markdownlint-disable -->

# Hardening Report: MeilCli--slack-upload-file/v5.0.7

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **MeilCli--slack-upload-file/v5.0.7** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Six `run:` blocks in .github/workflows/debug.yml directly interpolate GitHub Actions expressions into shell commands (rule a — direct expression interpolation). The user-controlled `workflow_dispatch` input `github.event.inputs.message` is embedded verbatim into shell commands without quoting or env-var indirection, allowing an attacker to inject arbitrary shell metacharacters. Similarly, `github.run_number` and `steps.slack_upload.outputs.uploaded_file_id` are interpolated directly.

Offending lines:
- Line 22: `run: 'echo ${{ github.event.inputs.message }} > test1.txt'`
- Line 23: `run: 'echo ${{ github.event.inputs.message }} > test2.txt'`
- Line 37: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test1.txt'`
- Line 38: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test2.txt'`
- Line 50: `run: 'echo ${{ github.event.inputs.message }}${{ github.run_number }} > replacement_test.txt'`
- Line 57: `run: 'echo ${{ steps.slack_upload.outputs.uploaded_file_id }}'`

Fix: move the values into `env:` variables and reference them as quoted shell variables, e.g. `env: { MESSAGE: "${{ github.event.inputs.message }}" }` then `run: echo "$MESSAGE" > test1.txt`.

Locations:

- `.github/workflows/debug.yml:22`
- `.github/workflows/debug.yml:23`
- `.github/workflows/debug.yml:37`
- `.github/workflows/debug.yml:38`
- `.github/workflows/debug.yml:50`
- `.github/workflows/debug.yml:57`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed all six script-injection findings in hardened/action/.github/workflows/debug.yml:
- Lines 22-23 (post1 job): Moved `github.event.inputs.message` into `env: { MESSAGE: ... }` and changed `run:` to `echo "$MESSAGE" > test1.txt` / `echo "$MESSAGE" > test2.txt`.
- Lines 37-38 (post2 job): Same fix for the two echo steps writing to testsrc/main/.
- Line 50 (post3 job): Moved both `github.event.inputs.message` and `github.run_number` into `env: { MESSAGE: ..., RUN_NUMBER: ... }` and changed `run:` to `echo "${MESSAGE}${RUN_NUMBER}" > replacement_test.txt`.
- Line 57 (post3 job): Moved `steps.slack_upload.outputs.uploaded_file_id` into `env: { UPLOADED_FILE_ID: ... }` and changed `run:` to `echo "$UPLOADED_FILE_ID"`.
All expressions are now safely indirected through environment variables and properly double-quoted in the shell commands.

