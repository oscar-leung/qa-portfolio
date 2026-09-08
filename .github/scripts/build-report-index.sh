#!/usr/bin/env bash
# Write site/index.html linking to whichever suite reports exist.
# Inputs: $1 = site directory; env SELENIUM_RESULT, PLAYWRIGHT_RESULT, RUN_URL.
set -euo pipefail

site="${1:-site}"
mkdir -p "$site"
stamp="$(date -u +'%Y-%m-%d %H:%M UTC')"

badge() {  # badge <result>
  case "$1" in
    success) printf '<span class="ok">passing</span>' ;;
    failure) printf '<span class="bad">failing</span>' ;;
    *)       printf '<span class="meh">%s</span>' "$1" ;;
  esac
}

sel_link="site missing"
[ -f "$site/selenium/report.html" ] && sel_link='<a href="selenium/report.html">open report</a>'
pw_link="site missing"
[ -f "$site/playwright/index.html" ] && pw_link='<a href="playwright/index.html">open report</a>'

cat >"$site/index.html" <<HTML
<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>QA Portfolio nightly reports</title>
<style>
  :root { color-scheme: light dark; font-family: system-ui, sans-serif; }
  body { max-width: 720px; margin: 3rem auto; padding: 0 1rem; line-height: 1.5; }
  h1 { font-size: 1.6rem; margin-bottom: .25rem; }
  .sub { opacity: .7; margin-top: 0; }
  table { width: 100%; border-collapse: collapse; margin-top: 1.5rem; }
  td, th { text-align: left; padding: .6rem .4rem; border-bottom: 1px solid #8884; }
  .ok { color: #1a7f37; font-weight: 600; } .bad { color: #cf222e; font-weight: 600; } .meh { opacity: .7; }
  footer { margin-top: 2rem; font-size: .9rem; opacity: .7; }
</style>
<h1>QA Portfolio: nightly run</h1>
<p class="sub">Oscar Leung &middot; last run $stamp &middot; <a href="$RUN_URL">workflow log</a></p>
<table>
  <tr><th>Suite</th><th>Stack</th><th>Result</th><th>Report</th></tr>
  <tr><td>End-to-end, SauceDemo</td><td>Selenium 4 + pytest</td><td>$(badge "$SELENIUM_RESULT")</td><td>$sel_link</td></tr>
  <tr><td>End-to-end + API, SauceDemo and JSONPlaceholder</td><td>Playwright + TypeScript</td><td>$(badge "$PLAYWRIGHT_RESULT")</td><td>$pw_link</td></tr>
</table>
<footer>Source and case studies: <a href="https://github.com/oscar-leung/qa-portfolio">github.com/oscar-leung/qa-portfolio</a></footer>
HTML
echo "wrote $site/index.html"
