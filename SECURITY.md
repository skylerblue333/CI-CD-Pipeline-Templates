# Security Policy

This repository contains CI examples, not centrally enforced policy or a hosted deployment system.

Report template defects that could grant unnecessary GitHub token permissions, expose secrets, publish artifacts unexpectedly, weaken dependency/security gates, or create unsafe default runner behavior.

Consumers must independently review action pinning, fork-pull-request behavior, runner trust, environment protections, deployment credentials, artifact signing, branch protection, and repository-specific threat models before adopting a template.

The templates intentionally use read-only repository permissions and do not deploy or publish by default.
