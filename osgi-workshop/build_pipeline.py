#!/usr/bin/env python3
"""
Smart Build Pipeline for Northwind Order Management System
Supports:
  Scenario 1: Build all modules in correct dependency order
  Scenario 2: Build only changed modules + their dependents
"""

import os
import sys
import subprocess
import hashlib
import json
from pathlib import Path
from collections import defaultdict, deque

# ─────────────────────────────────────────────
# MODULE DEFINITIONS — from MANIFEST.MF analysis
# ─────────────────────────────────────────────

MODULES = {
    "com.northwind.oms.core": {
        "path": "catalog/plugins/com.northwind.oms.core",
        "depends_on": [],
        "label": "Core"
    },
    "com.northwind.oms.security": {
        "path": "security/plugins/com.northwind.oms.security",
        "depends_on": [],
        "label": "Security"
    },
    "com.northwind.oms.customer": {
        "path": "customer/plugins/com.northwind.oms.customer",
        "depends_on": [],
        "label": "Customer"
    },
    "com.northwind.oms.tpcl.org.slf4j": {
        "path": "thirdparty/plugins/com.northwind.oms.tpcl.org.slf4j",
        "depends_on": [],
        "label": "SLF4J (3rd party)"
    },
    "com.northwind.oms.inventory": {
        "path": "catalog/plugins/com.northwind.oms.inventory",
        "depends_on": ["com.northwind.oms.core"],
        "label": "Inventory"
    },
    "com.northwind.oms.pricing": {
        "path": "orders/plugins/com.northwind.oms.pricing",
        "depends_on": ["com.northwind.oms.core"],
        "label": "Pricing"
    },
    "com.northwind.oms.shipping": {
        "path": "shipping/plugins/com.northwind.oms.shipping",
        "depends_on": ["com.northwind.oms.core", "com.northwind.oms.customer"],
        "label": "Shipping"
    },
    "com.northwind.oms.payment": {
        "path": "payment/plugins/com.northwind.oms.payment",
        "depends_on": ["com.northwind.oms.core", "com.northwind.oms.security", "com.northwind.oms.tpcl.org.slf4j"],
        "label": "Payment"
    },
    "com.northwind.oms.gateway": {
        "path": "orders/plugins/com.northwind.oms.gateway",
        "depends_on": ["com.northwind.oms.core", "com.northwind.oms.inventory",
                       "com.northwind.oms.pricing", "com.northwind.oms.tpcl.org.slf4j"],
        "label": "Gateway (Orders)"
    },
    "com.northwind.oms.notification": {
        "path": "notification/plugins/com.northwind.oms.notification",
        "depends_on": ["com.northwind.oms.customer", "com.northwind.oms.shipping", "com.northwind.oms.tpcl.org.slf4j"],
        "label": "Notification"
    },
    "com.northwind.oms.reporting": {
        "path": "reporting/plugins/com.northwind.oms.reporting",
        "depends_on": ["com.northwind.oms.core", "com.northwind.oms.payment",
                       "com.northwind.oms.gateway", "com.northwind.oms.tpcl.org.slf4j"],
        "label": "Reporting"
    },
}

HASH_FILE = ".build_hashes.json"

# ─────────────────────────────────────────────
# COLOURS
# ─────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RED    = "\033[91m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def header(text):
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  {text}{RESET}")
    print(f"{BOLD}{CYAN}{'='*60}{RESET}")

def info(text):    print(f"{BLUE}  ℹ  {text}{RESET}")
def success(text): print(f"{GREEN}  ✓  {text}{RESET}")
def warn(text):    print(f"{YELLOW}  ⚠  {text}{RESET}")
def error(text):   print(f"{RED}  ✗  {text}{RESET}")
def step(text):    print(f"{BOLD}  ▶  {text}{RESET}")

# ─────────────────────────────────────────────
# DEPENDENCY GRAPH UTILITIES
# ─────────────────────────────────────────────

def build_reverse_graph():
    """Who depends on each module (reverse edges)."""
    rev = defaultdict(set)
    for mod, meta in MODULES.items():
        for dep in meta["depends_on"]:
            rev[dep].add(mod)
    return rev

