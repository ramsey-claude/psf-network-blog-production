# Decision register

Standing decisions, each with the evidence that proves it was made. A decision
lands here when it changes what the pipeline does from now on and is not fully
captured by a rule in [rules.md](rules.md).

Cite decisions by id (`D-004`) in reviews, briefs, and commit messages.
`workflow/brain.py check` fails on any brain page citing a D number this file
does not define.

---

### D-001. Drive delivery runs on the Drive REST API, never the Drive MCP

- **Decided:** 2026-05-14
- **Why:** the MCP `create_file` conversion table covers text/plain and
  text/csv only, so a .docx either stayed a .docx or landed as a raw-markdown
  Google Doc with visible frontmatter. The MCP also has no delete, so re-runs
  accumulated junk in the folder.
- **Consequence:** Stage 9 runs on three local scripts (`render-for-drive.py`,
  `drive_auth.py`, `drive_cli.py`) against OAuth project `my-project-82896`.
- **Evidence:** `workflow/incident-log.md` 2026-05-14 entry, `checklist/delivery.md`
- **Rule:** `R-tooling-drive-uploads`

### D-002. Credentials live outside the repo, in files, never in code

- **Decided:** 2026-05-14
- **Why:** `push.sh` shipped with the PAT embedded. Rotation meant editing the
  file and a leak would have been permanent in history.
- **Consequence:** one token path for every consumer, and a security policy
  that names the paths that must never be committed.
- **Evidence:** `workflow/incident-log.md` 2026-05-14 entry, `SECURITY.md`
- **Rule:** `R-auth-infrastructure-github-token`, `R-auth-infrastructure-drive-token`

### D-003. Background QA runs four times a day, not once

- **Decided:** 2026-05-14
- **Why:** a slug pushed at 09:14 waited a full day for its first post-publish
  look under the single 09:13 run.
- **Consequence:** Stage 10 fires at 03:13, 09:13, 15:13, 21:13. The token
  check stays daily at 09:07 so the first Stage 10 of the day sees fresh
  sentinel state. The stated principle: background QA cadence runs at roughly
  four times the typical pipeline cadence.
- **Evidence:** `workflow/incident-log.md`, "Resolved on 2026-05-14" section

### D-004. A permission prompt is recovered from, not escalated

- **Decided:** 2026-05-15
- **Why:** the operator rejected a compound Bash call to make the point that a
  run pausing for approval is not autonomous. The permission system matches the
  whole invocation string, so a compound command fails even when every part of
  it is allowed.
- **Consequence:** rewrite the call first, narrow-allowlist second, never
  broaden, always log what happened for the next retrospective.
- **Evidence:** `workflow/incident-log.md` 2026-05-15 entries,
  `workflow/trigger-contract.md` "Permission prompt self-recovery"
- **Rule:** `R-process-permission-prompts-self-recover-do-not-pause`,
  `R-process-single-command-bash-calls`, `R-process-one-shot-push-scripts-go-in-repo`

### D-005. The expiry-warning path stays in the token check even though it cannot fire

- **Decided:** 2026-05-15
- **Why:** the live token is a classic PAT minted with no expiration, so GitHub
  never sends the expiry header the warning path reads.
- **Consequence:** `token_expiry_check.py` still runs daily. The 401 path is
  the one that actually protects the pipeline, and the warning path activates
  by itself if the operator ever swaps in a token that does expire.
- **Evidence:** `workflow/incident-log.md` 2026-05-15 "Classic PAT expiry verification"

### D-006. PSFnetwork publishes for the US market, in English, only

- **Decided:** 2026-05-26
- **Why:** operating scope, stated at the top of the roadmap.
- **Consequence:** `target_markets` defaults to `["EN-US"]`, which makes Stage 5
  and Stage 6 no-ops that still write their artifacts. The multi-market
  localization spec stays in the repo for a future that has not arrived, and
  Gulf and UAE gap research stays out of scope.
- **Evidence:** `ROADMAP.md` operating scope note, `workflow/pipeline.md` Stage 5,
  `checklist/localization-guide.md`

### D-007. Delivery goes through deliver.py, which will not ship unreviewed work

- **Decided:** 2026-05-26
- **Why:** a delivery skipped Stage 7 and put two rounds of violations in front
  of the client before anyone noticed.
- **Consequence:** `deliver.py` refuses to upload without a QA report that
  records PUBLISH and lists no FAILs. Direct `drive_cli.py upload-as-gdoc` is
  retained for operator cleanup, and is no longer a legal Stage 9 path.
- **Evidence:** `workflow/pipeline.md` Stage 9, `workflow/deliver.py`

### D-008. Alternatives comparisons stay on the shelf

- **Decided:** 2026-05-26
- **Why:** the operator flagged that fractional against high-yield savings,
  against direct rental ownership, and against vacation rentals can position
  PSFnetwork weakly in some scenarios.
- **Consequence:** those three framings are excluded from the topic pool until
  the competitive posture is stronger. This is a hold, not a cancellation.
- **Evidence:** `ROADMAP.md` Step 2, exclusion note

### D-009. Grammar became a gate, not a hope

- **Decided:** 2026-05-26
- **Why:** a customer read a Stage-7-cleared document and found grammar and
  mobile formatting problems. Sections A through D of the gate could not have
  caught either.
