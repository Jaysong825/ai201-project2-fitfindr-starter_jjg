# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```

## Setup

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

`data/listings.json` contains 40 mock secondhand listings across categories (tops, bottoms, outerwear, shoes, accessories) and styles (vintage, y2k, grunge, cottagecore, streetwear, and more).

Each listing has: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

Load it with:
```python
from utils.data_loader import load_listings
listings = load_listings()
```

## The Wardrobe Schema

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: field definitions for a wardrobe item
- `example_wardrobe`: a sample wardrobe with 10 items you can use for testing
- `empty_wardrobe`: a starting template for a new user

Load an example wardrobe with:
```python
from utils.data_loader import get_example_wardrobe
wardrobe = get_example_wardrobe()
```

## Tool Inventory

Your README submission must document each tool's name, inputs, and return value. **These must exactly match your actual function signatures in `tools.py`.** Your documented interfaces will be checked against your actual function signatures in `tools.py` — if the parameter count or types contradict what's in the code, you may not receive full credit for that tool.

---

## Interaction Walkthrough



**User query:**"I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1 — Tool called:** `search_listings`**
- Input: `description="vintage graphic tee"`, `size=None`, `max_price=30.0`
- Why this tool:- Why this tool: Always the first step — parses the query for keywords, price, and size, then scores listings by keyword match.
- Output: Two matching listings. Top result: `Y2K Baby Tee — Butterfly Print`, $18.00, depop, excellent condition

**Step 2 — Tool called: `suggest_outfit`**
- Input: `new_item={"title": "Y2K Baby Tee — Butterfly Print", "price": 18.0, ...}`, `wardrobe=<example wardrobe with 10 items>`
- Why this tool: `search_listings` returned results, so the agent selects the top match and passes it to `suggest_outfit` along with the session wardrobe.(only called if Step 1 passes)
- Output: "Pair the Y2K Baby Tee with your Baggy straight-leg jeans, dark wash, and Chunky white sneakers... Or wear it with your Wide-leg khaki trousers and Black combat boots..."


**Step 3 — Tool called: `create_fit_card`**
- Input: `outfit=<suggestion from Step 2>`, `new_item=<top listing from Step 1>`
- Why this tool: Both previous tools succeeded and returned non-empty output, so the agent generates the final shareable caption. This tool is only called if Step 2 produced a suggestion.
- Output: "i just got this adorable y2k baby tee - butterfly print from depop for $18 and i'm obsessed with it. been pairing it with my baggy jeans and chunky sneakers 🙃"

**Final output to user:**

---All three Gradio panels populate — the listing details, the outfit suggestion, and the fit card caption ready to copy.

## Error Handling and Fail Points

<!-- For each tool, describe the specific failure mode and what your agent does in response.
     This maps to the error handling section of the rubric (F5-C1). -->

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| `search_listings` | No listings match the query | Sets `session["error"]` and returns early — `suggest_outfit` is never called. |
| `suggest_outfit` | Wardrobe is empty | Returns general styling advice based on the item's tags and colors instead of crashing. |
| `create_fit_card` | `outfit` is empty or whitespace-only | Returns a descriptive error string — never raises an exception. |

---

## Spec Reflection

<!-- Answer both questions with at least 2–3 sentences each. -->

**One way planning.md helped during implementation:**
Helped organize workflow and document ai implentaton/help
**One divergence from your spec, and why:**
I used regex instead of the LLM to parse queries — faster and no extra API call.
---

## Where to Start

1. **Read `planning.md` and fill it out before writing any code.**
2. Verify the data loads correctly by running `python utils/data_loader.py`.
3. Build and test each tool individually before connecting them through your planning loop.

Your implementation files go in this same directory. There's no required file structure for your agent code — organize it however makes sense for your design.
