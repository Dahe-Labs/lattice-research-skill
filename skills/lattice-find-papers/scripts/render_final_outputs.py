#!/usr/bin/env python3
import argparse
from pathlib import Path
from lattice_common import find_papers_root, read_csv, safe_run_dir

def md_table(rows, columns, empty="暂无。"):
    if not rows:
        return empty + "\n"
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join(["---"] * len(columns)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(c, "")).replace("|", "/") for c in columns) + " |")
    return "\n".join(lines) + "\n"

def top_requests(rows, limit=10):
    priority_rank = {"high": 0, "medium": 1, "low": 2}
    return sorted(rows, key=lambda r: (priority_rank.get(str(r.get("priority", "")).lower(), 9), r.get("request_id", "")))[:limit]

def main():
    p = argparse.ArgumentParser(description="Render concise final_report.md and final_summary.txt from run tables.")
    p.add_argument("run_dir")
    args = p.parse_args()
    run_dir = safe_run_dir(args.run_dir)
    output_root = find_papers_root(run_dir)
    requests = read_csv(output_root / "request_queue" / "full_text_requests.csv")
    availability = read_csv(output_root / "tables" / "full_text_availability.csv")
    local_checked = sum(1 for row in availability if str(row.get("local_library_checked", "")).lower() in {"true", "1", "yes"})
    local_resolved = sum(1 for row in availability if row.get("local_full_text_status") in {"pdf_found", "html_found", "raw_data_found", "code_found"} or row.get("local_supplement_status") == "supplement_found")
    report = ["# Lattice Find Papers Compact Report", "", "## 1. 结论", ""]
    if requests:
        report += ["- 本轮已完成在线全文检查，并按配置尝试 Zotero / 本地 PDF / 本地补充材料检查。", f"- 本地检查覆盖 {local_checked} 篇候选，解决或部分解决 {local_resolved} 篇全文/补充材料缺失。", f"- 仍有 {len(requests)} 篇需要用户下载、上传或人工确认。", "- 当前不能基于摘要完成被全文缺失阻断的数据轮、实验轮、机制轮或可比性轮强结论。", "- 补充 Request 文献目录中的 PDF、全文或补充材料后，可以从断点继续。"]
    else:
        report += ["- 本轮已完成在线全文检查，并按配置尝试 Zotero / 本地 PDF / 本地补充材料检查。", f"- 本地检查覆盖 {local_checked} 篇候选，解决或部分解决 {local_resolved} 篇全文/补充材料缺失。", "- 当前未生成 Request 文献目录。", "- 仍需按证据等级逐项确认事实主张。"]
    request_preview = top_requests(requests)
    request_note = (
        f"仅显示最高优先级的 {len(request_preview)} 项；完整队列见 "
        "request_PDF/doi_list.md 和 find_papers_outputs/request_queue/。"
        if requests else "暂无。"
    )
    report += [
        "",
        "## 2. 证据边界",
        "",
        "| 项目 | 状态 |",
        "|---|---|",
        "| 在线全文检查 | 已完成或按当前可用来源记录 |",
        f"| 本地全文检查 | 已尝试 {local_checked} 篇；本地解决或部分解决 {local_resolved} 篇 |",
        f"| 全文可得性 | {'存在缺全文阻断' if requests else '未发现 Request 阻断'} |",
        f"| 当前可做判断 | {'只能对已获 L2+ 证据的文献做有限判断' if availability else '需要先补充候选文献状态'} |",
        f"| 需要用户补充 | {'PDF / 图表 / 补充材料 / 人工确认' if requests else '暂无 Request 阻断'} |",
        "",
        "## 3. Request 文献目录",
        "",
        request_note,
        "",
        md_table(request_preview, ["request_id", "paper_id", "title", "priority", "needed_sections", "local_resolution_status"]),
        "## 4. 不应夸大的结论",
        "",
        "- 不能把摘要、metadata 或 indexed text 写成全文级数据/实验/方法结论。",
        "- 不能把“统一框架 / 数据归一化 / 多因素耦合”直接写成研究空白。",
        "- 不能把相关关系写成因果或机制裁决。",
        "",
        "## 5. 下一步最小动作",
        "",
        "- 优先补充 high priority 的全文、图表或补充材料。",
        "- 补充后运行 resume 流程，从断点继续。",
        "- 需要完整变量矩阵或实验审计时，再显式请求 full evidence mapping。",
        "",
    ]
    text = "\n".join(report)
    (output_root / "outputs" / "final_report.md").write_text(text, encoding="utf-8")
    (output_root / "outputs" / "final_summary.txt").write_text("缺全文时已生成 Request；补充文件后可断点续跑。\n" if requests else "当前无 Request 阻断。\n", encoding="utf-8")
    print(output_root / "outputs" / "final_report.md")

if __name__ == "__main__":
    main()
