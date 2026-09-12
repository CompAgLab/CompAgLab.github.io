---
name: research-page
description: Edit research.html, the CompAgLab research pillars page - pillar anatomy and the unfilled image placeholders each pillar still carries. Use when adding, reordering, or rewriting a research theme, or when supplying pillar artwork.
---

# research.html

Read `site-conventions` first.

## Pillar anatomy

```html
        <article class="pillar">
          <div class="pillar-text">
            <h2>Theme name</h2>
            <p>Two to four sentences.</p>
          </div>
          <div class="pillar-media" aria-hidden="true">
            <span>Image Placeholder</span>
          </div>
        </article>
```

Current pillars, in order: **LLMs for Editing**, **Mechanistic Ag AI**,
**Active Learning for Ag**, **Loss Functions for Ag**, **Agents for Ag Design**.

`.research-pillars` is a flex column with `gap: 22px` - pillars stack, so order in
the file is order on the page.

## Every pillar still shows "Image Placeholder"

All five `.pillar-media` divs are literal placeholder spans. When artwork arrives,
replace the `<span>` with an `<img>`, put the file in `images/` (a
`images/research/` subdirectory would match the `images/people/` and
`images/pubpic/` convention), and **remove `aria-hidden="true"`** from the wrapper
once it holds real content, adding a descriptive `alt`.

A good source of pillar artwork is the papers themselves - see
`publications-page` for the Ghostscript-render-then-crop recipe, which produces
clean figures at 760px wide.

## Writing a pillar

Match the existing voice: what the lab builds, then what it is for. Keep each to
one paragraph - the page is a scan, not a read. Each pillar should map to real
work; cross-check against `publications.html` so the themes and the papers agree.
