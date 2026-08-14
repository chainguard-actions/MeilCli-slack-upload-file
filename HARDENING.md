<!-- markdownlint-disable -->

# Hardening Report: MeilCli--slack-upload-file/v5.0.1

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **MeilCli--slack-upload-file/v5.0.1** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Multiple `run:` steps in debug.yml directly interpolate GitHub Actions expressions inside shell command strings (rule a), enabling script injection. An attacker-controlled `workflow_dispatch` input value is embedded verbatim into the shell before quoting occurs.

Offending lines:
- Line 22: `run: 'echo ${{ github.event.inputs.message }} > test1.txt'`
- Line 23: `run: 'echo ${{ github.event.inputs.message }} > test2.txt'`
- Line 37: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test1.txt'`
- Line 38: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test2.txt'`
- Line 51: `run: 'echo ${{ github.event.inputs.message }}${{ github.run_number }} > replacement_test.txt'`
- Line 60: `run: 'echo ${{ steps.slack_upload.outputs.uploaded_file_id }}'`

Fix: move each expression into an `env:` variable and reference it as a double-quoted shell variable, e.g. `echo "$MESSAGE" > test1.txt`.

Locations:

- `.github/workflows/debug.yml:22`
- `.github/workflows/debug.yml:23`
- `.github/workflows/debug.yml:37`
- `.github/workflows/debug.yml:38`
- `.github/workflows/debug.yml:51`
- `.github/workflows/debug.yml:60`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed all 6 script injection findings in hardened/action/.github/workflows/debug.yml:

1. Lines 22-23 (post1 job): Moved `${{ github.event.inputs.message }}` into `env: MESSAGE:` and changed `echo ${{ ... }} > test1.txt` / `test2.txt` to `echo "$MESSAGE" > test1.txt` / `test2.txt`.

2. Lines 37-38 (post2 job): Same fix for the testsrc/main/test1.txt and test2.txt steps.

3. Line 51 (post3 job): Moved both `${{ github.event.inputs.message }}` and `${{ github.run_number }}` into `env: MESSAGE:` and `env: RUN_NUMBER:`, then used `echo "${MESSAGE}${RUN_NUMBER}" > replacement_test.txt`.

4. Line 60 (post3 job): Moved `${{ steps.slack_upload.outputs.uploaded_file_id }}` into `env: UPLOADED_FILE_ID:` and changed `echo ${{ ... }}` to `echo "$UPLOADED_FILE_ID"`.

All expressions are now safely passed through environment variables and referenced as double-quoted shell variables, preventing script injection attacks.

