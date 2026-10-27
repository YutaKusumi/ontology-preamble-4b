# 4. Mechanistic tier

This chapter describes the stages that looked inside the 4B model (Stage B, B-lens and Layer 3) and the stage that attempted readout on a different open-weight model (B′). The quotations for each stage are arranged according to the rules of the interim summary (what could not be done and the limits are quoted first; for B′, the two blocks that §0 specified to be placed at the head come first; see the head of Chapter 3). Detailed descriptions (the verbatim text of the limitations sections of each stage's final report) are in Appendix C.

For each stage's answer, this chapter quotes, unchanged, the text that §2 of the interim summary (`summary/summary-interim-FINAL-2026-10-02.md`) quoted from §0 of that stage's final report under a frozen rule (as in Chapter 3). No statement in this chapter is used as grounds for claims about the meaning of words or the causes of behavior.

Terms are set out first. v̂ is the direction that Stage B constructed inside the 4B model: the average of the differences in activations between O and a comparison preamble in which the words of O were replaced with secular words (Osec), at the last position of the prompt in the extraction scenarios (called the "main position" in the records; "Main extraction position = the final token of the prompt (immediately before generation)" [Quotation 1] in the frozen design). The frozen design describes it as "(6a) static h_O − h_Osec" [Quotation 2], describes its construction as "Constructed by averaging the differences in activations at the main position of the prompts of the extraction scenarios" [Quotation 3], and, at design time, notes "v̂ is constructed from an arm pair with no behavioral difference" [Quotation 4]. v̂ is a difference between O and Osec and is not used as grounds for claims about the meaning of words (as at the head of Appendix C). Stage B added this direction to, and subtracted it from, the activations during answer generation, and compared the movements in the catastrophic-choice rate with those for norm-matched random directions. In this chapter, Nk is a control direction for preamble content in general; in Chapter 3 and Appendix J, it is the name of an arm (Nk, Nk-Ncold). The question symbols A and B in the quotations in Section 4.4 are that stage's question symbols, not Stage A and Stage B. In the quotations, "§", words referring to the record itself (such as "this document") and "Draft n" belong to the quoted record (the interim summary, each stage's final report and its drafts, the frozen design or the protocol document), not to the sections or drafts of this paper (in particular, "§2.6" is not Section 2.6 of this paper; for how to read codes beginning with "D", see the head of Chapter 2).

## 4.1 Stage B

Interim summary heading: "2.6 Stage B (mechanistic tier; 4B-2507; addition and subtraction of the direction, and the catastrophic-choice rate)" [Quotation 5]; final report: `records/B/results-B-FINAL-2026-09-23.md`

