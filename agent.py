"""
agent.py

The FitFindr planning loop. Orchestrates the three tools in response to a
natural language user query, passing state between them via a session dict.
"""

import re
from tools import search_listings, suggest_outfit, create_fit_card


# -- session state --------------------------------------------------------------

def _new_session(query: str, wardrobe: dict) -> dict:
    return {
        "query": query,
        "parsed": {},
        "search_results": [],
        "selected_item": None,
        "wardrobe": wardrobe,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }


# -- query parser ---------------------------------------------------------------

def _parse_query(query: str) -> dict:
    # Extract max price
    price_match = re.search(r'(?:under|max|less than|up to)\s*\$?(\d+(?:\.\d+)?)', query, re.IGNORECASE)
    max_price = float(price_match.group(1)) if price_match else None

    # Extract size
    size_match = re.search(r'\bsize\s+([A-Z0-9/]+)\b', query, re.IGNORECASE)
    size = size_match.group(1) if size_match else None

    # Description: strip price/size fragments and filler words
    description = query
    if price_match:
        description = description[:price_match.start()] + description[price_match.end():]
    if size_match:
        description = description[:size_match.start()] + description[size_match.end():]
    description = re.sub(r'\b(looking for|i want|i need|find me|a|an|the|some)\b', '', description, flags=re.IGNORECASE)
    description = ' '.join(description.split())

    return {
        "description": description,
        "size": size,
        "max_price": max_price,
    }


# -- planning loop --------------------------------------------------------------

def run_agent(query: str, wardrobe: dict) -> dict:
    # Step 1: Initialize session
    session = _new_session(query, wardrobe)

    # Step 2: Parse query
    parsed = _parse_query(query)
    session["parsed"] = parsed

    # Step 3: Search — stop early if no results
    results = search_listings(
        description=parsed["description"],
        size=parsed["size"],
        max_price=parsed["max_price"],
    )
    session["search_results"] = results

    if not results:
        session["error"] = (
            f"No listings matched your search for '{parsed['description']}'"
            + (f" in size {parsed['size']}" if parsed["size"] else "")
            + (f" under ${parsed['max_price']:.0f}" if parsed["max_price"] else "")
            + ". Try broadening your description, adjusting the price, or leaving size blank."
        )
        return session

    # Step 4: Select top result
    session["selected_item"] = results[0]

    # Step 5: Suggest outfit
    session["outfit_suggestion"] = suggest_outfit(
        session["selected_item"], session["wardrobe"]
    )

    # Step 6: Create fit card
    session["fit_card"] = create_fit_card(
        session["outfit_suggestion"], session["selected_item"]
    )

    # Step 7: Return session
    return session


# -- CLI test -------------------------------------------------------------------

if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== Happy path: graphic tee ===\n")
    session = run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    )
    if session["error"]:
        print(f"Error: {session['error']}")
    else:
        print(f"Found: {session['selected_item']['title']}")
        print(f"\nOutfit: {session['outfit_suggestion']}")
        print(f"\nFit card: {session['fit_card']}")

    print("\n\n=== No-results path ===\n")
    session2 = run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    )
    print(f"Error message: {session2['error']}")