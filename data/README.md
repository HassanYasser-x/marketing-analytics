# Snapshot provenance

The 3,000 records were decoded locally from the supplied Power BI DataModel using PBIXRay 0.15.5. This is recovered project data; its original publisher, license and whether it is synthetic were not supplied.

The exported `Revenue` column was normalized to `revenue`, weekend booleans were serialized as 0/1, numeric values were written to four decimal places, and records were sorted for stable Git diffs. No observations were invented or removed. The original cleaning view and its six category counts were preserved.

The model snapshot originally contained 31 columns, including `channel_type` and `roas_category_fixed`; the original raw `roas_category` had already been removed. Its original values cannot be reconstructed or audited from this package.

No names, email addresses, customer identifiers or source-machine connection strings are included. The CSV and embedded model snapshot still contain the supplied marketing metrics. The owner should establish data redistribution rights before publishing a public repository. No license has been assigned to the underlying data.
