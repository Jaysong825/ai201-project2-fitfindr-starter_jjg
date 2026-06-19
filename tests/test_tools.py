from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import load_listings, get_example_wardrobe, get_empty_wardrobe


# -- search_listings ------------------------------------------------------------

def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0

def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)

def test_search_no_filters():
    results = search_listings("jeans", size=None, max_price=None)
    assert len(results) > 0


# -- suggest_outfit -------------------------------------------------------------

def test_suggest_outfit_with_wardrobe():
    item = load_listings()[0]
    result = suggest_outfit(item, get_example_wardrobe())
    assert isinstance(result, str)
    assert len(result) > 0

def test_suggest_outfit_empty_wardrobe():
    item = load_listings()[0]
    result = suggest_outfit(item, get_empty_wardrobe())
    assert isinstance(result, str)
    assert len(result) > 0


# -- create_fit_card ------------------------------------------------------------

def test_fit_card_returns_string():
    item = load_listings()[1]
    outfit = "Pair with baggy jeans and chunky sneakers for a 90s vibe."
    result = create_fit_card(outfit, item)
    assert isinstance(result, str)
    assert len(result) > 0

def test_fit_card_empty_outfit_returns_error_string():
    item = load_listings()[0]
    result = create_fit_card("", item)
    assert isinstance(result, str)
    assert "Error" in result

def test_fit_card_whitespace_outfit_returns_error_string():
    item = load_listings()[0]
    result = create_fit_card("   ", item)
    assert isinstance(result, str)
    assert "Error" in result