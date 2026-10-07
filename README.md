# SEC EDGAR Full-Text Search API: Filings Scraper (No Key)

Full-text search across all SEC EDGAR filings: 10-K annual reports, 10-Q quarterly reports, 8-K current reports, and 200+ other form types. Search by keyword and filter by form type, date, and company. Returns filing URL, company, date, and matched excerpt.

**Run it on Apify:** [apify.com/themineworks/sec-edgar-fulltext-search](https://apify.com/themineworks/sec-edgar-fulltext-search)
**Docs, FAQ and pricing:** [themineworks.com/actors/sec-edgar-fulltext-search](https://themineworks.com/actors/sec-edgar-fulltext-search/)

**Price:** From $0.60 per 1,000 filings on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Full-text search across all SEC EDGAR filings
* 10-K, 10-Q, 8-K and 200+ form types
* Filter by company, form type, and date range
* Returns filing URL, company name, and excerpt
* Empty results are never charged

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/sec-edgar-fulltext-search").call(run_input={
    "query": "\"climate risk\"",
    "formTypes": [
        "10-K"
    ],
    "dateFrom": "2024-01-01",
    "dateTo": "2024-12-31"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/sec-edgar-fulltext-search').call({
    "query": "\"climate risk\"",
    "formTypes": [
        "10-K"
    ],
    "dateFrom": "2024-01-01",
    "dateTo": "2024-12-31"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~sec-edgar-fulltext-search/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "\"climate risk\"", "formTypes": ["10-K"], "dateFrom": "2024-01-01", "dateTo": "2024-12-31"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 sec_edgar_full_text_search_api.py --token YOUR_APIFY_TOKEN --query ""climate risk"" --form-types "10-K" --date-from "2024-01-01" --date-to "2024-12-31"
node sec_edgar_full_text_search_api.mjs --token YOUR_APIFY_TOKEN --query ""climate risk"" --form-types "10-K" --date-from "2024-01-01" --date-to "2024-12-31"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `query` (required) | string |  | Word or exact phrase (use quotes for an exact phrase, for example "climate risk") |
| `formTypes` | array |  | Filter to specific form types (for example 10-K, 10-Q, 8-K, S-1) |
| `dateFrom` | string |  | Only filings filed on or after this date (YYYY-MM-DD) |
| `dateTo` | string |  | Only filings filed on or before this date (YYYY-MM-DD), for example 2024-12-31 |
| `maxResults` | integer | `200` | Maximum number of filing hits to return (newest first) |
| `contactEmail` | string | `"contact@example.com"` | SEC fair-access requires a contact email in the User-Agent |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `company` | string | Primary company name from the filing |
| `all_companies` | array | All company display names associated with this filing |
| `ciks` | array | List of CIK numbers for the associated companies |
| `form` | string | SEC form type (for example 10-K, 10-Q, 8-K) |
| `file_date` | string | Date the filing was submitted (YYYY-MM-DD) |
| `period_ending` | string | Period of report end date (YYYY-MM-DD) |
| `accession_number` | string | Unique SEC accession number |
| `file_type` | string | MIME type or file extension of the document |
| `file_description` | string | Human-readable description of the filing document |
| `items` | array | 8-K item codes reported |
| `sic` | string | Standard Industrial Classification code |
| `biz_location` | string | Business location of the filing entity |
| `biz_state` | string | US state of the business location |
| `inc_state` | string | State of incorporation |
| `filing_url` | string | Direct URL to the filing document |
| `scraped_at` | string | ISO timestamp when this record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/sec-edgar-fulltext-search
```

## FAQ

### How is this different from the SEC EDGAR Filings scraper?

The Filings scraper fetches all filings for a specific company or CIK by form type. The Full-Text Search scraper searches the text content of all filings across all companies by keyword. Use Full-Text for cross-company research; use Filings for a single company.

### What is EDGAR EFTS?

EDGAR Full-Text Search (EFTS) is the SEC's own full-text search endpoint at efts.sec.gov. It indexes the body text of all filings. This scraper wraps EFTS with pagination, date filtering, and structured output.

### Can I search for specific risk factors or contract terms?

Yes. Full-text search finds any keyword within the filing body. Searches like "supply chain disruption", "material weakness", or "change of control" return every filing that contains those terms.

### What fields does each result include?

Filing URL, CIK (company ID), company name, form type, filing date, period of report, and the matched text excerpt from the filing body.

### Does this cover international company filings?

It covers all foreign private issuers (FPIs) that file with the SEC, which includes most major foreign companies listed on US exchanges. They typically file 20-F (annual) and 6-K (current report) instead of 10-K and 8-K.

### How much does the SEC EDGAR Full-Text Search API cost?

From $0.60 per 1,000 filings on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [B2B Leads Finder](https://themineworks.com/actors/b2b-leads-finder/): Business emails and LinkedIn profiles for target companies
* [LinkedIn Company Scraper](https://themineworks.com/actors/linkedin-company-details/): Company size, industry, website, and followers without login
* [Zillow Rental Listings Scraper](https://themineworks.com/actors/zillow-rental-listings/): Scrape Zillow for-rent listings by city or zip. $1 per 1,000 results

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
