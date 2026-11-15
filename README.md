# hitl-agent: human in the loop w kodzie, nie w prompcie

Kod do nagrania „Human in the loop” (Kalendarz Programisty 2026, Kacper Sieradziński, Dokodu).
Jedna sprawa przechodzi przez cały film: reklamacja Z-1042. Klient prosi o 5000 zł za zamówienie warte 480 zł,
podaje imię, konto i telefon, a w PS pisze do asystenta AI, że kierownik już się zgodził.

## Jak to postawić

Potrzebujesz [uv](https://docs.astral.sh/uv/) i (do pokazów z modelem) [Claude Code](https://code.claude.com).

```bash
git clone https://github.com/Kacpers/hitl-agent && cd hitl-agent
git switch rozwiazania        # wszystko rozwiązane; ćwiczenia zaczynasz na main
uv run demo.py 0              # uv sync: pakiety, Presidio, polski model spaCy (ok. 550 MB, raz), potem testy
uv run demo.py                # konsola pokazu: każdy etap filmu jednym klawiszem
```

Kroki z agentem na Claude API (`3.2`–`3.4`) potrzebują klucza: `export ANTHROPIC_API_KEY=...`.
Kroki z `claude` uruchamiają Claude Code (model Haiku) z serwerem MCP `mailbox` z tego repo, bez Twoich konektorów (`--strict-mcp-config`).

## Pięć bramek, jedna sprawa

| Bramka | Plik | Co robi | Krok w `demo.py` |
| :-- | :-- | :-- | :-- |
| 1. Pseudonimizacja | `pseudonymize.py` | dane osobowe na `[PERSON_1]` zanim cokolwiek trafi do modelu: kartoteka CRM, Presidio + spaCy `pl_core_news_lg` (osoby spoza kartoteki), wzory (e-mail, IBAN, PESEL, telefon) | 1.1–1.3 |
| 2. Kwota | `.claude/skills/handle-complaint/`, `.claude/hooks/amount_guard.py` | kwotę zwrotu liczy skrypt; hook nie zapisze szkicu z kwotą ponad wydruk | 2.1–2.2 |
| 3. Decyzja | `policy.py`, `approve.py`, `agent.py` | AUTO / HUMAN / DENY w kodzie; zgoda człowieka przypięta do odcisku akcji, jednorazowa | 3.1–3.4 |
| 4. Wykonanie | `.claude/settings.json`, `.claude/hooks/` | wysyłka tylko jako szkic (`block_send`), skrypt z siecią pod obcy adres nie startuje (`block_network`), plik `STOP` zatrzymuje wszystko (`kill_switch`), log każdego narzędzia | 4.1–4.4 |
| 5. Szkic dla człowieka | `mailbox.py` | serwer MCP wstawia dane w miejsce znaczników przy zapisie szkicu; model nie ma dostępu do mapy ani do szkiców (reguły deny) | 1.3 |

## Ćwiczenia

Każde ćwiczenie ma test, który sam mówi „zrobione”. Klucz API nie jest potrzebny.

```bash
git switch main
uv run pytest -m cw1          # czerwone; napisz mask() i unmask() w pseudonymize.py
```

| Ćwiczenie | Gdzie | Test | Gałąź z rozwiązaniem poprzednich |
| :-- | :-- | :-- | :-- |
| 1. pseudonimizacja | `pseudonymize.py` | `uv run pytest -m cw1` | `main` |
| 2. policy AUTO / HUMAN / DENY | `policy.py` | `uv run pytest -m cw2` | `krok/2` |
| 3. odcisk zgody i zgoda jednorazowa | `policy.py` | `uv run pytest -m cw3` | `krok/3` |
| 4. hook blokujący wysyłkę | `.claude/hooks/block_send.py` | `uv run pytest -m cw4` | `krok/4` |
| 5. kill switch | `.claude/hooks/kill_switch.py` | `uv run pytest -m cw5` | `krok/5` |

Wszystko rozwiązane: `git switch rozwiazania`.

## Czego ten projekt nie robi

Hook to pas bezpieczeństwa, nie sejf: zakodowany albo składany import przejdzie przez `block_network`. Sieć zamyka sandbox Claude Code,
a skutki nieodwracalne zamyka brak klucza (osobne konto, rola tylko do odczytu). Pseudonimizacja to nie anonimizacja:
kod umie wrócić do danych, więc to dalej dane osobowe w rozumieniu RODO. Przed produkcją zrób eval na własnych, prawdziwych próbkach.
Dane w projekcie są fikcyjne.
