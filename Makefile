run: build
	python benchmark.py

.PHONY: build
build: venv
	venv/bin/pip install hyperscan pyahocorasick flashtext rust_fst
	cd pyrustac && cargo build --release && cp -f target/release/libpyrustac.so ../pyrustac.so

venv:
	python3.8 -m venv venv
