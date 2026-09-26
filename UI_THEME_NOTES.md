# UI Theme Notes - Sheffield Hallam Inspired Research Prototype

Date: 13 September 2026

## Purpose

The Streamlit interface uses Sheffield Hallam University's online website and publicly available brand guidance as visual inspiration. The aim is to make the prototype feel academically connected to the module and institution while remaining clearly identifiable as an independent student research artefact.

The prototype is not an official Sheffield Hallam University application, website, sub-brand or commercial service.

## Sources used for visual inspiration

1. Sheffield Hallam Online website: `https://online.shu.ac.uk/`
2. Public Sheffield Hallam University brand guidelines, particularly the colour and typeface guidance.
3. Browser-inspected CSS supplied during development from the Sheffield Hallam Online website.

## Extracted online-site design characteristics

The inspected website CSS showed the following useful interface characteristics:

- Body text size: approximately 16px / 1rem.
- Body line height: approximately 1.5rem.
- Body text colour: approximately `#445063` (`rgb(68, 80, 99)`).
- Sans-serif typography.
- White page background and restrained spacing.
- Border-box sizing and clean, modern content blocks.

The extracted CSS also contained generic WordPress preset colours, Tailwind utility variables, browser reset rules and preset gradients. These were not treated as Sheffield Hallam visual identity and were not copied into the Streamlit prototype.

## Sheffield Hallam public brand colours used

The current public Sheffield Hallam brand guidance identifies the following relevant colours:

- Hallam Maroon: `#672146`
- Collegiate Crimson: `#AC145A`
- Hallam Pink: `#E31C79`
- Peaks Pink: `#F4CDD4`
- Sheffield Steel: `#5B6770`
- HUBS Silver: `#D0D3D4`

The prototype uses Hallam Maroon as the main Streamlit interactive colour, Collegiate Crimson and Hallam Pink as secondary accents, HUBS Silver for borders, and the extracted online-site body colour `#445063` for general text.

## Typography decision

Sheffield Hallam's public brand guidance identifies Meta Pro as the primary font and Arial as the alternative when Meta is not available. Meta Pro is proprietary and is not bundled, copied or redistributed by this project.

The Streamlit application therefore uses a standard sans-serif configuration, following the same accessible typographic direction without distributing or embedding Sheffield Hallam font files.

## Streamlit theme implementation

The project-level `.streamlit/config.toml` defines:

- Light theme.
- Hallam Maroon primary colour.
- White application background.
- Very light neutral secondary surface.
- `#445063` text.
- Collegiate Crimson links.
- HUBS Silver borders.
- 16px base font size.
- Small border radius and visible widget borders.

The application header also includes a simple three-part accent strip using Hallam Maroon, Collegiate Crimson and Hallam Pink. Primary chatbot buttons inherit the Hallam Maroon application accent.

## Accessibility and restraint

The design intentionally avoids copying the University logo, creating a new Sheffield Hallam sub-brand, embedding proprietary fonts, or reproducing the website layout exactly. It also avoids unnecessary gradients and decorative effects from generic WordPress presets.

The visual approach is deliberately restrained so that the interface remains a research instrument. Both chatbot conditions retain the same layout, spacing and interaction pattern to avoid introducing an unnecessary user-interface difference into the comparison.

## Attribution shown in the application

The prototype states that its visual theme is inspired by Sheffield Hallam University's online website and publicly available brand guidance and that it remains an independent student research prototype rather than an official University digital service.


## Final interface status - 26 September 2026

The visual design remains frozen. Later changes were functional research additions rather than aesthetic redesigns.

The final top-level interface contains three tabs:

- **Chatbot A** - Google Gemini 3.5 Flash-Lite.
- **Chatbot B** - Cohere Command A+.
- **TESTS and METRICS** - result capture, latency summaries, manual scoring, CSV export/Drive save and Google Drive corpus checks.

Both chatbot conditions continue to use the same visual structure and interaction treatment. The addition of the TESTS and METRICS tab does not change the comparative presentation of A and B; it exposes the research instrumentation required by the final empirical study.

The final application also displays retrieved document-source filenames beneath grounded answers. This is treated as research evidence/provenance rather than a visual redesign.

No further cosmetic changes are planned before submission. Any remaining interface change should be limited to a defect that prevents valid testing or evidence capture.

