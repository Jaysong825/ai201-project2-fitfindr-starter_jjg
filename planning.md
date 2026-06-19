# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): ...
- `size` (str): ...
- `max_price` (float): ...

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->

---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): ...
- `wardrobe` (dict): ...

**What it returns:**
<!-- Describe the return value -->

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->

---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (str): ...
- `new_item` (dict): ...

**What it returns:**
<!-- Describe the return value -->

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->

---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- an agent will follow a conditional sequence driven by what each tool it has returns. after user input it ALWAYS calls search_listings first. if no results come back it will stop and ask the user to change or adjust the query. no other tools are called.  if results are returned it picks the top match to the query and calls suggest_outfit using that item plus the users wardrobe. if the outfit suggestion succeeds, it calls create_fit_card to generate the final caption. the loop will end when either a fit card is made or and error interrupt the chain early. the agent never calls a tool with an empty or missing input from the previous step. -->

---an agent will follow a conditional sequence driven by what each tool it has returns. after user input it ALWAYS calls search_listings first. if no results come back it will stop and ask the user to change or adjust the query. no other tools are called.  if results are returned it picks the top match to the query and calls suggest_outfit using that item plus the users wardrobe. if the outfit suggestion succeeds, it calls create_fit_card to generate the final caption. the loop will end when either a fit card is made or and error interrupt the chain early. the agent never calls a tool with an empty or missing input from the previous step. -->


## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->

---The agent maintains a session state dictionary that is updated after each tool call. It tracks: search_results (list returned by search_listings), selected_item (the top result passed forward), wardrobe (provided by the user at the start of the session), outfit_suggestion (returned by suggest_outfit), and fit_card (final output from create_fit_card). Each tool reads what it needs from this dictionary and writes its output back into it. Nothing is re-entered by the user between steps.

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query |Tells the user no matches were found, explains which filters were used, and suggests adjusting size, price, or description. Does not call suggest_outfit. |
| suggest_outfit | Wardrobe is empty |Returns a generic styling suggestion based on the item's style tags alone, and notes that adding wardrobe items will produce more personalized results. |
| create_fit_card | Outfit input is missing or incomplete |Returns a minimal fit card using only the new item's title, price, and platform, rather than crashing or returning nothing. |

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     Use ASCII art or a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html).
     Do NOT embed an image — graders need to read your diagram directly in the file;
     an embedded image or screenshot cannot be evaluated.
     You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->

---User Input
    │
    ▼
┌─────────────────────────────────────┐
│            Planning Loop            │
│                                     │
│  1. Parse description, size, price  │
│  2. Call search_listings            │
│     ├── No results → STOP, tell user│
│     └── Results found ──────────────┼──► session["selected_item"]
│                                     │
│  3. Call suggest_outfit             │
│     ├── Empty wardrobe → fallback   │
│     └── Suggestion returned ────────┼──► session["outfit_suggestion"]
│                                     │
│  4. Call create_fit_card            │
│     ├── Missing input → minimal card│
│     └── Fit card returned ──────────┼──► session["fit_card"]
│                                     │
│  5. Return fit card to user → DONE  │
└─────────────────────────────────────┘
         ▲            │
         │            ▼
    ┌─────────────────────┐
    │   Session State     │
    │  - wardrobe         │
    │  - search_results   │
    │  - selected_item    │
    │  - outfit_suggestion│
    │  - fit_card         │
    └─────────────────────┘

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

**Milestone 3 — Individual tool implementations:**
---I'll give Claude the spec for each tool one at a time (inputs, return value, failure mode from this file) and ask it to implement each function using load_listings() or get_example_wardrobe() from data_loader.py. For search_listings I'll test it against 3 queries: one that matches, one with no results, and one at the price boundary. For suggest_outfit I'll test with the example wardrobe and with the empty wardrobe. For create_fit_card I'll call it twice with different inputs and confirm the output differs each time.
**Milestone 4 — Planning loop and state management:**

---
Milestone 4 — Planning loop and state management:

I'll give Claude the architecture diagram above plus the session state spec and ask it to implement the planning loop in agent.py. I'll verify it by running a full interaction in the terminal and confirming: (1) state passes correctly between tools without user re-entry, (2) the loop stops cleanly when search_listings returns nothing, and (3) all three tools are called in the correct order on a successful query.

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
<!-- What does the agent do first? Which tool is called? With what input? --> The agent calls search_listing(description="vintage graphic tee", size=None, max_price=30.0) It scans listings for items whose title, description, or style_tags match "vintage" and "graphic tee" with price ≤ $30. Returns 2 matches; top result is: {title: "Y2K Baby Tee — Butterfly Print", price: 18.0, platform: "depop", condition: "excellent"}. This is saved to session["selected_item"].

**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->The agent calls suggest_outfit(new_item=session["selected_item"], wardrobe=session["wardrobe"]). The wardrobe contains baggy straight-leg jeans and chunky white sneakers. Returns: "Pair the Y2K butterfly tee with your baggy straight-leg jeans and chunky sneakers — tuck the front of the tee in slightly and add a black crossbody for a clean Y2K streetwear look." Saved to session["outfit_suggestion"].

**Step 3:**
<!-- Continue until the full interaction is complete -->The agent calls create_fit_card(outfit=session["outfit_suggestion"], new_item=session["selected_item"]). Returns: "snagged this y2k butterfly tee off depop for $18 and it was literally made for my baggy jeans era 🦋 full fit incoming"

**Final output to user:**
<!-- What does the user actually see at the end? -->
The agent prints the outfit suggestion and fit card together — the styling advice so they know how to wear it, and the caption ready to copy for their post.