# Agentic VMware-to-Azure migration assessment for 250 VMs and 40 applications

**Readiness:** `blocked`
**Evidence:** `synthetic-estate`
**Receipt:** `099f9e64abb80a39987052870b7213cadee25f9f6962c56ab1ffa932710f23d8`

## Cloud migration and modernization portfolio

| Workload group | Applications | VMs | 7R strategy | Target | Status |
|---|---:|---:|---|---|---|
| customer-portals | 5 | 32 | replatform | Azure Kubernetes Service | eligible |
| order-processing | 4 | 38 | refactor | Azure application landing zone | eligible |
| erp-estate | 8 | 64 | rehost | Azure virtual machines | eligible |
| shared-services | 10 | 58 | rehost | Azure virtual machines | eligible |
| manufacturing-control | 1 | 16 | retain | on-premises with hybrid connectivity | blocked |
| legacy-archive | 2 | 8 | retire | decommission with evidence retention | blocked |
| collaboration-tools | 2 | 10 | repurchase | SaaS integration landing zone | eligible |
| regional-apps | 8 | 24 | rehost | Azure virtual machines | eligible |

## Dependency-aware migration waves

- Wave 0: landing-zone
- Wave 1: identity-dns, network-connectivity
- Wave 2: shared-services
- Wave 3: customer-portals, erp-estate
- Wave 4: order-processing

## Cloud migration business case

- `current_monthly_cost_usd`: `180000`
- `target_monthly_cost_usd`: `130000`
- `modeled_monthly_difference_usd`: `50000`
- `migration_investment_usd`: `600000`
- `dual_run_cost_usd`: `270000.0`
- `simple_payback_months`: `12.0`
- `modeled_outage_exposure_reduction_usd`: `150000`

## Claim boundary

- No live VMware, Azure, AWS, GCP or Kubernetes inventory was accessed
- No workload was migrated and no production cutover was performed
- Costs and outage values are configurable synthetic inputs
- Recommendations require customer evidence and accountable-owner approval
