# Lipstick Unfiltered: What Shoppers Really Say About Their Lipsticks

A Voice of Customer (VoC) dashboard and copilot built on 2,635 public Nykaa lipstick and liquid lipstick reviews (22 products, 286 shades). It turns reviews into product decisions: top pain points, what shoppers love, shades to watch, and recommended actions backed by real review quotes.

## Problem statement
Star ratings tell a brand *what* customers feel, but not *why* or what to fix first. Reviews hold the answer, but there are too many to read, and the useful signals (dryness, poor wear, shade mismatch) are buried in free text.

Shoppers face a related problem: choosing a lip shade online is hard. "Try shade" is not available for every brand and does not show how accurate its match is, and many brands do not show which skin tones a shade suits.

**Goal:** build a copilot that reads the reviews, finds recurring patterns, and recommends product actions with evidence, so a product team can decide what to fix or test first.

## How insights help product teams
- **Prioritise:** rank complaints by how many low-rated reviews mention them, so the team fixes the biggest issue first.
- **Find hidden problems:** about 20% of 4 and 5 star reviews still mention a complaint, which ratings alone would miss.
- **Act at shade level:** spot weak shades and test reformulations or better shade previews, instead of treating the whole range the same.
- **Improve listings and discovery:** use customer language to improve product pages, swatches and shade guidance.
- **Back decisions with evidence:** every recommendation links to the reviews behind it.

## What it shows
- Sentiment split and low-rated share over time (star ratings used as sentiment)
- Top 5 pain points and top "loves", with tap-to-expand customer quotes
- Recommended actions linked to the evidence behind them
- Shades to watch (lowest-rated shades with review counts)
- Filters by product and by type (lipstick / liquid lipstick)
- Optional "Ask the copilot" Q&A (runs inside Claude only; not available on this static page)

## How it was built
1. Collected public reviews with an Apify Nykaa scraper, using negative-first and newest sorts to fix the 5-star bias of the default sort (the first scrape was 99.5% five-star).
2. Merged and de-duplicated by review ID, and mapped shade IDs to shade names (Python, pandas).
3. Tagged reviews into themes with keyword rules (`build.py`).
4. Generated a single self-contained dashboard page (`tpl.html` -> `index.html`).

## AI architecture
- **Theme detection (dashboard):** rule-based. Regex keyword patterns tag each review with complaint and praise themes. No LLM is used here, so results are fast, free and explainable, but approximate.
- **Ask the copilot (Q&A):** retrieval plus generation. The question is matched to the 25 most relevant reviews in the current filter (keyword overlap, with extra weight for low-rated reviews on complaint questions). Those reviews are sent to Claude with instructions to answer only from them, explain the why, suggest actions, and cite review numbers.
- **Guardrails:** answers must cite review numbers and say when evidence is thin.

## Evaluation
**Done: data validation.** I manually compared the scraped reviews, ratings and dates against what is published on Nykaa's product pages, and they matched.

**Still to do:**
- Write 20 to 30 realistic product-team questions (e.g. "Why do customers say this lipstick feels drying?") and hand-check each Q&A answer: are the cited reviews real and relevant, and is the conclusion supported?
- Check the theme tags against a hand-labelled sample of about 100 reviews and report precision.
- Report the results here once complete.

## Run it
```bash
pip install -r requirements.txt
python build.py        # reads nykaa_lipstick_voc_dataset.xlsx, writes index.html
```
Open `index.html` in a browser. To change colours or text, edit `tpl.html`. To change themes or recommendations, edit the `NEG` and `POS` lists in `build.py`.

## Limitations
- Themes come from keyword rules, so counts are directional, not exact. Shade-mismatch complaints are probably undercounted.
- A snapshot of 22 products, not all of Nykaa. Not affiliated with Nykaa.
- The Q&A retrieval is keyword-based, so it can miss relevant reviews that use different words.
- The review data file is not included in this repository; the dashboard page embeds review text for demonstration only.

