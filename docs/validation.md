# Validation and remaining checks

## Completed checks

- 54 PBIP/PBIR/PBISM and report definition JSON files validate against downloaded Microsoft public schemas, with zero errors.
- Both Power Query partitions pass syntax parsing with Microsoft's `@microsoft/powerquery-parser` 4.0.1. Results are in `m-syntax-validation.json`; syntax parsing does not evaluate the queries.
- All 3,000 CSV records match the embedded Power Query payload, cell for cell, after documented serialization.
- All report fields and DAX column/measure references resolve to the included model.
- The active single-direction Calendar-to-Marketing relationship is present; Year-Month has an explicit numeric sort column.
- All 45 visual containers stay inside the three 1440 × 900 page canvases.
- Reference totals were recalculated independently from the CSV with decimal arithmetic. Checks are recorded in `validation.json`.
- No exact duplicate records were found. All 31 snapshot fields are populated.
- Package text was checked for original local user paths, original desktop host identifiers, and common connection-secret strings. The binary model, SecurityBindings and local cache files are excluded.
- Preview images use actual CSV aggregations and were visually inspected. They are static design previews, not Desktop renderings.

## Pending local checks

Power BI Desktop and SQL Server were unavailable during creation. Therefore, the following are **not yet verified**:

1. Open `powerbi/Marketing.pbip` and refresh successfully in Desktop. Verify the M partition and DAX measures evaluate.
2. Confirm native card, chart, slicer and table formatting; adjust table widths or font sizing if Desktop renders differently from the static preview.
3. Check period filtering changes fact values and monthly categories, and test chart selections and independent page slicers. Confirm Paid Performance remains paid-only.
4. Compare unfiltered totals with `methodology.md`, including blank ratios for zero denominators. The paid-only page should show 1.43x and zero-return spend share around 4.0%.
5. Run the four SQL scripts in a test SQL Server database. Confirm 3,000 loaded rows and matching query totals.
6. Optionally save a PBIX and capture actual report screenshots for the public README.

Schema validation confirms file structure; it does not evaluate M/DAX, validate every visual-specific formatting property, or guarantee compatibility with every Desktop version.