- **Consequence:** Section E of the QA gate, the grammar heuristics in
  `check-rules.py`, the six-column table rule, and a documented intake path so
  the next piece of customer feedback has somewhere to go.
- **Evidence:** `checklist/qa-gate.md` Section E, `checklist/customer-feedback-intake.md`

### D-010. A character name is a cross-article resource

- **Decided:** 2026-05-26
- **Why:** the same first name anchored the human story in 13 of 15 Batch 2
  articles, in five different professions. Each article passed its own
  humanization review; nothing looked across articles.
- **Consequence:** every Real Story anchor name is unique across the whole
  blog, checked at the gate and pinned by a test.
- **Evidence:** `workflow/incident-log.md` 2026-05-26 entry,
  `tests/test_persona_uniqueness.py`

### D-011. Voice samples are permanently unavailable

- **Decided:** 2026-07-22
- **Why:** the brand does not produce internal writing of that kind and will
  not supply it. This is an answer, not a pending request.
- **Consequence:** `brand/voice-samples/` stays empty. Stage 2.5 runs in its
  voice-samples-empty mode as the standing default, drafting against
  `brand/tone-and-voice.md` alone with a conservative bias. Audits and
  retrospectives do not re-open it.
- **Evidence:** `brand/voice-samples/README.md`, `workflow/incident-log.md`
  2026-07-22 entry, `checklist/humanization-pass.md`

### D-012. Every article carries its own external authority

- **Decided:** 2026-07-22
- **Why:** GEO and reader trust both need the article to point at primary
  sources inside the body, not only in a Sources block at the end.
- **Consequence:** at least two inline external links per article from the
  allowed federal domain list, verified live, Batch 3 onward. Batch 2's gap
  became visible debt at the go-live QA three weeks later.
- **Evidence:** `checklist/qa-gate.md` Section B, `ROADMAP.md` pool status

### D-013. A rule states its scope, and its debt becomes visible the same day

- **Decided:** 2026-08-11
- **Why:** the external-link rule shipped scoped to Batch 3 onward, which left
  Batch 2 quietly non-compliant. Diff-mode CI only reads touched files, so the
  gap sat dormant until a human went looking during go-live QA.
- **Consequence:** every new gate rule says "all content" or "batch N onward"
  on the same line. Anything the scope leaves behind goes into
  `workflow/qa-baseline.txt` that day. The baseline is a remove-only ratchet:
  entries leave when a backfill fixes the content, and nothing authored after a
  rule existed is ever added to it.
- **Evidence:** `checklist/qa-gate.md` "Rule scope", `workflow/incident-log.md`
  2026-08-11 entry, `workflow/qa_battery.py`

### D-014. PSFnetwork is not described as a traditional structure

- **Decided:** 2026-08-11
- **Why:** a delivered article said "we run a traditional structure". The brand
  had already built blockchain infrastructure for on-chain ownership
  management, so the sentence was wrong about the company.
- **Consequence:** positioning passages describe PSFnetwork as a Reg A,
  per-square-foot structure with that infrastructure already built, and any
  reference to a live secondary market stays conditional, "if and when", never
  a forward-looking promise.
- **Evidence:** `workflow/incident-log.md` 2026-08-11 feedback round 2 entry

### D-015. The bylines are standing personas, and the disclosure lives on the About page

- **Decided:** standing, predates the current log
- **Why:** the operator authorized automated use of two brand-approved bylines
  so no post needs per-post approval.
- **Consequence:** Maya Reyes and Daniel Cho are the only names that may appear
  as author or reviewer. Neither is a real individual. Quotes follow the six
  rules in the personas file, and the post itself does not repeat the
  production-model disclosure. The pipeline never touches the About page.
- **Evidence:** `brand/personas.md`
- **Rule:** `R-tooling-personas`, `R-content-quality-author-reviewer`

### D-016. Research runs on public sources, not on a paid keyword tool

- **Decided:** standing, recorded in the active rules
- **Why:** cost and dependency. Stage 1 has to work with what a browser can see.
- **Consequence:** Semrush is not called during a run, even though the
  competitor tables in the roadmap originally came from it. Search Console
  cannibalization checks wait until the blog passes 100 published posts.
- **Evidence:** `workflow/incident-log.md` Active rules, Tooling
- **Rule:** `R-tooling-research`

### D-017. Three topics are closed by the operator, not by the pipeline

- **Decided:** 2026-05-26 and after
- **Why:** operator judgment on the value of each.
- **Consequence:** pool items 17 (platform fees comparison) and 18 (real estate
  operating agreement) are cancelled. Item 8 (REITs 101) is deferred, not
  cancelled. Stage -2 does not pick any of them up.
- **Evidence:** `ROADMAP.md` pool status line

### D-018. The Batch 2 cover refresh was reverted, and the reason is not in the repo

- **Decided:** 2026-08-18
- **Why:** unknown. The revert commit carries only the default message.
- **Consequence:** `brand/cover-image-spec.md`, `workflow/make_cover.py`, the
  batch cover copy, and 15 rendered covers are no longer in the tree. The
  reverted commit's own message says all 15 had been uploaded to the Batch 2
  Drive folders and the previous covers archived, so Drive and the repo may
  disagree about what the current cover of a Batch 2 article is.
- **Consequence for the next run:** confirm intent with the operator before
  rebuilding, re-rendering, or re-uploading any of it.
- **Evidence:** commits `a5a06ee` and `0bf8ddf` in git history
