#!/usr/bin/env bash

set -euo pipefail

site_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$site_root"

ruby scripts/sync_shared_content.rb --check

export JEKYLL_ENV="${JEKYLL_ENV:-production}"

personal_config=("$site_root/_config.yml")
if ! command -v convert >/dev/null 2>&1; then
  echo "ImageMagick is unavailable; skipping responsive-image generation locally."
  personal_config+=("$site_root/scripts/_config.no-imagemagick.yml")
fi

config_value="$(IFS=,; echo "${personal_config[*]}")"
bundle exec jekyll build --config "$config_value" --destination "$site_root/_site"
(
  cd "$site_root/lab"
  BUNDLE_GEMFILE="$site_root/Gemfile" bundle exec jekyll build --destination "$site_root/_site/lab"
)

echo "Built taohu.me and taohu.me/lab into $site_root/_site"
