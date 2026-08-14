<!-- markdownlint-disable -->

# Hardening Report: MeilCli--slack-upload-file/v5.0.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **MeilCli--slack-upload-file/v5.0.0** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Multiple `run:` steps in debug.yml directly interpolate GitHub Actions expressions into shell commands (sub-rule a). The user-controlled `${{ github.event.inputs.message }}` is interpolated directly into `echo` commands, `${{ github.run_number }}` is concatenated into a shell string, and `${{ steps.slack_upload.outputs.uploaded_file_id }}` is echoed directly. An attacker can supply shell metacharacters via the `workflow_dispatch` `message` input to achieve command injection. All six affected steps must use an `env:` variable with double-quoted expansion instead of direct `${{ }}` interpolation in the shell string.

Affected lines:
- Line 22: `run: 'echo ${{ github.event.inputs.message }} > test1.txt'`
- Line 23: `run: 'echo ${{ github.event.inputs.message }} > test2.txt'`
- Line 36: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test1.txt'`
- Line 37: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test2.txt'`
- Line 50: `run: 'echo ${{ github.event.inputs.message }}${{ github.run_number }} > replacement_test.txt'`
- Line 56: `run: 'echo ${{ steps.slack_upload.outputs.uploaded_file_id }}'`

Locations:

- `.github/workflows/debug.yml:22`
- `.github/workflows/debug.yml:23`
- `.github/workflows/debug.yml:36`
- `.github/workflows/debug.yml:37`
- `.github/workflows/debug.yml:50`
- `.github/workflows/debug.yml:56`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed all 6 script injection instances in hardened/action/.github/workflows/debug.yml:
- Lines 22-23 (post1 job): Moved `github.event.inputs.message` into `env: MESSAGE:` and changed `echo ${{ ... }}` to `echo "$MESSAGE"` for both test1.txt and test2.txt steps.
- Lines 36-37 (post2 job): Same fix for the testsrc/main/test1.txt and test2.txt steps.
- Line 50 (post3 job): Moved both `github.event.inputs.message` and `github.run_number` into `env:` as `MESSAGE` and `RUN_NUMBER`, and changed the run command to `echo "${MESSAGE}${RUN_NUMBER}"`.
- Line 56 (post3 job): Moved `steps.slack_upload.outputs.uploaded_file_id` into `env: UPLOADED_FILE_ID:` and changed the echo to `echo "$UPLOADED_FILE_ID"`.

