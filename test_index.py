def test_index_html():
    with open("index.html") as f:
        content = f.read()
    assert "<h1>Pipeline CI/CD OK 🚀</h1>" in content
