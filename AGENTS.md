# PA Research agent workflow

This repository researches price action through AI chart reading. It does not authorize trades or connect to execution systems.

## Repository ownership and pull request approval

- The canonical repository is https://github.com/justin371/pa_research. Its code owner is Lijie_Wang (`@justin371`), as defined in [.github/CODEOWNERS](.github/CODEOWNERS).
- Every pull request requires the human owner's explicit approval of the current changes before merging or enabling auto-merge. Approval of another pull request or an earlier version is not approval of new changes. Preserve all required repository checks and review requirements.
- Never submit a review or approval comment on the owner's behalf, infer approval from passing checks, bypass protection, or weaken approval requirements to complete a merge. Leave an unapproved pull request open for review.
- GitHub does not allow a pull request author to approve their own pull request. If the pull request is authored by `@justin371` and requires a formal GitHub review, report that limitation and leave it blocked until a separate authorized author is available; do not impersonate another author or reviewer.

## Research workflow

Start with [the AI visual research workflow](docs/ai_visual_research_CN.md). Use the model selected for the current task; preserve explicit configuration. Inspect actual chart images with the available image-viewing tool before making visual claims. Text summaries alone are not chart inspection.

Let AI interpret context, pressure, legs, location, competing hypotheses and useful Brooks examples. Choose timeframes and zoom from the question and evidence. Do not turn legacy pattern enums, EMA slopes, a fixed two-year window or a fixed candidate quota into discovery gates. Ask for missing evidence only when it changes the conclusion; incomplete views can still support explicitly limited hypotheses.

Read pattern notes and reference examples on demand. Use [the example registry](knowledge/brooks_visual_examples.json) to find teaching references; open the actual page/image before claiming a visual comparison. Teaching examples contain outcomes and are not holdout tests.

After reading professional books, papers, course materials or technical documents for this project, save reusable findings in the repository before completing the task. Record the source, page or section references, actual reading coverage, useful interpretations and limitations in a research memo, and link it from the relevant index so later analyses can find it. Extend an existing memo when appropriate; keep source observations separate from new hypotheses. Preserve access and copyright limits, and do not promote teaching claims into validated results or production rules. Consult these notes on demand and reopen the original evidence when a new comparison depends on visual detail.

Keep observations distinct from interpretation. Record chart sources, visible cutoff and uncertainty. Do not infer exact prices from ambiguous pixels, fabricate current data, use future bars to select a historical entry, or call subjective confidence a validated win rate.

The old daily selection rules, visual cards and output schema apply only when reproducing their named legacy experiment or exporting a compatible frozen contract. They do not govern ordinary AI discovery. Existing replay tooling requires its exact schema and honest reviewer provenance; never label an AI review as human_chart_review. Unsupported hypotheses remain research memos until a suitable replay adapter is implemented and tested.

For code changes, run relevant unit tests; run the full suite for cross-cutting behavior changes. For indexed documentation changes, run the repository documentation validator. Keep tests focused on behavior, evidence integrity and concrete regressions. Use the central validator for document structure and canonical contract checks; avoid duplicating those checks in tests that only pin wording, headings or historical counts. Preserve historical samples and results. No changes to Codex Trading, credentials, broker state, global configuration or publication without authorization.
