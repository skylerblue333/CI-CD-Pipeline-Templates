# Sky CI Template Catalog

**Status: engineering beta / reusable examples.**

This repository contains versionable GitHub Actions workflow templates for common SKYCOIN4444 engineering-lab stacks. The templates are intended to be copied and adapted into consuming repositories; they are not a hosted CI platform or a deployment service.

## Included templates

- `templates/github-actions/node-ci.yml` — install, optional lint/typecheck/test/build, production dependency audit
- `templates/github-actions/python-ci.yml` — compile, Ruff, pytest, pip-audit
- `templates/github-actions/go-ci.yml` — gofmt, vet, race tests, build, govulncheck
- `templates/github-actions/docker-ci.yml` — local image build plus non-root runtime-user check; never publishes

All shipped templates default to `permissions: contents: read`, use explicit job timeouts, and avoid deployment credentials or publishing behavior.

## Validate this catalog

```bash
python scripts/validate_templates.py
```

The repository CI runs the same structural policy check and rejects obvious private-key/AWS-access-key material in the template directory.

## Usage

Copy a template into the consuming repository's `.github/workflows/` directory and review every command for that repository's package manager, test layout, runtime version, and threat model. Do not assume a template proves production readiness.

Example:

```bash
mkdir -p .github/workflows
cp templates/github-actions/go-ci.yml .github/workflows/ci.yml
```

## Security boundary

These are examples, not centrally enforced organization policy. Consumers remain responsible for action pinning strategy, dependency provenance, secret access, environment approvals, branch protection, deployment authorization, runner trust, artifact signing, and repository-specific security gates.

No template in this repository deploys infrastructure or publishes an image by default.