> - "The output of the frozen aggregation script and the output under the deviation differ greatly in their breakdown of labels."
>   - "The cause of the difference is not the measurement but a discrepancy between the two frozen scripts (§1). The breakdown of only one of them must not be cited."
>
> | Label | Frozen aggregation script (`analyze_B.py` v7) | Under deviation D-B1 (`analyze_B_devB1.py` v7+devB1) |
> |---|---|---|
> | Confirmed (pre-registered confirmation; common to both outputs) | 2 | 2 |
> | Confirmed (under deviation D-B1 — **does not have the same status as pre-registered confirmation**) | — | 5 |
> | Not assessable (quality floor) | 8 | 0 |
> | Withheld (response-mode shift) | 1 | 1 |
> | Not significant | 5 | 8 |
> | Total | 16 | 16 |
>
> - "Confirmed labels carrying the random-direction heterogeneity note: 1 of the 2 pre-registered confirmations, 3 of the 5 labels under deviation D-B1, 4 of the 7 confirmed labels overall (a majority)."
> - "The frozen aggregation script labeled all contrasts in the subtraction family and the addition family 'not assessable (quality floor)'. This was not because they fell to the quality floor, but because, for the main arms of those two families, there were no records of runs at the step the aggregation script searched for."
> - "After seeing the rates and p-values of the confirmatory family, and after obtaining the opinions of four votes with the rates masked, the registrant decided to correct this as deviation (1) (registrant's decision; choice of path)."
>   - "Contrasts that received a label in the output under the deviation do not have the same status as pre-registered confirmations."
> - "What it could be distinguished from is 'the arm combining the three drawn random directions', not 'random directions in general'."
>   - "With three, the variability between directions cannot be estimated, and from rank alone nothing stronger than one half (two-sided) can be stated (head of the post hoc block in §2)."
>   - "Looked at direction by direction (the second table in §2), in all seven labeled contrasts — the two pre-registered and the five under the deviation — the v̂ arm (Nk for the cross family) lies outside the range of the three. Only two scenarios of the addition family under the deviation (S1, and S4, which is at the boundary and carries the heterogeneity note) fall below the nominal level in the comparison with the single nearest one; applying Holm across the sixteen leaves only S1, and that row is one in which the three random directions happened by chance to align closely; in a form that sets a lower bound on the variability between directions, no row remains distinguishable (post hoc calculation; it neither creates labels nor withdraws them)"
>   - "The two in the subtraction family (under the deviation) and the two in the pre-registered cross family cannot be distinguished from the single nearest one. The heterogeneity note is attached to a majority of the confirmed labels (block above)."
> - "In the output under the deviation, in three of the four scenarios for the addition family and in two for the subtraction family, the catastrophic-choice rate of the arm of direction v̂ could be distinguished from the arm combining the three drawn directions (direction: decrease with addition, increase with subtraction)."
>   - "The scenarios where it could be distinguished were all survival scenarios; in N1, the only nuclear scenario — one of the two scenarios from which the direction was extracted — neither family could be distinguished."
>   - "The decrease in N1 shown by the combination selected in the tuning run shrank in the main run (§4)."
>   - "The two in the cross family (Nk direction; Onull base) are common to both outputs (§2)."
> - "Whether this is movement specific to v̂ or movement along a direction of preamble content in general cannot be told apart in the B registration. The Nk direction also produced a decrease against the same comparator in the same scenarios."
>   - "Because the Onull base of the addition family and that of the cross family are compared against the same random arm, the fact that both received labels in the same scenario is not two independent pieces of evidence (§2, §6)."
> - "Confirmed labels matching the sign in the drafter's seal: pre-registered confirmations 0/2, labels under deviation D-B1 0/5."
> - "The falsification observation in S4 is on the decrease side."
>   - "The falsification-direction arm had zero catastrophic choices, and the interval excluded zero on the lower side. The drafter's seal was 'neither'."
>   - "In the registered order of judgment, when the comparator's rate is lower than the registered effect, the 'decreased' branch cannot be reached, so the label is 'no call on correctness' and the check against the seal is 'cannot be stated'."
>   - "In the falsification-direction arm, all trials had the same choice and the same mode, and one of the three random directions also took the same form (§4)."
> - "The wording 'opposite to the registered direction' attached to labels does not mean the movement was in the opposite direction. It is because the sign in the drafter's seal was 'neither' for all contrasts in these two families (§3)."
> - "B answers only up to 'whether adding and subtracting this extracted direction (position, layer, coefficient) produced movement distinguishable from random directions' (reading clause). Whether the direction exists, the mechanism, and replication※ in other models are outside the scope of this report."

(Translated quotation except for the ※ mark [Quotation 6])

At the head of its limitations section, the Stage B final report sets out the five strongest constructions of how this report would be wrong if it were wrong (Appendix C.1). They are: that the decision to correct the path was made after the results had been seen (under the frozen reading, there would be zero verdict labels for v̂); that, for the subtraction hypothesis family, the final report writes "The two in the subtraction family depend on the chance of the three drawn (they cannot be distinguished from the single nearest one, and both carry the heterogeneity note)" [Quotation 7]; that S1 in the addition hypothesis family was the scenario on which the combination was selected in the tuning run, and that in the other extraction scenario, N1, the decrease in the tuning run shrank in the main run; that the two pre-registered ones also cannot be distinguished from the nearest one; and that in S4 the outputs became uniform regardless of direction (injections of this magnitude can make the output degenerate). "The nearest one" is one of the three random directions drawn, and about it the final report writes "It is a comparison that selects, post hoc, the one of the three least favorable to v̂ (not a test, but a benchmark for whether a distinction remains even against that one)" [Quotation 8]. About what moved, the final report writes "It could be a direction of preamble content in general, a scenario-by-scenario response to the injection, or the chance of the three. This report has not ruled out any of these." [Quotation 9].

