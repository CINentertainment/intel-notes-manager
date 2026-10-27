from html import escape

from app import models


RELIABILITY_DESCRIPTIONS = {
    "A": "Completely reliable",
    "B": "Usually reliable",
    "C": "Fairly reliable",
    "D": "Not usually reliable",
    "E": "Unreliable",
    "F": "Reliability cannot be judged",
}

CREDIBILITY_DESCRIPTIONS = {
    "1": "Confirmed by other sources",
    "2": "Probably true",
    "3": "Possibly true",
    "4": "Doubtfully true",
    "5": "Improbable",
    "6": "Truth cannot be judged",
}


def display_value(
    value: object | None,
    fallback: str = "Not specified",
) -> str:
    if value is None:
        return escape(fallback)

    normalized_value = str(value).strip()

    if not normalized_value:
        return escape(fallback)

    return escape(normalized_value)


def build_source_evaluation(
    note: models.IntelligenceNote,
) -> str:
    reliability = note.reliability
    credibility = note.credibility

    if not reliability and not credibility:
        return "Not evaluated"

    reliability_code = reliability or "—"
    credibility_code = credibility or "—"

    evaluation_code = (
        f"{reliability_code}{credibility_code}"
    )

    reliability_description = (
        RELIABILITY_DESCRIPTIONS.get(
            reliability,
            "Not evaluated",
        )
        if reliability
        else "Not evaluated"
    )

    credibility_description = (
        CREDIBILITY_DESCRIPTIONS.get(
            credibility,
            "Not evaluated",
        )
        if credibility
        else "Not evaluated"
    )

    return (
        f"{escape(evaluation_code)} — "
        f"{escape(reliability_description)}; "
        f"{escape(credibility_description)}"
    )


