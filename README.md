# Overmind Python

[![Overmind Intelligence Check](https://github.com/NEUS-DEVELOPMENT/overmind-python/actions/workflows/test.yml/badge.svg)](https://github.com/NEUS-DEVELOPMENT/overmind-python/actions/workflows/test.yml)

Central Command & Control for NEUS Sentinels.

---

## Overview

**Overmind** is the centralized command and control (C&C) system for orchestrating the NEUS Sentinel security agents.
It is responsible for:
- Managing and monitoring all Sentinel agents on the network.
- Sending remote commands and policy updates to Sentinel instances.
- Collecting alerts and aggregated security data from all agents.
- Activating and deactivating advanced defense mechanisms across the network.

---

## Features

- Centralized management of distributed Sentinel agents (written in Go).
- RESTful API for easy integration and remote operations.
- Automated security posture adjustments for the entire network.
- Python-based, modular, and extendable architecture.

---

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/NEUS-DEVELOPMENT/overmind-python.git
   cd overmind-python
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run tests**
   ```bash
   pytest
   ```

---

## Project Structure

- `overmind/` — Main Overmind service code and modules.
- `tests/` — Unit and integration tests.
- `.github/workflows/test.yml` — Automated CI for code validation on push.

---

## License

This project is licensed under the MIT License.

---

## Contributors

- NEUS-DEVELOPMENT organization and contributors.

---

> For questions, issues, or contributing guidelines, please open an issue or contact the maintainers.
