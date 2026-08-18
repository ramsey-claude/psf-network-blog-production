# Drive doc sync, 2026-08-18 (Batch 2 GO-LIVE SYNC)

Why: the operator asked whether Drive held the current state of everything.
It did not. The newest docs were the 16.08 "(UPDATED + FORMAT FIXED)" wave,
which missed three articles entirely (their newest docs were from 14.08),
and every doc predated the 17.08 repo fixes: hero-alt trims on 11 articles,
two dead source URLs replaced (debt-vs-equity, reit-dividend-taxation), two
moved source URLs repointed (legal-tax-guide, real-estate-etfs). The 14.08
and some 16.08 docs also still carried the retired editor byline in their
production notes; the repo drafts carry Youssef Kholeif, CMO.

What was done: all 15 Batch 2 repo drafts (blog/<slug>/draft.md, the state
that matches the live site) were converted to HTML with make_paste_kit's
md_to_html and uploaded as new Google Docs via the Drive connector, one per
article folder, titled "18.08.2026 | PSFnetwork | <Title> (GO-LIVE SYNC)".
Nothing was deleted or overwritten, per the standing no-delete rule; the
older docs stay where they are and the operator moves them to "old version"
if desired.

| Article | Doc ID |
|---|---|
| debt-vs-equity-fractional | 1_X66CteyKDmAojkISEmV0x1iYNvVWaM0iD-MfTda0AA |
| fractional-real-estate-ira | 1t3S-OrwX4oVWliJkzi1ribIIHLJd6NTTpLmIll_7bAM |
| fractional-real-estate-vs-other-investments | 12Yn1CP9dfUHVGfJPZa9WEZpuaJNHDcGXvPd6HL8Qlys |
| how-to-choose-fractional-real-estate-platform | 1FP0ABWH49S02JWWQEuGM7BHtAH8OqpOLF7RPpaO9N0g |
| how-to-read-reg-a-offering-circular | 13XTvhl2rjDVn9cLbVRRqNRbSDIyJc89xWqvVS4U2JXI |
| legal-tax-guide-fractional-real-estate | 1ELm8-I8ZlAXT5oUYVs_JEGJLRvr60hGgsPSlyBXqJQ8 |
| proptech-future-of-real-estate | 1TSp7YQatGDt6BqtFHrGTuxVVHq1m_XaMthTfPakhLgA |
| proptech-trends-2026 | 15rLXNZTquedfsryHHtH-KSlLuyDUo-eMLv2C537uWfo |
| real-estate-as-an-asset-class | 1SdmZJ1MDpnOgNni5jzvOE2R77qAAQw0BmdL0DjOSul4 |
| real-estate-etfs-vs-fractional | 1mw_LvPffFy0pzlEdA2Ll8Zgd1z4Z0JmRD_yee6mMqmw |
| real-estate-vs-index-funds-retirement | 1MgisDqUquKieqnpeaAOwmSVxPZ44I8BQ-wgg0Vdx_AU |
| reit-dividend-taxation | 19A_Z1yL8STEsHMCVRQ-83LuJ4F85orn73eB0BHuVnjw |
| single-family-vs-multifamily-fractional | 1sz8ilx4kM9bPLIIwseP9k_p3mWgWkytx6jucPN2L_4o |
| tokenized-vs-traditional-fractional | 1pagH3ZdvaFicAbBQWSQdhRcbzPXSt2jrzUTvMiqnfbI |
| how-to-sell-fractional-real-estate | 1mKXYBuKAftNZv4zPAuAAz0eMVCyKfL6-0XD8sUrA6qk |

Article folder IDs used (recorded so the next sync does not have to search):
debt-vs-equity 13mJVEqKVKKmVzd7Xz_WOTn1Lw1gnb-WU · ira
1rqHzoeWTS_OPlJDopLceKwFF6UyvGUTI · vs-other
1mPrc4xqjAHdM45V0DJ0XFl9t8TAyTF0H · how-to-choose
1All-0uOnVZikBVfyIWHU18NpkjMaWWLt · reg-a-circular
17vVDChtS-MgaVVP9sIILbRUu1IMcLLeD · legal-tax
1nO5PmFfSQP2-i1sLDV9Bf3FsqI7ZEcSu · proptech-future
1UEmdFqnCjJsfvTGxS_dfnwBfFWw9dzD5 · proptech-trends
162UQ5BwZB-LwbXieYdU1_THifwnGcmDN · asset-class
15INkEIzk15IfI6ez09E2hGzc8c18GPwS · etfs
1mMkYw_iNY2UKf8IMPlaCSYo0UuZMiNOl · index-funds
10vrgjO53d92s53XJshk60UtqK78hgN8u · reit-dividend
1iI6ehIMq6SsLgyuOFdg4O1bpCdABr17r · single-multi
10IVFn77Ncuz79EMnja50LODXlTDQ7GjV · tokenized
1RCy14YBfRgAiqLmDjMFj_B-mBxaKryfO · how-to-sell
1yJhdI7gyZPPnqGXQhe9FSBBH3jGC8t29

Known limitation: the docs mirror the repo drafts exactly, so they still
contain the FAQ and Sources sections (in the CMS these live in their own
fields) and the production-notes bullets render one bullet per line. That
is faithful to the pipeline's source of truth and matches how earlier doc
waves were built.
