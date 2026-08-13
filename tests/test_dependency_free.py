"""계약 4 — heysenlyt_ai_port는 의존성 0 (표준 라이브러리만). AST 수준 강제."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import heysenlyt_ai_port


def test_ports_package_is_dependency_free():
    allowed = set(sys.stdlib_module_names) | {"heysenlyt_ai_port"}
    pkg = Path(heysenlyt_ai_port.__file__).parent
    for py in pkg.rglob("*.py"):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                roots = [(node.module or "").split(".")[0]] if node.level == 0 else []
            else:
                continue
            for r in roots:
                assert r in allowed, f"{py.name}: 외부 의존 import '{r}' — 의존성 0 위반"
