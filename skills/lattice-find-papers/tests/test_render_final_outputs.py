import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from render_final_outputs import main


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class RenderFinalOutputsTest(unittest.TestCase):
    def test_renders_compact_report_without_default_long_sections(self):
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td) / "run-test"
            output_root = run_dir / "find_papers_outputs"
            (output_root / "outputs").mkdir(parents=True)
            write_csv(
                output_root / "request_queue" / "full_text_requests.csv",
                ["request_id", "paper_id", "title", "priority", "needed_sections", "local_resolution_status"],
                [{"request_id": "R001", "paper_id": "P001", "title": "Example", "priority": "high", "needed_sections": "Methods", "local_resolution_status": "request_required"}],
            )
            write_csv(
                output_root / "tables" / "full_text_availability.csv",
                ["paper_id", "local_library_checked", "local_full_text_status", "local_supplement_status"],
                [{"paper_id": "P001", "local_library_checked": "true", "local_full_text_status": "not_found", "local_supplement_status": "not_found"}],
            )

            with patch.object(sys, "argv", ["render_final_outputs.py", str(run_dir)]):
                main()

            report = (output_root / "outputs" / "final_report.md").read_text(encoding="utf-8")
            self.assertIn("# Lattice Find Papers Compact Report", report)
            self.assertIn("## 5. 下一步最小动作", report)
            self.assertNotIn("## 4. 变量关系矩阵", report)
            self.assertNotIn("## 5. 实验流程审计", report)
            self.assertNotIn("## 6. 机制对比与冲突", report)


if __name__ == "__main__":
    unittest.main()
