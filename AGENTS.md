# PA Research agent workflow

This repository researches price action through AI chart reading. It does not authorize trades or connect to execution systems.

## Repository ownership and pull request approval

- The canonical repository is https://github.com/justin371/pa_research. Its code owner is Lijie_Wang (`@justin371`), as defined in [.github/CODEOWNERS](.github/CODEOWNERS).
- Determine ownership from the pull request's GitHub author login, not commit metadata, branch names, or assignees. A pull request authored by `@justin371` is approved by default under the owner's standing policy; no separate approving review is required. This approval exception does not waive required checks, conflict resolution, or the scope of the requested merge.
- Every pull request authored by anyone else must have a current, non-stale GitHub APPROVED review from `@justin371` before merging or enabling auto-merge. Verify approval against the current PR head and any outstanding change requests; passing checks, another reviewer's approval, or approval of another PR is insufficient.
- Never submit a review or approval comment on the owner's behalf or impersonate another author or reviewer. Leave another author's unapproved pull request open for the owner to review.
- Keep `main` protected with required code-owner review, stale-approval dismissal, and administrator enforcement. GitHub prohibits self-approval and its native protection does not provide an author-only exception. For an owner-authored PR only, after verifying author, exact head, target, reviews and required checks, temporarily disable administrator enforcement to perform the authorized merge as the owner; restore it immediately in a finally block even if merging fails. Preserve all other protection settings, verify restoration, and report a restoration failure immediately. Never use this exception for another author's PR. See [GitHub's approval restrictions](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews).

## Research workflow

Start with [the AI visual research workflow](docs/ai_visual_research_CN.md). Use the model selected for the current task; preserve explicit configuration. Inspect actual chart images with the available image-viewing tool before making visual claims. Text summaries alone are not chart inspection.

Let AI interpret context, pressure, legs, location, competing hypotheses and useful Brooks examples. Choose timeframes and zoom from the question and evidence. Do not turn legacy pattern enums, EMA slopes, a fixed two-year window or a fixed candidate quota into discovery gates. Ask for missing evidence only when it changes the conclusion; incomplete views can still support explicitly limited hypotheses.

Read pattern notes and reference examples on demand. Use [the example registry](knowledge/brooks_visual_examples.json) to find teaching references; open the actual page/image before claiming a visual comparison. Teaching examples contain outcomes and are not holdout tests.

After reading professional books, papers, course materials or technical documents for this project, save reusable findings in the repository before completing the task. Record the source, page or section references, actual reading coverage, useful interpretations and limitations in a research memo, and link it from the relevant index so later analyses can find it. Extend an existing memo when appropriate; keep source observations separate from new hypotheses. Preserve access and copyright limits, and do not promote teaching claims into validated results or production rules. Consult these notes on demand and reopen the original evidence when a new comparison depends on visual detail.

Keep observations distinct from interpretation. Record chart sources, visible cutoff and uncertainty. Do not infer exact prices from ambiguous pixels, fabricate current data, use future bars to select a historical entry, or call subjective confidence a validated win rate.

The old daily selection rules, visual cards and output schema apply only when reproducing their named legacy experiment or exporting a compatible frozen contract. They do not govern ordinary AI discovery. Existing replay tooling requires its exact schema and honest reviewer provenance; never label an AI review as human_chart_review. Unsupported hypotheses remain research memos until a suitable replay adapter is implemented and tested.

For code changes, run relevant unit tests; run the full suite for cross-cutting behavior changes. For indexed documentation changes, run the repository documentation validator. Keep tests focused on behavior, evidence integrity and concrete regressions. Use the central validator for document structure and canonical contract checks; avoid duplicating those checks in tests that only pin wording, headings or historical counts. Preserve historical samples and results. No changes to Codex Trading, credentials, broker state, global configuration or publication without authorization.