def topological_sort(module_set):
    """Return modules in build order (dependencies first)."""
    in_degree = {m: 0 for m in module_set}
    graph = defaultdict(set)
    for mod in module_set:
        for dep in MODULES[mod]["depends_on"]:
            if dep in module_set:
                graph[dep].add(mod)
                in_degree[mod] += 1
    queue = deque(sorted([m for m in module_set if in_degree[m] == 0]))
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in sorted(graph[node]):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order

def get_all_dependents(changed, reverse_graph):
    """BFS to find all modules that need rebuilding."""
    visited = set(changed)
    queue = deque(changed)
    while queue:
        mod = queue.popleft()
        for dependent in reverse_graph.get(mod, []):
            if dependent not in visited:
                visited.add(dependent)
                queue.append(dependent)
    return visited

# ─────────────────────────────────────────────
# FILE HASHING FOR CHANGE DETECTION
# ─────────────────────────────────────────────

def hash_module(base_path, module_path):
    """Hash all source files in a module."""
    full_path = Path(base_path) / module_path
    hasher = hashlib.md5()
    if not full_path.exists():
        return "NOT_FOUND"
    for f in sorted(full_path.rglob("*.java")) + sorted(full_path.rglob("MANIFEST.MF")) + sorted(full_path.rglob("pom.xml")):
        hasher.update(f.read_bytes())
    return hasher.hexdigest()

def load_hashes(base_path):
    hf = Path(base_path) / HASH_FILE
    if hf.exists():
        return json.loads(hf.read_text())
    return {}

def save_hashes(base_path, hashes):
    hf = Path(base_path) / HASH_FILE
    hf.write_text(json.dumps(hashes, indent=2))

def detect_changed_modules(base_path):
    old = load_hashes(base_path)
    current = {}
    changed = []
    for mod, meta in MODULES.items():
        h = hash_module(base_path, meta["path"])
        current[mod] = h
        if old.get(mod) != h:
            changed.append(mod)
    return changed, current

# ─────────────────────────────────────────────
# BUILD SIMULATION
# ─────────────────────────────────────────────

