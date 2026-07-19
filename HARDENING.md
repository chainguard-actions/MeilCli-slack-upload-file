<!-- markdownlint-disable -->

# Hardening Report: MeilCli--slack-upload-file/v5.0.5

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **MeilCli--slack-upload-file/v5.0.5** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Multiple `run:` steps in debug.yml directly interpolate GitHub Actions expressions inside shell command strings (sub-rule a). The workflow_dispatch input `${{ github.event.inputs.message }}` is interpolated directly into shell `echo` commands in all three jobs (post1, post2, post3). Additionally, `${{ github.run_number }}` and `${{ steps.slack_upload.outputs.uploaded_file_id }}` are also interpolated directly. An attacker with workflow_dispatch access could supply a crafted `message` value containing shell metacharacters to achieve command injection. These values must be passed via `env:` variables and then referenced as quoted shell variables (e.g., `"$MESSAGE"`) instead of being interpolated directly.

Locations:

- `.github/workflows/debug.yml:22`
- `.github/workflows/debug.yml:23`
- `.github/workflows/debug.yml:37`
- `.github/workflows/debug.yml:38`
- `.github/workflows/debug.yml:52`
- `.github/workflows/debug.yml:62`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed all 6 script injection locations in .github/workflows/debug.yml by moving GitHub Actions expressions out of run: shell strings and into env: blocks:

1. post1 job, line 22: `echo ${{ github.event.inputs.message }} > test1.txt` → env: MESSAGE + `echo "$MESSAGE" > test1.txt`
2. post1 job, line 23: `echo ${{ github.event.inputs.message }} > test2.txt` → env: MESSAGE + `echo "$MESSAGE" > test2.txt`
3. post2 job, line 37: `echo ${{ github.event.inputs.message }} > testsrc/main/test1.txt` → env: MESSAGE + `echo "$MESSAGE" > testsrc/main/test1.txt`
4. post2 job, line 38: `echo ${{ github.event.inputs.message }} > testsrc/main/test2.txt` → env: MESSAGE + `echo "$MESSAGE" > testsrc/main/test2.txt`
5. post3 job, line 52: `echo ${{ github.event.inputs.message }}${{ github.run_number }} > replacement_test.txt` → env: MESSAGE + RUN_NUMBER + `echo "${MESSAGE}${RUN_NUMBER}" > replacement_test.txt`
6. post3 job, line 62: `echo ${{ steps.slack_upload.outputs.uploaded_file_id }}` → env: UPLOADED_FILE_ID + `echo "$UPLOADED_FILE_ID"`

All expressions are now safely passed through environment variables and referenced as double-quoted shell variables, preventing shell metacharacter injection.