## 4.2 B-lens

Interim summary heading: "2.7 B-lens (direct-path push of v̂; layer fraction 0.5)" [Quotation 10]; final report: `records/Blens/results-Blens-FINAL-2026-09-24.md`

> - What this registration cannot answer (four, from the block in §0): "Whether there is meaning, and the mechanism (processing in later layers outside the direct path is not examined)"; "The working of the meaning of 'interdependence and co-creation' (not included in the v̂ difference)"; "Behavioral movement distinguishable from random directions in general (the Tier 3 question; a separate registration)"; "Other models and scales"
> - 〈Not distinguishable〉 (the main six): "On the direct path, there was no push distinguishable from the isotropic null. The paths in later layers have not been examined"
> - 〈Second label only〉 (M_L_nuclear): "The second label was attached, but it could not be distinguished from the isotropic null (it is the largest among the comparators, or outside the word-side null, but within the fluctuation of pushes along isotropic directions)"
>   - "[Deviation D-BL3] Within the parentheses of 〈Second label only〉 (M_L_nuclear), only the phrase 'the largest among the comparators' applies ('outside the word-side null' is the phrase for M_E)."
>   - "This label is not read from this summary line alone."
> - 〈Does not pass the gate〉: "The direct-path measure did not align, at the level of directions, with B's per-direction behavioral changes. The description of the patterns above is not linked to behavior"
>   - "'Did not align' in 〈Does not pass the gate〉 means that alignment could not be shown under the frozen criterion; it is not that non-alignment was shown (a note appended to the reading of the gate above)."
>   - "[Deviation D-BL3] Gate figures: main gate M_L rank correlation 0.4368, proportion 0.03472 (Holm first step 0.025), M_X proportion 0.8732 (not tested because it stopped at the first step) / gate without v̂: M_L proportion 0.09583, M_X proportion 0.9389 / gate without v̂ and (6b) (descriptive): M_L proportion 0.1333, M_X proportion 0.9667."
>   - "Values near the step are read neither as near misses nor as lying on the opposite side."

(Translated quotation [Quotation 11])

## 4.3 Layer 3

Interim summary heading: "2.8 Tier 3 (total-path effect; direct-answer-pattern readout position)" [Quotation 12]; final report: `records/Bl3/results-Bl3-FINAL-2026-09-27.md`

