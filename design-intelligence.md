# Design Intelligence Standard

**A corpus-wide synthesis of 73 company `DESIGN.md` systems from VoltAgent's `awesome-design-md` collection.**

Version: 1.0  
Status: Reference standard  
Recommended repository path: `docs/standards/design-intelligence.md`

---

## 1. Purpose

This document converts a large collection of company-specific design analyses into one reusable, high-level design intelligence standard.

It is intended to help product teams and AI coding agents:

- recognise recurring design principles;
- select an appropriate visual archetype;
- build a coherent product-specific `DESIGN.md`;
- avoid generic AI-generated interfaces;
- adapt inspiration without copying another company's brand;
- define layouts, colours, typography, buttons, components, motion, and responsive behaviour consistently.

This is not a replacement for approved client brand guidelines.

```text
Client brand
→ Product requirements
→ Product-specific DESIGN.md
→ VLCO enterprise standards
→ External design references
```

---

## 2. Source and Method

The synthesis covers the 73 company design profiles available in:

- Repository: `VoltAgent/awesome-design-md`
- Collection path: `design-md/`
- Repository licence at review: MIT
- Review date: 2026-08-04

The collection uses a recurring structure covering:

1. Visual theme and atmosphere
2. Colour palette and roles
3. Typography
4. Components
5. Layout
6. Depth and elevation
7. Do and do not rules
8. Responsive behaviour
9. Agent guidance

### Interpretation rule

This document distinguishes two layers:

- **Corpus finding:** a recurring pattern observed across the design profiles.
- **Normalised standard:** a practical reusable rule inferred from those patterns for enterprise product delivery.

The normalised standards are synthesis and engineering judgement. They are not claims that every company uses identical values.

### Brand and licensing rule

Use the analysed systems as inspiration and reference.

Do not copy or imply rights to:

- logos;
- trademarks;
- proprietary fonts;
- photography;
- illustrations;
- branded icons;
- product screenshots;
- protected trade dress.

---

# Part I — What the Best Systems Have in Common

## 3. Twelve Universal Principles

### 3.1 One dominant idea

Strong design systems can usually be explained in one sentence.

Examples of dominant ideas include:

- enterprise flatness;
- cinematic product gallery;
- editorial broadsheet;
- dark technical precision;
- friendly marketplace;
- expressive creative canvas;
- luxury reduction.

A weak system attempts to communicate multiple conflicting personalities simultaneously.

**Normalised standard**

```text
Choose one primary visual idea.
Allow one supporting idea.
Reject incompatible ideas.
```

---

### 3.2 Neutral structure, selective colour

Most mature systems use neutral foundations:

- white, cream, near-black, charcoal, or soft gray canvas;
- two to four text-neutral levels;
- one primary signal colour;
- semantic colours reserved for meaning.

Even expressive brands normally confine multiple colours to illustrations, photography, campaign blocks, or controlled feature sections.

**Normalised standard**

```text
70–90% neutral structure
5–20% brand colour
<10% semantic or decorative colour
```

This is a directional composition rule, not a pixel-count requirement.

---

### 3.3 Colour has a job

The strongest palettes assign roles rather than merely listing hex values.

Typical roles:

```text
Primary action
Primary hover
Primary pressed
Focus ring
Canvas
Surface 1
Surface 2
Primary text
Muted text
Hairline
Success
Warning
Error
Information
On-dark text
On-primary text
```

A colour without a role becomes decoration and eventually creates inconsistency.

---

### 3.4 Typography creates most of the hierarchy

High-quality systems rarely require many font families.

They create hierarchy using:

- scale;
- weight;
- line height;
- letter spacing;
- width and measure;
- case;
- alignment;
- selective mono or serif use.

Common structures:

```text
One sans family
One sans + mono
Display sans + text sans
Display serif + reading serif + metadata sans
```

Three or more unrelated families should require a strong editorial reason.

---

### 3.5 Spacing is systematic

The recurring spacing foundation is based on small increments, most commonly around a 4px or 8px rhythm.

Typical reusable scale:

```text
4
8
12
16
24
32
48
64
96
```

Not every system uses each value, but strong systems repeat a small set instead of inventing spacing for every component.

---

### 3.6 Geometry communicates personality

Border radius is not a universal quality marker. It is a personality decision.

| Geometry | Typical signal |
|---|---|
| 0–4px | Technical, editorial, engineered, institutional |
| 6–12px | Modern product, balanced, operational |
| 14–24px | Friendly consumer, approachable SaaS |
| Full pill | Marketplace, retail, conversational, premium CTA |
| Circles/orbits | Human, connected, editorial, dynamic |
| Mixed but governed | Expressive creative brands |

The error is not using square or rounded components. The error is using every radius without a hierarchy.

---

### 3.7 Components need states, not only appearance

The best systems define:

- default;
- hover;
- focus;
- active or pressed;
- selected;
- disabled;
- loading;
- error;
- success.

A button specification containing only background, text colour, and radius is incomplete.

---

### 3.8 Imagery often carries the emotion

