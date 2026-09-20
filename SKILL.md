---
name: paper-to-cn-patent
description: Convert scientific papers, theses, technical reports, source code, figures, or research manuscripts into evidence-grounded Chinese invention patent drafts. Use when an AI agent must extract patentable technical contributions, map every claimed feature to source evidence, preserve core formulas as editable Office Math, generate claim-aligned flowcharts and methodology figures, compare a paper with an existing patent, audit support and consistency, or deliver separate Chinese DOCX files for claims, specification, abstract, and abstract figure.
---

# Paper to Chinese Patent

Use this file as the router for the patent-drafting workflow. Do not draft the
application directly from the paper abstract or contribution list.

## 1. Load the workflow

Read `manifest.yaml`, then read every file under `always_load`.

Detect these axes from the user's files and request:

- `source_format`: selectable PDF, scanned PDF, pasted text, or mixed project;
- `task_mode`: full draft, claim set, disclosure analysis, or paper-patent audit;
- `invention_type`: algorithm/software, apparatus/system, process/material, or mixed.

State the detected values in one short line. Load only the matching fragments
declared in the manifest. Load detailed references only when their condition
applies.

## 2. Preserve source grounding

Create stable source IDs before drafting:

- `P001...` for paper text blocks;
- `E001...` for equations;
- `F001...` for source figures;
- `C001...` for source-code or supplementary evidence.

Every material feature in a formal claim must map to one or more source IDs.
Use only `explicit`, `inherent`, `needs-confirmation`, or `unsupported` as
support states. Exclude `unsupported` features from formal claims.

Never infer inventorship, ownership, unpublished implementation details,
publication dates, prior-art conclusions, or legal sufficiency. Use
`[TO CONFIRM: specific question]` outside formal claims when facts are missing.

## 3. Draft through stage gates

Complete the stages in `static/core/workflow.md` in order. Persist the
intermediate artifacts specified there. Do not move to formal claims until the
source map, terminology ledger, inventories, evidence ledger, and invention
concept pass their gates.

For a full application, draft claims first, then align the specification,
figures, embodiments, and abstract to the claim terminology and step order.

## 4. Produce Chinese formal documents

Agent-facing analysis may use the user's preferred language. Produce formal
Chinese patent deliverables in Chinese:

- 权利要求书;
- 说明书;
- 说明书摘要;
- 摘要附图;
- figure labels and descriptions.

For algorithmic inventions, retain source-supported core formulas, define every
symbol, explain each formula's technical operation, and render formulas as
native editable Office Math in DOCX. Do not use plain LaTeX strings as the
visible formula.

Generate the main flowchart from the ordered steps of the principal method
claim. Its final node must name the concrete domain output, such as a defect
detection result, target pose, state estimate, or control instruction. Reuse
the same main figure as the abstract figure and a specification figure.

## 5. Validate before delivery

Populate the structured draft described in `references/draft-schema.md`, then
run:

```bash
python scripts/validate_patent_draft.py draft.json
python scripts/build_patent_package.py draft.json --output-dir outputs --prefix patent
```

Resolve all validation `ERROR` findings. Review every `WARNING` against the
source. Label the result `incomplete draft` when a required quality threshold
in `static/core/output-contract.md` is not met.

The generated package is a drafting aid for inventor and patent-professional
review, not a patentability opinion, infringement opinion, or filing guarantee.


## STRICT OVERRIDE — Project-specific Chinese patent requirements

Apply these rules as hard gates. They override any less strict wording elsewhere in the repository.

- The invention title must be within 25 characters under the project counting rule and use a standard technical term.
- Formal document text uses 宋体、小四号（12pt）、1.5倍行距. The title is centered and bold. 技术领域、背景技术、发明内容、附图说明、具体实施方式 headings are bold and have no punctuation.
- The specification must be clear, complete, and enabling. The technical problem, technical solution, and beneficial effects must correspond.
- Background must objectively describe relevant prior technology and its deficiency. Never fabricate a citation or silently treat the paper's own method as prior art. A verified patent citation should record country, publication number, title, and preferably publication date.
- Exactly one independent claim is permitted by default. It must precede all dependent claims. Do not automatically add device/system/storage-medium/use independent claims.
- The independent claim must contain the necessary technical features and form a closed technical chain. For method claims, preserve input/object → operation → technical processing/condition → concrete output.
- Dependent claims must reference an earlier claim and add a concrete technical limitation supported by the specification.
- Product claims should use structural features and relationships. Avoid pure function/effect limitations.
- Reject ambiguous scope words such as 厚、薄、强、弱、高温、高压、很宽范围、约、接近、等、或类似物, and non-limiting expressions such as 例如、最好是、尤其是、必要时.
- Each claim is one sentence: it may contain exactly one Chinese full stop, and that full stop must be the final character. No internal Chinese full stop.
- Formal claims must contain no placeholders such as [TO CONFIRM] or [待确认].
- The abstract must be no more than 300 characters including punctuation, with the technical solution as the main content.
- Every core formula must be source-grounded, have complete symbol definitions, and be rendered as editable Office Math.
- The overall flowchart must cover every numbered step of claim 1 and end in a concrete domain output.

Before delivery, run the deterministic validators. Any hard-gate error makes the draft incomplete-draft.

## NON-NEGOTIABLE EXECUTION ORDER

1. **Evidence before drafting**: do not draft formal claims from an abstract, contribution list, or model-generated summary alone. Inspect the full substantive disclosure and establish source IDs first.
2. **Closest prior technology before claim wording**: identify and verify the most relevant prior technology where external search is requested or available. Never invent a citation, publication number, date, or disclosed feature. If verification is unavailable, preserve the uncertainty rather than filling it.
3. **Claim 1 before dependent claims**: create exactly one independent claim unless the user explicitly supplies a different requirement. Claim 1 must contain the necessary technical features and a closed technical chain. It must use a clear preamble/characterizing-part structure.
4. **Dependent claims only narrow**: every dependent claim must cite an earlier claim and add a concrete technical limitation. Never create a dependent claim that only restates an effect, purpose, advantage, or optional prose.
5. **Specification must support the claims**: after claims are drafted, write the specification so every claimed term, operation, relationship, parameter, formula, and alternative is actually explained to an enabling level. Do not backfill unsupported details.
6. **Abstract is last**: the abstract must be generated from the final claim/specification, be <=300 Chinese characters including punctuation, and emphasize the technical solution.
7. **Application handoff is a separate state**: administrative facts such as applicant/inventor identity, order, identification numbers, fee approvals, institutional forms, and submission routing are external inputs. The Skill must never infer them. Word/PDF files must represent the same approved technical version.

## HARD FAIL CONDITIONS

Stop formal drafting and report incomplete draft when any of the following occurs:

- required source material has not been inspected or is unavailable;
- an essential claim feature is only needs-confirmation or unsupported;
- claim 1 cannot form a complete technical chain;
- there is more than one independent claim;
- a dependent claim references itself or a later claim;
- a claim contains an internal Chinese full stop, an unresolved placeholder, or a prohibited vague-scope expression;
- the specification cannot support a claimed feature or required implementation detail;
- a core formula lacks source linkage, complete symbol definitions, or editable Office Math output;
- the main flowchart does not cover every numbered step of claim 1;
- title >25 characters or abstract >300 characters;
- final Word/PDF versions are inconsistent.

Do not “repair” a hard failure by inventing technical content. Ask for the missing source or inventor confirmation, and keep the affected item out of the formal claim set.
