# Transaction-level migration validation

Infrastructure health is not business acceptance. Each workload must define synthetic transactions, for example:

```text
User login
→ customer lookup
→ pricing API
→ database write
→ payment authorization
→ confirmation event
```

Compare the baseline and target on success rate, p50/p95/p99 latency, identity, DNS, network paths, database behavior, event delivery, recovery objectives and cost per successful transaction. A failed business transaction blocks cutover even when every Azure resource reports healthy.

Production cutover remains human-controlled and requires a tested rollback.