Apple, Tesla, Nike, Airbnb, automotive brands, and retail systems rely on photography to carry emotion while UI chrome stays restrained.

Developer and enterprise systems often replace emotional photography with:

- product screenshots;
- diagrams;
- code;
- dashboards;
- architecture visuals.

**Normalised standard**

Use visual assets that prove the product's value. Do not add decorative imagery merely to fill space.

---

### 3.9 Motion explains relationships

Motion is strongest when it clarifies:

- what changed;
- where an element came from;
- what is interactive;
- what is selected;
- what content belongs together;
- how navigation or hierarchy changed.

Motion is weakest when it introduces:

- constant floating;
- arbitrary parallax;
- glow pulsing;
- long entrance sequences;
- repeated spring effects;
- animation that delays work.

---

### 3.10 Density follows the task

There is no universally correct amount of whitespace.

- Product galleries and luxury brands use large isolated messages.
- Editorial systems use dense information grids.
- Enterprise applications use compact operational layouts.
- Consumer marketplaces use moderate density with large touch targets.
- Developer tools use dense, precise, keyboard-friendly surfaces.

A management dashboard should not copy a luxury automotive landing page's density.

---

### 3.11 Contrast is controlled

High-quality systems establish clear polarity:

```text
Light canvas + dark text
Dark canvas + light text
Brand block + approved on-brand text
```

They avoid ambiguous medium-contrast combinations for important content.

---

### 3.12 Restraint creates identity

A recognisable brand often comes from repeated restraint:

- one accent;
- one radius strategy;
- one dominant composition;
- one display voice;
- one recurring image treatment;
- one motion pattern.

Adding more styling does not necessarily create more identity.

---

# Part II — Design Archetypes

## 4. Archetype Selection

Choose one primary archetype based on product, user, task, and brand.

### 4.1 Enterprise Structured

**Reference patterns:** IBM, HashiCorp, ClickHouse, HP

Use for:

- governance platforms;
- operations systems;
- B2B administration;
- finance operations;
- compliance tools;
- management reporting.

Characteristics:

- white or soft-gray canvas;
- square or lightly rounded surfaces;
- strong grid;
- restrained colour;
- visible hairlines;
- high information density;
- predictable navigation;
- direct language.

Avoid:

- oversized decorative cards;
- excessive pills;
- cinematic empty space;
- ambiguous controls.

---

### 4.2 Dark Technical Precision

**Reference patterns:** Linear, Vercel, Resend, Supabase, Cursor, Warp, VoltAgent

Use for:

- developer tools;
- technical infrastructure;
- monitoring;
- APIs;
- engineering interfaces.

Characteristics:

- near-black canvas;
- layered charcoal surfaces;
- one cool accent;
- code or mono details;
- hairline borders;
- compact controls;
- product screenshots;
- subtle motion.

Avoid:

- low-contrast gray-on-gray text;
- neon on every component;
- glow as a substitute for hierarchy.

---

### 4.3 Data-Dense Operational

**Reference patterns:** Kraken, Sentry, Airtable, ClickHouse

Use for:

- dashboards;
- exception management;
- analytics;
- trading;
- risk operations;
- operational command centres.

Characteristics:

- compact spacing;
- strong table structure;
- status semantics;
- filters and toolbars;
- drill-down;
- stable navigation;
- clear selection states.

Avoid:

- fake charts;
- KPI cards without source and drill-down;
- using cards for every row of data.

---

### 4.4 Editorial Authority

**Reference patterns:** WIRED, The Verge, Runway, Sanity

Use for:

- research;
- thought leadership;
- media;
- long-form reports;
- knowledge platforms.

Characteristics:

- deliberate text measure;
- display/body contrast;
- strong section bands;
- rule lines;
- image-caption discipline;
- dense but readable rhythm.

Avoid:

- app-style card grids for long-form reading;
- narrow mono body copy;
- excessive floating UI.

---

### 4.5 Product Gallery Minimalism

**Reference patterns:** Apple, Tesla, SpaceX, Meta

Use for:

- premium physical products;
- product launches;
- high-quality visual portfolios;
- focused product storytelling.

Characteristics:

- product-first imagery;
- minimal chrome;
- one message per section;
- limited CTA hierarchy;
- large composition;
- restrained colour.

Avoid:

- using this style for complex workflows;
- hiding navigation required for operational work;
- large empty sections without strong imagery.

---

### 4.6 Friendly Marketplace

**Reference patterns:** Airbnb, Intercom, Wise, Starbucks

Use for:

- marketplaces;
- employee platforms;
- service discovery;
- customer-facing financial products;
- onboarding journeys.

Characteristics:

- warm canvas;
- friendly brand signal;
- moderate rounding;
- large touch targets;
- clear search;
- approachable copy;
- human imagery.

Avoid:

- infantilising enterprise users;
- decorative rounding without functional hierarchy.

---

### 4.7 Expressive Creative

**Reference patterns:** Figma, Miro, Framer, Clay, Lovable

Use for:

