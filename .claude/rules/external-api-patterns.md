# External API Interaction Patterns

> Generic rules for agents interacting with external APIs and services.

## Pacing

- **Minimum interval**: 3 seconds between same-type API calls (e.g., consecutive comments,
  follows, or votes). Bursts trigger spam detection and waste rate limits.
- **Batch awareness**: If performing N similar actions, space them out. Never fire-and-forget
  a loop of API calls without per-call delay and response validation.

## Response Validation

- **Validate before logging**: Do not log `success: true` based solely on HTTP 2xx.
  Check that the response body contains expected fields (e.g., a valid resource ID).
- **Detect soft failures**: Empty IDs (`""`), placeholder IDs (`"1"`), or missing expected
  fields indicate the operation was silently rejected. Log these as failures.
- **Read-back verification**: After write operations (create post, update profile), perform
  a read-back (GET) to confirm the resource exists and matches expectations.

## Effectiveness

- **Track metrics delta**: Before starting an interaction campaign, snapshot relevant metrics
  (karma, followers, posts_count, etc.). After completion, compare. If action count
  greatly exceeds metric delta, investigate which actions had no effect.
- **Abort on pattern failure**: If 3+ consecutive same-type actions produce no metric change
  or return empty IDs, stop and diagnose before continuing.
