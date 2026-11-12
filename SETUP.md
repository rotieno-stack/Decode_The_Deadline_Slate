# Decode the Deadline: Slate setup

```
decode-the-deadline-slate/
  puzzle.html          The whole front end (HTML + CSS + JS in one file)
  queries/guess.sql    Slate query web service #1 (checks a guess)
  queries/hint.sql     Slate query web service #2 (parity/primality hint)
  SETUP.md             This file
```

The answer grid exists only inside the two SQL queries. The page never
contains it; it only receives `true`/`false` (and odd/prime hints).

## 1. Create the "guess" query (needs Administrator role)

1. Queries / Reports -> New Query. Name it `DTD Guess`.
2. Add three **custom parameters**: `row`, `col`, `value`.
3. Paste the contents of `queries/guess.sql` as the query's custom SQL.
   (Slate's documented pattern for custom REST services is a SELECT
   ending in `for xml path(...), type`. If your Query Builder asks you
   to build from a base object and export fields instead, ask your Slate
   admin or Technolutions support how to run a raw SELECT; the logic is
   the same.)
4. Edit Web Service -> Service type: **JSON**.
5. Save, click the **Web Services** link, and copy the endpoint URL.
   Use a public (token-only) endpoint. It exposes only true/false, so
   it is safe, but never put a service-account password in the page.

## 2. Create the "hint" query

Same steps with `queries/hint.sql` and parameters `row`, `col`. Name it
`DTD Hint`. Copy its endpoint too.

## 3. Test before touching the page

Open this in a browser (substituting your endpoint):

```
<GUESS endpoint>&row=0&col=0&value=7   ->  correct: true
<GUESS endpoint>&row=0&col=0&value=3   ->  correct: false
<HINT endpoint>&row=0&col=0            ->  odd: true, prime: true
```

If the parameter names differ from `row`/`col`/`value`, change
`PARAM_ROW`/`PARAM_COL`/`PARAM_VALUE` in `puzzle.html`.

## 4. Publish the page

1. In `puzzle.html`, replace `PASTE_GUESS_ENDPOINT_HERE` and
   `PASTE_HINT_ENDPOINT_HERE` in the CONFIG block.
2. Paste the whole file into a Slate page's HTML/source area (or host it
   and embed with an iframe).
3. Load the page, solve it, and confirm the reveal shows **7:45 AM PST**
   (or your own time).

## Notes

- **Rate limits:** Slate limits web services to roughly 300 requests per
  5 minutes per database, shared with all other Caltech integrations.
  The page caps hints (`MAX_HINTS`), caches hints and wrong guesses, and
  blocks overlapping requests. If traffic is expected to be high, ask
  Caltech's Slate admin whether this is acceptable.
- **CORS:** if the page lives on a different domain than the query
  endpoint, `TRANSPORT: 'auto'` falls back to JSONP, which Slate supports.
- **Fonts:** the page loads Google Fonts. If Slate blocks them, it falls
  back to Georgia / system monospace automatically.
- **Staff visibility:** anyone with permission to view the queries can
  read the solution.

## Changing the release time

1. Edit the grid in **both** SQL files (keep them identical).
2. Diagonal decode (in `checkComplete()` in `puzzle.html`): 1st digit =
   hour, 2nd digit x 5 = minutes, 3rd digit parity = AM (odd) / PM (even).
3. Rewrite `CLUES` and `GIVENS` in `puzzle.html` so the grid is unique.
4. Update `TIME_ZONE_LABEL` if needed.