- creative tools;
- workshops;
- portfolio experiences;
- collaborative canvases;
- maker platforms.

Characteristics:

- monochrome structural frame;
- controlled colourful blocks;
- expressive composition;
- selective motion;
- playful but consistent component language.

Avoid:

- applying every colour simultaneously;
- novelty that damages task clarity.

---

### 4.8 Financial Trust

**Reference patterns:** Stripe, Mastercard, Coinbase, Wise

Use for:

- payments;
- embedded finance;
- lending;
- financial infrastructure;
- customer money journeys.

Characteristics:

- calm information hierarchy;
- strong numeric typography;
- clear action states;
- trustworthy neutral base;
- one recognisable accent;
- transparent disclosures;
- careful semantic colour.

Avoid:

- speculative visual language;
- untraceable values;
- decorative financial charts;
- inaccessible status colours.

---

### 4.9 Performance and Luxury

**Reference patterns:** Ferrari, Lamborghini, Bugatti, BMW M, Nike

Use for:

- premium launches;
- performance brands;
- high-end campaigns;
- limited product storytelling.

Characteristics:

- dramatic contrast;
- monumental display type;
- black or image-led surfaces;
- very limited accent colour;
- controlled motion;
- high-quality photography.

Avoid:

- copying this intensity into routine enterprise workflows;
- using luxury minimalism to hide missing information.

---

### 4.10 Retro and Nostalgic

**Reference patterns:** Dell 1996, Nintendo 2001

Use for:

- deliberate period experiences;
- campaign microsites;
- cultural or archival storytelling.

Characteristics:

- era-specific type;
- bevels, badges, textures, GIF-like details;
- intentionally dense layouts;
- historical colour logic.

Avoid:

- accidental retro caused by poor spacing or outdated defaults;
- using nostalgia for accessibility-critical workflows without adaptation.

---

# Part III — The Normalised Design System

## 5. Colour Architecture

### 5.1 Required token groups

```yaml
color:
  brand:
    primary:
    hover:
    pressed:
    soft:
    on-primary:
  canvas:
    default:
    subtle:
    inverse:
  surface:
    1:
    2:
    3:
    elevated:
  text:
    primary:
    secondary:
    muted:
    inverse:
    link:
  border:
    subtle:
    default:
    strong:
    focus:
  semantic:
    success:
    warning:
    error:
    information:
```

### 5.2 Palette rules

1. Define one primary action colour.
2. Do not use the primary action colour decoratively across all surfaces.
3. Separate semantic colours from brand colours.
4. Define light and dark text explicitly.
5. Define hover and pressed states rather than calculating them ad hoc.
6. Ensure charts have an independent, accessible categorical palette.
7. Use gradients only when they are part of the chosen archetype.
8. Keep the default application surface calmer than marketing surfaces.

### 5.3 Gradient guidance

Common appropriate uses:

- hero atmosphere;
- campaign transitions;
- creative-tool storytelling;
- premium fintech marketing;
- visual separation between large sections.

Avoid gradients on:

- routine form controls;
- tables;
- status badges;
- every card;
- critical operational actions;
- body text.

### 5.4 Dark mode

Dark mode is a complete polarity system, not canvas inversion.

Define:

- dark canvas;
- at least three dark surfaces;
- primary and secondary text;
- muted text;
- borders;
- focus ring;
- image treatment;
- chart colours;
- semantic colours;
- shadow or edge strategy.

---

## 6. Typography

### 6.1 Recommended hierarchy

| Role | Typical range | Purpose |
|---|---:|---|
| Display | 48–96px | Marketing or major storytelling |
| H1 | 36–64px | Page identity |
| H2 | 28–48px | Major sections |
| H3 | 22–32px | Feature or card groups |
| H4 | 18–24px | Component headings |
| Body large | 17–20px | Lead text |
| Body | 15–17px | Default reading |
| Small | 13–14px | Secondary information |
| Caption | 11–13px | Metadata |
| Mono | 12–14px | Code, identifiers, technical values |

These ranges must be adapted to application density.

### 6.2 Typography rules

- Use display size sparingly.
- Keep body line height approximately 1.4–1.65.
- Keep long-form line length around 55–80 characters.
- Use negative tracking primarily for large display sizes.
- Use uppercase only for short labels or deliberate campaign language.
- Use tabular numerals for financial amounts, dates, KPIs, and tables.
- Use monospace for code, IDs, technical labels, or deliberate contrast—not general body text.
- Prefer variable fonts when available and licensed.
- Document legal fallback fonts.

### 6.3 Weight strategy

A mature system usually needs:

```text
Regular
Medium
Semibold
Optional light display
Optional bold campaign
```

Do not create hierarchy only by making everything bold.

---

## 7. Spacing and Grid

### 7.1 Base scale

```yaml
spacing:
  1: 4px
  2: 8px
  3: 12px
  4: 16px
  5: 24px
  6: 32px
  7: 48px
  8: 64px
  9: 96px
```

### 7.2 Layout widths

Normalised recommendations:

