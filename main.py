from bs4 import BeautifulSoup
import re
import json


def clean_text(text):
    return " ".join(text.replace("\n", "").split())


def get_heading_information(heading_text):
    """
    Highlight(<span class="highlight_orange">orange</span>) - Page 7 · Location 150
    Highlight(<span class="highlight_orange">orange</span>) - Page 7 · Location 155
    Highlight(<span class="highlight_orange">orange</span>) - Page 8 · Location 178
    Highlight(<span class="highlight_orange">orange</span>) - 1: The Surprising Power of Atomic Habits &gt; Page 13 · Location 219
    Highlight(<span class="highlight_orange">orange</span>) - 1: The Surprising Power of Atomic Habits > Page 13 · Location 219
    Highlight(orange) - 1: The Surprising Power of Atomic Habits > Page 16 · Location 259
    Highlight(orange) - Page 7 ·
            Location 150
    """
    pattern = r"(.*\s-\s)([^>]*)(\s\>\s)?(Page\s\d*)\s*.\s*(Location\s\d*)"
    result = re.search(pattern, heading_text)

    chapter = clean_text(result.group(2))
    page = clean_text(result.group(4))
    location = clean_text(result.group(5))

    return chapter, page, location


def extract_quotes_from_kindle(html_content):
    note_texts = html_content.find_all("div", class_="noteText")
    quotes = []

    for note_text in note_texts:
        note_heading = note_text.find_previous_siblings("div", limit=1)[0]

        heading = clean_text(note_heading.text)
        text = clean_text(note_text.text)

        chapter, page, location = get_heading_information(heading)

        quote = {"chapter": chapter, "page": page, "location": location, "text": text}
        quotes.append(quote)
    return quotes


def extract_quotes_from_apple_book(html_content):
    """
    <div>
        <div>
        <div>2022. August 9.</div>
        <div>
            Book 2: On the River Gran, Among the
            Quadi
        </div>
        </div>
        <div>
        <div></div>
        <div></div>
        <p>
            Remember how long you’ve been
            putting this off, how many
            extensions the gods gave you, and
            you didn’t use them. At some point
            you have to recognize what world it
            is that you belong to; what power
            rules it and from what source you
            spring; that there is a limit to the
            time assigned you, and if you don’t
            use it to free yourself it will be
            gone and will never return.
        </p>
        <p></p>
        </div>
    </div>

    """
    main_content = html_content.find_all("div", {"dir": "ltr"})
    divs = main_content[0].find_all("div", recursive=False)

    quotes = []
    for div in divs:
        if len(div.find_all()) > 0:
            first_div = div.find("div")
            date_div, chapter_div = first_div.find_all("div")
            p = div.find("p")  # first p is text

            quote = {
                "date": clean_text(date_div.text),
                "chapter": clean_text(chapter_div.text),
                "text": clean_text(p.text),
            }
            quotes.append(quote)
    return quotes


def format_quotes(quotes, author, book):
    formatted_quotes = []
    for quote in quotes:
        formatted_quote = {
            "author": author,
            "book": book,
            "chapter": quote.get("chapter"),
            "text": quote.get("text"),
        }
        formatted_quotes.append(formatted_quote)
    return formatted_quotes


# with open('./html/Atomic Habits_ the life-changing million-copy #1 bestseller - Notebook (1).html') as f:
#     content = f.read()

# with open('./html/Gmail - Notes from “Meditations” by Marcus Aurelius (Emperor of Rome).html') as f:
#     content = f.read()


# html_content = BeautifulSoup(content, "html.parser")


# print('=====')

# title = html_content.find("div", class_="bookTitle")
# author = html_content.find("div", class_="authors")

# q = extract_quotes_from_kindle(html_content)

# print("++++++++++++")
# print(q[-1])

# print(title)
# print(author)


# author = "James Clear"
# book = "Atomic Habits"
# author = "Marcus Aurelius"
# book = "Meditations"

# q = extract_quotes_from_apple_book(html_content)

# q = format_quotes(q, author, book)
# print(q[-1])

# with open('output.json', 'w') as file:
#     file.write(json.dumps(q, indent=4))


# with open('output2.json', 'w') as file:
#     file.write(json.dumps(q, indent=4))
