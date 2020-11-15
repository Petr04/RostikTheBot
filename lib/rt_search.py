from googlesearch import search

def rt_search(question, section, pages=3):
    if section == 'video':
        question+=' site:help.smarthome.rt.ru/'
    else:
        question+=' site:rt.ru/support/'+section
    # Google Search query results as a Python List of URLs
    return list(search(question, stop=pages, pause=1))
