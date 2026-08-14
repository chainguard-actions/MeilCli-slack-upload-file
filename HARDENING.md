<!-- markdownlint-disable -->

# Hardening Report: MeilCli--slack-upload-file/v4.0.52

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **MeilCli--slack-upload-file/v4.0.52** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation: GitHub Actions expressions are directly interpolated inside run: shell commands in debug.yml. The values `${{ github.event.inputs.message }}` and `${{ github.event.inputs.delete_file_ids_before_upload }}` are attacker-controlled workflow_dispatch inputs that flow through YAML template substitution before the shell sees them, enabling command injection. Offending lines include: `run: 'echo ${{ github.event.inputs.message }} > test1.txt'`, `run: 'echo ${{ github.event.inputs.message }} > test2.txt'`, `run: 'echo ${{ github.event.inputs.message }}${{ github.run_number }} > replacement_test.txt'`, and `run: 'echo ${{ steps.slack_upload.outputs.uploaded_file_id }}'`. These must be moved to env: vars and the shell expansions double-quoted.

Locations:

- `.github/workflows/debug.yml:19`
- `.github/workflows/debug.yml:20`
- `.github/workflows/debug.yml:33`
- `.github/workflows/debug.yml:44`
- `.github/workflows/debug.yml:54`

### unpinned-uses (severity: high)

Multiple workflow files reference actions using mutable tags or branch names instead of immutable 40-character commit SHAs, making them vulnerable to supply-chain attacks if the referenced tag or branch is moved. Failing references: ci-base-approve.yml — `dependabot/fetch-metadata@v1`, `actions/github-script@v7`; ci-base-build.yml — `actions/checkout@v4`, `actions/setup-node@v4`, `actions/cache@v4`, `actions/upload-artifact@v4`, `peter-evans/create-pull-request@v6`; ci-base-merge.yml — `actions/github-script@v7`; debug.yml — `actions/checkout@v4` (×3); metrics.yml — `lowlighter/metrics@latest` (×2, especially dangerous as @latest always tracks HEAD); release.yml — `actions/checkout@v4`, `actions/setup-node@v4`, `MeilCli/bump-release-action@master` (branch ref); report.yml — `dawidd6/action-download-artifact@v6`, `MeilCli/common-lint-reporter/transformer/eslint@v1`, `MeilCli/common-lint-reporter@v1`.

Locations:

- `.github/workflows/ci-base-approve.yml:8`
- `.github/workflows/ci-base-approve.yml:10`
- `.github/workflows/ci-base-build.yml:7`
- `.github/workflows/ci-base-build.yml:8`
- `.github/workflows/ci-base-build.yml:9`
- `.github/workflows/ci-base-build.yml:18`
- `.github/workflows/ci-base-build.yml:25`
- `.github/workflows/ci-base-merge.yml:8`
- `.github/workflows/debug.yml:18`
- `.github/workflows/debug.yml:30`
- `.github/workflows/debug.yml:42`
- `.github/workflows/metrics.yml:6`
- `.github/workflows/metrics.yml:22`
- `.github/workflows/release.yml:25`
- `.github/workflows/release.yml:26`
- `.github/workflows/release.yml:29`
- `.github/workflows/report.yml:12`
- `.github/workflows/report.yml:16`
- `.github/workflows/report.yml:20`

### missing-permissions (severity: medium)

None of the 10 workflow files under .github/workflows/ declare a top-level `permissions:` block, and no individual job within any of these files declares job-level `permissions:` either. Without explicit permissions, workflows run with the repository's default token permissions (often write-all for private repos or read-all for public repos), violating the principle of least privilege. Affected files: ci-base-approve.yml, ci-base-build.yml, ci-base-merge.yml, ci-master.yml, ci-pr.yml, debug.yml, merge.yml, metrics.yml, release.yml, report.yml.

Locations:

- `.github/workflows/ci-base-approve.yml:1`
- `.github/workflows/ci-base-build.yml:1`
- `.github/workflows/ci-base-merge.yml:1`
- `.github/workflows/ci-master.yml:1`
- `.github/workflows/ci-pr.yml:1`
- `.github/workflows/debug.yml:1`
- `.github/workflows/merge.yml:1`
- `.github/workflows/metrics.yml:1`
- `.github/workflows/release.yml:1`
- `.github/workflows/report.yml:1`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions

**Notes:**

Fixed all three findings across 10 workflow files:

1. script-injection (debug.yml): Moved all ${{ github.event.inputs.message }}, ${{ github.run_number }}, and ${{ steps.slack_upload.outputs.uploaded_file_id }} expressions from run: shell commands into step-level env: blocks. Shell variables are now double-quoted in the run: commands.

2. unpinned-uses: Pinned all 11 unique action references to full 40-char commit SHAs across ci-base-approve.yml, ci-base-build.yml, ci-base-merge.yml, debug.yml, metrics.yml, release.yml, and report.yml. Original tags preserved as comments.

3. missing-permissions: Added top-level `permissions: {}` to all 10 workflow files (ci-base-approve.yml, ci-base-build.yml, ci-base-merge.yml, ci-master.yml, ci-pr.yml, debug.yml, merge.yml, metrics.yml, release.yml, report.yml). Jobs that require specific permissions (approve, build, merge, automerge, github-metrics, release, lint) have job-level permissions blocks with minimum required access.

