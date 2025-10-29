
# Minimal IPA helper (placeholder).
# In practice you might use a library or your own mapping table.
def hint(word: str) -> str:
    # Very naive placeholders for demo
    mapping = {
        "hypothesis": "/haɪˈpɒθəsɪs/",
        "counterfactual": "/ˌkaʊntərˈfæktʃuəl/",
        "would": "/wʊd/",
        "could": "/kʊd/"
    }
    return mapping.get(word.lower(), "")
