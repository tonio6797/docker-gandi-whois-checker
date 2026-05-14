#!/usr/bin/env sh
set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Starting gandi-whois-checker..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

UPDATE_SCHEDULE=$(printf '%s' "${UPDATE_SCHEDULE:-0 9 * * *}" | tr -d '"')

echo "    [+] Schedule: ${UPDATE_SCHEDULE}"
echo "    [+] Creating CRON entry..."
echo "${UPDATE_SCHEDULE} python /gandi-whois-checker.py" > /etc/crontabs/root
chmod 600 /etc/crontabs/root

echo "    [+] Running..."
echo ""
exec "$@"