def build_note_report(
    note: models.IntelligenceNote,
) -> str:
    classification = (
        note.classification or "UNCLASSIFIED"
    )

    title = display_value(
        note.title,
        "Untitled Intelligence Note",
    )

    body = display_value(
        note.body,
        "No intelligence narrative was recorded.",
    )

    source_evaluation = build_source_evaluation(
        note
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>{title} · Intel Notes Manager</title>

    <style>
        :root {{
            --ink: #17151d;
            --muted: #696573;
            --border: #d7d2df;
            --panel: #f6f4f9;
            --purple: #6f42d8;
            --purple-light: #eee8ff;
            --warning: #8a5a00;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            background: #ece9f1;
            color: var(--ink);
            font-family:
                Arial,
                Helvetica,
                sans-serif;
            line-height: 1.55;
        }}

        .report {{
            width: min(950px, calc(100% - 2rem));
            margin: 2rem auto;
            padding: 2.5rem;
            background: white;
            box-shadow:
                0 18px 50px rgba(24, 18, 35, 0.15);
        }}

        .classification-banner {{
            padding: 0.5rem;
            border: 1px solid var(--border);
            background: var(--panel);
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-align: center;
        }}

        .report-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 2rem;
            margin: 2rem 0;
            padding-bottom: 1.5rem;
            border-bottom: 3px solid var(--purple);
        }}

        .eyebrow {{
            margin: 0 0 0.5rem;
            color: var(--purple);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.16em;
        }}

        h1 {{
            margin: 0;
            font-size: 2rem;
            line-height: 1.15;
        }}

        .record-id {{
            flex-shrink: 0;
            color: var(--muted);
            font-size: 0.82rem;
            text-align: right;
        }}

        .record-id strong {{
            display: block;
            color: var(--ink);
            font-size: 1rem;
        }}

        .metadata-grid {{
            display: grid;
            grid-template-columns:
                repeat(3, minmax(0, 1fr));
            gap: 0.85rem;
            margin-bottom: 1.5rem;
        }}

        .metadata-field {{
            min-height: 5.6rem;
            padding: 0.9rem;
            border: 1px solid var(--border);
            border-radius: 0.4rem;
            background: var(--panel);
        }}

        .metadata-field span {{
            display: block;
            margin-bottom: 0.35rem;
            color: var(--muted);
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .metadata-field strong {{
            font-size: 0.9rem;
        }}

        .narrative {{
            margin-bottom: 1.5rem;
            padding: 1.25rem;
            border-left: 4px solid var(--purple);
            background: var(--purple-light);
        }}

        .narrative h2,
        .source-evaluation h2 {{
            margin: 0 0 0.75rem;
            font-size: 0.8rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .narrative p {{
            margin: 0;
            white-space: pre-wrap;
        }}

        .source-evaluation {{
            margin-bottom: 1.5rem;
            padding: 1rem;
            border: 1px solid var(--border);
            border-radius: 0.4rem;
        }}

        .source-evaluation p {{
            margin: 0;
        }}

        .development-warning {{
            margin: 1.5rem 0;
            padding: 0.85rem;
            border: 1px solid #d6a64e;
            background: #fff8e8;
            color: var(--warning);
            font-size: 0.78rem;
        }}

        .report-footer {{
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 0.72rem;
        }}

        .print-button {{
            position: fixed;
            right: 1.25rem;
            bottom: 1.25rem;
            min-height: 2.8rem;
            padding: 0.7rem 1rem;
            border: 0;
            border-radius: 0.5rem;
            background: var(--purple);
            color: white;
            font-weight: 750;
            cursor: pointer;
            box-shadow:
                0 12px 28px rgba(78, 45, 155, 0.3);
        }}

        @media (max-width: 750px) {{
            .report {{
                width: 100%;
                margin: 0;
                padding: 1.25rem;
            }}

            .report-header {{
                flex-direction: column;
            }}

            .record-id {{
                text-align: left;
            }}

            .metadata-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        @media print {{
            @page {{
                margin: 0.55in;
            }}

            body {{
                background: white;
            }}

            .report {{
                width: 100%;
                margin: 0;
                padding: 0;
                box-shadow: none;
            }}

            .print-button {{
                display: none;
            }}

            .metadata-field,
            .narrative,
            .source-evaluation {{
                break-inside: avoid;
            }}
        }}
    </style>
</head>

<body>
    <main class="report">
        <div class="classification-banner">
            {display_value(classification)}
        </div>

        <header class="report-header">
            <div>
                <p class="eyebrow">
                    INTELLIGENCE NOTE REPORT
                </p>

                <h1>{title}</h1>
            </div>

            <div class="record-id">
                Record Identifier
                <strong>INM-{note.id:06d}</strong>
            </div>
        </header>

        <section class="metadata-grid">
            <div class="metadata-field">
                <span>Reporting Date</span>
                <strong>
                    {display_value(note.date)}
                </strong>
            </div>

            <div class="metadata-field">
                <span>Classification</span>
                <strong>
                    {display_value(note.classification)}
                </strong>
            </div>

            <div class="metadata-field">
                <span>Intelligence Discipline</span>
                <strong>
                    {display_value(note.discipline)}
                </strong>
            </div>

            <div class="metadata-field">
                <span>Source</span>
                <strong>
                    {display_value(note.source)}
                </strong>
            </div>

            <div class="metadata-field">
                <span>Location</span>
                <strong>
                    {display_value(note.location)}
                </strong>
            </div>

            <div class="metadata-field">
                <span>Tags</span>
                <strong>
                    {display_value(note.tags, "None")}
                </strong>
            </div>
        </section>

        <section class="source-evaluation">
            <h2>Source Evaluation</h2>
            <p>{source_evaluation}</p>
        </section>

        <section class="narrative">
            <h2>Intelligence Narrative</h2>
            <p>{body}</p>
        </section>

        <aside class="development-warning">
            <strong>Development Environment:</strong>
            This report is generated by a development application.
            Do not use the system to store or process classified,
            controlled, personally identifiable, operational, or
            otherwise sensitive information.
        </aside>

        <footer class="report-footer">
            <span>
                Intel Notes Manager · Version 2.0.0
            </span>

            <span>
                CIN Entertainment
            </span>
        </footer>

        <div class="classification-banner">
            {display_value(classification)}
        </div>
    </main>

    <button
        class="print-button"
        type="button"
        onclick="window.print()"
    >
        Print / Save as PDF
    </button>
</body>
</html>
"""