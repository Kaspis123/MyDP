
def bitlylink(url):
    import pyshorteners
    type_bitly = pyshorteners.Shortener(api_key='ee422324cdb8e1c0e630c180a51db0b06492284b')
    if not url.startswith("https://"):
        url = "https://" + url


    if not url.startswith("https://www.") and not url.startswith("https://wwww."):
        url = url.replace("https://", "https://www.")
    short_url = type_bitly.bitly.short(url)
    return short_url
