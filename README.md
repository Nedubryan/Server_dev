# 🔍 Multithreaded File Search Server (Secure TCP)

This is a **high-performance**, multithreaded TCP server for **exact string matches** in large text files. It supports SSL encryption, payload size limits, dynamic file reloading, and performance benchmarking.

---

## 🚀 Features

* ✅ **Exact line matching** (no partial matches)
* 🔐 **SSL/TLS support** (optional)
* 🔄 **Hot file reloading** (via config)
* 🧠 **Multiple search algorithms**: `line-by-line`, `mmap`, `set`, `regex`, etc.
* 📦 **Modular design** with full test coverage
* 📈 **Benchmark tools** for stress & speed testing
* ✅ **PEP8 compliant** and battle-tested with `pytest` + `coverage`

---

## 📁 Directory Structure

```
search_server_dev_final/
├── server/                # Core server logic
│   ├── server.py
│   ├── connection_handler.py
│   ├── file_search.py
│   ├── logger.py
│   ├── cert_utils.py
│   ├── config.py
│   └── config_loader.py
├── tests/                 # Unit & integration tests
│   ├── test_*.py
│   ├── test_utils.py
│   └── test_data/
├── benchmark.py           # Search algorithm benchmarks
├── stress_test.py         # Threaded stress test
├── client.py              # Sample TCP client
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuration

Use a `config.json` file in the root or set a test path via `TEST_CONFIG_PATH`:

```json
{
  "linuxpath": "tests/test_data/test_data.txt",
  "REREAD_ON_QUERY": false,
  "SSL_ENABLED": false,
  "port": 12345
}
```

* `linuxpath`: File to search
* `REREAD_ON_QUERY`: Reload file on every query
* `SSL_ENABLED`: Enable TLS
* `port`: TCP port to bind

---

## 🧪 Testing

```bash
# Run all tests with coverage
coverage run -m pytest
coverage report -m

# Alternatively:
pytest -v --cov=server --cov-report=term-missing

# Check PEP8 style
flake8 . --max-line-length=99
```

---

## 🔐 SSL Mode

Generate a self-signed certificate for local testing:

```bash
python -m server.cert_utils
```

Or use the built-in generator during testing (`test_utils.py`).

---

## 📊 Benchmarks

Compare search strategies by running:

```bash
python benchmark.py
```

This measures time across algorithms like:

* `line-by-line`
* `mmap`
* `set lookup`
* `regex`
* `grep`

---

## 🧵 Stress Test

```bash
python stress_test.py
```

Simulates 100+ simultaneous clients querying the server with varied payloads.

---

## 🔧 Usage Example

```bash
# Start the server
python -m server.server

# In another terminal
python client.py <host> <port> <search_string>
```

---

## ✅ Requirements

* Python 3.8+
* Works on **Linux**, **Windows**, and **macOS**
* Required packages: `cryptography`, `pytest`, `flake8`, `coverage`

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## 👨‍🔬 Author & Maintainer

**Chinedu** — Software Engineer & Data Platform Architect
📧 Feel free to reach out for feedback, collaborations, or contributions.

---

## 📦 Status

✅ Final candidate — all core tests passing
🧼 PEP8 compliant & benchmarked
🔐 Secure-by-default, production-ready base

---
