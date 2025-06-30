import os
from dotenv import load_dotenv
from string import Template
from utils.openai_client import summarize_text
from utils.email_sender import send_email
from fetchers.uk_fetcher import fetch_uk_updates
from fetchers.france_fetcher import fetch_france_updates
from fetchers.uae_fetcher import fetch_uae_updates

load_dotenv()

def run_digest():
    updates_by_mu = {
        'UKIA': fetch_uk_updates(),
        'Gallia': fetch_france_updates(),
        'Middle East': fetch_uae_updates(),
    }

    content_block = ""
    for mu, updates in updates_by_mu.items():
        content_block += f"<h2>{mu}</h2>"
        for update in updates:
            summary = summarize_text(update['content'])
            content_block += f"<p><strong>{update['title']}</strong><br>{summary}</p>"

    with open("templates/email_template.html", "r") as file:
        template = Template(file.read())

    digest_html = template.safe_substitute(DIGEST_CONTENT=content_block)
    send_email("ESG Compliance Digest – EMEA Update", digest_html)

if __name__ == "__main__":
    run_digest()