| Content | Suggested width |
|---|---:|
| Long-form reading | 640–760px |
| Form flow | 480–720px |
| Standard marketing container | 1120–1280px |
| Wide product/enterprise container | 1280–1440px |
| Full-bleed media | Viewport width |
| Operational application | Fluid with controlled minimums |

### 7.3 Layout patterns

**Marketing**

```text
Global navigation
Hero
Trust or proof
Problem/benefit
Product demonstration
Feature bands
Customer proof
Pricing or CTA
Footer
```

**Enterprise application**

```text
Global shell
Sidebar or module navigation
Header
Breadcrumbs
Page title and actions
Filter/action bar
Primary operational content
Detail drawer or drill-down
Status and feedback
```

**Editorial**

```text
Masthead
Section navigation
Headline and deck
Hero media
Body measure
Supporting rail
Related stories
Footer
```

### 7.4 Whitespace rule

Whitespace should separate decisions, not merely enlarge pages.

Use more whitespace for:

- brand storytelling;
- premium product presentation;
- new conceptual sections.

Use less whitespace for:

- repeated operational actions;
- tables;
- search results;
- monitoring;
- exception management.

---

## 8. Radius and Shape System

Recommended governed scale:

```yaml
radius:
  none: 0
  small: 4px
  medium: 8px
  large: 12px
  xlarge: 20px
  pill: 9999px
```

Select a dominant radius family:

- engineered: `0 / 4 / 8`;
- balanced product: `4 / 8 / 12`;
- friendly consumer: `8 / 14 / 20 / pill`;
- editorial/luxury: mostly `0`, with selected circles or large media radii;
- expressive: controlled mixed shapes with documented roles.

Do not use large radius on every container.

---

# Part IV — Components

## 9. Buttons

### 9.1 Button hierarchy

Every product should define:

1. Primary
2. Secondary
3. Tertiary or ghost
4. Destructive
5. Icon-only
6. Link action
7. Optional inverse variants

### 9.2 Recommended dimensions

| Context | Height |
|---|---:|
| Compact desktop tool | 32–36px |
| Standard application | 40px |
| Touch-friendly primary | 44–48px |
| Marketing hero | 44–52px |
| Icon-only touch target | Minimum 44×44px |

### 9.3 Button specification

Each button requires:

```text
Role
Label style
Height
Horizontal padding
Radius
Background
Text
Border
Icon placement
Default
Hover
Focus-visible
Pressed
Disabled
Loading
Destructive behaviour
```

### 9.4 Button principles from the corpus

- One button style usually carries the highest-priority action.
- Primary colour is often reserved almost entirely for primary actions.
- Pills suit friendly, retail, marketplace, and premium editorial systems.
- Square or low-radius buttons suit technical, editorial, enterprise, and automotive systems.
- Icon-only buttons need tooltips and accessible names.
- Marketing CTA styling should not automatically become application-control styling.
- Text links remain valuable where a filled button would create excessive weight.

### 9.5 Avoid

- multiple primary buttons in one decision area;
- gradients on routine buttons;
- hover-only meaning;
- low-contrast disabled states that remain clickable;
- icon buttons below accessible target size;
- labels such as “Click here”;
- destructive actions styled as ordinary primary actions.

---

## 10. Cards and Surfaces

### 10.1 Use a card only when it establishes a meaningful boundary

Appropriate card purposes:

- self-contained entity;
- comparison;
- selected plan;
- media story;
- action group;
- summary requiring drill-down;
- separate background or interaction context.

Do not use cards merely because the page has empty space.

### 10.2 Surface hierarchy

```text
Canvas
Surface 1
Surface 2
Selected or highlighted surface
Overlay or modal
Inverse surface
```

### 10.3 Elevation strategy

Choose one primary strategy:

- hairline borders;
- surface-tone contrast;
- shadows;
- opacity/backdrop;
- image depth;
- layering and z-index.

Combining thick borders, heavy shadows, gradients, and glow on every card creates noise.

### 10.4 Enterprise card rule

A KPI card must define:

```text
Metric
Meaning
Period
Source
Freshness
Comparison
Status
Drill-down
Access
```

---

## 11. Navigation

### 11.1 Navigation principles

- Show the user's current location.
- Keep primary navigation stable.
- Use descriptive labels.
- Separate global navigation from page actions.
- Use breadcrumbs for hierarchical enterprise products.
- Keep mobile navigation task-focused.
- Make keyboard traversal predictable.

### 11.2 Common patterns

| Pattern | Best use |
|---|---|
| Top navigation | Marketing, simple SaaS |
| Sidebar | Multi-module enterprise application |
| Command palette | Keyboard-first tools |
| Floating pill navigation | Premium editorial/consumer marketing |
| Mega menu | Broad product portfolio |
| Tabs | Related views within one context |
| Bottom navigation | Small set of mobile-primary actions |

### 11.3 Avoid

- hiding important actions in hover menus;
- changing navigation position between pages;
- mixing product navigation and marketing navigation without hierarchy;
- using icons without labels for unfamiliar modules.

