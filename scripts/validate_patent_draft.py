#!/usr/bin/env python3
"""Validate traceability, completeness, and quality gates in a patent draft."""

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


SOURCE_ID = re.compile(r"^[PEFC]\d{3,}$")
PLACEHOLDER = re.compile(r"\[(?:TO CONFIRM|待确认)[^\]]*\]", re.IGNORECASE)
VAGUE_RESULT = re.compile(r"(技术结果|处理结果|最终结果)")
VAGUE_CLAIM_WORDS = re.compile(r"(厚|薄|强|弱|高温|高压|很宽范围|约|接近|等|或类似物|例如|最好是|尤其是|必要时)")
QUALITY_THRESHOLDS = {
    "evidence_support": 4,
    "claim_architecture": 4,
    "terminology_consistency": 4,
    "enablement_detail": 3,
    "technical_effect_reasoning": 3,
}


@dataclass
class Finding:
    level: str
    code: str
    message: str


def add(findings: list[Finding], level: str, code: str, message: str) -> None:
    findings.append(Finding(level, code, message))


def validate(data: dict) -> list[Finding]:
    findings: list[Finding] = []
    required = (
        "title",
        "metadata",
        "source_analysis",
        "source_map",
        "terminology_ledger",
        "formula_inventory",
        "figure_inventory",
        "evidence_ledger",
        "claims",
        "claim_feature_map",
        "figures",
        "specification",
        "abstract",
        "quality_assessment",
    )
    for key in required:
        if key not in data:
            add(findings, "ERROR", "MISSING_KEY", f"缺少顶层字段：{key}。")

    claims = data.get("claims", [])
    numbers = [claim.get("number") for claim in claims]
    if not claims:
        add(findings, "ERROR", "NO_CLAIMS", "完整草稿必须包含权利要求。")
    elif numbers != list(range(1, len(numbers) + 1)):
        add(findings, "ERROR", "CLAIM_SEQUENCE", f"权利要求编号不连续：{numbers}。")
    for claim in claims:
        text = str(claim.get("text", ""))
        if not text.strip():
            add(findings, "ERROR", "EMPTY_CLAIM", f"权利要求{claim.get('number')}为空。")
        if PLACEHOLDER.search(text):
            add(
                findings,
                "ERROR",
                "CLAIM_PLACEHOLDER",
                f"权利要求{claim.get('number')}仍含待确认标记。",
            )

    # Strict Chinese patent gates derived from the project drafting requirements.
    title = str(data.get("title", ""))
    abstract_text = re.sub(r"\s+", "", str(data.get("abstract", "")))
    title_count = len(re.sub(r"\s+", "", title))
    if title_count > 25:
        add(findings, "ERROR", "TITLE_LENGTH", f"发明名称为{title_count}个字符，超过25个字符上限。")
    if not abstract_text:
        add(findings, "ERROR", "EMPTY_ABSTRACT", "说明书摘要为空。")
    elif len(abstract_text) > 300:
        add(findings, "ERROR", "ABSTRACT_LENGTH", f"摘要为{len(abstract_text)}个字符，超过300个字符上限。")

    independent_claims = []
    for claim in claims:
        text = str(claim.get("text", ""))
        number = claim.get("number")
        claim_type = claim.get("claim_type")
        if claim_type == "independent" or (claim_type is None and number == 1):
            independent_claims.append(claim)
        if number == 1 and claim_type not in (None, "independent"):
            add(findings, "ERROR", "CLAIM_1_NOT_INDEPENDENT", "第1项权利要求必须为独立权利要求。")
        if number == 1 and not re.search(r"其特征在于", text):
            add(findings, "ERROR", "CLAIM_1_FEATURE_PART", "独立权利要求必须具有“其特征在于”或等同的特征部分。")
        if "。" in text[:-1]:
            add(findings, "ERROR", "CLAIM_INTERNAL_FULL_STOP", f"权利要求{claim.get('number')}内部含句号；句号只能出现在结尾。")
        if not text.endswith("。"):
            add(findings, "ERROR", "CLAIM_FINAL_FULL_STOP", f"权利要求{claim.get('number')}必须以一个句号结尾。")
        if VAGUE_CLAIM_WORDS.search(text):
            add(findings, "ERROR", "CLAIM_VAGUE_WORD", f"权利要求{claim.get('number')}包含保护范围可能不清的用语。")
        if PLACEHOLDER.search(text):
            add(findings, "ERROR", "CLAIM_PLACEHOLDER", f"权利要求{claim.get('number')}含待确认标记。")
    if len(independent_claims) != 1:
        add(findings, "ERROR", "INDEPENDENT_CLAIM_COUNT", f"独立权利要求数量为{len(independent_claims)}，项目规则要求恰好1项。")
    if independent_claims and independent_claims[0].get("number") != 1:
        add(findings, "ERROR", "INDEPENDENT_CLAIM_ORDER", "独立权利要求必须为第1项并位于从属权利要求之前。")
    for claim in claims[1:]:
        number = claim.get("number")
        text = str(claim.get("text", ""))
        refs = [int(x) for x in re.findall(r"根据权利要求\s*(\d+)\s*所述", text)]
        if not refs:
            add(findings, "ERROR", "DEPENDENT_REFERENCE", f"权利要求{number}未检测到明确的在先权利要求引用。")
        elif any(ref >= int(number) for ref in refs):
            add(findings, "ERROR", "DEPENDENT_REFERENCE_ORDER", f"权利要求{number}引用了自身或后续权利要求。")
        if claim.get("claim_type") == "independent":
            add(findings, "ERROR", "UNEXPECTED_INDEPENDENT", f"第{number}项不允许成为第二项独立权利要求。")

    source_records = data.get("source_map", [])
    source_ids = set()
    for record in source_records:
        source_id = str(record.get("id", ""))
        if not SOURCE_ID.fullmatch(source_id):
            add(findings, "ERROR", "SOURCE_ID", f"无效来源ID：{source_id!r}。")
        if source_id in source_ids:
            add(findings, "ERROR", "DUPLICATE_SOURCE_ID", f"来源ID重复：{source_id}。")
        source_ids.add(source_id)
        if not record.get("locator"):
            add(findings, "WARNING", "SOURCE_LOCATOR", f"{source_id}缺少页码、章节或行号。")

    canonical_terms = set()
    forbidden_aliases = set()
    for item in data.get("terminology_ledger", []):
        canonical = str(item.get("canonical_zh", "")).strip()
        if not canonical:
            add(findings, "ERROR", "CANONICAL_TERM", "术语表存在空的canonical_zh。")
        elif canonical in canonical_terms:
            add(findings, "ERROR", "DUPLICATE_TERM", f"规范术语重复：{canonical}。")
        canonical_terms.add(canonical)
        forbidden_aliases.update(
            str(alias).strip() for alias in item.get("forbidden_aliases", []) if str(alias).strip()
        )

    ledger_ids = set()
    for item in data.get("evidence_ledger", []):
        ledger_id = str(item.get("id", ""))
        if not ledger_id:
            add(findings, "ERROR", "LEDGER_ID", "证据台账条目缺少ID。")
        elif ledger_id in ledger_ids:
            add(findings, "ERROR", "DUPLICATE_LEDGER_ID", f"证据台账ID重复：{ledger_id}。")
        ledger_ids.add(ledger_id)
        status = item.get("support_status")
        if status not in {"explicit", "inherent", "needs-confirmation", "unsupported"}:
            add(findings, "ERROR", "SUPPORT_STATUS", f"{ledger_id}的支持状态无效：{status}。")
        referenced = item.get("source_ids", [])
        if status in {"explicit", "inherent"} and not referenced:
            add(findings, "ERROR", "MISSING_SOURCE_LINK", f"{ledger_id}没有来源ID。")
        for source_id in referenced:
            if source_ids and source_id not in source_ids:
                add(findings, "ERROR", "UNKNOWN_SOURCE_ID", f"{ledger_id}引用未知来源ID：{source_id}。")

    mapped_claims = set()
    for mapping in data.get("claim_feature_map", []):
        claim_number = mapping.get("claim_number")
        mapped_claims.add(claim_number)
        if claim_number not in numbers:
            add(findings, "ERROR", "UNKNOWN_CLAIM", f"特征映射引用不存在的权利要求：{claim_number}。")
        if not str(mapping.get("feature", "")).strip():
            add(findings, "ERROR", "EMPTY_FEATURE", "权利要求特征映射存在空特征。")
        evidence_ids = mapping.get("evidence_ids", [])
        if not evidence_ids:
            add(
                findings,
                "ERROR",
                "UNMAPPED_FEATURE",
                f"权利要求{claim_number}的特征“{mapping.get('feature', '')}”没有证据ID。",
            )
        for evidence_id in evidence_ids:
            if evidence_id not in ledger_ids:
                add(
                    findings,
                    "ERROR",
                    "UNKNOWN_EVIDENCE_ID",
                    f"权利要求{claim_number}引用未知证据ID：{evidence_id}。",
                )
        for evidence_id in evidence_ids:
            ledger_item = next((item for item in data.get("evidence_ledger", []) if item.get("id") == evidence_id), None)
            if ledger_item and ledger_item.get("support_status") not in {"explicit", "inherent"}:
                add(
                    findings,
                    "ERROR",
                    "CLAIM_UNSUPPORTED_STATUS",
                    f"权利要求{claim_number}的特征“{mapping.get('feature', '')}”引用了非正式支持状态证据：{evidence_id}。",
                )
    for number in numbers:
        if number not in mapped_claims:
            add(findings, "ERROR", "CLAIM_NOT_MAPPED", f"权利要求{number}没有特征证据映射。")
    formal_text = "\n".join(str(claim.get("text", "")) for claim in claims)
    formal_text += "\n" + json.dumps(data.get("specification", {}), ensure_ascii=False)
    for alias in sorted(forbidden_aliases):
        if alias in formal_text:
            add(findings, "ERROR", "FORBIDDEN_ALIAS", f"正式文本使用了禁用别名：{alias}。")

    source_analysis = data.get("source_analysis", {})
    spec = data.get("specification", {})
    equations = spec.get("equations", [])
    formula_inventory = data.get("formula_inventory", [])
    for item in formula_inventory:
        source_id = item.get("source_id")
        if source_ids and source_id not in source_ids:
            add(findings, "ERROR", "FORMULA_INVENTORY_SOURCE", f"公式清单引用未知来源ID：{source_id}。")
        if not item.get("disposition"):
            add(findings, "ERROR", "FORMULA_DISPOSITION", f"来源公式{source_id}缺少处理去向。")
    expected_formula_count = source_analysis.get("formula_count_in_source")
    if isinstance(expected_formula_count, int) and expected_formula_count != len(formula_inventory):
        add(
            findings,
            "WARNING",
            "FORMULA_INVENTORY_COUNT",
            f"来源标记{expected_formula_count}个公式，公式清单记录{len(formula_inventory)}个。",
        )
    if "equations" not in spec:
        add(findings, "ERROR", "EQUATIONS_ARRAY", "说明书必须包含equations数组。")
    if source_analysis.get("contains_core_formulas") and not equations:
        add(findings, "ERROR", "MISSING_CORE_EQUATIONS", "来源包含核心公式，但说明书未收录公式。")
    equation_numbers = [equation.get("number") for equation in equations]
    if equation_numbers and equation_numbers != list(range(1, len(equation_numbers) + 1)):
        add(findings, "ERROR", "EQUATION_SEQUENCE", f"公式编号不连续：{equation_numbers}。")
    for equation in equations:
        number = equation.get("number")
        if not equation.get("latex"):
            add(findings, "ERROR", "EQUATION_LATEX", f"公式{number}缺少可转换的LaTeX源。")
        if not equation.get("source_ids"):
            add(findings, "ERROR", "EQUATION_SOURCE", f"公式{number}缺少来源ID。")
        for source_id in equation.get("source_ids", []):
            if source_ids and source_id not in source_ids:
                add(findings, "ERROR", "EQUATION_SOURCE", f"公式{number}引用未知来源ID：{source_id}。")
        if not equation.get("symbols"):
            add(findings, "ERROR", "EQUATION_SYMBOLS", f"公式{number}缺少结构化符号定义。")
        if not equation.get("technical_role"):
            add(findings, "ERROR", "EQUATION_ROLE", f"公式{number}缺少技术作用说明。")

    figures = data.get("figures", [])
    for item in data.get("figure_inventory", []):
        source_id = item.get("source_id")
        if source_ids and source_id not in source_ids:
            add(findings, "ERROR", "FIGURE_INVENTORY_SOURCE", f"附图清单引用未知来源ID：{source_id}。")
        if not item.get("disposition"):
            add(findings, "ERROR", "FIGURE_DISPOSITION", f"来源附图{source_id}缺少处理去向。")
    figure_numbers = [figure.get("number") for figure in figures]
    if not figures:
        add(findings, "ERROR", "NO_FIGURES", "完整草稿必须包含至少一幅专利附图。")
    elif figure_numbers != list(range(1, len(figure_numbers) + 1)):
        add(findings, "ERROR", "FIGURE_SEQUENCE", f"附图编号不连续：{figure_numbers}。")
    abstract_figure = data.get("abstract_figure_number")
    if abstract_figure not in figure_numbers:
        add(findings, "ERROR", "ABSTRACT_FIGURE", "摘要附图编号未指向现有附图。")
    for figure in figures:
        if not figure.get("source_ids"):
            add(findings, "WARNING", "FIGURE_SOURCE", f"图{figure.get('number')}缺少来源ID或重绘依据。")
        for source_id in figure.get("source_ids", []):
            if source_ids and source_id not in source_ids:
                add(
                    findings,
                    "ERROR",
                    "FIGURE_SOURCE",
                    f"图{figure.get('number')}引用未知来源ID：{source_id}。",
                )
        end_nodes = set(str(node.get("id")) for node in figure.get("nodes", []))
        for edge in figure.get("edges", []):
            end_nodes.discard(str(edge.get("from")))
        for node in figure.get("nodes", []):
            if str(node.get("id")) in end_nodes and VAGUE_RESULT.search(str(node.get("label", ""))):
                add(
                    findings,
                    "ERROR",
                    "VAGUE_FINAL_RESULT",
                    f"图{figure.get('number')}末端节点使用了模糊结果名称。",
                )

    # 每一个独立权利要求步骤都必须在主流程图中出现，并与实施方式对应。
    claim1 = next((claim for claim in claims if claim.get("number") == 1), None)
    main_flow = next((fig for fig in figures if fig.get("number") == abstract_figure and fig.get("type") == "flowchart"), None)
    if claim1 and main_flow:
        claim_steps = set(re.findall(r"\bS\d+\b", str(claim1.get("text", ""))))
        figure_steps = {str(node.get("claim_step")) for node in main_flow.get("nodes", []) if node.get("claim_step")}
        missing_steps = sorted(claim_steps - figure_steps)
        if missing_steps:
            add(findings, "ERROR", "FLOWCHART_STEP_COVERAGE", f"主流程图缺少权利要求1步骤：{', '.join(missing_steps)}。")

    for field in ("technical_field", "background", "embodiments", "figure_descriptions"):
        if not spec.get(field):
            add(findings, "ERROR", "SPEC_SECTION", f"说明书缺少或清空了字段：{field}。")
    invention = spec.get("invention_content", {})
    for field in ("problem", "solution", "beneficial_effects"):
        if not invention.get(field):
            add(findings, "ERROR", "INVENTION_CONTENT", f"发明内容缺少：{field}。")

    abstract = re.sub(r"\s+", "", str(data.get("abstract", "")))
    if not abstract:
        add(findings, "ERROR", "EMPTY_ABSTRACT", "说明书摘要为空。")
    elif len(abstract) > 300:
        add(findings, "WARNING", "ABSTRACT_LENGTH", f"摘要约{len(abstract)}字，建议人工核对篇幅。")

    quality = data.get("quality_assessment", {})
    if quality.get("status") not in {"review-draft", "incomplete-draft"}:
        add(
            findings,
            "WARNING",
            "DRAFT_STATUS",
            "quality_assessment.status建议使用review-draft或incomplete-draft。",
        )
    scores = quality.get("scores", {})
    for dimension, threshold in QUALITY_THRESHOLDS.items():
        item = scores.get(dimension)
        if not isinstance(item, dict) or not isinstance(item.get("score"), int):
            add(findings, "ERROR", "QUALITY_SCORE", f"缺少质量评分：{dimension}。")
            continue
        score = item["score"]
        if score < 1 or score > 5:
            add(findings, "ERROR", "QUALITY_RANGE", f"{dimension}评分超出1-5：{score}。")
        elif score < threshold:
            add(
                findings,
                "ERROR",
                "QUALITY_THRESHOLD",
                f"{dimension}评分{score}，低于交付阈值{threshold}。",
            )
        if not str(item.get("evidence", "")).strip():
            add(findings, "WARNING", "QUALITY_EVIDENCE", f"{dimension}评分缺少依据。")

    if source_analysis.get("contains_core_formulas"):
        formula_item = scores.get("formula_coverage", {})
        if formula_item.get("score", 0) < 4:
            add(findings, "ERROR", "FORMULA_SCORE", "存在核心公式时，formula_coverage必须至少为4。")
    if figures:
        figure_item = scores.get("figure_alignment", {})
        if figure_item.get("score", 0) < 4:
            add(findings, "ERROR", "FIGURE_SCORE", "存在附图时，figure_alignment必须至少为4。")

    return findings


def format_report(findings: list[Finding]) -> str:
    if not findings:
        return "PASS: 草稿通过结构、溯源和质量门槛检查。\n"
    lines = [f"{item.level}\t{item.code}\t{item.message}" for item in findings]
    errors = sum(item.level == "ERROR" for item in findings)
    warnings = sum(item.level == "WARNING" for item in findings)
    lines.extend(("", f"汇总: {errors} 个错误, {warnings} 个警告"))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="UTF-8 structured patent draft JSON")
    parser.add_argument("--report", type=Path, help="Write the validation report to a file")
    parser.add_argument("--json", action="store_true", help="Print findings as JSON")
    args = parser.parse_args()

    data = json.loads(args.draft.read_text(encoding="utf-8"))
    findings = validate(data)
    report = format_report(findings)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    if args.json:
        print(json.dumps([item.__dict__ for item in findings], ensure_ascii=False, indent=2))
    else:
        print(report, end="")
    return 1 if any(item.level == "ERROR" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
