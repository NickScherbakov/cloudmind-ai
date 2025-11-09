# Plugin Architecture (Draft)

CloudMind AI aims to support a rich ecosystem of plugins extending providers, metrics, optimization strategies, policies, and integrations.

## 1. Goals
- Easy third‑party extensibility
- Clear lifecycle (load → validate → register → execute → unload)
- Isolation and safety: no arbitrary code execution without guardrails
- Versioning & compatibility metadata
- Discoverability (future Marketplace index)

## 2. Plugin Types
| Type | Purpose |
|------|---------|
| Provider Adapter | Adds a new cloud/on-prem provider implementation |
| Metrics Collector | Ingests additional metrics sources (e.g., Prometheus) |
| Cost Source | Normalizes cost data from external billing APIs |
| Optimizer | Provides custom recommendation logic / ML models |
| Policy Module | Adds rule evaluation or enforcement logic |
| Action Executor | Implements resource actions beyond basics (e.g., snapshot) |
| Notification Channel | Sends alerts (Slack, Teams, Email) |

## 3. Directory & Packaging
Proposed structure:
```
plugins/
  my_optimizer/
    plugin.yaml
    __init__.py
    optimizer.py
  prometheus_metrics/
    plugin.yaml
    collector.py
```

## 4. Manifest (plugin.yaml)
Example:
```yaml
name: prometheus-metrics
version: 0.1.0
entrypoint: collector:PrometheusCollector
plugin_type: metrics_collector
requires:
  cloudmind_core: ">=0.1.0"
permissions:
  network: ["prometheus.local:9090"]
config_schema:
  endpoint: {type: string, required: true}
  auth_token: {type: string, required: false}
```

## 5. Python Interface (Draft)
```python
class CloudMindPlugin(Protocol):
    def load(self, config: dict) -> None: ...
    def validate(self) -> bool: ...
    def capabilities(self) -> dict: ...
    def shutdown(self) -> None: ...
```
Specialized mixins (e.g., `MetricsCollectorPlugin`, `OptimizerPlugin`) refine methods.

## 6. Registration Flow
1. Scan `plugins/` or configured external paths
2. Parse `plugin.yaml`
3. Resolve entrypoint (module:Class)
4. Instantiate plugin class
5. Validate (schema, compatibility)
6. Register in plugin registry with capability map
7. Expose via API (`/plugins`, `/plugins/{name}`)

## 7. Security & Safety
- Allowlist network endpoints
- Restrict file system access (future sandboxing)
- Digital signatures for Marketplace submissions (future)
- Explicit version compatibility constraints

## 8. Observability
Each plugin should emit structured logs with prefix `[plugin:<name>]` and expose metrics:
- Load time
- Errors count
- Actions executed

## 9. Testing Guidelines
- Unit: manifest parsing, validation, capability reporting
- Integration: end‑to‑end invocation using mock provider or metrics source

## 10. Example Optimizer Plugin Skeleton
```python
# plugins/my_optimizer/optimizer.py
from cloudmind.ai.interfaces import OptimizerPluginBase
from cloudmind.core.models import CloudResource, OptimizationRecommendation

class CostAwareDownsizer(OptimizerPluginBase):
    def load(self, config: dict) -> None:
        self.threshold = config.get("cpu_threshold", 25)

    def analyze(self, resource: CloudResource, metrics: dict) -> list[OptimizationRecommendation]:
        recs = []
        cpu = metrics.get("cpu_usage")
        if cpu is not None and cpu < self.threshold:
            recs.append(OptimizationRecommendation(
                resource_id=resource.id,
                resource_name=resource.name,
                provider=resource.provider,
                action="downsize",
                reason=f"CPU {cpu}% < {self.threshold}%",
                estimated_savings=42.0,
                confidence=0.8,
            ))
        return recs
```

## 11. Future Roadmap
- Dynamic enable/disable via API
- Plugin sandbox (subprocess / WASI / microVM)
- Signed distribution + Marketplace registry
- Dependency graph visualization
- Plugin health checks & auto-restart

## 12. Open Questions
- How strict should permission model be at early stage?
- Do we enforce semantic version ranges or pin exact versions?
- Should optimizer plugins chain or compete (arbitration strategy)?

---
Draft — feedback welcome via RFC (`docs/rfc/`).
