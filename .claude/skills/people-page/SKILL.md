---
name: people-page
description: Add or update lab members on people.html - card anatomy, how the sections are ordered, role and affiliate conventions, headshot handling, and the rule about never inventing biographical facts. Use whenever someone joins, leaves, or changes role.
---

# people.html

Read `site-conventions` first.

## Section order

1. **(PI, unlabelled section)** - Ethan, `<h2>` name, `.person-links` row (CV,
   GitHub, LinkedIn, Google Scholar, ResearchGate), bio as plain `<p>`.
2. **Lab Members** - postdocs.
3. **Graduate Students**
4. **Undergraduate Researchers**

Everyone below the PI uses `<h3>` and a `<details><summary>Biography</summary>` block.

**Group people by what they do, not by their employment relationship.** Roth and
Ashmita were originally filed under a separate "Affiliates" heading, which buried
their actual roles; Ethan asked for them to sit with their peers with the
affiliation noted instead. Follow that pattern.

## Card anatomy

```html
        <article class="person-card">
          <div class="person-photo">
            <img src="images/people/<first-last>.jpg" alt="Full Name" />
          </div>
          <div class="person-meta">
            <h3>Full Name</h3>
            <p class="person-role">Postdoctoral Scholar</p>
            <ul class="person-facts">
              <li>Ph.D., Institution</li>
              <li>Started: YEAR</li>
            </ul>
            <details>
              <summary>Biography</summary>
              <p>...</p>
            </details>
          </div>
        </article>
```

### Role line

`Postdoctoral Scholar` | `Ph.D. Student` | `Undergraduate Researcher`, comma-
suffixed for affiliates, matching the PI's `Associate Professor, Principal
Investigator` style:

- `Postdoctoral Scholar, Affiliate`
- `Ph.D. Student, Affiliate`

For an affiliate, put their home lab in `.person-facts` **and** name it in the
first sentence of the bio, so the card reads correctly on its own. Ashmita
Upadhyay is the worked example: Josh Clevenger Lab at HudsonAlpha
(<https://www.hudsonalpha.org/faculty/josh-clevenger/>), affiliate member here.

### `.person-facts` is optional - omit it rather than guess

Degree and start year are only listed where Ethan supplied them. Four of the five
members added in Sept 2026 have no facts list because those facts were never
given. **Do not infer a degree, institution, or start date** from an offer letter,
a paper, or a name. Ask.

## Biographies

Ethan supplies a one-or-two-sentence description of the work; expand it into a
paragraph that names the methods and then the point of them, in the voice of the
existing cards (third person, concrete, no hype). Stay strictly inside the facts
given - no invented education history, prior institutions, or awards.

## Headshots

- `images/people/<first-last>.<ext>`, kebab-case. Source files arrive in
  `~/Downloads` with names like `Roth_Conrad_Headshot.jpg`.
- `chmod 644` after copying - some arrive mode 600 and would 404.
- **Crop square before adding.** `.person-photo img` is `height: auto`, so a
  landscape photo renders short and wide next to square ones (visible on Roth
  Conrad's card). The alternative fix is `aspect-ratio: 1; object-fit: cover` on
  `.person-photo img`, which has been proposed but not applied.
- Check the pixel size; David Uzor's photo is only 200x200 and looks soft.

`check_site.py` verifies every card has a `.person-role` and a photo that exists.