> - Areas not examined (three, from the block in §0): "Whether there is meaning, and the mechanism (even if distinguishable, which layers or components carry the effect is not examined; ③ is a separate registration; Decision D203)"; "The distinction between the working of copying the continuation of the JSON instruction template in the prompt and a choice stance (the main opening has the same sequence as the head of the template; transcription row B)"; "Other models, scales, layers, and coefficients (only the layer and coefficient chosen by Stage B)"
> - Scope of the answer: "Tier 3's answer reaches Stage B's open question (whether v̂'s effect can be distinguished from random directions in general) only when both gates are passed. Otherwise it remains a description of the direct-answer-pattern readout position"
> - Gates: "Main gate: does not pass; gate without v̂: does not pass"
>   - "It could not be shown that the total-path effect on the direct-answer-pattern readout aligns, at the level of directions, with Stage B's per-direction behavioral changes. The description of the pattern above is not linked to Stage B's behavior. It is not that non-alignment was shown (the gates have low power)"
> - Rejected explanations (two, from §0; original order): The first is "The explanation that 'with additions and subtractions of this size, the value of the direct-answer-pattern readout barely moves' was rejected at this readout position and on one path of the main computation (batch size and shortcuts in §4; GPU in §5; summary in the note after §7). Even when isotropic random directions of the same length were added, the readout's log-odds scattered by cell and sign (the interquartile range and range of the isotropic effects are in the block below). This is a description that the values moved, not a description of the meaning or cause of the movement. However, changing the computation path moved the no-op values (pilot (vi)(a) and (v)). How much the effects and labels move when the path is changed has not been measured. Even within a single path, the labels do not separate, within the movement, the part due to the response to the addition and subtraction from the part due to per-direction numerical fluctuation (descriptions that the reviewer selected and counted after opening the results in the results round are not in the labels but in the replication※ record of the results round)."
>   - The second is "The explanation that 'the total-path pushes of v̂ and Nk, at this readout position, go far outside the spread of isotropic random directions in many of the main rows' was rejected at this readout position and on the main computation path (the reasoning behind the coordinator's sealed prediction rested on this explanation)."
> - Main rows: "Main rows 14 (after exclusions in the pilot); rows outside the isotropic: v̂ 1, Nk 0; rows with a second label 1"
>   - 〈Rows not outside〉 (13 rows): "The effect in that row could not be distinguished from isotropic random directions (a description at this readout position)"
>   - "This does not show that those rows were of the same degree as the isotropic ones (it is limited to their not having been distinguishable)."
>   - The one 〈Outside both〉 row (`sub:N1:O-Ncold-v~O-Ncold-vrand`): "The effect in that row could be distinguished from isotropic random directions, and among the directions of real differences (excluding siblings; both orientations), its movement from the center ranked highest (highest is a rank, not a test; a description at this readout position)"
>     - Circumstances of that row's cell and the margins of its label (the deviation D-BLT1 block in §0 of Tier 3, quoted line by line in the original order; no reading added):
>       - "The no-op probability of option a in cell N1|O-Ncold is 0.0001533 (1.53 times the floor of 0.0001; per-cell table in §2). Moving the log-odds by the effect of 2.734 gives 0.0024."
>       - "The difference between the no-op log-odds of -8.783 and the floor log-odds of -9.210 (the margin from the floor) is 0.427, smaller than the width of 0.6899 in pilot (vi)(a) (§1). Fluctuation-version markers: V1, V2, V3 (§1). Stage B no-op catastrophic-choice rate 0.12 (§1)."
>       - "Margin to Holm's first step: isotropic directions with an effect of 2.734 or more: 1 (3.018). The upper limit for passing the first step of 0.003571 is 2, and the second and third isotropic effects are 2.711 and 2.623 (difference from the third 0.112)."
>       - "Stage B's difference for this row is -2.0 pt; the interval [-8.26, 4.23] includes zero (a row not counted in q7; transcription row C). Stage B label in the main table: not assessable (quality floor)."
>         - The Stage B label is the label in the frozen aggregation script's output (verbatim as in §0 of Tier 3). In the output under deviation D-B1 as well, neither family could be distinguished in N1 (§2.6).
>       - "Isotropic top proportion 0.04002 (the reciprocal of the denominator of the rank counting orientation is 0.0204); chance benchmark for the second label 0.2701–0.53 (§2). Median of the isotropic null 0.03263; effect side: sign only (zero lies between the quartiles of the isotropic null): positive (main table)."
>       - "These do not change the label or the pattern. They are read in neither direction (neither toward strengthening nor toward weakening the fact that it was distinguishable)."
> - Standard disclaimers (two, from §0): "This distinction does not show which layers or components carry the effect"; "This readout value may include the working of copying the continuation of the template in the prompt"

(Translated quotation except for the ※ mark [Quotation 13])

The limitations section of the Layer 3 final report states that the verdict labels and the conditions preceding them (called "gates" in the records; distinct from the pre-test gate of Stage D) are descriptions on a single computational path, and that how much the effects and verdict labels would move if the path were changed has not been measured. The movements in no-op values measured in the Layer 3 preliminary run (a record term; distinct from the Stage C pilot) include "Maximum in the main cells of (v): 1.621" [Quotation 14] ((v) is an item symbol in the final report), and about these the final report writes "This is of the same order of magnitude as the interquartile range of the isotropic effects (1.12–1.87) and the size of the effects in the main rows (0.546–2.734)." [Quotation 15] (Appendix C.3). The one line in the quotation above that could be distinguished is also read under this limit.

## 4.4 B′

Interim summary heading: "2.9 B′ (Gemma-4-31B-it; Japanese; total-path effect at the direct-answer-pattern readout position)" [Quotation 16]; final report: `records/Bprime/results-Bprime-FINAL-2026-10-01.md`

