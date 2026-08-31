# Production acceptance

MigrationForge is a production-oriented reference control plane, not evidence that a customer workload has been migrated. Production acceptance is environment-specific.

Before use for a real cutover:

- Replace the reference SQLite state volume with a managed PostgreSQL adapter for multi-replica operation and point-in-time recovery.
- Integrate Entra workload identity/OIDC instead of the reference bearer-token boundary.
- Import signed inventory from Azure Migrate, vCenter, CMDB and network-flow sources.
- Establish target landing-zone, network, identity, DNS, backup and disaster-recovery ownership.
- Define business transaction contracts and capture baseline success, latency and reconciliation evidence.
- Exercise canary, rollback, dual-write/CDC and total target-region failure.
- Pin images by digest, generate an SBOM, sign artifacts and enforce admission policy.
- Connect logs, traces and alerts to an owned on-call process.
- Require accountable application, business and change-owner approvals.
- Reconcile forecast savings with billing and decommission evidence after cutover.

The default state machine advances one phase at a time. Missing evidence fails closed, and agents cannot manufacture an approval by changing workflow order.
