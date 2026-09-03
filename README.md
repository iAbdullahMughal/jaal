# jaal

A small, open collection of Indicators of Compromise (IOCs) — IP addresses,
domains, hashes and other artifacts that I observed in traffic and wanted to
share openly with anyone who finds them useful.

If you're a blue-teamer, analyst, or just curious, take what's here and block,
hunt, or cross-check your own logs.

## What's inside

- `iocs/` — one JSON file per indicator, plain and readable
- `feeds/` — simple aggregated lists you can pull into a firewall or SIEM
- `scripts/` — a tiny verify helper

## IOCs

Each file in `iocs/` looks like this:

```json
{
  "type": "ipv4-addr",
  "value": "45.153.34.235",
  "first_seen": "2026-09-02",
  "last_seen": "2026-09-03",
  "category": "network-scan",
  "notes": "Repeated SSH connection attempts."
}
```

Fields:

- `type` — what kind of thing it is (`ipv4-addr`, `domain-name`, `file`…)
- `value` — the actual indicator
- `first_seen` / `last_seen` — approximate first/last observation dates
- `category` — rough grouping (e.g. `network-scan`, `credential-stuffing`)
- `notes` — plain-English context, if any

Every file is plain JSON. No wrappers, no nested specifications. Open it and it's obvious.

## Feeds

`feeds/ipv4.json` is a flat array of the IP addresses from `iocs/`, ready to be
consumed by scripts or SIEMs. A new feed is added when there's enough IOCs of a
type to justify it.

## Verify

Run the sanity check on any file to confirm it's well-formed JSON and uses the
expected fields:

```bash
python3 scripts/verify.py iocs/45.153.34.235.json
```

## Contribute

Found something interesting? Open an issue or PR. Keep it factual: an indicator,
what you observed it doing, and how confident you are in it. No vendor fluff.

## License

MIT — see [LICENSE](LICENSE). The IOCs are facts I observed; use your own
judgement before acting on anyone else's observations, and test before you block.