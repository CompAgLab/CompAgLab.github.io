---
name: home-page
description: Edit index.html, the CompAgLab landing page - the background-video pattern, the hero panel, and the recruiting and location copy that needs periodic review. Use when changing the homepage message, hero text, or background media.
---

# index.html

Read `site-conventions` first. The shortest page in the repo and the only one
with a `.hero`.

## Structure

```html
<body class="page-home">
  <div class="site-background" aria-hidden="true">
    <video autoplay muted loop playsinline poster="images/hero/soy-poster.jpg">
      <source src="videos/soy-background.mp4" type="video/mp4" />
    </video>
  </div>
  <header class="site-header"> ... nav ... </header>
  <main>
    <section class="hero">
      <div class="hero-content content-panel"> ... </div>
    </section>
  </main>
</body>
```

## Background video pattern

Shared with `people.html`, which uses `corn-sunset.mp4` / `corn-sunset-poster.jpg`.
Every background video needs:

- a `poster` still in `images/hero/` - it is what shows before the video loads and
  on devices that refuse autoplay, so it must look right on its own;
- `autoplay muted loop playsinline` (drop `muted` or `playsinline` and iOS will
  not autoplay);
- `aria-hidden="true"` on the wrapper - it is decoration, not content.

`videos/soy-background.mp4` is 8MB, `corn-sunset.mp4` 1MB. Keep new loops near the
smaller end; this is the first thing a visitor downloads.

## Copy that goes stale

The hero carries three things worth re-reading whenever the lab changes:

1. the guiding question (italicised);
2. **the recruiting paragraph** - currently actively recruiting PhD students and
   postdocs. Take it down when that stops being true;
3. the department/college/university line.

Nav order is Home, Research, People, Publications on all four pages, with
`aria-current="page"` on the current one - update every page if it changes.