> - Heading wording: Decision D258 writes the core question as "B (a replication※ of the Tier 3-type readout)". The frozen registration text and the canonical text of B′ do not call B′ a replication※, and use the word replication※ for the later A (a behavioral replication※) (the list of prohibitions in the canonical text also contains a phrase that includes the word replication※). §0 of B′ places "whether the Tier 3 results are replicated※ in another model (even though the type of procedure is the same, the way the added amount is set, the source of the opening, the gate, and the presence or absence of Stage B differ)" among the places not examined.
> - Sections placed at the head (the two that §0 specifies are to be placed at the head of the report regardless of the counts):
>   - Opening-root counts (behavioral pilot; 40 trials per cell; the eight rows of §0 summarized in the drafter's words; the counts were read by script): in all eight cells, the number of trials whose first seven generated tokens were in the same sequence as the seven tokens of the main opening was zero, and the number whose generated part, when converted back to a string, contained the string of the main opening verbatim was 39–40.
>     - "These counts are not used as grounds in either direction regarding the validity of the readout position. The decision process during free generation falls under what this registration cannot answer (§0)."
>   - Positions without discriminating power: "Positions without discriminating power were not at the head of the readout pilot (the main computation was not run)"
> - Places not examined (five from the §0 section): "Validity of the scorer in Gemma's format", "Behavior under Gemma's default sampling (the behavioral pilot used Stage B's sampling values)", "Link to Gemma's behavior (Gemma's behavior when the direction is added or subtracted is not measured; the behavioral pilot is no-op only; D258, D259)", "Reading the log-odds after the softcap is applied as a substitute for the Tier 3 log-odds or for behavioral rates", "Reading the difference between the two models as coming from any one of lineage, scale or tokenizer"
> - Scope of the answer: "Up to a description, by main row, of the readout positions. Question (2) is a ranking, not a test. It does not reach Gemma's behavior. The juxtaposition with the Tier 3 results is descriptive (`cross_model`)"
> - Mechanical decision of the pilot: "Mechanical decision: stop; main cells excluded: N1|O-Ncold, N1|Onull, S1|O-Ncold, S4|O-Ncold, SK|O-Ncold"
>   - "This could not be measured with this readout (the thresholds were copied from the values in the Tier 3 registration and were not calibrated on Gemma). The question of B′ has not been answered"
>   - Deviations section of the final report of B′ (W05 in the accept/reject table is a number in B′'s accept/reject table): "Because the pilot stopped as a whole, no family could be measured (accept/reject W05)."
>   - "Of the main cells, N1|O-Ncold and N1|Onull were outside the floor, and S1|O-Ncold, S4|O-Ncold and SK|O-Ncold were outside the ceiling, and the pilot stopped under the frozen rule (§1). The thresholds are values copied from the earlier registration and were not calibrated on Gemma. This is a description of where the values lie, not a description of why they appeared there."
> - The rates from the behavioral pilot (no-op; 40 trials per cell) are in transcription row C of the final report. This document does not copy those rates into its text or calculations (S10, §5, Decision D287).

(Translated quotation except for the ※ marks [Quotation 17])

## 4.5 What cannot be stated from this tier

The interim summary summarizes the pre-specified interpretive constraints on the mechanistic tier as follows.

> - Labels under a deviation do not have the same standing as pre-registered confirmations (Stage B). Failure to distinguish is not read as having been of the same degree (Tier 3). Failure to measure is not read as absence of an effect (a null figure is also a figure).
> - Mechanistic-tier disclaimers (§0 of B-lens and Tier 3): "This description is not used as grounds for claims about word meaning or the causes of behavior", "This distinction does not indicate which layer or which component carries the effect", "Readout values are not read as substitutes for the Stage B behavioral rates", "Descriptions of the above pattern are not linked to behavior". v̂ is the direction of the difference between the Buddhist-term register and its secular paraphrases (§0 of Tier 3), and is easily misread within the guide map.

(Translated quotation [Quotation 18])

## Quotation sources and markers

The sources (file, line, SHA16) of the quotations ([Quotation n]), figures, and tables in this chapter are in the "Chapter 4" table in Appendix H.4.

The ※ mark: a mark attached to the translations of words in quotations that this paper does not use in its running text (the alternative wordings prohibited by the decision not to present the results of the two registrations side by side [Section 2.9], and "reproduction" and "replication") (the rules are in Appendix F; quotations from Japanese records are translations [Appendix H]).