---

## 12. Forms and Inputs

Required input states:

```text
Default
Hover
Focus
Filled
Disabled
Read-only
Error
Success where useful
Loading
```

Principles:

- Labels should remain visible.
- Placeholder text is not a label.
- Error messages should explain correction.
- Use input masks carefully.
- Preserve user input after validation failures.
- Group related fields.
- Use progressive disclosure for advanced options.
- Separate destructive or sensitive fields.
- Provide accessible focus indication.

Financial and governance products should also define:

- source of prefilled values;
- edit permissions;
- maker-checker logic;
- audit trail;
- effective date;
- validation and reconciliation.

---

## 13. Tables, Lists, and Data

Operational systems should treat tables as primary interface components.

Required capabilities where relevant:

- sorting;
- filtering;
- search;
- column visibility;
- pagination or virtualisation;
- row selection;
- bulk actions;
- frozen identifiers;
- status;
- totals;
- drill-down;
- export;
- empty state;
- loading state;
- permission state;
- stale-data indication.

Avoid converting dense tables into oversized cards without a mobile-specific reason.

---

## 14. Status, Badges, and Semantics

Use status indicators only when they represent operational state.

A status definition should include:

```text
Name
Meaning
Colour
Icon
Allowed transitions
Owner
Next action
Accessibility label
```

Do not rely on colour alone.

Recommended semantic families:

- success;
- attention;
- warning;
- error;
- information;
- neutral;
- inactive.

---

## 15. Charts

Charts should answer a defined question.

Every chart requires:

- metric definition;
- unit;
- time period;
- source;
- filters;
- comparison basis;
- accessible legend;
- tooltip;
- empty and partial states;
- record-level path where practical.

Use:

- line for time trend;
- bar for comparison;
- stacked bar for composition;
- area only when volume/accumulation matters;
- scatter for relationship;
- table when precise lookup is primary.

Avoid:

- decorative doughnuts;
- 3D charts;
- random colour;
- truncated axes without disclosure;
- too many series;
- animation that delays reading.

---

# Part V — Motion and Interaction

## 16. Motion Principles

### 16.1 Corpus pattern

Motion ranges from nearly absent in IBM, WIRED, Tesla, and other restrained systems to a central brand material in Framer, Raycast, automotive, and creative systems.

The common quality signal is not the amount of motion. It is consistency and purpose.

### 16.2 Normalised duration bands

These are reusable engineering recommendations derived from the corpus, not exact values shared by every brand.

| Motion | Duration |
|---|---:|
| Immediate state feedback | 80–120ms |
| Hover/focus/colour | 120–180ms |
| Small component transition | 160–240ms |
| Drawer/menu/modal | 200–320ms |
| Section or media transition | 300–500ms |
| Deliberate campaign sequence | 500–800ms maximum, sparingly |

### 16.3 Easing

- Enter: ease-out
- Exit: ease-in
- Reposition: ease-in-out
- Productive interfaces: restrained cubic easing
- Creative experiences: spring only when it supports the brand

### 16.4 Appropriate motion

- button press;
- hover affordance;
- focus transition;
- tab indicator;
- accordion;
- disclosure;
- drawer;
- modal;
- list insertion/removal;
- skeleton-to-content;
- chart update;
- image carousel;
- scroll-linked storytelling when content requires it.

### 16.5 Motion rules

1. Motion must not block the next action.
2. Repeated actions should become faster, not slower.
3. Avoid animating large layout properties when transforms or opacity work.
4. Preserve spatial continuity.
5. Provide `prefers-reduced-motion`.
6. Do not animate critical financial values in a way that obscures the final value.
7. Disable decorative autoplay when it competes with reading.
8. Avoid infinite animation in operational products.

---

## 17. Hover and Focus

Hover should communicate:

- clickable;
- selected;
- expandable;
- draggable;
- previewable.

Focus should be at least as visible as hover.

Recommended focus treatment:

```text
2px visible ring
2px offset where required
high contrast on both light and dark surfaces
not removed without replacement
```

Touch interfaces cannot depend on hover.

---

# Part VI — Images, Illustration, and Iconography

## 18. Photography

Common successful treatments:

- full-bleed hero;
- gallery tile;
- circular portrait;
- product cut-out;
- editorial crop;
- dark cinematic frame;
- neutral product screenshot.

Rules:

- establish aspect ratios;
- document object positioning;
- define mobile crops;
- maintain readable overlays;
- use scrims only when required;
- define loading treatment;
- preserve alt text;
- do not use low-quality stock imagery as filler.

---

## 19. Illustration

Illustration is most effective when it:

- extends the brand;
- explains abstraction;
- supports onboarding;
- humanises technical concepts;
- creates recognisable campaign language.

It should not compete with operational controls.

---

## 20. Icons

- Use one icon family.
- Maintain consistent stroke weight.
- Define 16, 20, 24, and optional 32px sizes.
- Pair unfamiliar icons with labels.
- Do not use sparkle icons as a generic signal for AI.
- Use brand or integration icons only with appropriate rights.
- Define filled versus outlined usage.
- Provide accessible names for actionable icons.

