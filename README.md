# Gandi Whois Checker

Domain availability checker using Gandi's API. Sends a notification via [Shoutrrr](https://containrrr.dev/shoutrrr/) when a domain is available.

## Run with Docker

```shell
docker run --name gandi-whois-checker \
           --rm \
           -e GANDI_DOMAIN="mydomain.net" \
           -e GANDI_PAT="your-pat" \
           areg97/gandi-whois-checker:latest
```

Authentication is required. Use either a PAT or an API key.

## Configuration

| Variable          | Default                    | Description                                                                                                                                     |
| ----------------- |----------------------------| ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `GANDI_URL`       | `https://api.gandi.net/v5/` | Base URL of the Gandi API.                                                                                                                      |
| `GANDI_DOMAIN`    | —                          | Domain name(s) to check. Comma-separated for multiple domains (e.g. `example.com,example.net`). **Required.**                                   |
| `GANDI_PAT`       | —                          | Personal Access Token for your [Gandi.net account](https://docs.gandi.net/en/managing_an_organization/organizations/personal_access_token.html). **Required** if `GANDI_API_KEY` is not set. |
| `GANDI_API_KEY`   | —                          | Gandi API key. **Required** if `GANDI_PAT` is not set. ⚠️ Deprecated by Gandi but still functional.                                            |
| `SHOUTRRR_URL`    | —                          | [Shoutrrr](https://containrrr.dev/shoutrrr/) notification URL(s). Comma-separated for multiple destinations (e.g. `telegram://...,slack://...`). |
| `UPDATE_SCHEDULE` | `0 9 * * *`                | Cron-style schedule for availability checks (default: every day at 9am).                                                                        |

> If both `GANDI_PAT` and `GANDI_API_KEY` are set, `GANDI_PAT` takes precedence.