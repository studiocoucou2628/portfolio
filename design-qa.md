# Design QA — Studio Coucou portfolio

## Comparison target

- Source visual truth: `/Users/gatao/.codex/generated_images/019fdfbd-0cf6-7a81-a2b3-b21aeb9b59e3/exec-9647866e-f91d-4c05-9c59-486d2287976e.png`
- Source pixels: 1054 × 1492
- Implementation capture (desktop): `implementation-desktop.png`
- Implementation pixels: 1440 × 3890
- Implementation capture (mobile): `implementation-mobile-top.png`
- Mobile pixels / CSS viewport / density: 390 × 844 / 390 × 844 / 1×
- Desktop CSS viewport / density: 1440 × 1000 / 1×
- State: initial page load; primary CTA was also tested to `#contact`.

The source and the implementation capture were opened together for comparison. The source is a visual direction rather than a claimable portfolio case: its generated people, child photo, fictitious signature, and illustrative icons were intentionally not carried into the site. This keeps the page free of fabricated people, credentials, and imagery until Studio Coucou has licensed or supplied real materials.

## Findings

- [P3] Replace the intentionally omitted photography only with real, approved material.
  - Location: hero and Studio Coucou introduction.
  - Evidence: the reference uses warm parent-and-child imagery; the implementation uses typography, color, and editorial spacing instead.
  - Impact: the current version is more honest and less AI-like, but will gain more immediate warmth when Studio Coucou has its own photos or approved client images.
  - Fix: add only user-owned or licensed photos after their use and captions are confirmed.

## Required fidelity surfaces

- Fonts and typography: the implementation uses a Japanese Mincho display face with a restrained sans-serif body, preserving the reference’s calm editorial hierarchy. Headline wraps were checked at 1440 px and 390 px; no clipping or truncation was found.
- Spacing and layout rhythm: a generous generated-paper hero, a four-step path, dark green statement band, comparison, principles, and closing CTA preserve the source’s storytelling cadence without copying its fake assets. At 1054 px, measured desktop content widths remained within the viewport.
- Colors and visual tokens: forest green, warm paper, off-white, muted gold, and rust are defined as reusable CSS tokens. Contrast remains clear in the dark sections and primary CTA.
- Image quality and asset fidelity: the existing Studio Coucou logo is used. No generated people, customer photos, fake logos, placeholder imagery, CSS art, or inline SVG substitutes were added.
- Copy and content: copy now leads with the parent journey and a concrete site-improvement consultation, rather than generic service cards or unverified results. The email address is visible, the mail link points to `studiocoucou2628@gmail.com`, and the Instagram profile link provides a second DM consultation route.

## Interaction and resilience checks

- Header “サイト改善を相談する” and the hero CTA both move to `#contact`.
- The mail CTA was inspected as a `mailto:` link but was not activated.
- The Instagram CTA points to `https://www.instagram.com/studiocoucou.jp/` and opens in a new tab; it was not activated during verification.
- Desktop 1440 px: `scrollWidth` 1440 px, no horizontal overflow.
- Mobile 390 px: `scrollWidth` 390 px, no horizontal overflow; primary CTA remains within the viewport.
- Browser console: no warnings or errors.

## Comparison history

1. Initial comparison: identified that the reference contains generated people, a fictitious personal signature, and illustrative assets that cannot be represented as Studio Coucou’s real work.
2. Resolution: retained the selected direction’s narrative, palette, hierarchy, and conversion path while omitting those unverified assets; verified desktop, intermediate-width layout measurements, and mobile rendering.
3. CTA revision: made the consultation purpose explicit and restored Instagram as a parallel DM route; verified both calls to action at 390 px without horizontal overflow.

## Final result

passed
