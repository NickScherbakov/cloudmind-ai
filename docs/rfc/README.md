# CloudMind AI RFCs

RFCs (Requests for Comments) are formal design proposals for significant changes:

## When to Write an RFC
Write an RFC when a change:
- Introduces a new subsystem or provider architecture
- Adds external integrations (Terraform, Kubernetes, Prometheus, etc.)
- Alters public APIs, CLI commands, or core data models
- Introduces ML/AI pipelines that affect optimization semantics
- Impacts security, compliance, or resource governance

## RFC Lifecycle
1. Draft — initial proposal (open PR with label `rfc`)
2. Review — collaborative feedback, revisions
3. Accepted — merged; implementation issues created
4. Rejected — closed with rationale
5. Superseded — replaced by a new RFC

## How to Submit
1. Copy `RFC_TEMPLATE.md` to `RFC-<number>-<slug>.md` (e.g., `RFC-001-provider-factory.md`)
2. Fill in sections; keep concise but clear
3. Open PR with title: `RFC: <short description>`
4. Link related issues / prior discussions

## Numbering
Use the next incremental number. If unsure, open a placeholder PR and request number assignment.

## Review Guidelines
Reviewers assess:
- Clarity of problem & motivation
- Architectural soundness & cohesion
- Operational & security considerations
- Backward compatibility plan
- Observability & test strategy

## Post-Acceptance
Create implementation issues referencing the RFC number. Track progress in a milestone if scope is broad.

## Index
(Add links to accepted RFCs here)

None yet — be the first!