---

# Part VII — Responsive and Accessible Behaviour

## 21. Responsive Principles

Responsive design is not merely stacking columns.

Define:

- content priority;
- navigation transformation;
- filter behaviour;
- table strategy;
- image crop;
- typography scale;
- control size;
- sticky elements;
- modal/drawer behaviour;
- chart simplification;
- touch targets.

### 21.1 Common transformation patterns

```text
Multi-column → fewer columns → single column
Mega menu → drawer
Sidebar → collapsible navigation
Horizontal filters → wrap or filter sheet
Wide table → horizontal scroll or priority columns
Split hero → stacked copy and media
Floating controls → bottom sheet or fixed action
```

### 21.2 Breakpoint philosophy

Use content-driven breakpoints.

A practical starting set:

```text
Small: ~480px
Mobile/tablet boundary: ~768px
Desktop: ~1024px
Wide: ~1280px
Large canvas: ~1440px+
```

Do not treat these as universal device categories.

---

## 22. Accessibility

Required baseline:

- WCAG-conscious contrast;
- keyboard operation;
- visible focus;
- semantic HTML;
- accessible names;
- error association;
- reduced motion;
- zoom support;
- screen-reader status announcements;
- target sizes;
- logical heading order;
- colour-independent meaning;
- captions/transcripts where required.

Design quality includes accessibility. Accessibility is not a later compliance layer.

---

# Part VIII — Enterprise Adaptation

## 23. Marketing Design vs Product Design

Do not directly transfer all marketing characteristics into an operational product.

| Marketing | Operational product |
|---|---|
| Large display type | Compact hierarchy |
| Cinematic media | Functional evidence |
| Isolated message | Multi-step workflow |
| Large CTA | Repeated actions |
| Campaign colour | Semantic colour |
| Scroll storytelling | Stable navigation |
| Decorative motion | State feedback |
| Sparse information | Appropriate density |

A product may share brand tokens while using a different density and component system.

---

## 24. Recommended VLCO Enterprise Default

When client branding is incomplete, begin with:

```yaml
archetype: enterprise-structured
canvas: neutral-light
primary-action: client-brand-or-deep-plum
surface-strategy: tonal-plus-hairline
radius-family: 4-8-12
spacing-base: 4px
body-size: 14-16px
table-density: compact
motion: restrained
navigation: sidebar-plus-header
```

Required enterprise elements:

- breadcrumbs;
- page title;
- primary action;
- filter/action bar;
- operational table;
- drill-down;
- loading/empty/error/permission/success states;
- audit and freshness information;
- accessible focus;
- responsive priority.

---

## 25. Universal Starter Tokens

```css
:root {
  --color-brand: #53284f;
  --color-brand-hover: #43203f;
  --color-brand-soft: #f3edf2;
  --color-on-brand: #ffffff;

  --color-canvas: #ffffff;
  --color-surface-1: #f7f7f8;
  --color-surface-2: #efeff1;
  --color-surface-inverse: #1c1c1f;

  --color-text: #1c1c1f;
  --color-text-secondary: #4f4f56;
  --color-text-muted: #73737c;
  --color-text-inverse: #ffffff;

  --color-border: #dedee3;
  --color-border-strong: #b8b8c0;
  --color-focus: #245bdb;

  --color-success: #16834a;
  --color-warning: #a96600;
  --color-error: #c43131;
  --color-info: #245bdb;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-7: 48px;
  --space-8: 64px;
  --space-9: 96px;

  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 20px;
  --radius-pill: 9999px;

  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.06);
  --shadow-md: 0 8px 24px rgb(0 0 0 / 0.10);

  --motion-fast: 140ms;
  --motion-standard: 220ms;
  --motion-slow: 360ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
}
```

This is a starting point, not a client brand.

---

# Part IX — Design Decision Framework

## 26. Before Creating a Product `DESIGN.md`

Record:

```text
Product:
Primary users:
Primary task:
Environment:
Information density:
Client brand:
Primary archetype:
Secondary influence:
Patterns adopted:
Patterns rejected:
Accessibility constraints:
Motion level:
Approval owner:
```

### Selection sequence

```text
Understand task
→ Confirm brand
→ Select archetype
→ Select one reference system
→ Optional second reference for a narrow need
→ Extract principles
→ Create original tokens
→ Define components and states
→ Validate
```

### Mixing rule

Do not combine more than two reference systems without explicit design rationale.

Example:

```text
Primary: IBM — enterprise structure
Secondary: Linear — navigation and interaction precision

Rejected:
- Stripe mesh gradients
- Airbnb consumer rounding
- Lamborghini luxury black
```

---

## 27. Design Review Score

| Measure | Weight |
|---|---:|
| Brand alignment | 15 |
| Product suitability | 15 |
| Visual hierarchy | 10 |
| Layout consistency | 10 |
| Component completeness | 10 |
| Operational usability | 15 |
| Accessibility | 10 |
| Responsive behaviour | 5 |
| Motion discipline | 5 |
| Context efficiency | 5 |
| **Total** | **100** |

