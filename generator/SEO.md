# SEO for SystemForge (organic)

Source of truth: `generator/seo-keywords.json`. The n8n workflows read it from GitHub on every run, so changing that file changes the next posts. No n8n edit needed.

## Where the keywords come from
- Google, YouTube and Bing autocomplete (US, English), pulled 2026-10-22.
- Pinterest and Etsy autocomplete block bots, so check them by hand: type the main keyword in the search bar and note the suggestions.
- Words with "free" are skipped on purpose: we sell, and "free" brings the wrong buyer.

## Main keyword per product
| Product | Main keyword | Also use |
|---|---|---|
| Freelancer Client OS | freelancer Notion template | Notion CRM template, client tracker Notion, Notion freelancer dashboard |
| Freelance Invoice Tracker | Notion invoice tracker | invoice tracker template, client payment tracker |
| Weekly Content Planner | Notion content calendar | content calendar template, weekly content planner, social media content calendar |
| Content Creator Studio | Notion template for content creators | Notion content planner, content creator planner, YouTube content planner |
| Proposal Tracker | Notion proposal tracker | proposal tracker template, Notion client proposal template, sales pipeline Notion template |
| Brand Deal Tracker | brand deal tracker | Notion brand deal tracker, UGC deal tracker, influencer tracker template, rate card template for influencers |

## Rules
1. Main keyword in the first 40 characters of the title.
2. Description: the main keyword once, plus 2 to 4 of the other keywords, in normal sentences. No keyword stuffing.
3. Hashtags: use the product's list from the JSON, not general ones like #productivity.
4. Never claim a feature to fit a keyword (e.g. we track invoices, we don't generate PDF invoices).
5. Every month: check Pinterest/Etsy search bar suggestions for each main keyword and update the JSON.
