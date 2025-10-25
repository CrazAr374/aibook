#!/usr/bin/env bash
set -euo pipefail

# Render build helper: install rustup into local writable directories and install Python deps
# Usage (Render Build Command): bash render/render_build.sh

echo "[render_build] creating local cargo/rustup dirs"
export CARGO_HOME="$PWD/.cargo"
export RUSTUP_HOME="$PWD/.rustup"
mkdir -p "$CARGO_HOME" "$RUSTUP_HOME"
export PATH="$CARGO_HOME/bin:$PATH"

echo "[render_build] installing rustup (non-interactive)"
curl https://sh.rustup.rs -sSf | sh -s -- -y --no-modify-path
source "$CARGO_HOME/env" || true
rustup default stable

echo "[render_build] upgrading pip and installing python deps"
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "[render_build] done"