Passing rule:

```text
Score >= 85
AND
No critical accessibility, usability, or brand-precedence failure
```

Critical failures:

- client brand overridden;
- insufficient text contrast;
- missing keyboard focus;
- critical action unclear;
- destructive action misleading;
- non-functional control;
- inaccessible mobile layout;
- invented operational data;
- protected brand assets copied without permission.

---

# Part X — Anti-Patterns

## 28. Avoid Generic AI UI

Avoid:

- default purple-to-blue gradients;
- glow around every card;
- glassmorphism without functional layering;
- oversized rounded cards;
- large empty spaces unsupported by media;
- random status pills;
- sparkle icons for every AI feature;
- fake charts;
- arbitrary dark mode;
- excessive centre alignment;
- repeated hero sections inside an application;
- inconsistent icon families;
- non-functional controls;
- decorative animation loops.

---

## 29. Avoid Blind Brand Copying

Do not:

- duplicate a company's exact palette without a valid brand reason;
- use proprietary typefaces without rights;
- recreate logos or wordmarks;
- copy branded illustrations or photography;
- combine famous styles into an incoherent collage;
- claim a reference company endorsed the design.

Extract principles, then create an original product system.

---

# Part XI — Company Pattern Index

The following index records the high-level design signal extracted from every company profile in the reviewed collection.


## AI & LLM Platforms

| Company | High-level design DNA |
|---|---|
| Claude | Warm editorial minimalism; restrained terracotta; conversational and human. |
| Cohere | Enterprise AI with vivid gradients, structured data surfaces, and confident scale. |
| ElevenLabs | Dark cinematic audio interface; waveform-led visual storytelling. |
| Minimax | Bold dark interface with neon signal accents and futuristic contrast. |
| Mistral AI | French-engineered minimalism; compact technical structure with purple tonality. |
| Ollama | Terminal-first monochrome; nearly no decorative UI. |
| OpenCode AI | Developer-centric dark theme with code-led hierarchy. |
| Replicate | Clean white canvas; code-forward content and low visual noise. |
| Runway | Cinematic editorial system; film-festival atmosphere with dark heroes and paper-white reading bands. |
| Together AI | Technical blueprint language; infrastructure credibility through structure. |
| VoltAgent | Void-black canvas, emerald signal colour, terminal-native details. |
| xAI | Stark monochrome futurism with radical visual reduction. |

## Developer Tools & IDEs

| Company | High-level design DNA |
|---|---|
| Cursor | Dark AI-editor language with sleek gradients and product screenshots. |
| Expo | Dark developer canvas, tight tracking, code-centric content. |
| Lovable | Friendly builder aesthetic with playful gradients and approachable components. |
| Raycast | Premium dark chrome, vibrant gradients, and command-palette precision. |
| Superhuman | Keyboard-first premium dark UI with restrained purple glow. |
| Vercel | Black-and-white precision; geometric typography; minimal technical confidence. |
| Warp | Dark IDE structure with block-based command interfaces. |

## Backend, Database & DevOps

| Company | High-level design DNA |
|---|---|
| ClickHouse | Yellow-accented technical documentation and analytical density. |
| Composio | Modern dark integration interface with colourful service icons. |
| HashiCorp | Enterprise-clean monochrome system with strict structure. |
| MongoDB | Green-led developer documentation with approachable technical content. |
| PostHog | Playful developer brand with dark product surfaces and illustrated personality. |
| Sanity | Dark-first editorial marketing with coral-red used only for priority actions. |
| Sentry | Deep violet developer system, lime highlights, code typography, and illustrated personality. |
| Supabase | Dark emerald code-first system with product and documentation parity. |

## Productivity & SaaS

| Company | High-level design DNA |
|---|---|
| Cal.com | Clean neutral scheduling interface with simple, predictable controls. |
| Intercom | Friendly blue conversational design with rounded, human components. |
| Linear | Near-black product system with one lavender accent, dense structure, and quiet luxury. |
| Mintlify | Reading-optimised documentation system with green signal colour. |
| Notion | Warm workspace language with navy anchors, colourful feature cards, and illustration. |
| Resend | Minimal dark developer system with monospace accents. |
| Zapier | Warm orange, friendly illustration, and straightforward automation storytelling. |

## Design & Creative Tools

| Company | High-level design DNA |
|---|---|
| Airtable | Colourful structured-data design with friendly operational surfaces. |
| Clay | Organic shapes, art-directed layouts, and soft atmospheric gradients. |
| Figma | Strict black-and-white frame interrupted by oversized pastel colour blocks. |
| Framer | Bold black-and-blue design language with motion as a primary material. |
| Miro | Bright yellow collaborative system reflecting an infinite canvas. |
| Webflow | Blue-accented polished marketing system for visual builders. |

## Fintech & Payments

