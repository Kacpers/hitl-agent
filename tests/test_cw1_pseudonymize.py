import pathlib
import pytest
from pseudonymize import mask, unmask

pytestmark = pytest.mark.cw1
MAIL = (pathlib.Path(__file__).resolve().parents[1] / "data" / "mail" / "1_complaint.txt").read_text(encoding="utf-8")
PERSONAL_DATA = ["Anna Testowa", "Tomasz Wiśniewski", "anna.testowa@firma-testowa-2.example", "+48 500 000 002",
                 "PL12 3456 0000 0000 0000 0000 0002", "ul. Testowa 2, Kraków"]


def test_model_never_sees_personal_data():
    masked, _ = mask(MAIL)
    for item in PERSONAL_DATA:
        assert item not in masked, item


def test_person_outside_crm_found_by_presidio():
    masked, mapping = mask("Paczkę odebrał Tomasz Wiśniewski.")
    assert "Tomasz Wiśniewski" not in masked and "Tomasz Wiśniewski" in mapping.values()


def test_case_stays_readable():
    masked, _ = mask(MAIL)
    assert "Z-1042" in masked and "5000 zł" in masked and "[PERSON_1]" in masked


def test_same_value_same_placeholder():
    masked, mapping = mask("Anna Testowa pisze. Podpisano: Anna Testowa")
    assert masked == "[PERSON_1] pisze. Podpisano: [PERSON_1]" and len(mapping) == 1


def test_pesel_is_not_a_phone():
    masked, _ = mask("PESEL 90010112345, tel. 600 100 200")
    assert "[PESEL_1]" in masked and "[PHONE_1]" in masked


def test_unmask_restores_original():
    masked, mapping = mask(MAIL)
    assert unmask(masked, mapping) == MAIL
