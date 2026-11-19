## ADDED Requirements

### Requirement: Draft-preserving fetch (F7)

When the offer stream has `has_draft`, the system SHALL merge Keitaro stream data instead of replacing local offer rows: service streams may refresh; local unpushed adds remain; offers that were active in the published snapshot but are missing from Keitaro become **removed**.

#### Scenario: Drift marks removed

- **WHEN** the user runs Fetch with a draft and Keitaro no longer lists an offer that was active in the published snapshot
- **THEN** that local row becomes removed and active weights are recalculated

#### Scenario: Local add survives fetch

- **WHEN** the user added an offer only locally (not in the published snapshot) and runs Fetch
- **THEN** that row stays active even if Keitaro does not list it yet

#### Scenario: No draft replaces

- **WHEN** `has_draft` is false
- **THEN** Fetch replaces local streams from Keitaro and updates the published snapshot