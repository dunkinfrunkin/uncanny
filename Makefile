.PHONY: install test bench bench-json bench-fast lint clean

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

bench:
	uncanny bench

bench-json:
	uncanny bench --json

bench-fast:
	uncanny bench --analyzers compression

clean:
	rm -rf .pytest_cache __pycache__ src/uncanny/__pycache__ .venv dist build *.egg-info
