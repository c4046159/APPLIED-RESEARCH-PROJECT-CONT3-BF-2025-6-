## Design Freeze of the Applied Research Project Streamlit application (streamlit_app.py, research_results.py, google_drive.py)

Date: 13/09/2026
Comments: 

The current Streamlit user interface is now frozen as the design baseline for the Applied Research Project prototype.

No further aesthetic redesign is planned. From this point onward, interface changes should only be made when they are necessary for one of the following reasons:

- correcting a functional bug;
- addressing an accessibility issue;
- supporting a research-method requirement;
- presenting new experimental information that is necessary for the study;
- maintaining compatibility with Streamlit or the external AI APIs.

Purely cosmetic changes should be avoided so that the prototype remains stable during the experimental phase.

## Research rationale

Freezing the design improves experimental stability. Both chatbot conditions now use the same interface structure and visual treatment, reducing the risk that later presentation changes introduce unnecessary variation into the comparison.

Subsequent development was restricted to research functionality rather than presentation. The permitted additions were the shared engineering-document source, common grounded prompting, response-time measurement, result capture, TESTS and METRICS instrumentation and Google Drive CSV evidence storage.

## Related documentation

- `UI_THEME_NOTES.md` records the design inspiration, colour choices, typography decisions and attribution.
- `PROJECT_LOG.md` records the development history, provider trials, scope reduction, interface refinement and SHU-inspired theme implementation.

This file marks the point at which the visual design is considered complete for the purposes of the research prototype.

## Final freeze status - 26 September 2026

The design freeze remains in force.

Since the original freeze, the following functional additions were accepted because they were required by the research method rather than for aesthetics:

- shared Google Drive PDF grounding;
- source-reference display;
- lazy Drive loading to prevent startup blocking;
- TESTS and METRICS result capture;
- model/API latency display;
- manual scoring controls;
- local CSV export;
- timestamped Google Drive CSV saving.

The comparative chatbot presentation itself remains visually equivalent between Gemini and Cohere.

The final experiment must not introduce further cosmetic changes. Only a defect that prevents valid data collection, scoring, evidence preservation or API operation justifies a code change during the formal run, and any such change must be recorded in `PROJECT_LOG.md`.

