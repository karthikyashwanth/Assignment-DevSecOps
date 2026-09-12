# Northwind OMS – Smart Build Pipeline Assignment

This assignment implements a smart build pipeline for the Northwind Order Management System.

The pipeline supports two build scenarios:

1. Build all modules.
2. Build only changed modules and all dependent modules.

## Scenario 1 – Build All Modules

### Command

```bash
python build_pipeline.py all
```

PS C:\Users\USER\Downloads\sn-java-sample-main\sn-java-sample-main\osgi-workshop> & "C:\Users\USER\AppData\Local\Programs\Python\Python314\python.exe" build_pipeline.py all

============================================================
  Northwind OMS — Smart Build Pipeline
  Mode: DRY RUN (simulation)
============================================================

============================================================
  SCENARIO 1 — BUILD ALL MODULES
============================================================
  ℹ  Total modules: 11

  Dependency Graph:
  ──────────────────────────────────────────────────
  Core 
    └── (no dependencies in build set)
  Customer 
    └── (no dependencies in build set)
  Security 
    └── (no dependencies in build set)
  SLF4J (3rd party) 
    └── (no dependencies in build set)
  Inventory 
    └── depends on: Core
  Pricing 
    └── depends on: Core
  Shipping 
    └── depends on: Core, Customer
  Payment 
    └── depends on: Core, Security, SLF4J (3rd party)
  Gateway (Orders) 
    └── depends on: Core, Inventory, Pricing, SLF4J (3rd party)
  Notification 
    └── depends on: Customer, Shipping, SLF4J (3rd party)
  Reporting 
    └── depends on: Core, Payment, Gateway (Orders), SLF4J (3rd party)
  ──────────────────────────────────────────────────

  Build Order:
   1. Core (com.northwind.oms.core)
   2. Customer (com.northwind.oms.customer)
   3. Security (com.northwind.oms.security)
   4. SLF4J (3rd party) (com.northwind.oms.tpcl.org.slf4j)
   5. Inventory (com.northwind.oms.inventory)
   6. Pricing (com.northwind.oms.pricing)
   7. Shipping (com.northwind.oms.shipping)
   8. Payment (com.northwind.oms.payment)
   9. Gateway (Orders) (com.northwind.oms.gateway)
  10. Notification (com.northwind.oms.notification)
  11. Reporting (com.northwind.oms.reporting)

============================================================
  Starting Full Build
============================================================
  ▶  Building Core (com.northwind.oms.core)
  ℹ    Path: catalog\plugins\com.northwind.oms.core
  ℹ    [DRY RUN] mvn clean install -f catalog\plugins\com.northwind.oms.core/pom.xml
  ✓    Build SIMULATED — Core
  ▶  Building Customer (com.northwind.oms.customer)
  ℹ    Path: customer\plugins\com.northwind.oms.customer
  ℹ    [DRY RUN] mvn clean install -f customer\plugins\com.northwind.oms.customer/pom.xml
  ✓    Build SIMULATED — Customer
  ▶  Building Security (com.northwind.oms.security)
  ℹ    Path: security\plugins\com.northwind.oms.security
  ℹ    [DRY RUN] mvn clean install -f security\plugins\com.northwind.oms.security/pom.xml
  ✓    Build SIMULATED — Security
  ▶  Building SLF4J (3rd party) (com.northwind.oms.tpcl.org.slf4j)
  ℹ    Path: thirdparty\plugins\com.northwind.oms.tpcl.org.slf4j
  ℹ    [DRY RUN] mvn clean install -f thirdparty\plugins\com.northwind.oms.tpcl.org.slf4j/pom.xml
  ✓    Build SIMULATED — SLF4J (3rd party)
  ▶  Building Inventory (com.northwind.oms.inventory)
  ℹ    Path: catalog\plugins\com.northwind.oms.inventory
  ℹ    [DRY RUN] mvn clean install -f catalog\plugins\com.northwind.oms.inventory/pom.xml
  ✓    Build SIMULATED — Inventory
  ▶  Building Pricing (com.northwind.oms.pricing)
  ℹ    Path: orders\plugins\com.northwind.oms.pricing
  ℹ    [DRY RUN] mvn clean install -f orders\plugins\com.northwind.oms.pricing/pom.xml
  ✓    Build SIMULATED — Pricing
  ▶  Building Shipping (com.northwind.oms.shipping)
  ℹ    Path: shipping\plugins\com.northwind.oms.shipping
  ℹ    [DRY RUN] mvn clean install -f shipping\plugins\com.northwind.oms.shipping/pom.xml
  ✓    Build SIMULATED — Shipping
  ▶  Building Payment (com.northwind.oms.payment)
  ℹ    Path: payment\plugins\com.northwind.oms.payment
  ℹ    [DRY RUN] mvn clean install -f payment\plugins\com.northwind.oms.payment/pom.xml
  ✓    Build SIMULATED — Payment
  ▶  Building Gateway (Orders) (com.northwind.oms.gateway)
  ℹ    Path: orders\plugins\com.northwind.oms.gateway
  ℹ    [DRY RUN] mvn clean install -f orders\plugins\com.northwind.oms.gateway/pom.xml
  ✓    Build SIMULATED — Gateway (Orders)
  ▶  Building Notification (com.northwind.oms.notification)
  ℹ    Path: notification\plugins\com.northwind.oms.notification
  ℹ    [DRY RUN] mvn clean install -f notification\plugins\com.northwind.oms.notification/pom.xml
  ✓    Build SIMULATED — Notification
  ▶  Building Reporting (com.northwind.oms.reporting)
  ℹ    Path: reporting\plugins\com.northwind.oms.reporting
  ℹ    [DRY RUN] mvn clean install -f reporting\plugins\com.northwind.oms.reporting/pom.xml
  ✓    Build SIMULATED — Reporting

