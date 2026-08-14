<!-- markdownlint-disable -->

# Hardening Report: MeilCli--slack-upload-file/v5.0.4

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **MeilCli--slack-upload-file/v5.0.4** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Multiple `run:` blocks in `.github/workflows/debug.yml` directly interpolate GitHub Actions expressions inside shell command strings (sub-rule a). This allows an attacker to inject arbitrary shell commands via the `workflow_dispatch` `message` input or other context values.

Offending lines:
- Line 22: `run: 'echo ${{ github.event.inputs.message }} > test1.txt'`
- Line 23: `run: 'echo ${{ github.event.inputs.message }} > test2.txt'`
- Line 38: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test1.txt'`
- Line 39: `run: 'echo ${{ github.event.inputs.message }} > testsrc/main/test2.txt'`
- Line 52: `run: 'echo ${{ github.event.inputs.message }}${{ github.run_number }} > replacement_test.txt'`
- Line 59: `run: 'echo ${{ steps.slack_upload.outputs.uploaded_file_id }}'`

Fix: Move the values into `env:` variables and reference them as quoted shell variables, e.g.:
```yaml
env:
  MESSAGE: ${{ github.event.inputs.message }}
run: echo "$MESSAGE" > test1.txt
```

Locations:

- `.github/workflows/debug.yml:22`
- `.github/workflows/debug.yml:23`
- `.github/workflows/debug.yml:38`
- `.github/workflows/debug.yml:39`
- `.github/workflows/debug.yml:52`
- `.github/workflows/debug.yml:59`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed all 6 script injection findings in hardened/action/.github/workflows/debug.yml:
- Lines 22-23 (post1 job): Moved `github.event.inputs.message` into `env: MESSAGE:` and used `echo "$MESSAGE"` in each run step.
- Lines 38-39 (post2 job): Same fix for the two echo steps writing to testsrc/main/.
- Line 52 (post3 job): Moved both `github.event.inputs.message` and `github.run_number` into `env:` block as `MESSAGE` and `RUN_NUMBER`, then used `echo "${MESSAGE}${RUN_NUMBER}"` in the run step.
- Line 59 (post3 job): Moved `steps.slack_upload.outputs.uploaded_file_id` into `env: UPLOADED_FILE_ID:` and used `echo "$UPLOADED_FILE_ID"` in the run step.

