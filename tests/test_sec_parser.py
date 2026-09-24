from atlas.ingestion.sec_parser import extract_text


def test_extract_text_removes_hidden_xbrl_but_keeps_visible_facts() -> None:
    html = b"""
    <html>
        <body>
            <ix:header>
                <div>us-gaap:HiddenMetadata</div>
                <div>0001045810</div>
            </ix:header>

            <script>
                console.log("irrelevant");
            </script>

            <p>
                Revenue was
                <ix:nonfraction name="us-gaap:Revenue">
                    $10 billion
                </ix:nonfraction>
                in fiscal 2026.
            </p>
        </body>
    </html>
    """

    text = extract_text(html)

    assert "us-gaap:HiddenMetadata" not in text
    assert "0001045810" not in text
    assert "irrelevant" not in text

    assert "Revenue was" in text
    assert "$10 billion" in text
    assert "in fiscal 2026." in text