| Company | High-level design DNA |
|---|---|
| Binance | Black-and-yellow trading-floor clarity with urgent action hierarchy. |
| Coinbase | Clean blue institutional trust and simplified financial communication. |
| Kraken | Purple-accented dark trading interface with high data density. |
| Mastercard | Warm cream editorial canvas, orbital imagery, extreme pill geometry, and restrained orange. |
| Revolut | Sleek dark fintech precision with gradients and card-led storytelling. |
| Stripe | Deep navy and electric indigo with atmospheric mesh gradients and refined technical typography. |
| Wise | Bright green financial clarity with plain-language confidence. |

## E-commerce & Retail

| Company | High-level design DNA |
|---|---|
| Airbnb | Warm white marketplace with coral signal colour, photography, pills, and generous spacing. |
| Meta | Photography-first retail system using binary light/dark surfaces and blue CTAs. |
| Nike | Monochrome retail chrome, enormous campaign type, full-bleed photography, and black pills. |
| Shopify | Dark cinematic commerce with neon green and ultra-light display typography. |
| Starbucks | Earth-green hierarchy, warm cream canvas, and rounded retail storytelling. |

## Media & Consumer Technology

| Company | High-level design DNA |
|---|---|
| Apple | Museum-gallery product marketing; light/dark tiles, action blue, cinematic imagery, almost no chrome. |
| HP | Pure white technology canvas with electric blue and geometric decorative structure. |
| IBM | Carbon-inspired enterprise flatness, square geometry, light display type, and one assertive blue. |
| NVIDIA | Green-on-black technical power with product-led visual energy. |
| Pinterest | Red signal colour with masonry, imagery, and discovery-first composition. |
| PlayStation | Layered light/dark channel surfaces with cyan interaction cues. |
| SpaceX | Stark black-and-white, full-bleed imagery, and aerospace minimalism. |
| Spotify | Vibrant green on dark surfaces with bold type and album-art-driven colour. |
| The Verge | High-energy editorial system with acid mint, ultraviolet, and distinctive display typography. |
| Uber | Bold black-and-white urban interface with compressed typographic energy. |
| Vodafone | Monumental uppercase display type with red chapter bands. |
| WIRED | Broadsheet editorial density; serif display/body paired with sans metadata. |

## Automotive

| Company | High-level design DNA |
|---|---|
| BMW | Dark premium surfaces, disciplined grids, and precise engineering language. |
| BMW M | Motorsport contrast with performance colour accents and dynamic composition. |
| Bugatti | Cinema-black luxury with monumental display typography and almost no colour. |
| Ferrari | Black-white chiaroscuro with Ferrari red used extremely sparingly. |
| Lamborghini | True-black cathedral surfaces with gold accents and angular authority. |
| Renault | Vivid aurora gradients, proprietary display type, and zero-radius action geometry. |
| Tesla | Full-viewport automotive photography, near-zero chrome, one electric-blue CTA, and sharp buttons. |

## Retro Web

| Company | High-level design DNA |
|---|---|
| Dell 1996 | Catalogue-era enterprise web with colour ribbons, chunky display type, and GIF-like badges. |
| Nintendo 2001 | Y2K console chrome, bevels, halftone textures, and playful circuit-board surfaces. |


---

# Part XII — Agent Usage Guide

## 30. Instructions for an AI Coding or Design Agent

```text
1. Read approved client brand material.
2. Read this design intelligence standard.
3. Identify the product archetype.
4. Select one primary external reference.
5. Select one optional secondary reference for a narrow purpose.
6. State patterns adopted and rejected.
7. Create the product-specific DESIGN.md.
8. Define tokens, components, states, responsive rules, accessibility, and motion.
9. Build one representative page or component set.
10. Review implementation against DESIGN.md.
11. Record deviations and approval.
```

The agent must not load all 73 design profiles into active context during ordinary work.

Use progressive disclosure:

```text
This standard
→ Selected archetype
→ One primary reference
→ Relevant implementation files
```

---

## 31. Required Product-Specific `DESIGN.md` Sections

```text
1. Product and users
2. Brand precedence
3. Visual theme
4. Selected archetype
5. Reference systems
6. Patterns adopted
7. Patterns rejected
8. Colour tokens and roles
9. Typography
10. Spacing and grid
11. Radius and geometry
12. Navigation
13. Buttons and actions
14. Forms
15. Tables and data
16. Cards and surfaces
17. Status and feedback
18. Charts
19. Imagery and icons
20. Motion
21. Responsive behaviour
22. Accessibility
23. Loading, empty, error, permission, and success states
24. Do and do not
25. Validation checklist
```

---

## 32. Final Principle

```text
Consistency does not mean sameness.
Distinctiveness does not require excess.
The best system is the smallest coherent set of decisions
that makes the product unmistakably appropriate for its users and purpose.
```

---

## Attribution

This synthesis was informed by the MIT-licensed `VoltAgent/awesome-design-md` collection. Individual company names and trademarks remain the property of their respective owners. The synthesis is an independent high-level analysis and does not imply endorsement by VoltAgent or any referenced company.
