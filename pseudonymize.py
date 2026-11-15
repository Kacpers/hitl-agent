"""Pseudonymization: the model works on [PERSON_1], never on the customer's personal data. Exercise 1: uv run pytest -m cw1

Code, not the model, replaces personal data with placeholders before anything reaches the model:
  1. known customers and addresses from the CRM export (data/customers/contacts.csv),
  2. any other person named in the text: Presidio + spaCy pl_core_news_lg (named entity recognition),
  3. patterns: e-mail, IBAN, PESEL, phone number.
The placeholder -> value map stays on the code side. Data comes back only in the draft a human reads.

CLI (used by the Claude Code skill):  uv run pseudonymize.py data/mail/1_complaint.txt
"""
import csv
import functools
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
CONTACTS = ROOT / "data" / "customers" / "contacts.csv"   # company;person;phone;address
PLACEHOLDERS = ROOT / "placeholders.json"                 # map for the last mail; the model is denied access to it

PATTERNS = [  # order matters: IBAN and PESEL before phone, because a phone number is 9 digits
    ("EMAIL", r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    ("IBAN", r"\bPL ?\d{2}(?: ?\d{4}){6}\b"),
    ("PESEL", r"(?<!\d)\d{11}(?!\d)"),
    ("PHONE", r"(?<![\d\w])(?:\+48 ?)?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\d)"),
]
NOT_A_NAME = {"dzień", "dobry", "pozdrawiam", "reklamacja", "zamówienie", "klient", "kierownik", "asystent"}


def contacts() -> list[dict]:
    with open(CONTACTS, encoding="utf-8", newline="") as f:
        return [dict(zip(("company", "person", "phone", "address"), row)) for row in csv.reader(f, delimiter=";") if row]


@functools.lru_cache(maxsize=1)
def _analyzer():
    """Presidio with the Polish spaCy model: finds people who are not in the CRM export."""
    from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
    from presidio_analyzer.nlp_engine import NerModelConfiguration, SpacyNlpEngine
    from presidio_analyzer.predefined_recognizers import SpacyRecognizer

    nlp = SpacyNlpEngine(models=[{"lang_code": "pl", "model_name": "pl_core_news_lg"}],
                         ner_model_configuration=NerModelConfiguration(model_to_presidio_entity_mapping={"persName": "PERSON"}))
    registry = RecognizerRegistry(supported_languages=["pl"])
    registry.add_recognizer(SpacyRecognizer(supported_language="pl", supported_entities=["PERSON"]))
    return AnalyzerEngine(nlp_engine=nlp, registry=registry, supported_languages=["pl"])


def people(text: str) -> list[str]:
    """Names found by Presidio, without placeholders, e-mails and common words."""
    found = _analyzer().analyze(text=text, language="pl", entities=["PERSON"], score_threshold=0.5)
    return [text[r.start:r.end] for r in found
            if text[r.start:r.end].lower() not in NOT_A_NAME and not re.search(r"[\d\[\]@]", text[r.start:r.end])]


# EXERCISE 1
def mask(text: str) -> tuple[str, dict]:
    """Exercise 1a. Return (text with placeholders, map placeholder -> original) before the text reaches the model.
    - people and addresses from contacts() (fields "person", "address") -> [PERSON_1], [ADDRESS_1],
    - other people found by people(text) (Presidio) -> [PERSON_n],
    - PATTERNS (e-mail, IBAN, PESEL, phone) -> [EMAIL_1], [IBAN_1], ...
    The same value must get the same placeholder. The order id and the amount stay.
    Check: uv run pytest -m cw1
    """
    raise NotImplementedError("Exercise 1a: write mask()")


def unmask(text: str, mapping: dict) -> str:
    """Exercise 1b. Placeholders back to data (code does it when the draft goes to a human)."""
    raise NotImplementedError("Exercise 1b: write unmask()")
# END OF EXERCISE 1


if __name__ == "__main__":
    masked, mapping = mask(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    PLACEHOLDERS.write_text(json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")
    print(masked)
    print(f"\n[{len(mapping)} personal data items replaced with placeholders; the map stays in code]")
