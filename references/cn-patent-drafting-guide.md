# Chinese Invention Patent Drafting Guide

## Contents

1. Evidence discipline
2. Converting paper structure
3. Independent claims
4. Dependent claims
5. Specification
6. Algorithm-related inventions
7. Final audit
8. Quality rubric

## 1. Evidence Discipline

Create the claim language from disclosed operations, relationships, structures, and parameters. A paper's broad statement of purpose is not, by itself, support for every implementation that could achieve that purpose.

Distinguish:

- a result demonstrated by experiments;
- a technical effect caused by identified features;
- an aspiration or future research direction.

Use the first two with appropriate scope. Exclude the third unless inventors provide additional disclosure.

## 2. Converting Paper Structure

Map common paper sections as follows:

| Paper material | Patent destination |
|---|---|
| research motivation and limitations | background and technical problem |
| contribution list | candidate essential features and dependent-claim branches |
| method overview | independent-claim sequence |
| module architecture | dependent claims and embodiments |
| formulas and losses | dependent claims and detailed embodiments |
| dataset preparation | acquisition/preprocessing claims and embodiments |
| experiments and ablations | beneficial effects and verification examples |
| conclusion | effect summary, not a substitute for technical detail |
| limitations/future work | inventor questions; normally not claimed |

Rewrite causal and operational relationships. Do not merely translate academic prose.

## 3. Independent Claims

For a method claim:

- identify the technical input;
- state the essential processing sequence;
- preserve dependencies between intermediate data;
- state the specific domain result or control action, such as a detection result, estimated state, target position, classification result, or control instruction;
- include only features needed for the central effect.

Prefer observable operations over labels such as "intelligent module" or "novel network." Define what the module receives, performs, and produces.

Avoid:

- result-only wording unsupported by means;
- unnecessary dataset names, exact model depth, or experimental values;
- optional features mixed into the essential chain;
- steps that appear only in the patent draft and not in the source.

## 4. Dependent Claims

Use dependent claims to build fallback positions around:

- data sources, labels, and preprocessing;
- component topology and data flow;
- feature extraction branches;
- training stages and loss functions;
- reconstruction, fusion, attention, or optimization operations;
- inference and post-processing;
- equations, thresholds, ranges, and preferred parameters;
- deployment as device and storage medium.

Each dependent claim must add a technical limitation. A statement of advantage alone does not narrow a claim.

## 5. Specification

### Technical Field

Use one concise paragraph naming the relevant technical field and the specific subject.

### Background

Describe known approaches and a concrete technical deficiency without unsupported admissions about the closest prior art. Do not use the paper's own method as background.

### Invention Content

State:

1. the technical problem;
2. the technical solution in language aligned with the claims;
3. beneficial effects linked to particular features.

### Figures

Propose only figures supported by available information, such as:

- overall method flow;
- model or system architecture;
- core module structure;
- training and inference flow;
- data-processing flow.

Mark missing drawings as `[待补图]`.

### Detailed Embodiments

Provide enough operational detail for implementation. Include data origin, preprocessing, model flow, training, inference, formulas, parameter examples, and evaluation where disclosed.

Present paper-specific settings as examples unless they are essential. Preserve alternatives disclosed in the source to support broader scope.

### Formulas

For a paper whose technical contribution depends on mathematical operations, reproduce the core formulas in patent notation and explain them in the specification.

Include formulas that define:

- sample selection or prototype computation;
- feature transformation or reconstruction;
- attention, weighting, alignment, or fusion;
- training objectives and loss functions;
- estimation, detection, positioning, or decision rules.

For every formula:

1. assign a consecutive patent formula number;
2. identify its source page and paper formula number in the drafting record;
3. define every variable, index, operator, norm, and weight;
4. explain what input the formula processes and what output it produces;
5. connect the formula to a method step and technical effect.

Do not leave a core operation described only as "calculated according to a formula." Do not add unrelated evaluation metrics merely to increase the number of formulas.

### Abstract

Summarize the field, problem, essential solution, and main technical effect. Keep terminology aligned with claim 1 and avoid promotional language.

## 6. Algorithm-Related Inventions

Tie algorithmic operations to a technical context and technical data, such as sensor signals, industrial process variables, images, battery measurements, or remote-sensing data.

Describe:

- how data is obtained;
- how data is transformed;
- how model components cooperate;
- what technical quantity, state, location, class, or control instruction is produced;
- how that output improves a technical process.

Do not rely solely on accuracy claims. Explain the mechanism that reduces redundancy, preserves multiscale information, handles domain shift, reconstructs disturbed features, or otherwise produces the effect.

## 7. Final Audit

Confirm:

- claim 1 can be traced line by line to the source;
- dependent claims have correct antecedent basis;
- all claimed terms appear in the specification;
- the same object is not given multiple names;
- no equation has undefined variables;
- every source-supported core formula is present in the specification rather than only in claims or notes;
- the flowchart exists as both SVG and PNG and the PNG is embedded in the specification;
- the designated abstract figure is the same main figure reused in the specification and is embedded in the abstract deliverables;
- claims, specification, and abstract are delivered as separate DOCX files;
- no performance number is copied without its test context;
- publication and filing dates are flagged for professional novelty review;
- the draft is labeled for inventor and patent-professional review.

## 8. Quality Rubric

