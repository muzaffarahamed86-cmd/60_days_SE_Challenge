# unit_converter

Lightweight `unit_converter` package with simple conversion helpers and a CLI.

Contents
- `converters/` — individual converter modules (`currency`, `temperature`, `length`, `weight`).
- `engine.py` — central dispatch function `convert(category, value, from_unit, to_unit)`.
- `main.py` — tiny CLI wrapper for quick conversions.

Quick examples (run from `pythonChallenge/unit_converter`):

```powershell
python main.py currency 100 USD EUR
python main.py temperature 100 C F
python main.py length 10 km mi
python main.py weight 5 kg lb
```

Notes
- The `currency` converter uses demo/hard-coded rates for offline use. Replace with a live rates API for production.
- This package is intentionally minimal to keep it easy to test and extend.

If you want, I can add packaging metadata (`pyproject.toml`) or a small test suite next.
