# Output Contract

## Full package

A full-draft job must produce:

- `权利要求书.docx`;
- `说明书.docx`;
- `说明书摘要.docx`;
- `摘要附图.docx`;
- `完整审阅稿.docx`;
- `结构化草稿.json`;
- `权利要求检查.txt`;
- `草稿验证报告.txt`;
- SVG and PNG files for every generated patent figure.

The structured draft is the source of truth. DOCX files are rendered outputs.

## Required traceability

- Every material claim feature maps to at least one source ID.
- Every source-supported core equation has a recorded disposition.
- Every formal term uses the terminology ledger's canonical Chinese form.
- Every numbered claim step maps to one main-flowchart node and one embodiment
  explanation.
- Every methodology figure is source-supported or explicitly identified as a
  redrawing of supported operations.

## Formal-document rules

- Use Chinese for claims, specification, abstract, and figure labels.
- Do not place source IDs, support labels, drafting notes, or quality scores in
  formal claims.
- Render formal equations as editable Office Math.
- Use a concrete final method output; do not use “技术结果”“处理结果” or
  “最终结果”.
- Keep the abstract concise and free of promotional or unsupported promises.

## Quality thresholds

Score each dimension from 1 to 5 and record one sentence of evidence:

- evidence support: at least 4;
- claim architecture: at least 4;
- terminology and dependency consistency: at least 4;
- enablement detail: at least 3;
- technical-effect reasoning: at least 3;
- formula coverage: at least 4 when core formulas exist;
- figure alignment: at least 4 when figures are required.

Any validation `ERROR`, an unmapped material claim feature, or a missing core
formula forces the status `incomplete draft`.

## Delivery note

State that the package requires inventor confirmation and qualified Chinese
patent-professional review. Do not describe it as filing-ready merely because
the automated checks pass.

## Strict Formal Contract

- 发明名称不超过25个字符。
- 正文采用宋体、小四号（12pt）、1.5倍行距。
- 标题居中加黑；技术领域、背景技术、发明内容、附图说明、具体实施方式标题加黑且不带标点。
- 默认且本项目强制要求一项独立权利要求，写在全部从属权利要求之前。
- 每项权利要求只能在末尾出现一个中文句号，不得在正文中出现其他中文句号。
- 禁止在权利要求中出现待确认标记、含义不确定的范围词以及例如/最好是/尤其是/必要时等限定不清用语。
- 产品权利要求优先使用结构及结构关系；方法权利要求使用工艺、操作、步骤或流程特征。
- 摘要不超过300个字符（含标点）。
