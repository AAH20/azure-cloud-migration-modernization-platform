# Azure Cloud Migration and Application Modernization Platform

## VMware to Azure, Azure Migrate, Landing Zones, Kubernetes, Infrastructure as Code and FinOps

**MigrationForge** is an open-source, agent-ready cloud migration assessment and modernization foundation. It converts normalized VMware, on-premises and multi-cloud estate evidence into explainable 7R strategies, dependency-aware migration waves, Azure landing-zone infrastructure, transaction-level validation requirements and a configurable cloud migration business case.

[![Azure cloud migration assessment CI](https://github.com/AAH20/azure-cloud-migration-modernization-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/AAH20/azure-cloud-migration-modernization-platform/actions/workflows/ci.yml)

> **Claim boundary:** this repository uses a synthetic 250-VM estate. It does not access VMware vCenter, Azure Migrate, AWS, GCP or a customer network and performs no production migration.

## Why cloud migration is painful, urgent and frequent

Data-center exits, VMware changes, infrastructure end of life, acquisitions, cloud-cost pressure and AI-readiness programs repeatedly force enterprises to move or modernize workloads. Projects fail when teams migrate virtual machines without proving application dependencies, business transactions, network latency, rollback or unit economics.

MigrationForge turns every dependency and migration failure into reusable planning and validation evidence.

## Executable VMware-to-Azure migration case study

The first vertical slice models:

- 250 VMware virtual machines;
- 40 applications;
- two data centers;
- three business units;
- AKS modernization candidates;
- shared identity, DNS and network dependencies;
- an unsupported legacy estate;
- a latency-sensitive manufacturing system that must remain on premises;
- a configurable migration and FinOps business case.

```bash
PYTHONPATH=src python3 -m migrationforge.cli \
  examples/vmware-to-azure/250-vm-estate.json \
  --output generated/250-vm-assessment

PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The deterministic compiler:

1. Validates application and VM totals.
2. Assigns explainable retain, retire, rehost, replatform, refactor or repurchase strategies.
3. Blocks migrations that violate latency or support constraints.
4. Produces dependency-aware migration waves.
5. Rejects cyclic dependency graphs.
6. Calculates migration investment, dual-running cost, payback and outage exposure.
7. Prohibits autonomous production cutover.
8. Emits a reproducible migration receipt.

## Azure Migrate and dependency mapping

The normalized estate schema is designed for future connectors to Azure Migrate, VMware vCenter, Azure Resource Graph, AWS Config, Google Cloud Asset Inventory, Kubernetes, CMDB and flow-log sources. No live connector is claimed in the current release.

## Application modernization and the 7R strategy

Workloads are evaluated for retain, retire, relocate, rehost, replatform, refactor and repurchase outcomes. Agents may enrich evidence and propose strategies, but deterministic constraints enforce latency, supportability, ownership, recovery and cutover requirements.

## Azure landing zone and hybrid-cloud networking

The compilable subscription-scope Bicep creates a simplified migration foundation:

- dedicated evidence and connectivity resource groups;
- hub virtual network and shared-services subnets;
- Log Analytics migration evidence workspace;
- private Blob Storage migration-receipt container.

This is a demonstration foundation—not a claim of full enterprise-scale Azure Landing Zone implementation. Management groups, identity, ExpressRoute, Azure Firewall, private DNS and policy modules remain roadmap items.

## Kubernetes migration and AKS modernization

Five container-ready customer applications are directed toward Azure Kubernetes Service. The repository does not deploy AKS or claim application compatibility without build, runtime, data, performance and transaction evidence.

## Dependency-aware migration wave planning

The graph compiler places the landing zone before identity, DNS and connectivity; shared services before ERP and customer portals; and business transaction workloads after their dependencies. Cycles block the plan instead of producing a dangerous cutover order.

## Cloud cost optimization and FinOps

The configurable scenario models:

- `$180,000` current monthly operating cost;
- `$130,000` target monthly cost;
- `$600,000` one-time migration investment;
- 45 days of dual running;
- 12-month simple payback;
- `$150,000` modeled reduction in cutover outage exposure.

These are scenario inputs—not Azure prices or guaranteed savings. A production business case must include licensing, circuits, egress, support, labor, modernization, decommissioning, risk and time value of money.

## Infrastructure as Code to Compliance as Code

Architecture intent maps to Bicep resources, deterministic cutover policy, transaction evidence, rollback gates and receipt hashes. Compliance supports delivery rather than replacing it.

## Repository map

```text
src/migrationforge/                  7R and dependency-wave compiler
examples/vmware-to-azure/            250-VM synthetic estate
contracts/                           normalized estate schema
infra/azure/                         subscription-scope Azure Bicep
policy/                              cutover gates
generated/                           assessment and receipts
docs/                                search evidence and validation design
tests/                               behavioral guarantees
```

See the [search and ATS evidence map](docs/search-and-ats-evidence.md) and [transaction-level migration validation](docs/transaction-validation.md).

## Roadmap

- Azure Migrate and VMware vCenter importers
- Azure Resource Graph, AWS and GCP inventory adapters
- Network-flow dependency discovery
- Terraform and OpenTofu target generation
- Enterprise Azure Landing Zone modules
- ExpressRoute, Virtual WAN and overlapping-IP planner
- AKS application-modernization assessment
- Synthetic transaction replay and OpenTelemetry comparison
- Azure Site Recovery and rollback evidence
- Managed migration-wave portal
- Post-migration FinOps and continuous modernization

## Work with A2Z SOC

Planning a data-center exit, VMware migration or Azure modernization? **[Request a Cloud Migration Readiness and Business-Case Assessment](https://a2zsoc.com)** covering dependencies, Azure landing zones, hybrid networking, Kubernetes, FinOps, security, compliance and cutover validation.
