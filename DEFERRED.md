# Deferred

Things deliberately taken off the site, or never put on it, because the material
we have right now isn't good enough — **not** because they're wrong or finished.
Each entry records what was removed, why, and what would let us bring it back.

Review this when new papers, figures, or artwork land.

---

## Research pillar: "Loss Functions for Ag"

**Removed** 2026-09-12 from `research.html`. The writing is good and the theme is
real — it was pulled because the only figure we could pair with it (Information
FOMO) doesn't actually illustrate loss-function design, and a pillar with
mismatched artwork reads worse than no pillar.

Restore verbatim:

```html
        <article class="pillar">
          <div class="pillar-text">
            <h2>Loss Functions for Ag</h2>
            <p>
              Mean-squared error is rarely the best objective for agricultural
              design. We develop loss functions that focus learning on what
              matters most: rare discoveries, cell-type specificity, and
              targeted populations or alleles. The goal is to learn what we
              need for actionable design, not everything possible.
            </p>
          </div>
          <div class="pillar-media" aria-hidden="true">
            <span>Image Placeholder</span>
          </div>
        </article>
```

**Bring it back when:** there's a figure from the actual loss-function work —
the CV lists rare-event loss functions and disease-resistance-preserving loss
functions (AI-Driven Drug Discovery Summit 2024, PAG 2024), and the
output-weighted sampling material in `~/Downloads` may hold one. Insert it
between "Active Learning for Ag" and "Agents for Ag Design".

## Research pillar: "Agents for Ag Design" — artwork resolved

The pillar uses the AgCRADLE workflow graphic. Ethan supplied a 2556×1084
original on 2026-09-12, replacing the 832×357 copy scraped from the VIPR team
page, so it is now readable when enlarged. Nothing outstanding.

It briefly used the PEAgent figure (`images/pubpic/yao2026peagent.png`). **That
was wrong:** despite the name, PEAgent is a framework and web portal for training
and interpreting sequence models — there is no agent in it. Don't reuse it here.

## Publications left off the site

Five works OpenAlex lists that Ethan chose not to publish (2026-09-12). They're
in `EXCLUDED_DOIS` in `scripts/pubs_sync.py`; delete an entry there to start
reporting it again.

| Year | Work | DOI |
|---|---|---|
| 2024 | Nonlinear Interactions in Non-Resonant, Homogeneous Turbulent Jets | `10.2514/6.2024-3414` |
| 2024 | Resolvent Modeling of Subsonic Jet Noise | `10.2514/6.2024-3199` |
| 2020 | Data analytics applied to office building electricity consumption | `10.1080/17512549.2020.1730239` |
| 2019 | Furthering resolvent-based jet noise models (abstract) | `10.1121/1.5137546` |
| 2018 | Resolvent analysis for jet noise source identification (abstract) | `10.1121/1.5067573` |

## Publication removed: Two-point measurements (AIAA 2023)

**Removed** 2026-09-12 from `publications.html`, along with the 2023 year section
it was alone in. Not a quality judgement on the paper — we simply cannot host it.
`arc.aiaa.org` returns **403** to direct download and there is no arXiv preprint,
so it was the only entry on the site with no PDF and no figure.

Its DOI is in `EXCLUDED_DOIS` in `scripts/pubs_sync.py`; delete that line to start
reporting it again.

**Bring it back when:** Ethan supplies the PDF. Then restore the markup below,
recreate the `<section class="pub-year"><h2>2023</h2>` wrapper around it, crop a
figure per `.claude/skills/publications-page/SKILL.md`, and drop the
`pub-item-nofigure` class.

```html
  <article class="pub-item pub-item-nofigure">
    <div class="pub-meta">
      <h3>Two-point measurements on the acoustic field of subsonic turbulent jets</h3>
      <p class="pub-authors">B. Gramiscelli Hasparyk, P. Jordan, A. Lebedev, L. Lesshafft, E. Pickering, T. Colonius</p>
      <p class="pub-venue">AIAA AVIATION 2023 Forum, 4290 (2023)</p>
      <div class="pub-links">
        <a href="https://doi.org/10.2514/6.2023-4290" target="_blank" rel="noreferrer">DOI</a>
      </div>
      <details>
        <summary>Abstract</summary>
        <p>
          Two-point acoustic measurements are made for subsonic, isothermal turbulent jets over a range of
          Mach numbers, spanning from 0.4 to 0.9. The measurements are made using two antennae, each with
          18 azimuthally distributed microphones, that can be independently displaced in the streamwise
          direction. The measurement system is used to construct CSD matrices of the sound field for each
          Mach number. We report a detailed analysis of the two-point structure of the sound field, which
          is decomposed using a Fourier series in azimuth, Fourier transform in time, and Spectral Proper
          Orthogonal Decomposition in the inhomogeneous streamwise direction. Analysed in this way, Mach-
          and Strouhal-number dependencies of the low-rank structure of the sound field are explored.
          Based on Crow’s model [1], we use a wavepacket source to explore features of the axisymmetric
          mode of the radiated sound. The model considers all components of Lighthill’s stress tensor to
          understand the physics behind the observed trends, and this suggests a modification to Crow’s
          wavepacket. The model proposed reproduces qualitatively some of the different scalings observed
          at low and high polar angles.
        </p>
      </details>
    </div>
  </article>
```

## Repository size

Measured 2026-09-12: published site ~240 MB against GitHub Pages' **1 GB hard
limit**; repo 477 MB on disk against a 1 GB recommendation; `.git` alone 237 MB.
`papers/` is 188 MB, 78% of what we publish. History grows monotonically -
replaced and recompressed PDFs keep their old blobs forever.

**Act when:** the repo passes ~700 MB. Two options, neither urgent:

1. Stop hosting PDFs that are one DOI or arXiv click away. Dropping the six
   largest reclaims ~90 MB of the published site. Costs readers a click.
2. Rewrite history to purge superseded blobs, reclaiming most of `.git`. This
   rewrites every commit SHA on a public repo - only on an explicit ask.

## Cosmetic debt

- **Headshot aspect ratios.** `.person-photo img` is `height: auto`, so Roth
  Conrad's landscape photo renders short and wide beside the square ones. Fix is
  `aspect-ratio: 1; object-fit: cover` on `.person-photo img`, or re-crop the
  source square. Proposed, not applied — it changes every card at once.
- **David Uzor's headshot** is only 200×200 and looks soft; a larger original
  would help.
- **`towne2022efficient.pdf` is 17MB.** Ghostscript can't shrink it because the
  bulk is vector figure geometry, and rasterizing would wreck the figures. Either
  accept it or drop the local copy and rely on the DOI.

## Person facts not yet supplied

`.person-facts` (degree, institution, start year) is omitted for Olatunde
Akanbi, Roth Conrad, Ashmita Upadhyay, Phong Nguyen, and David Uzor because
those facts were never given. Don't infer them — ask, then add.
