<!-- markdownlint-disable -->

# Hardening Report: MeilCli--slack-upload-file/v5.0.8

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **MeilCli--slack-upload-file/v5.0.8** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Multiple `run:` blocks in debug.yml directly interpolate GitHub Actions expressions into shell commands (sub-rule a). This allows an attacker-controlled `workflow_dispatch` input to inject arbitrary shell commands. Offending lines:
- Line 21: `run: 'echo ${{ github.event.inputs.message }} > test1.txt'`
- Line 22: `run: 'echo ${{ github.event.inputs.message }} > test2.txt'`
- Line 36: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test1.txt'`
- Line 37: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test2.txt'`
- Line 48: `run: 'echo ${{ github.event.inputs.message }}${{ github.run_number }} > replacement_test.txt'`
- Line 56: `run: 'echo ${{ steps.slack_upload.outputs.uploaded_file_id }}'`

All of these embed `${{ ... }}` expressions directly inside shell `run:` strings. The values should be passed via `env:` variables and then referenced as quoted shell variables (e.g., `"$MESSAGE"`) instead.

Locations:

- `.github/workflows/debug.yml:21`
- `.github/workflows/debug.yml:22`
- `.github/workflows/debug.yml:36`
- `.github/workflows/debug.yml:37`
- `.github/workflows/debug.yml:48`
- `.github/workflows/debug.yml:56`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed all 6 script injection instances in hardened/action/.github/workflows/debug.yml:
- Lines 21-22 (post1 job): Moved `github.event.inputs.message` into `env: MESSAGE:` blocks; shell now uses `echo "$MESSAGE" > test1.txt` and `echo "$MESSAGE" > test2.txt`.
- Lines 36-37 (post2 job): Same fix for the testsrc/main/ variants.
- Line 48 (post3 job): Moved both `github.event.inputs.message` and `github.run_number` into `env:` as `MESSAGE` and `RUN_NUMBER`; shell uses `echo "${MESSAGE}${RUN_NUMBER}" > replacement_test.txt`.
- Line 56 (post3 job): Moved `steps.slack_upload.outputs.uploaded_file_id` into `env: UPLOADED_FILE_ID:`; shell uses `echo "$UPLOADED_FILE_ID"`.
All `${{ }}` expressions are now passed through environment variables and referenced as quoted shell variables, preventing shell command injection.