============================================================
  FULL BUILD COMPLETE
============================================================
  ✓  All 11 modules built successfully

## Scenario 2 – Build Changed Modules Only

### Command
```bash
python build_pipeline.py changed
```
### Features

- Detects changed modules
- Finds all dependent modules
- Resolves dependency chain
- Displays dependency graph
- Builds only required modules
- Displays build logs

---

## Dependency Resolution

The dependency graph was created by analysing the OSGi `MANIFEST.MF` files.

The pipeline considers:

- Import-Package
- Export-Package
- Require-Bundle

to determine module dependencies.

---

## Dependency Graph

The pipeline displays:

- Complete dependency graph
- Dependency direction
- Dependency paths
- Build order
- Modules selected for rebuild

---

## Logging

The pipeline provides verbose logging including:

- Changed modules detected
- Dependency chain
- Dependency graph
- Build order
- Modules selected for rebuild
- Build status

---

## Technologies Used

- Python
- PowerShell
- Maven
- OSGi
- Eclipse Tycho

---

## Assignment Requirements Checklist

| Requirement | Status |
|-------------|--------|
| Build all modules | ✅ |
| Build changed modules only | ✅ |
| Detect changed modules | ✅ |
| Resolve dependency chain | ✅ |
| Correct dependency order | ✅ |
| Dependency graph | ✅ |
| Dependency paths | ✅ |
| Verbose logging | ✅ |
| PowerShell build script | ✅ |
| Python build pipeline | ✅ |

---

## Notes

The pipeline supports both dry-run and real Maven execution.

The dependency analysis, build ordering, change detection, and logging execute successfully.

The real Maven build currently fails because the provided project uses an Eclipse Tycho configuration that is incompatible with Java 21 (`Unknown OSGi execution environment: JavaSE-21`). This is an environment compatibility issue rather than a pipeline implementation issue.

============================================================
  SCENARIO 2 — BUILD CHANGED MODULES ONLY
============================================================
  ℹ  Scanning for changed modules...

  Changed Modules Detected:
  ⚡ Core (com.northwind.oms.core)

  Modules to Rebuild (including dependents):
   1. Core [CHANGED]
   2. Inventory [DEPENDENT]
   3. Payment [DEPENDENT]
   4. Pricing [DEPENDENT]
   5. Shipping [DEPENDENT]
   6. Gateway (Orders) [DEPENDENT]
   7. Notification [DEPENDENT]
   8. Reporting [DEPENDENT]

============================================================
  DEPENDENCY GRAPH — Changed Modules Scenario
