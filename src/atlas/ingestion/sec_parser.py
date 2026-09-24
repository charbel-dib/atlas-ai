import re
import warnings

from bs4 import (
    BeautifulSoup,
    NavigableString,
    Tag,
    XMLParsedAsHTMLWarning,
)

REMOVABLE_TAGS = {
    "script",
    "style",
    "noscript",
}

BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "caption",
    "dd",
    "div",
    "dl",
    "dt",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "tbody",
    "tfoot",
    "thead",
    "tr",
    "ul",
}


def parse_html(html: bytes) -> BeautifulSoup:
    with warnings.catch_warnings():
        warnings.simplefilter(
            "ignore",
            XMLParsedAsHTMLWarning,
        )

        return BeautifulSoup(
            html,
            "lxml",
        )


def remove_non_content_elements(
    soup: BeautifulSoup,
) -> None:
    for tag_name in REMOVABLE_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    for tag in soup.find_all("ix:header"):
        tag.decompose()


def _extract_node_text(
    node: Tag | NavigableString,
    output: list[str],
) -> None:
    if isinstance(node, NavigableString):
        output.append(str(node))
        return

    if not isinstance(node, Tag):
        return

    tag_name = node.name.lower()

    if tag_name == "br":
        output.append("\n")
        return

    if tag_name in {"td", "th"}:
        for child in node.children:
            _extract_node_text(child, output)

        output.append("\t")
        return

    is_block = tag_name in BLOCK_TAGS

    if is_block:
        output.append("\n")

    for child in node.children:
        _extract_node_text(child, output)

    if is_block:
        output.append("\n")


def normalize_whitespace(text: str) -> str:
    text = text.replace("\xa0", " ")

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r" *\n *",
        "\n",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


def extract_text(html: bytes) -> str:
    soup = parse_html(html)

    remove_non_content_elements(soup)

    output: list[str] = []

    root = soup.body or soup

    _extract_node_text(
        root,
        output,
    )

    text = "".join(output)

    return normalize_whitespace(text)
