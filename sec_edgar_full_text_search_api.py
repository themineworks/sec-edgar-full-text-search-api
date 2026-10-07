#!/usr/bin/env python3
"""Search 10-K, 10-Q, 8-K, and any SEC filing by keyword. Python, Node.js and cURL clients for the SEC EDGAR Full-Text Search API on Apify, pay per result.

Command-line client for the themineworks/sec-edgar-fulltext-search actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/sec-edgar-fulltext-search/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/sec-edgar-fulltext-search"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--query", help="Word or exact phrase (use quotes for an exact phrase, for example 'climate risk')")
    ap.add_argument("--form-types", help="Comma-separated. Filter to specific form types (for example 10-K, 10-Q, 8-K, S-1)")
    ap.add_argument("--date-from", help="Only filings filed on or after this date (YYYY-MM-DD)")
    ap.add_argument("--date-to", help="Only filings filed on or before this date (YYYY-MM-DD), for example 2024-12-31")
    ap.add_argument("--max-results", type=int, help="Maximum number of filing hits to return (newest first)")
    ap.add_argument("--contact-email", help="SEC fair-access requires a contact email in the User-Agent")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.query is not None: run_input["query"] = a.query
    if a.form_types: run_input["formTypes"] = [s.strip() for s in a.form_types.split(",") if s.strip()]
    if a.date_from is not None: run_input["dateFrom"] = a.date_from
    if a.date_to is not None: run_input["dateTo"] = a.date_to
    if a.max_results is not None: run_input["maxResults"] = a.max_results
    if a.contact_email is not None: run_input["contactEmail"] = a.contact_email

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
