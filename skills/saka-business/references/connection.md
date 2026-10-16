# Customer connection contract

Checked against https://saka.run/docs/auth and https://saka.run/api/openapi.json on 2026-10-15.

| Server | Resource | Purpose |
|---|---|---|
| saka | https://saka.run/api/mcp | Free quotes, account balance, explicitly approved prepaid purchases |
| saka-library | https://saka.run/api/library/mcp | Read existing purchased records only |

Both use Streamable HTTP and OAuth. Use the host's OAuth flow; tokens are audience-specific and cannot be exchanged between these resources. No API-key issuing endpoint exists. OAuth consent is not a spending budget. The owner may disable connected-agent purchasing access. Never use the internal/legacy /mcp business dataset endpoint for this customer plugin.

Purchasing tool names: saka_quote, saka_balance, saka_purchase. Library tool names: saka_list_purchases, saka_read_purchase. Inspect actual schemas before execution. A free quote example is:

```json
{"kind":"basic","limit":5,"result_grain":"company","filters":{"country":["US"],"category":["Plumbing"]}}
```

Use library-only configuration if no new purchasing is desired. Installing skills alone does not require Saka access. For a no-account integration test run the bundled sandbox-check.py; its records are fictional and cannot be purchased. The HTTP 401 boundary proves authentication is required, not that authenticated actions work.