def build_module(mod, base_path, dry_run=True):
    meta = MODULES[mod]
    path = Path(base_path) / meta["path"]
    step(f"Building {BOLD}{meta['label']}{RESET} ({mod})")
    info(f"  Path: {path}")
    if dry_run:
        info(f"  [DRY RUN] mvn clean install -f {path}/pom.xml")
        success(f"  Build SIMULATED — {meta['label']}")
    else:
        result = subprocess.run(
            ["cmd", "/c", "mvn", "clean", "install", "-f", str(path / "pom.xml")],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            success(f"  Build SUCCESS — {meta['label']}")
        else:
            error(f"  Build FAILED — {meta['label']}")
            print("\n========== MAVEN STDOUT ==========")
            print(result.stdout)
            print("\n========== MAVEN STDERR ==========")
            sys.exit(1)

# ─────────────────────────────────────────────
# DEPENDENCY GRAPH DISPLAY
# ─────────────────────────────────────────────

def print_dependency_graph(modules_to_show, highlight=None):
    highlight = highlight or set()
    print(f"\n{BOLD}  Dependency Graph:{RESET}")
    print(f"  {'─'*50}")

    order = topological_sort(set(modules_to_show))
    for mod in order:
        meta = MODULES[mod]
        deps = [d for d in meta["depends_on"] if d in modules_to_show]
        tag = f"{YELLOW}[CHANGED/REBUILD]{RESET}" if mod in highlight else ""
        label = f"{BOLD}{meta['label']}{RESET}"
        if deps:
            dep_labels = ", ".join(MODULES[d]["label"] for d in deps)
            print(f"  {label} {tag}")
            print(f"    └── depends on: {dep_labels}")
        else:
            print(f"  {label} {tag}")
            print(f"    └── (no dependencies in build set)")
    print(f"  {'─'*50}")

def print_dependency_paths(changed_mods, to_rebuild, reverse_graph):
    print(f"\n{BOLD}  Dependency Paths for Changed Modules:{RESET}")
    print(f"  {'─'*50}")
    for mod in sorted(changed_mods):
        meta = MODULES[mod]
        dependents = reverse_graph.get(mod, set()) & to_rebuild
        print(f"  {YELLOW}{meta['label']}{RESET} (changed)")
        if dependents:
            for dep in sorted(dependents):
                print(f"    → triggers rebuild of: {MODULES[dep]['label']}")
        else:
            print(f"    → no downstream dependents")
    print(f"  {'─'*50}")

# ─────────────────────────────────────────────
# SCENARIO 1 — BUILD ALL
# ─────────────────────────────────────────────

def scenario_build_all(base_path, dry_run=True):
    header("SCENARIO 1 — BUILD ALL MODULES")
    all_mods = list(MODULES.keys())
    order = topological_sort(set(all_mods))

    info(f"Total modules: {len(order)}")
    print_dependency_graph(all_mods)

    print(f"\n{BOLD}  Build Order:{RESET}")
    for i, mod in enumerate(order, 1):
        print(f"  {i:2}. {MODULES[mod]['label']} ({mod})")

    header("Starting Full Build")
    for mod in order:
        build_module(mod, base_path, dry_run)

    # Save hashes after successful build
    _, current = detect_changed_modules(base_path)
    save_hashes(base_path, current)

    header("FULL BUILD COMPLETE")
    success(f"All {len(order)} modules built successfully")

# ─────────────────────────────────────────────
# SCENARIO 2 — BUILD CHANGED ONLY
# ─────────────────────────────────────────────

def scenario_build_changed(base_path, dry_run=True):
    header("SCENARIO 2 — BUILD CHANGED MODULES ONLY")

    info("Scanning for changed modules...")
    changed, current_hashes = detect_changed_modules(base_path)

    if not changed:
        success("No changes detected. Nothing to build.")
        return

    reverse_graph = build_reverse_graph()
    to_rebuild = get_all_dependents(changed, reverse_graph)
    order = topological_sort(to_rebuild)

    # ── Summary ──
    print(f"\n{BOLD}  Changed Modules Detected:{RESET}")
    for mod in sorted(changed):
        print(f"  {YELLOW}⚡ {MODULES[mod]['label']}{RESET} ({mod})")

    print(f"\n{BOLD}  Modules to Rebuild (including dependents):{RESET}")
    for i, mod in enumerate(order, 1):
        tag = f"{YELLOW}[CHANGED]{RESET}" if mod in changed else f"{CYAN}[DEPENDENT]{RESET}"
        print(f"  {i:2}. {MODULES[mod]['label']} {tag}")

    # ── Dependency Graph ──
    header("DEPENDENCY GRAPH — Changed Modules Scenario")
    print_dependency_graph(list(to_rebuild), highlight=to_rebuild)
    print_dependency_paths(changed, to_rebuild, reverse_graph)

    # ── Build ──
    header(f"Building {len(order)} modules")
    for mod in order:
        build_module(mod, base_path, dry_run)

    # Save updated hashes
    save_hashes(base_path, current_hashes)

    header("CHANGED-MODULES BUILD COMPLETE")
    success(f"Rebuilt {len(order)} modules ({len(changed)} changed, {len(to_rebuild)-len(changed)} dependents)")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Smart Build Pipeline — Northwind OMS")
    parser.add_argument("scenario", choices=["all", "changed"],
                        help="'all' = build everything, 'changed' = build changed + dependents")
    parser.add_argument("--base", default=".", help="Path to osgi-workshop directory")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Simulate build without running Maven (default: True)")
    parser.add_argument("--real", action="store_true",
                        help="Actually run Maven builds")
    args = parser.parse_args()

    dry_run = not args.real
    base = args.base

    print(f"\n{BOLD}{GREEN}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  Northwind OMS — Smart Build Pipeline{RESET}")
    print(f"{BOLD}{GREEN}  Mode: {'DRY RUN (simulation)' if dry_run else 'REAL BUILD'}{RESET}")
    print(f"{BOLD}{GREEN}{'='*60}{RESET}")

    if args.scenario == "all":
        scenario_build_all(base, dry_run)
    else:
        scenario_build_changed(base, dry_run)

if __name__ == "__main__":
    main()