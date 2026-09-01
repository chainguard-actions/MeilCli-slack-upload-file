<!-- markdownlint-disable -->

# Hardening Report: MeilCli--slack-upload-file/v5.0.9

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **MeilCli--slack-upload-file/v5.0.9** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Multiple `run:` blocks in debug.yml directly interpolate GitHub Actions expressions inside shell commands, violating sub-rule (a). Specifically:
- Line 22: `run: 'echo ${{ github.event.inputs.message }} > test1.txt'` — attacker-controlled workflow_dispatch input interpolated directly into shell.
- Line 23: `run: 'echo ${{ github.event.inputs.message }} > test2.txt'` — same issue.
- Line 37: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test1.txt'` — same issue.
- Line 38: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test2.txt'` — same issue.
- Line 51: `run: 'echo ${{ github.event.inputs.message }}${{ github.run_number }} > replacement_test.txt'` — two expressions interpolated directly.
- Line 57: `run: 'echo ${{ steps.slack_upload.outputs.uploaded_file_id }}'` — step output interpolated directly into shell.
An attacker who can control the `message` workflow_dispatch input (or a compromised step output) could inject arbitrary shell commands. These values must be passed via `env:` variables and then referenced as quoted `"$VAR"` shell variables.

Locations:

- `.github/workflows/debug.yml:22`
- `.github/workflows/debug.yml:23`
- `.github/workflows/debug.yml:37`
- `.github/workflows/debug.yml:38`
- `.github/workflows/debug.yml:51`
- `.github/workflows/debug.yml:57`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed all 6 script injection findings in hardened/action/.github/workflows/debug.yml:
- Lines 22-23 (post1 job): Moved `github.event.inputs.message` into `env: MESSAGE:` blocks; changed `echo ${{ ... }} > test1.txt` and `test2.txt` to `echo "$MESSAGE" > test1.txt` / `test2.txt`.
- Lines 37-38 (post2 job): Same fix for `testsrc/main/test1.txt` and `testsrc/main/test2.txt`.
- Line 51 (post3 job): Moved both `github.event.inputs.message` and `github.run_number` into `env:` block as `MESSAGE` and `RUN_NUMBER`; changed shell command to `echo "${MESSAGE}${RUN_NUMBER}" > replacement_test.txt`.
- Line 57 (post3 job): Moved `steps.slack_upload.outputs.uploaded_file_id` into `env: UPLOADED_FILE_ID:` block; changed shell command to `echo "$UPLOADED_FILE_ID"`.
All GitHub Actions expressions are now passed through environment variables and referenced as quoted shell variables, preventing shell injection attacks.

