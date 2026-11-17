#!/usr/bin/env bash

set -euo pipefail

site_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
port="${1:-4000}"

cd "$site_root"
scripts/build_all.sh

echo "Previewing both sites at http://127.0.0.1:${port}/"
exec ruby -run -e httpd "$site_root/_site" -p "$port"
