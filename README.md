# 🏨 Tripadvisor API: hotel and restaurant reviews as clean JSON

Actor: [johnvc/tripadvisor-api](https://apify.com/johnvc/tripadvisor-api?fpr=9n7kx3) · [Input schema](https://apify.com/johnvc/tripadvisor-api/input-schema?fpr=9n7kx3)

This repo shows two ways to use the [Tripadvisor API](https://apify.com/johnvc/tripadvisor-api?fpr=9n7kx3) on Apify: a Python quick start and MCP installs for five AI clients. Search hotels, restaurants and attractions by keyword, then pull the full review stream for any place you found. If you were about to scrape Tripadvisor with a headless browser, this is the same data with none of the maintenance.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

### Text walkthrough

The tripadvisor api takes a search_mode of search or reviews. Search mode takes a query like hotels in paris and returns places with title, placeType, rating, reviewCount, location and a placeId. Reviews mode takes that placeId and returns the full review stream: snippet, rating, reviewDate, tripDate, tripType, votes and authorName, ten per request with automatic paging. A common workflow is exporting every review of a property to CSV for sentiment analysis, which the export_reviews recipe in this repo does end to end. There is no place-detail mode, so addresses and phone numbers are out of scope by design.

## Quick Start

You need Python 3.11+ and a free Apify API key: sign up at [apify.com](https://apify.com?fpr=9n7kx3), then copy your token from Console Settings.

```bash
git clone https://github.com/johnisanerd/Apify-Tripadvisor-API.git
cd Apify-Tripadvisor-API
uv sync
cp .env.example .env   # then paste your APIFY_API_TOKEN
uv run python tripadvisor-api-example.py
```

Run a specific recipe:

```bash
uv run python tripadvisor-api-example.py --example export_reviews
```

## Why use this API

- Search hotels, restaurants and attractions by keyword, filtered by place type
- Full review text with trip type, trip date, language and helpful votes
- Reviewer context: display name and how many contributions the author has made
- Ten regional domains for language and currency control
- Automatic paging to your max_results; pay only per row returned

## Recipes

The example script ships ready-made recipes that mirror this API's main use cases:

- **Export a place's reviews** (`--example export_reviews`): Pulls the review stream for one placeId, ready for CSV or sentiment work.
- **Build a fresh hotel dataset** (`--example hotel_dataset`): Searches a city and keeps only ACCOMMODATION rows, a current alternative to stale public datasets.

**Schedule tip:** save any of these inputs as a task in the [Apify Console](https://apify.com/johnvc/tripadvisor-api?fpr=9n7kx3) and attach a schedule. A daily or weekly run turns a one-off pull into a pipeline with zero manual work.

## Usage Examples

Basic input:

```json
{
  "search_mode": "search",
  "query": "hotels in paris",
  "max_results": 5
}
```

Advanced input:

```json
{
  "search_mode": "reviews",
  "place_id": "143336",
  "max_results": 50,
  "tripadvisor_domain": "www.tripadvisor.co.uk"
}
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `search_mode` | string | yes | `"search"` | What to fetch. |
| `query` | string | no | none | Required when search mode is 'search'. |
| `place_id` | string | no | none | Required when search mode is 'reviews'. |
| `place_types` | array | no | none | Optional. |
| `max_results` | integer | no | `100` | How many rows to return before stopping. |
| `tripadvisor_domain` | string | no | `"www.tripadvisor.com"` | Optional. |

## Output Format

One row from a real run:

```json
{
  "resultType": "review",
  "placeId": "143336",
  "totalReviews": 39843,
  "title": "Paris in July",
  "snippet": "Loved my 5 days. Close and convenient to everything.",
  "rating": 5,
  "reviewDate": "2026-08-03",
  "tripDate": "2026-07-31",
  "tripType": "FAMILY",
  "votes": 0,
  "authorName": "Michele W",
  "authorContributions": 1
}
```

## n8n integration

Available as an n8n community node, **[n8n-nodes-tripadvisor-api](https://www.npmjs.com/package/n8n-nodes-tripadvisor-api)**. In n8n: Settings, Community Nodes, install `n8n-nodes-tripadvisor-api`, then use it in any workflow (it also works as an AI Agent tool).

## People also search for

### Is this a Tripadvisor scraper?

You can use it wherever you would use a Tripadvisor scraper, but you call it like an API: JSON in, JSON out, with paging and billing handled for you. No browser automation to maintain.

### How do I get Tripadvisor reviews from Python?

Run the quick start in this repo: uv sync, set your token, and call the export_reviews recipe with a placeId. Search mode hands you the placeId for any place.

### Can I get a hotel's address or phone number?

No. The place-detail source is unreliable upstream, so this API deliberately ships search and reviews only rather than a mode that fails.

### Can I run it on a schedule?

Yes. Save your input as a task in the Apify Console and attach a schedule; a weekly review pull keeps a sentiment dashboard fresh without manual runs.

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Tripadvisor API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings -> Connectors** (or **Settings -> Developer -> Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/tripadvisor-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Tripadvisor API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/tripadvisor-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/tripadvisor-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Tripadvisor API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings -> Connectors -> Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/tripadvisor-api`.
3. In any chat, open **+ -> Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/tripadvisor-api`, using OAuth when prompted.
5. Ask Claude to run the Tripadvisor API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/tripadvisor-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/tripadvisor-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor -> Settings -> MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Tripadvisor API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/tripadvisor-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp


---

Made with care by [johnvc on Apify](https://apify.com/johnvc?fpr=9n7kx3). This example repo is part of [Alpha OSINT](https://www.alphaosint.com), toolset of financial and operations data sources and APIs.

Last Updated: 2026.08.10
