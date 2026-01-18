import json
import zipfile
import tempfile
from pathlib import Path
import shutil
import re
from typing import Any, Dict


def pbit_to_json(pbit_path: str) -> Dict[str, Any]:
    p = Path(pbit_path)
    if p.suffix.lower() != ".pbit" or not p.is_file():
        raise ValueError(f"Invalid .pbit path: {pbit_path}")

    with tempfile.TemporaryDirectory(prefix="pbit_") as tmp:
        tmp = Path(tmp)

        zip_path = tmp / "file.zip"
        out_dir = tmp / "out"

        shutil.copyfile(p, zip_path)

        with zipfile.ZipFile(zip_path) as z:
            z.extractall(out_dir)

        schema = out_dir / "DataModelSchema"
        if not schema.exists():
            schema = out_dir / "DataModelSchema.txt"
        if not schema.exists():
            raise ValueError("DataModelSchema not found inside PBIT")

        raw_bytes = schema.read_bytes()

        try:
            raw = raw_bytes.decode("utf-16")
        except Exception:
            raw = raw_bytes.decode("utf-16-le", errors="ignore")

        raw = raw.translate(str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"'})).strip()

        return json.loads(raw)


def extract_grading_info(model: Dict[str, Any]) -> Dict[str, Any]:
    model_root = model.get("model") if isinstance(model.get("model"), dict) else model

    grading_info: Dict[str, Any] = {
        "model_name": model.get("name") or model_root.get("name") or "Unknown",
        "compatibility_level": model.get("compatibilityLevel") or model_root.get("compatibilityLevel"),
        "tables": [],
        "measures": [],
        "relationships": [],
        "hierarchies": [],
        "data_source": None,
        "summary": {}
    }

    tables = model_root.get("tables", []) if isinstance(model_root, dict) else []
    rels = model_root.get("relationships", []) if isinstance(model_root, dict) else []

    for table in tables:
        if table.get("isHidden") or table.get("isPrivate"):
            continue

        table_name = table.get("name")

        table_info = {"name": table_name, "columns": [], "measures": []}

        for col in table.get("columns", []) or []:
            if col.get("isHidden"):
                continue
            table_info["columns"].append({
                "name": col.get("name"),
                "data_type": col.get("dataType"),
                "summarize_by": col.get("summarizeBy"),
                "is_calculated": (col.get("type") == "calculated")
            })

        for measure in table.get("measures", []) or []:
            expr_lines = measure.get("expression", [])
            if isinstance(expr_lines, list):
                expr = "\n".join(line for line in expr_lines if isinstance(line, str) and line.strip())
            else:
                expr = (expr_lines or "").strip() if isinstance(expr_lines, str) else ""

            measure_info = {
                "name": measure.get("name"),
                "expression": expr,
                "table": table_name
            }

            table_info["measures"].append(measure_info)
            grading_info["measures"].append(measure_info)

        for partition in table.get("partitions", []) or []:
            source = partition.get("source") or {}
            if source.get("type") == "m":
                expr = source.get("expression", [])
                m_code = " ".join(expr) if isinstance(expr, list) else (expr if isinstance(expr, str) else "")
                match = re.search(r'File\.Contents\("([^"]+)"\)', m_code)
                if match and grading_info["data_source"] is None:
                    grading_info["data_source"] = {"type": "File", "path": match.group(1)}

        grading_info["tables"].append(table_info)

    for rel in rels:
        to_table = rel.get("toTable") or ""
        if "LocalDateTable" in to_table:
            continue
        grading_info["relationships"].append({
            "from": f"{rel.get('fromTable')}[{rel.get('fromColumn')}]",
            "to": f"{rel.get('toTable')}[{rel.get('toColumn')}]",
            "type": rel.get("joinOnDateBehavior") or "standard"
        })

    for table in tables:
        if table.get("isHidden"):
            continue

        for hierarchy in table.get("hierarchies", []) or []:
            annos = hierarchy.get("annotations", []) or []
            if any((a.get("name") == "TemplateId") for a in annos if isinstance(a, dict)):
                continue
            grading_info["hierarchies"].append({
                "name": hierarchy.get("name"),
                "table": table.get("name"),
                "levels": [lvl.get("name") for lvl in (hierarchy.get("levels", []) or []) if isinstance(lvl, dict)]
            })

    preferred = next((t for t in grading_info["tables"] if t.get("name") == "Sheet1"), None)
    main_table = preferred or (grading_info["tables"][0] if grading_info["tables"] else None)

    if main_table:
        grading_info["summary"] = {
            "main_table": main_table.get("name"),
            "total_columns": len(main_table.get("columns", [])),
            "total_measures": len(grading_info["measures"]),
            "total_relationships": len(grading_info["relationships"]),
            "total_hierarchies": len(grading_info["hierarchies"]),
            "has_time_intelligence": any(
                (isinstance(m.get("expression"), str) and "SAMEPERIODLASTYEAR" in m["expression"])
                or (isinstance(m.get("name"), str) and "YoY" in m["name"])
                for m in grading_info["measures"]
            )
        }

    return grading_info


def generate_grading_report(grading_info: Dict[str, Any]) -> str:
    lines = []

    lines.append(f"Model: {grading_info.get('model_name')}")
    lines.append(f"Compatibility Level: {grading_info.get('compatibility_level')}")
    lines.append("")

    if grading_info.get("data_source"):
        ds = grading_info["data_source"]
        lines.append("Data Source:")
        lines.append(f"  Type: {ds.get('type')}")
        lines.append(f"  Path: {ds.get('path')}")
        lines.append("")

    lines.append("Tables:")
    for table in grading_info.get("tables", []):
        lines.append(f"  - {table.get('name')}")

        lines.append("    Columns:")
        for col in table.get("columns", []):
            lines.append(
                f"      • {col.get('name')} "
                f"(type={col.get('data_type')}, "
                f"summarize_by={col.get('summarize_by')}, "
                f"calculated={col.get('is_calculated')})"
            )

        if table.get("measures"):
            lines.append("    Measures:")
            for m in table["measures"]:
                lines.append(f"      • {m.get('name')}")
        else:
            lines.append("    Measures: none")

        lines.append("")

    lines.append("Measures (details):")
    for m in grading_info.get("measures", []):
        lines.append(f"  - {m.get('name')} (table: {m.get('table')})")
        expr = m.get("expression") or ""
        for line in expr.split("\n"):
            lines.append(f"      {line}")
        lines.append("")

    lines.append("Relationships:")
    if grading_info.get("relationships"):
        for r in grading_info["relationships"]:
            lines.append(f"  - {r.get('from')} -> {r.get('to')} ({r.get('type')})")
    else:
        lines.append("  none")
    lines.append("")

    lines.append("Hierarchies:")
    if grading_info.get("hierarchies"):
        for h in grading_info["hierarchies"]:
            levels = h.get("levels") or []
            lines.append(f"  - {h.get('name')} (table: {h.get('table')}) levels: {', '.join(levels)}")
    else:
        lines.append("  none")
    lines.append("")

    lines.append("Summary:")
    for k, v in (grading_info.get("summary") or {}).items():
        lines.append(f"  - {k}: {v}")

    return "\n".join(lines)


def analyze_pbit(pbit_path: str) -> str:
    schema = pbit_to_json(pbit_path)
    grading_info = extract_grading_info(schema)
    report = generate_grading_report(grading_info)
    return report
