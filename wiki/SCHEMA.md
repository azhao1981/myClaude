# Wiki Schema

## Domain
AI 编程智能体工程化（AI Coding Agent Engineering）——覆盖 Loop Engineering、Agent 编排、Prompt Engineering 向系统设计的范式转移，以及相关工具（Claude Code、Codex 等）和关键人物。

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `loop-engineering.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]`
  at the end of paragraphs whose claims come from a specific source.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
# Optional quality signals:
confidence: high | medium | low
contested: true
contradictions: [other-page-slug]
---
```

## raw/ Frontmatter
```yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <hex digest of the raw content below the frontmatter>
---
```

## Wiki Syntax (Obsidian-flavored Markdown)

Wiki pages use Obsidian-flavored Markdown. Conventions:

- **Wikilink `[[page-name]]`** — wraps a target page's filename in double brackets.
  - Obsidian auto-resolves it to a clickable link; in plain text readers / external LLMs it renders as the literal `[[page-name]]` string (the brackets are part of the syntax, not noise).
  - Use the page slug (filename without `.md`), not the display title. Example: `[[loop-engineering]]` not `[[Loop Engineering]]`.
  - Minimum 2 outbound `[[wikilinks]]` per page (see Conventions above).

- **Provenance footnote `^[path/to/source.md]`** — appended after a paragraph that synthesizes a specific source.
  - Renders as an Obsidian footnote (superscript marker linking to the source).
  - In external contexts, treat the bracket contents as the source path; ignore the `^` prefix.
  - Every claim that comes from a specific article should carry one. Multi-source paragraphs may chain several: `^[a.md]^[b.md]`.

- **Frontmatter** — every page begins with a YAML block between `---` fences. See `Frontmatter` section above for fields. External readers that don't parse YAML will see the block as plain text; that's fine.

- **Section depth** — prefer `##` headings inside pages (the H1 is reserved for the page title). Obsidian's outline panel relies on this.

- **Tag values** — use the slugs from `Tag Taxonomy` below, lowercase, hyphen-case. Tags are free-form metadata, distinct from `[[wikilinks]]`.

## Tag Taxonomy
- Paradigms: loop-engineering, prompt-engineering, agent-orchestration, automation
- Components: skill, sub-agent, worktree, memory, automation, connector, mcp
- Evolution: react, autogpt, ralph-loop, goal-command, multi-agent-loop
- People: person
- Products: product, tool
- Companies: company
- Meta: comparison, timeline, controversy, cost, risk, benchmark
- Models: model

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines
- **Archive a page** when its content is fully superseded

## Entity Pages
One page per notable entity. Include: Overview, Key facts and dates, Relationships ([[wikilinks]]), Source references.

## Concept Pages
One page per concept or topic. Include: Definition, Current state of knowledge, Open questions, Related concepts ([[wikilinks]]).

## Comparison Pages
Side-by-side analyses. Include: What is compared, Dimensions (table preferred), Verdict, Sources.

## Update Policy
When new information conflicts with existing content:
1. Check dates — newer sources generally supersede
2. If genuinely contradictory, note both positions with dates and sources
3. Mark in frontmatter: `contradictions: [page-name]`
4. Flag for user review in lint report
