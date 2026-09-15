# Drive doc sync, 2026-09-15 (Batch 3 BRAND REVISED)

Why: the client's brand-forward positioning directive (see
workflow/client-decisions.md, 2026-09-15) required revising all nine Batch 3
drafts: PSFnetwork passages lead with strengths, apologetic formulas removed,
every CTA closes with a waitlist invitation, bylines swapped to the approved
Youssef/Omar set, internal links made absolute. The Drive docs had to follow
the revised repo drafts.

What was done: all 9 Batch 3 repo drafts (blog/<slug>/draft.md, as revised in
commit "feat(batch3): brand-forward revision per client directive
2026-09-15") were converted to HTML with make_paste_kit's md_to_html and
uploaded as new Google Docs via the Drive connector, one per article folder,
titled "15.09.2026 | PSFnetwork | <Title> (BRAND REVISED)". Nothing was
deleted or overwritten, per the standing no-delete rule; the older docs stay
where they are and the operator moves them to "old version" if desired.

| Article | Doc ID |
|---|---|
| how-to-verify-fractional-real-estate-platform | 1TVZwemRADPqR6rv_aF1_GylvFha4dZKscdKsmJ0leHQ |
| red-flags-fractional-offering-circular | 10O2_b5QDgrLGvTjBKlwVKQgFtuvFK4DNJ6sX8TleEg8 |
| questions-to-ask-fractional-platform | 14tNWb1Ccca5EyiFy4lY5Sw_rqUtz-tnYopmU98W-S_Q |
| fractional-real-estate-for-retirees | 1cDjJrllR3pZYBan8saMYOlnM1XRIUqbDhME3gHqVgNY |
| fractional-real-estate-high-income-earners | 1yLr1CpQ0u209PTLV8_9FR-Bd_jLv7hwQHRhCCOrmvLU |
| fractional-real-estate-401k-rollover | 1cGeBIbcK17Ev-bdg_FovaOyXFL8x42i8IgCeWiYZJ4o |
| reinvesting-fractional-real-estate-distributions | 1nlFikY3b_s3caSp9PgcwZHEDmOhBl6Quq83IIi2jNuM |
| diversifying-across-fractional-platforms | 1Dfr9nKovoG0-SGceqkNGQIR210TJOiQP7MriR18n9Ok |
| fractional-real-estate-vs-bonds | 1XqvqYBosiSQDKRJ-c-2zlGjq9ZuEGaBEwqxx6waX5-0 |

Article folder IDs used (recorded so the next sync does not have to search;
folder names are "NN - slug" under parent 1Cn__4EkSBANb3tg28rY1VxfZnB3mnu0L):

| Folder | ID |
|---|---|
| 30 - how-to-verify-fractional-real-estate-platform | 1EI1nWjGDUAfPvbjRFfWMlZNPWwGEVh3f |
| 31 - red-flags-fractional-offering-circular | 1vdY_g8kmWzD-MwUSaHCw7uVqcyKO-7RH |
| 32 - questions-to-ask-fractional-platform | 1aayasmJ_mZTpc9Yrk0Vkxun_NPqqs8UQ |
| 33 - fractional-real-estate-for-retirees | 1Jupa7dXOx6V5iniUoR2bgqgAewnT-Oj0 |
| 34 - fractional-real-estate-high-income-earners | 1JIB9NDkLet_MIHWH3bPlfIM40qXAGYKW |
| 35 - fractional-real-estate-401k-rollover | 1ZRC8DCquMjXVXsTrdvPaUsp64SOE2b5G |
| 36 - reinvesting-fractional-real-estate-distributions | 13LVA8wEBpCX89RlHJNVITLXameJtWFLM |
| 37 - diversifying-across-fractional-platforms | 1e0Pt_iItN_kEdWKE2nAVK5oG6RqE49SR |
| 38 - fractional-real-estate-vs-bonds | 1rkN68LAkC6mG0U_gd1FxhhvWWSSfgJ-5 |

Known limitation: same as the 18.08 sync. The docs mirror the repo drafts
exactly, so they contain the FAQ and Sources sections (in the CMS these live
in their own fields) and the frontmatter renders as production notes at the
top. That is faithful to the pipeline's source of truth and matches how
earlier doc waves were built.
