# Design Freeze - Applied Research Project Prototype

Date: 13 September 2026

## Decision

The current Streamlit user interface is now frozen as the design baseline for the Applied Research Project prototype.

No further aesthetic redesign is planned. From this point onward, interface changes should only be made when they are necessary for one of the following reasons:

- correcting a functional bug;
- addressing an accessibility issue;
- supporting a research-method requirement;
- presenting new experimental information that is necessary for the study;
- maintaining compatibility with Streamlit or the external AI APIs.

Purely cosmetic changes should be avoided so that the prototype remains stable during the experimental phase.

## Frozen visual baseline

The frozen interface includes:

- the module title `APPLIED RESEARCH PROJECT (CONT3 BF-2025/6)`;
- module code `55-709708-BF-20256`;
- student identification information;
- project overview and usage guidance;
- the non-commercial academic research disclaimer;
- two final chatbot tabs only;
- Chatbot A: Google Gemini 3.5 Flash-Lite;
- Chatbot B: Cohere Command A+ (`command-a-plus-05-2026`);
- consistent bordered interaction panels;
- assistant chat-message response presentation;
- visible provider/model information and operational status;
- Sheffield Hallam inspired colour treatment and typography direction;
- Hallam Maroon, Collegiate Crimson and Hallam Pink accent treatment;
- light background, restrained borders and approximately 16px base typography;
- visual attribution clarifying that the design is inspired by Sheffield Hallam University's online site and public brand guidance but is not an official University application.

## Research rationale

Freezing the design improves experimental stability. Both chatbot conditions now use the same interface structure and visual treatment, reducing the risk that later presentation changes introduce unnecessary variation into the comparison.

The next development work should focus on research functionality rather than presentation, particularly the shared engineering-document source, consistent prompting, response-time measurement, output capture and formal evaluation.

## Related documentation

- `UI_THEME_NOTES.md` records the design inspiration, colour choices, typography decisions and attribution.
- `PROJECT_LOG.md` records the development history, provider trials, scope reduction, interface refinement and SHU-inspired theme implementation.

This file marks the point at which the visual design is considered complete for the purposes of the research prototype.