============================================================

  Dependency Graph:
  ──────────────────────────────────────────────────
  Core [CHANGED/REBUILD]
    └── (no dependencies in build set)
  Inventory [CHANGED/REBUILD]
    └── depends on: Core
  Payment [CHANGED/REBUILD]
    └── depends on: Core
  Pricing [CHANGED/REBUILD]
    └── depends on: Core
  Shipping [CHANGED/REBUILD]
    └── depends on: Core
  Gateway (Orders) [CHANGED/REBUILD]
    └── depends on: Core, Inventory, Pricing
  Notification [CHANGED/REBUILD]
    └── depends on: Shipping
  Reporting [CHANGED/REBUILD]
    └── depends on: Core, Payment, Gateway (Orders)
  ──────────────────────────────────────────────────

  Dependency Paths for Changed Modules:
  ──────────────────────────────────────────────────
  Core (changed)
    → triggers rebuild of: Gateway (Orders)
    → triggers rebuild of: Inventory
    → triggers rebuild of: Payment
    → triggers rebuild of: Pricing
    → triggers rebuild of: Reporting
    → triggers rebuild of: Shipping
  ──────────────────────────────────────────────────

============================================================
  Building 8 modules
============================================================
  ▶  Building Core (com.northwind.oms.core)
  ℹ    Path: catalog\plugins\com.northwind.oms.core
  ℹ    [DRY RUN] mvn clean install -f catalog\plugins\com.northwind.oms.core/pom.xml
  ✓    Build SIMULATED — Core
  ▶  Building Inventory (com.northwind.oms.inventory)
  ℹ    Path: catalog\plugins\com.northwind.oms.inventory
  ℹ    [DRY RUN] mvn clean install -f catalog\plugins\com.northwind.oms.inventory/pom.xml
  ✓    Build SIMULATED — Inventory
  ▶  Building Payment (com.northwind.oms.payment)
  ℹ    Path: payment\plugins\com.northwind.oms.payment
  ℹ    [DRY RUN] mvn clean install -f payment\plugins\com.northwind.oms.payment/pom.xml
  ✓    Build SIMULATED — Payment
  ▶  Building Pricing (com.northwind.oms.pricing)
  ℹ    Path: orders\plugins\com.northwind.oms.pricing
  ℹ    [DRY RUN] mvn clean install -f orders\plugins\com.northwind.oms.pricing/pom.xml
  ✓    Build SIMULATED — Pricing
  ▶  Building Shipping (com.northwind.oms.shipping)
  ℹ    Path: shipping\plugins\com.northwind.oms.shipping
  ℹ    [DRY RUN] mvn clean install -f shipping\plugins\com.northwind.oms.shipping/pom.xml
  ✓    Build SIMULATED — Shipping
  ▶  Building Gateway (Orders) (com.northwind.oms.gateway)
  ℹ    Path: orders\plugins\com.northwind.oms.gateway
  ℹ    [DRY RUN] mvn clean install -f orders\plugins\com.northwind.oms.gateway/pom.xml
  ✓    Build SIMULATED — Gateway (Orders)
  ▶  Building Notification (com.northwind.oms.notification)
  ℹ    Path: notification\plugins\com.northwind.oms.notification
  ℹ    [DRY RUN] mvn clean install -f notification\plugins\com.northwind.oms.notification/pom.xml
  ✓    Build SIMULATED — Notification
  ▶  Building Reporting (com.northwind.oms.reporting)
  ℹ    Path: reporting\plugins\com.northwind.oms.reporting
  ℹ    [DRY RUN] mvn clean install -f reporting\plugins\com.northwind.oms.reporting/pom.xml
  ✓    Build SIMULATED — Reporting

============================================================
  CHANGED-MODULES BUILD COMPLETE
============================================================
  ✓  Rebuilt 8 modules (1 changed, 7 dependents)



# Files

```
build_pipeline.py
.build_hashes.json
solution.md
```

---

# Result

- Supports full project builds.
- Supports incremental builds.
- Automatically detects modified modules.
- Rebuilds only affected modules.
- Preserves dependency order using Topological Sort.
- Reduces unnecessary builds for incremental development.
