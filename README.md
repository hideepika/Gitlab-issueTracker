# GitLab Monitoring Stack (Docker)

This repository contains a complete Docker-based monitoring stack for GitLab, including:

- **GitLab CE** (Community Edition)
- **Prometheus** (for metrics collection)
- **Grafana** (for visualization)
- **GitLab CI Pipelines Exporter** by mvisonneau
- **Custom GitLab Issues Exporter** (Python-based)
- **GitLab Runner**

## 🚀 Getting Started

1. Clone the repository

2. Replace `__REPLACE_ME__` in `docker-compose.yml` and `your_token_here` in `gitlab_issues_exporter.py` with your GitLab personal access token.

3. Run the stack

```bash
docker-compose up -d --build
```

4. Access services:
- GitLab: http://localhost
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- CI Exporter: http://localhost:8080/metrics
- Issues Exporter: http://localhost:9200/metrics