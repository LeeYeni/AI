import requests, re

# --- Wikipedia raw 가져오기 ---
def fetch_wikipedia_wikitext(word: str) -> str:
    url = "https://en.wiktionary.org/w/api.php"
    params = {
        "action": "parse",
        "page": word,
        "prop": "wikitext",
        "format": "json"
    }

    # User-Agent가 없으면, "봇/스크래퍼"로 간주해서 응답을 제한함.
    headers = {
        "User-Agent": "Vocab-AI/1.0 (https://example.com)"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if "parse" not in data:
        return None
    
    wikitext = data["parse"]["wikitext"]["*"]
    return wikitext



# --- 어원만 가져오기 ---
def extract_etymology(wikitext: str) -> str:
    pattern = r"===Etymology===\n(.*?)(?=\n===)"
    match = re.search(pattern, wikitext, flags=re.DOTALL)

    if not match:
        return None

    return match.group(1).strip()



# --- pipeline ---
def wiktionary_pipeline(word: str) -> str:
    wikitext = fetch_wikipedia_wikitext(word)
    
    if wikitext is None:
        return None
    
    return extract_etymology(wikitext)