Score each dimension from 1 to 5 and give one sentence of evidence for the score.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| evidence support | major claimed features are unsupported | most features are traceable, with gaps marked | every claimed feature is traceable and unsupported matter is excluded |
| claim architecture | scope is incoherent or dependencies fail | usable independent claim with limited fallback positions | clear essential chain and layered fallback positions across appropriate categories |
| terminology and consistency | conflicting terms and broken references | mostly consistent with minor issues | terms, symbols, dependencies, figures, and sections align throughout |
| enablement detail | result-only description | principal implementation is described | data, operations, relationships, parameters, and alternatives are sufficiently described |
| technical-effect reasoning | effects are promotional or detached | some effects are linked to features | each material effect is causally tied to disclosed technical means |

Delivery thresholds:

- Require at least 4 for evidence support.
- Require at least 4 for claim architecture.
- Require at least 4 for terminology and consistency.
- Require at least 3 for enablement detail.
- Require no unresolved structural errors from `scripts/audit_claims.py`.

If a threshold is missed, label the output `incomplete draft` and list the exact inventor input needed to improve it.

## Strict Addendum — Supplied Drafting Requirements

### Specification

说明书必须对发明作出清楚、完整的说明，使所属技术领域的技术人员能够实现。凡本领域技术人员不能从现有技术直接、唯一得出的必要内容，必须在说明书中描述。技术问题、技术方案、有益效果必须相互适应。
技术领域应使用具体技术领域，并可采用“本发明属于【】技术领域，涉及一种【】，可用于【用途】”的结构，但不得为了套用格式虚构用途。
背景技术中的专利引证必须优先采用申请日前最近两年内公开的、与本发明技术领域和技术问题高度相关的专利文献；检索不足时必须明确标记“近两年相关专利不足”，不得用明显更早的专利冒充近两年依据。背景技术中的专利不得机械罗列，而应按照技术发展和问题演进形成递进链：第一篇说明较早/基础技术方案及其仍存在的具体问题；第二篇应在前述技术基础上针对该问题进行改进，并说明改进后仍存在的新的技术问题；后续文献依次体现“已有方案 → 针对性改进 → 暴露新的限制/问题”的逻辑。最终应自然收束到本发明所要解决的技术问题，并明确说明本发明的技术方案针对上述现有技术问题提供解决路径。不得把本发明的技术特征倒灌进现有技术，不得虚构文献之间不存在的改进关系。每篇引证专利至少核实国别、公开号、名称、公开日期以及与背景技术描述相对应的实际公开内容；非专利文献记录标题和详细出处。
有益效果应由技术特征直接带来或必然产生，并明确与现有技术的区别。引用实验数据时必须记录必要的实验条件和方法。
具体实施方式应充分说明原因、原理、作用和效果，并对区别于现有技术的技术特征以及从属权利要求中的附加技术特征作足够详细的说明。

### Claims

默认且本项目强制设置一项独立权利要求，置于全部从属权利要求之前。独立权利要求必须整体反映发明方案并包含解决技术问题的必要技术特征；其结构应体现前序部分与特征部分，特征部分使用“其特征在于”或同等清晰的连接。
方法权利要求按输入或对象、操作、操作方式或条件、技术输出的逻辑描述；产品权利要求描述组成部件、部件特征以及位置或连接关系。
从属权利要求必须引用在先权利要求，并增加具体技术限定，不得只重复技术效果。
每项权利要求必须以说明书为依据，不得超出公开范围。每项权利要求只能在结尾使用一个中文句号，句号前不得再出现句号。
不得使用“厚、薄、强、弱、高温、高压、很宽范围、约、接近、等、或类似物”等含义不确定用语；不得使用“例如、最好是、尤其是、必要时”等导致保护范围不清的用语。

### Abstract

摘要清楚反映所属技术领域、所要解决的技术问题、解决该问题的技术方案要点和主要用途，其中以技术方案为主；总字数含标点不超过300字。

### Formatting

正式申请文件内容采用宋体、小四字号、1.5倍行距。发明名称居中加黑。技术领域、背景技术、发明内容、附图说明、具体实施方式标题加黑且不带标点。

### Filing workflow

技术文件撰写完成后，Word与PDF应保持同一批准版本，并在交付前逐项核对。请求书、申请人和发明人信息、身份证明、院校登记表、资费批条、老师/代理老师审核等属于具体申请人或院校的行政流程信息，必须由用户提供；Skill不得猜测、补造或把机构内部流程冒充为普遍法律要求。



### Specification

说明书必须对发明作出清楚、完整的说明，使所属技术领域的技术人员能够实现。凡本领域技术人员不能从现有技术直接、唯一得出的必要内容，必须在说明书中描述。
技术问题、技术方案、有益效果必须相互适应。背景技术只写与本发明所解决问题相关的缺陷，不得把本发明本身伪装成现有技术。
发明名称不超过25个字符。技术领域、背景技术、发明内容、附图说明、具体实施方式标题不带标点。
### Claims

默认只设置一项独立权利要求，并置于所有从属权利要求之前。独立权利要求必须从整体反映发明方案并包含解决技术问题的必要技术特征。
方法权利要求应按输入/对象、操作、操作方式或条件、技术输出的逻辑描述步骤；产品权利要求应描述组成部件、部件特征及其位置或连接关系。
每项权利要求必须以说明书为依据，且不得超出说明书公开范围。每项权利要求只能在结尾使用一个句号，句号前不得再出现句号。
不得使用“厚、薄、强、弱、高温、高压、很宽范围、约、接近、等、或类似物”等含义不确定用语；不得使用“例如、最好是、尤其是、必要时”等导致保护范围不清的用语。
### Abstract

摘要清楚反映技术问题、技术方案和主要用途，且技术方案为主；总字数（含标点）不超过300字。
### Formatting

正式申请文件内容采用宋体、小四字号、1.5倍行距。标题居中加黑。
