# MOSAIC — Project Report & Technical Architecture

> **Working definition:** MOSAIC is a knowledge engine that turns fragmented human knowledge and trusted external evidence into verified, connected, continuously enriched knowledge, and then uses that knowledge to teach the user.

---

## 1. Executive Summary

MOSAIC is envisioned as a learning and knowledge platform built around a central idea:

> **Collect knowledge → verify it → connect it → enrich it → teach it.**

Users can upload handwritten notes and other learning material. MOSAIC uses OCR and AI to understand the material, extract individual claims, verify those claims against appropriate evidence, identify missing or incorrect information, and add only verified/corrected knowledge to a canonical knowledge base.

The canonical knowledge base is then used to generate concise, attractive flashcards and visual swipe sequences. When the user wants deeper understanding, MOSAIC retrieves grounded knowledge and generates an in-depth explanation.

A major architectural principle is:

> **User notes and external source documents are evidence/input, not automatically truth.**

MOSAIC should maintain a clear separation between raw source material, extracted claims/evidence, and the canonical verified knowledge base.

---

# 2. Product Vision

MOSAIC should not be positioned merely as an AI flashcard generator.

A stronger positioning is:

> **MOSAIC is a personal knowledge engine that continuously builds, verifies, connects, and teaches what you know.**

Or technically:

> **A system that converts messy personal knowledge and trusted external evidence into an evidence-backed, continuously enriched concept graph, tracks provenance and confidence, and generates personalized learning experiences from that graph.**

The long-term product loop is:

```text
Discover
   ↓
Intrigue
   ↓
Swipe
   ↓
Visualize
   ↓
"I want to understand this"
   ↓
In-depth explanation
   ↓
Learn
   ↓
Master
```

The difficult-to-copy part of the product should therefore be the **knowledge pipeline and knowledge representation**, not merely the LLM UI.

---

# 3. Core Product Capabilities

## 3.1 User Knowledge Ingestion

Users can upload:

- Handwritten notes
- Typed notes
- PDFs
- Images
- Other supported learning documents

The system should preserve the original material and independently create machine-readable representations.

## 3.2 OCR and Parsing

The uploaded document goes through OCR/vision parsing.

```text
User File
   ↓
OCR / Vision
   ↓
Structured Text
   ↓
Document Segmentation
```

## 3.3 Claim Extraction

The system should break notes into atomic claims rather than treating an entire document as one block of truth.

Example:

```text
Original note:
"Dijkstra's algorithm works with negative edge weights and has O(E log V) complexity."
```

Extracted claims:

```text
Claim 1:
Dijkstra's algorithm works with negative edge weights.

Claim 2:
Dijkstra's algorithm has O(E log V) complexity.
```

Each claim can then be independently verified.

## 3.4 Verification

Each claim should receive one of several states:

- `SUPPORTED`
- `CONTRADICTED`
- `PARTIALLY_SUPPORTED`
- `UNCERTAIN`

The system should avoid a simplistic `true/false` model because many claims are conditional or only partially correct.

## 3.5 Enrichment

Once a claim is verified, MOSAIC can enrich it with:

- Missing context
- Definitions
- Related concepts
- Examples
- Edge cases
- Prerequisites
- Complexity/details
- Useful connections

## 3.6 Canonical Knowledge Base

Only verified/corrected/enriched knowledge should become part of the canonical MOSAIC knowledge layer.

The original user note remains untouched.

This produces three distinct layers:

```text
RAW SOURCE
   ↓
EXTRACTED KNOWLEDGE
   ↓
VERIFIED / CANONICAL KNOWLEDGE
```

## 3.7 Flashcard Discovery

Canonical knowledge is converted into short, visually interesting flashcards.

Example:

```text
"Why does BFS find shortest paths in an unweighted graph?"
```

A swipe can reveal successive states of a static visual sequence.

For example:

```text
Graph
  ↓ swipe
Queue state 1
  ↓ swipe
Queue state 2
  ↓ swipe
Visited state
  ↓ swipe
Final traversal
```

The first version intentionally keeps these sequences **static rather than dynamically interactive**.

## 3.8 In-depth Explanation

A user who wants deeper understanding can request an in-depth explanation.

```text
Flashcard
   ↓
In-depth
   ↓
Retrieve canonical knowledge
   ↓
Retrieve supporting evidence
   ↓
LLM generation
   ↓
Grounded explanation
```

## 3.9 Recommendation System

The recommendation system can eventually consider:

- User interests
- Previously viewed concepts
- Saved concepts
- Difficulty
- Prerequisite relationships
- Learning history
- Feedback
- Mastery

Recommendation should be developed after the core knowledge pipeline works reliably.

## 3.10 Social Layer — Future Scope

Potential later features include:

- Friends
- Chat
- Comments
- Sharing
- Likes/upvotes
- Community contributions
- Contributor reputation
- Collaboration

These should not be central to the first MVP.

---

# 4. External Knowledge Sources

MOSAIC should use a source hierarchy rather than treating every website as equally authoritative.

## 4.1 Recommended Source Categories

### Tier 1 — Primary / Official Sources

Examples:

- Official programming language documentation
- Official framework documentation
- Official APIs
- Standards documentation
- Government/academic primary sources
- Research papers

These should generally receive the highest authority weighting.

### Tier 2 — Trusted Educational Sources

Examples:

- MDN Web Docs
- University educational repositories
- Open educational resources
- Reputable technical documentation
- High-quality educational publishers where licensing permits

### Tier 3 — Community Knowledge

Examples:

- Stack Exchange / Stack Overflow
- GitHub discussions/issues
- Reddit
- Technical forums

Community content is highly useful for explanations, edge cases and real-world experience, but should generally have lower default authority than primary/official evidence.

---

# 5. Recommended Initial Sources

| Source | Strong use case | Recommended role | Notes |
|---|---|---|---|
| GitHub | Code, READMEs, technical projects | Knowledge/evidence | Check repository/file licenses and applicable platform terms |
| Stack Overflow / Stack Exchange | Q&A, edge cases, solutions | Evidence/community knowledge | Respect applicable licensing and attribution requirements |
| MDN Web Docs | Web technologies | High-authority technical knowledge | Check license and attribution requirements |
| Official language docs | Python, Java, JS, etc. | Primary source | Prefer this for factual verification |
| Official framework docs | Django, React, FastAPI, etc. | Primary source | Prefer this for implementation facts |
| arXiv | Research papers | Research evidence | Check paper-specific rights/license |
| Wikimedia/Wikipedia | General facts and concept relationships | Background knowledge | Follow applicable licenses/attribution |
| freeCodeCamp | Programming education | Secondary educational source | Check content/license terms |
| MIT OpenCourseWare | University-level education | Research/prototyping source | Many materials have non-commercial restrictions |
| OpenStax | Textbook-style educational content | Research/prototyping source | Licensing must be checked for intended commercial use |

---

# 6. GitHub Strategy

GitHub should not be treated as a universal dump of all content.

Preferred pipeline:

```text
GitHub
   ↓
Repository discovery
   ↓
Check repository metadata
   ↓
Check license
   ↓
Select permitted material
   ↓
Record provenance
   ↓
Claim extraction
   ↓
Verification
   ↓
Canonical knowledge
```

Useful material may include:

- README files
- Documentation
- Architecture documents
- Educational repositories
- Tutorials
- Design documents
- Discussions/issues where permitted

The repository/file license and applicable GitHub terms should be recorded by the ingestion system.

---

# 7. Reddit Strategy

Reddit can be highly valuable as **community evidence** because discussions contain:

- Explanations
- Practical experiences
- Edge cases
- Alternative approaches
- Debate and disagreement

However, Reddit should not automatically become the canonical knowledge source.

A Reddit claim may be:

```text
Correct
Incorrect
Opinion
Outdated
Context-dependent
```

Therefore:

```text
Reddit
  ↓
Community evidence
  ↓
Claim extraction
  ↓
Verification against stronger evidence
  ↓
Canonical knowledge only when supported
```

MOSAIC should resolve the legal/terms position for Reddit data before making Reddit a business-critical ingestion source, especially for AI/ML use and persistent corpus storage.

---

# 8. Legal and Licensing Architecture

A fundamental principle:

> **Publicly accessible does not automatically mean freely reusable.**

MOSAIC should not be designed around indiscriminate scraping of sites whose terms prohibit crawling, scraping, copying, redistribution or related uses.

Instead, the system should support:

1. User-owned content
2. Appropriately licensed/open content
3. Official APIs
4. Licensed feeds
5. Direct partnerships
6. Source links/references without copying expressive content where appropriate

## 8.1 Source Registry

MOSAIC should maintain a source registry.

Suggested fields:

```text
source_id
name
domain
source_type
access_method
license
license_url
attribution_required
commercial_use_allowed
ai_use_allowed
scraping_allowed
api_available
authority_score
last_checked
```

This turns licensing/provenance into a software concern instead of an afterthought.

## 8.2 Provenance

For every piece of external evidence, MOSAIC should be able to answer:

- Where did this come from?
- Who/what published it?
- What license governs it?
- When was it retrieved?
- What claim does it support?
- What confidence does MOSAIC assign to it?

---

# 9. ChatGPT-Style Web Retrieval vs MOSAIC

MOSAIC can follow a similar principle to modern web-search-assisted AI systems.

The generic retrieval workflow is:

```text
User Question
   ↓
Query understanding
   ↓
Search / retrieval
   ↓
Relevant documents
   ↓
Relevant passages
   ↓
LLM reasoning
   ↓
Answer
```

MOSAIC can extend this model into a persistent knowledge system.

## 9.1 Generic Web Answer

```text
Question
   ↓
Search web
   ↓
Retrieve pages
   ↓
Read relevant information
   ↓
LLM
   ↓
Answer + citations
```

## 9.2 MOSAIC Retrieval

```text
User Question
   ↓
Query Understanding
   ↓
Source Selection
   ↓
Retrieve canonical knowledge
   ↓
Retrieve relevant relationships
   ↓
Retrieve supporting evidence
   ↓
LLM
   ↓
Grounded response
```

The key difference is that MOSAIC should maintain its own **verified knowledge layer** instead of relying exclusively on raw web pages at answer time.

---

# 10. Two RAG Pipelines in MOSAIC

## 10.1 Ingestion RAG

Used to build/update the knowledge base.

```text
External Source
   ↓
Document retrieval
   ↓
Claim extraction
   ↓
Evidence retrieval
   ↓
Claim ↔ Evidence comparison
   ↓
Verification
   ↓
Canonical KB update
```

## 10.2 User-Answer RAG

Used when a user requests information.

```text
User Question
   ↓
Retrieve canonical knowledge
   ↓
Retrieve relationships
   ↓
Retrieve supporting sources
   ↓
LLM generation
   ↓
Answer
```

Important principle:

> **RAG is the retrieval mechanism, not the knowledge base itself.**

---

# 11. Core Verification Architecture

The verification engine is one of the most important components of MOSAIC.

```text
                        CLAIM
                          │
                          ↓
                 Query Generation
                          │
              ┌───────────┼───────────┐
              ↓           ↓           ↓
          Official      Academic    Community
          Sources        Sources      Sources
              │           │           │
              └───────────┼───────────┘
                          ↓
                     Evidence
                          ↓
                  Evidence Ranking
                          ↓
                   Claim Verifier
                          ↓
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
      SUPPORTED      CONTRADICTED      UNCERTAIN
          │               │               │
          ↓               ↓               ↓
      Enrichment     Correction       Additional
                                      retrieval/review
```

The LLM should act as a **reasoning layer over evidence**, not as the ultimate source of truth.

---

# 12. Verification Confidence

A possible conceptual confidence model is:

```text
confidence =
    source_authority
  × evidence_relevance
  × cross_source_agreement
  × claim_specificity
  × recency_factor
```

The formula should be treated as a starting point, not a fixed final design.

A stronger system will likely combine learned scoring with deterministic rules and human review.

Example:

```text
Claim:
"Dijkstra's algorithm works with negative edge weights."

Official documentation       → strong contradictory evidence
Academic source              → strong contradictory evidence
Community discussion         → mixed evidence

Result:
CONTRADICTED
```

---

# 13. Knowledge Representation

A vector database alone should not be the complete knowledge model.

MOSAIC should represent:

- Concepts
- Claims
- Sources
- Evidence
- Relationships
- Embeddings
- Confidence
- Provenance

## 13.1 Concept Graph

Example:

```text
BFS
├── is-a → graph traversal algorithm
├── uses → queue
├── related-to → DFS
├── useful-for → shortest path in unweighted graphs
├── has-complexity → O(V + E)
└── prerequisite-for → advanced graph algorithms
```

This graph can initially be modeled using PostgreSQL relationships.

A dedicated graph database can be introduced later if required.

---

# 14. Canonical Knowledge Architecture

The canonical representation should be MOSAIC's own structured representation backed by evidence.

```text
                 RAW WORLD
                     ↓
             Extracted Claims
                     ↓
               Verification
                     ↓
               Canonical KB
                     ↓
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
    Concepts       Claims       Relations
       │             │             │
       └─────────────┼─────────────┘
                     ↓
            Evidence + Sources
```

User-provided notes and source documents should remain separately identifiable from canonical MOSAIC knowledge.

---

# 15. User Note Verification Example

Suppose a user uploads:

```text
BFS uses a queue.
BFS always finds the shortest path.
Dijkstra works with negative weights.
```

MOSAIC extracts:

```text
Claim 1 → BFS uses a queue.
Claim 2 → BFS always finds the shortest path.
Claim 3 → Dijkstra works with negative weights.
```

The system verifies each independently.

Potential result:

```text
Claim 1
SUPPORTED

Claim 2
PARTIALLY_SUPPORTED
Reason: shortest path guarantee depends on graph assumptions.

Claim 3
CONTRADICTED
Reason: Dijkstra's algorithm requires non-negative edge weights.
```

Canonical knowledge then contains corrected information rather than blindly storing the incorrect user claim.

---

# 16. Complete System Architecture — MVP

```text
                         ┌──────────────────────┐
                         │        USER          │
                         └──────────┬───────────┘
                                    │
                                    ↓
                         ┌──────────────────────┐
                         │   MOBILE APP         │
                         │ React Native + Expo  │
                         └──────────┬───────────┘
                                    │
                                    ↓
                         ┌──────────────────────┐
                         │      API LAYER       │
                         │ Django + DRF         │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ↓                      ↓                      ↓
       ┌────────────┐        ┌──────────────┐       ┌──────────────┐
       │    AUTH    │        │ NOTE SERVICE │       │ DISCOVERY    │
       └────────────┘        └──────┬───────┘       └──────┬───────┘
                                    │                      │
                                    ↓                      ↓
                           ┌────────────────┐      ┌──────────────┐
                           │ OCR / PARSING  │      │ RECOMMENDER  │
                           └───────┬────────┘      └──────────────┘
                                   │
                                   ↓
                           ┌────────────────┐
                           │ CLAIM EXTRACTOR│
                           └───────┬────────┘
                                   │
                                   ↓
                           ┌────────────────┐
                           │   VERIFIER     │
                           └───────┬────────┘
                                   │
                  ┌────────────────┼─────────────────┐
                  ↓                ↓                 ↓
              SUPPORTED        CONTRADICTED       UNCERTAIN
                  │                │                 │
                  └────────────────┼─────────────────┘
                                   ↓
                           ┌────────────────┐
                           │   ENRICHMENT   │
                           └───────┬────────┘
                                   ↓
                    ┌─────────────────────────┐
                    │ CANONICAL KNOWLEDGE     │
                    │                         │
                    │ Concepts                │
                    │ Claims                  │
                    │ Relations               │
                    │ Evidence                │
                    │ Sources                 │
                    │ Confidence              │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┼────────────────┐
                ↓                ↓                ↓
             RAG/Vector      PostgreSQL         Search
                │                │                │
                └────────────────┼────────────────┘
                                 ↓
                         ┌───────────────┐
                         │ RAG ENGINE    │
                         └───────┬───────┘
                                 ↓
                           ┌────────────┐
                           │    LLM     │
                           └─────┬──────┘
                                 ↓
                     ┌────────────────────────┐
                     │ FLASHCARDS / EXPLAINER │
                     └────────────────────────┘
```

---

# 17. Knowledge Acquisition Flowchart

```text
                EXTERNAL SOURCES
                       │
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
    GitHub        Stack Exchange      Web/API
       │               │                │
       └───────────────┼────────────────┘
                       ↓
                Source Registry
                       ↓
                 License Check
                       ↓
                 Document Parser
                       ↓
                   Chunking
                       ↓
               Claim Extraction
                       ↓
              Evidence Extraction
                       ↓
                 Verification
                       ↓
          ┌────────────┼────────────┐
          ↓            ↓            ↓
        Accept       Reject       Review
          │            │            │
          ↓            ↓            ↓
      Enrichment       X       Human/AI review
          │
          ↓
    Canonical Knowledge
```

---

# 18. User Note Processing Flowchart

```text
                    USER
                      │
                      ↓
                Upload Notes
                      │
                      ↓
                 File Storage
                      │
                      ↓
                 OCR / Parsing
                      │
                      ↓
              Structured Text
                      │
                      ↓
               Claim Extraction
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       Claim 1     Claim 2     Claim 3
          │           │           │
          └───────────┼───────────┘
                      ↓
                 Verification
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
    Supported     Contradicted   Uncertain
        │             │             │
        ↓             ↓             ↓
    Enrich       Find correction   Review
        │             │             │
        └─────────────┼─────────────┘
                      ↓
             Canonical Knowledge
```

---

# 19. Discovery / Learning Flowchart

```text
                USER
                  │
                  ↓
          Recommendation Engine
                  │
                  ↓
           Concept Selection
                  │
                  ↓
           Flashcard Generation
                  │
                  ↓
           Attractive Card
                  │
                  ↓
                SWIPE
                  │
                  ↓
          Next visual state
                  │
                  ↓
              Interesting?
              /          \
            NO            YES
            │              │
            ↓              ↓
        Next card       IN-DEPTH
                           │
                           ↓
                     RAG Retrieval
                           │
                           ↓
                  Grounded Explanation
                           │
                           ↓
                        Learning
```

---

# 20. Use-Case Diagram

```text
                         ┌─────────────────┐
                         │      USER       │
                         └────────┬────────┘
                                  │
          ┌───────────────────────┼────────────────────────┐
          │                       │                        │
          ↓                       ↓                        ↓
  Upload Notes              Explore Knowledge        Manage Profile
          │                       │
          ↓                       ↓
  View Verification         View Flashcards
          │                       │
          ↓                       ↓
  View Corrections          Swipe Visual Sequence
                                  │
                                  ↓
                           Request In-depth
                                  │
                                  ↓
                           Save Knowledge
                                  │
                                  ↓
                            Give Feedback
```

## External Systems

```text
                         ┌───────────────┐
                         │     USER      │
                         └───────┬───────┘
                                 │
                                 ↓
                            ┌─────────┐
                            │ MOSAIC  │
                            └─────────┘
                                 │
          ┌──────────────────────┼─────────────────────┐
          ↓                      ↓                     ↓
   ┌──────────────┐       ┌──────────────┐     ┌──────────────┐
   │ OCR Provider │       │ LLM Provider │     │ Web Sources  │
   └──────────────┘       └──────────────┘     └──────────────┘
```

---

# 21. Detailed Use Cases

| Actor | Use Case | Description |
|---|---|---|
| User | Register/Login | Create and authenticate an account |
| User | Upload Notes | Upload handwritten or digital knowledge material |
| User | View Processed Notes | See OCR/parsed representation |
| User | View Verification | See claim-level verification |
| User | View Corrections | Understand corrected or incomplete claims |
| User | Explore Flashcards | Discover concise concepts |
| User | Swipe Visual Sequence | Consume sequential visual explanations |
| User | Request In-depth Explanation | Open detailed grounded content |
| User | Save Concept | Bookmark knowledge |
| User | Provide Feedback | Mark content useful/incorrect/etc. |
| User | Track Learning | Monitor progress and mastery |
| System | OCR Notes | Convert images/handwriting into text |
| System | Extract Claims | Convert text into atomic claims |
| System | Verify Claims | Compare claims with evidence |
| System | Enrich Knowledge | Add missing context and relationships |
| System | Generate Flashcards | Convert verified concepts into discovery cards |
| System | Recommend Concepts | Personalize discovery |
| Admin | Review Uncertain Claims | Resolve difficult verification cases |
| Admin | Manage Sources | Add/remove/review source policies |
| Admin | Manage Licenses | Track permitted source usage |
| Admin | Monitor Quality | Evaluate verification and generation quality |

---

# 22. Domain Class Diagram

```text
┌─────────────────────┐
│        User         │
├─────────────────────┤
│ id                  │
│ name                │
│ email               │
│ profile             │
│ created_at          │
└──────────┬──────────┘
           │ 1
           │
           │ uploads
           │ *
           ↓
┌─────────────────────┐
│       Note          │
├─────────────────────┤
│ id                  │
│ user_id             │
│ file_url            │
│ raw_text            │
│ status              │
│ created_at          │
└──────────┬──────────┘
           │ 1
           │ contains
           │ *
           ↓
┌─────────────────────┐
│       Claim         │
├─────────────────────┤
│ id                  │
│ note_id             │
│ text                │
│ type                │
│ status              │
│ confidence          │
└──────────┬──────────┘
           │ 1
           │ verified by
           │ *
           ↓
┌─────────────────────┐
│   Verification      │
├─────────────────────┤
│ id                  │
│ claim_id            │
│ result              │
│ confidence          │
│ reasoning           │
│ verified_at         │
└──────────┬──────────┘
           │ 1
           │ supported by
           │ *
           ↓
┌─────────────────────┐
│       Evidence      │
├─────────────────────┤
│ id                  │
│ claim_id            │
│ source_id           │
│ excerpt             │
│ relevance_score     │
└──────────┬──────────┘
           │ *
           │ comes from
           │ 1
           ↓
┌─────────────────────┐
│       Source        │
├─────────────────────┤
│ id                  │
│ url                 │
│ title               │
│ author               │
│ source_type         │
│ license             │
│ retrieved_at        │
│ authority_score     │
└─────────────────────┘
```

---

# 23. Concept Model

```text
┌─────────────────────┐
│      Concept        │
├─────────────────────┤
│ id                  │
│ name                │
│ description         │
│ domain              │
│ difficulty          │
└──────────┬──────────┘
           │
           │ related to
           ↓
       Concept
```

A concept can have relationships such as:

```text
Concept
  ├── is_a → Concept
  ├── prerequisite_of → Concept
  ├── related_to → Concept
  ├── part_of → Concept
  ├── example_of → Concept
  └── contrasts_with → Concept
```

---

# 24. Extended Domain Model

```text
User
 │
 ├── Notes
 │     └── Claims
 │           └── Verification
 │                  └── Evidence
 │                         └── Source
 │
 ├── SavedConcepts
 ├── LearningProgress
 └── Feedback

Concept
 │
 ├── Claims
 ├── Relationships
 ├── Flashcards
 └── LearningProgress

Flashcard
 │
 ├── Concept
 ├── Sequence
 └── Provenance

Source
 │
 ├── License
 ├── Documents
 └── Evidence
```

---

# 25. Suggested Database Model

A first relational schema could contain:

### Identity

```text
users
profiles
```

### Documents

```text
notes
note_pages
note_assets
ocr_results
```

### Knowledge extraction

```text
claims
claim_concepts
concepts
concept_relationships
```

### Verification

```text
verifications
evidence
sources
source_snapshots
```

### Canonical knowledge

```text
canonical_claims
canonical_concepts
canonical_relationships
knowledge_versions
```

### Learning

```text
flashcards
flashcard_sequences
saved_concepts
learning_progress
mastery_records
```

### Feedback

```text
feedback
corrections
reports
```

### Source policy

```text
source_registry
source_license_records
```

---

# 26. Why PostgreSQL First?

PostgreSQL is sufficient for an MVP because it can model:

- Users
- Notes
- Claims
- Concepts
- Relationships
- Sources
- Evidence
- Learning progress

Vector retrieval can initially be added using **pgvector**.

This avoids prematurely introducing multiple database technologies.

A dedicated graph database can be evaluated later if graph traversal becomes a major bottleneck or product feature.

---

# 27. Vector Search vs Knowledge Graph

These technologies solve different problems.

## Vector search

Useful for:

- Semantic similarity
- Retrieval
- Finding related passages
- RAG
- Query-to-document matching

## Knowledge graph / relational relationships

Useful for:

- Prerequisites
- Concept relationships
- Dependency chains
- Structured navigation
- Explaining how ideas connect

Therefore:

```text
Knowledge Graph / Relational Model
          +
       Embeddings
          +
      Full-text Search
          ↓
       MOSAIC RAG
```

---

# 28. Production System Architecture — Later Stage

```text
                         ┌───────────────┐
                         │ Mobile Client │
                         └───────┬───────┘
                                 │
                                 ↓
                         ┌───────────────┐
                         │ API Gateway   │
                         └───────┬───────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ↓                     ↓                     ↓
      User Service          Knowledge Service    Discovery Service
           │                     │                     │
           │              ┌──────┴───────┐             │
           │              ↓              ↓             │
           │          Verification    Knowledge        │
           │              │              │             │
           │              └──────┬───────┘             │
           │                     │                     │
           └─────────────────────┼─────────────────────┘
                                 ↓
                        ┌──────────────────┐
                        │ Knowledge Store  │
                        ├──────────────────┤
                        │ PostgreSQL       │
                        │ Vector DB        │
                        │ Graph (later)    │
                        └────────┬─────────┘
                                 │
                                 ↓
                         ┌──────────────┐
                         │ RAG Engine   │
                         └──────┬───────┘
                                │
                                ↓
                              LLM
```

The production architecture should evolve gradually from the modular monolith rather than starting as a large microservice ecosystem.

---

# 29. Recommended MVP Technology Stack

| Layer | Technology |
|---|---|
| Mobile | React Native + Expo |
| Backend | Django |
| REST API | Django REST Framework |
| Database | PostgreSQL |
| Vector search | pgvector |
| Object/file storage | S3-compatible storage |
| OCR | Gemini Vision or specialized OCR provider |
| LLM | OpenAI/Gemini/other suitable provider |
| Background jobs | Celery + Redis |
| Authentication | Django auth + JWT/OAuth |
| Search | PostgreSQL initially; Elasticsearch/OpenSearch later if required |
| Deployment | Docker |
| CI/CD | GitHub Actions |
| Monitoring | Sentry + application metrics |

---

# 30. Background Processing Architecture

Heavy AI/OCR work should not block ordinary API requests.

```text
                 Django API
                     │
                     ↓
                Task Queue
                     │
              ┌──────┼───────┐
              ↓      ↓       ↓
             OCR   Verify   Embed
              │      │       │
              └──────┼───────┘
                     ↓
                  Storage
```

Typical asynchronous tasks:

- OCR
- Document parsing
- Claim extraction
- Evidence retrieval
- Verification
- Embedding generation
- Flashcard generation
- Recommendation recalculation

---

# 31. API Layer — Conceptual Endpoints

The exact endpoint design can change, but a first version could look like:

```text
POST   /api/auth/register
POST   /api/auth/login
POST   /api/notes
GET    /api/notes/{id}
POST   /api/notes/{id}/process
GET    /api/notes/{id}/claims
GET    /api/claims/{id}
GET    /api/claims/{id}/evidence
GET    /api/concepts/{id}
GET    /api/concepts/{id}/related
GET    /api/flashcards/feed
GET    /api/flashcards/{id}
GET    /api/concepts/{id}/explain
POST   /api/feedback
POST   /api/concepts/{id}/save
GET    /api/progress
```

These should expose stable domain operations rather than raw database tables.

---

# 32. Security and Privacy Considerations

User notes can contain personal or sensitive information. The system should therefore include:

- Authentication
- Authorization
- Per-user access control
- Secure object storage
- Encryption in transit
- Encryption at rest where available
- Audit logging
- Data deletion workflows
- Clear AI/data-retention policies
- Separation between user-private notes and public/canonical knowledge

A user's note should not automatically become public knowledge.

---

# 33. Data Isolation Principle

The architecture should distinguish:

```text
USER PRIVATE DATA
        │
        │ permissioned processing
        ↓
    MOSAIC AI
        │
        ↓
VERIFIED KNOWLEDGE
```

The system should not assume that a private upload is available for public training or redistribution.

---

# 34. Contributor Reliability

The reward/source-reliability system should primarily encourage useful contributions.

Possible inputs:

- Percentage of accepted claims
- Correction rate
- Evidence quality
- Community feedback
- Number of useful contributions
- Long-term accuracy

Important:

> Contributor reliability should influence prioritization/confidence carefully, but it should never replace evidence.

A highly reliable contributor can still be wrong.

---

# 35. Human-in-the-Loop Verification

Not every claim should be forced into an automatic verdict.

```text
                 Claim
                   │
                   ↓
              AI Verification
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
     Strong      Mixed      Weak
     evidence   evidence    evidence
        │          │          │
        ↓          ↓          ↓
      Auto       Human       Hold
     accept      review      state
```

Human review becomes particularly important for:

- Ambiguous claims
- Conflicting sources
- Medical/legal/scientific high-stakes information
- Rapidly changing information
- Low-confidence evidence

---

# 36. High-Stakes Knowledge

MOSAIC should distinguish ordinary educational content from high-stakes domains.

Examples:

- Medicine
- Law
- Finance
- Safety-critical engineering

These domains should have stricter source requirements, more explicit uncertainty, stronger provenance and potentially mandatory human review.

---

# 37. Recommendation System Evolution

### Phase 1

Basic recommendations based on:

- Topic interests
- Recently viewed concepts
- Saved topics

### Phase 2

Add:

- Difficulty
- Prerequisites
- User mastery
- Similar concepts
- Learning history

### Phase 3

Add:

- Collaborative signals
- Semantic user profile
- Long-term learning goals
- Context-aware recommendations

---

# 38. Flashcard Generation Architecture

Flashcards should be generated from canonical knowledge rather than raw user notes.

```text
Canonical Concept
       ↓
Select interesting fact / relationship
       ↓
LLM generation
       ↓
Validation
       ↓
Static visual/card sequence
       ↓
Recommendation feed
```

The flashcard system should retain provenance back to the underlying concept and evidence.

---

# 39. Flashcard Quality Controls

Generated flashcards should be checked for:

- Factual consistency
- No unsupported claims
- Clarity
- Appropriate difficulty
- Lack of copied expressive text
- Source/provenance traceability
- Appropriate visual sequence logic

The generator should never be trusted as an unverified content writer.

---

# 40. Example End-to-End Scenario

A student uploads handwritten notes about BFS.

### Step 1 — Upload

```text
Image → File Storage
```

### Step 2 — OCR

```text
Image → OCR → Text
```

### Step 3 — Claims

```text
Text → Claims
```

### Step 4 — Verification

```text
Claims → Evidence Retrieval → Verification
```

### Step 5 — Enrichment

MOSAIC adds:

- Queue-based traversal
- Time complexity
- Space complexity
- Shortest-path condition
- Related DFS concept

### Step 6 — Canonical KB

```text
BFS
├── uses queue
├── O(V + E)
├── shortest path in unweighted graphs
└── related-to DFS
```

### Step 7 — Flashcard

```text
"Why does BFS give the shortest path in an unweighted graph?"
```

### Step 8 — Swipe

```text
Graph → Queue → Expansion → Result
```

### Step 9 — In-depth

User taps **In-depth**.

MOSAIC retrieves the canonical BFS concept + relationships + evidence and generates a deeper explanation.

---

# 41. Architecture Principles

The system should follow these principles:

### 1. Source ≠ Truth

A source provides evidence; it is not automatically canonical truth.

### 2. Claim-Level Verification

Verify individual claims rather than entire documents.

### 3. Provenance Everywhere

Every canonical fact should be traceable to supporting evidence.

### 4. Uncertainty is Valid

The system should be able to say `UNCERTAIN`.

### 5. Evidence Before Generation

LLMs should generate from retrieved/approved knowledge.

### 6. Canonical Knowledge is Separate

Never mix raw user content and canonical MOSAIC knowledge into one untraceable corpus.

### 7. Start Simple

Use a modular monolith and PostgreSQL before introducing many microservices/databases.

### 8. Legal Compliance is an Engineering Constraint

Source licensing and usage rules should be represented in the ingestion pipeline.

---

# 42. MVP Scope

The recommended MVP should contain:

```text
✓ User authentication
✓ Handwritten note upload
✓ OCR
✓ Claim extraction
✓ Evidence retrieval
✓ Claim verification
✓ Canonical knowledge storage
✓ Basic enrichment
✓ Static flashcards
✓ Swipe sequence
✓ In-depth grounded explanation
✓ Basic feedback
```

Do not make these core MVP dependencies:

```text
✗ Complex social graph
✗ Friends/chat
✗ Large reputation system
✗ Microservices everywhere
✗ Full knowledge graph database
✗ Massive multi-site scraping operation
✗ Complex mastery engine
```

Those can follow once the core knowledge loop works.

---

# 43. Development Roadmap

## Phase 0 — Architecture and Research

- Finalize domain model
- Define source policy
- Define licensing/provenance model
- Select OCR provider
- Select LLM provider
- Define evaluation datasets

## Phase 1 — Note Intelligence

- Upload notes
- OCR
- Parsing
- Claim extraction
- Basic verification
- Correction UI

## Phase 2 — Canonical Knowledge

- Concepts
- Claims
- Evidence
- Sources
- Relationships
- Embeddings
- RAG

## Phase 3 — Learning Experience

- Flashcards
- Swipe sequences
- In-depth explanation
- Save/feedback

## Phase 4 — Personalization

- Recommendation engine
- Learning history
- Mastery
- Adaptive difficulty

## Phase 5 — Community

- Contributions
- Reputation
- Comments
- Sharing
- Friends

## Phase 6 — Scale

- Dedicated search infrastructure
- Specialized graph infrastructure if needed
- Service decomposition
- Source partnerships/licensing
- Advanced recommendation systems

---

# 44. Risks and Mitigation

| Risk | Impact | Mitigation |
|---|---:|---|
| OCR errors | High | Confidence thresholds + human correction |
| LLM hallucination | High | Evidence-backed generation |
| False verification | Very High | Multiple evidence sources + confidence + review |
| Bad source quality | High | Source authority hierarchy |
| Copyright/licensing issues | Very High | Source registry + permissions + legal review |
| Knowledge poisoning | Very High | Canonical KB separated from raw sources |
| AI cost | Medium/High | Async processing, caching, batch jobs |
| Slow processing | Medium | Background workers |
| Recommendation cold-start | Medium | Topic-based initial heuristics |
| Over-engineering | High | Modular monolith first |
| Knowledge becoming stale | Medium/High | Retrieval timestamps + re-verification |

---

# 45. Evaluation Metrics

MOSAIC should be evaluated using measurable quality metrics rather than only UI feedback.

## Verification

- Claim verification precision
- Claim verification recall
- False acceptance rate
- False rejection rate
- Uncertainty calibration

## OCR

- Character/word accuracy
- Claim extraction accuracy

## RAG

- Retrieval precision
- Retrieval recall
- Evidence support rate
- Citation correctness

## Flashcards

- Factual error rate
- User engagement
- Save rate
- Completion rate

## Learning

Eventually measure:

- Recall improvement
- Retention
- Mastery progression
- Time-to-understanding

---

# 46. Key Strategic Decision

MOSAIC should **not** compete primarily by having access to the most websites.

It should compete by doing a better job of:

```text
Collecting
   ↓
Understanding
   ↓
Verifying
   ↓
Connecting
   ↓
Enriching
   ↓
Teaching
```

The moat is therefore potentially:

```text
Evidence
   +
Claim graph
   +
Concept graph
   +
Provenance
   +
Personal learning history
   +
Recommendation data
   +
High-quality verification
```

---

# 47. Final Architecture Summary

```text
                              ┌───────────────┐
                              │     USER      │
                              └───────┬───────┘
                                      │
                     ┌────────────────┼─────────────────┐
                     │                                  │
                     ↓                                  ↓
              UPLOAD NOTES                         ASK / EXPLORE
                     │                                  │
                     ↓                                  │
                OCR / PARSER                            │
                     │                                  │
                     ↓                                  │
              CLAIM EXTRACTION                           │
                     │                                  │
                     ↓                                  │
              ┌──────────────┐                          │
              │ VERIFICATION │                          │
              └──────┬───────┘                          │
                     │                                  │
        ┌────────────┼────────────┐                     │
        ↓            ↓            ↓                     │
    SUPPORTED    CONTRADICTED  UNCERTAIN                │
        │            │            │                     │
        │            ↓            ↓                     │
        │       CORRECTION     HUMAN REVIEW              │
        │            │            │                     │
        └────────────┼────────────┘                     │
                     ↓                                  │
              ┌──────────────┐                          │
              │  ENRICHMENT  │                          │
              └──────┬───────┘                          │
                     ↓                                  │
          ┌─────────────────────┐                       │
          │ CANONICAL KNOWLEDGE │◄──────────────────────┘
          │                     │
          │ Concepts            │
          │ Claims              │
          │ Relations           │
          │ Evidence            │
          │ Sources             │
          │ Confidence          │
          └──────────┬──────────┘
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
      PostgreSQL  Vector DB   Search
          │          │          │
          └──────────┼──────────┘
                     ↓
                   RAG
                     ↓
                   LLM
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    FLASHCARDS   IN-DEPTH    RECOMMENDATION
        │        EXPLANATION       │
        ↓            ↓             ↓
      SWIPE       LEARN       PERSONALIZE
        │            │             │
        └────────────┼─────────────┘
                     ↓
                  FEEDBACK
                     ↓
              USER KNOWLEDGE
```

---

# 48. Recommended Immediate Build Order

The most practical implementation order is:

```text
1. Django + DRF + PostgreSQL
        ↓
2. User authentication
        ↓
3. Note upload + object storage
        ↓
4. OCR pipeline
        ↓
5. Claim extraction
        ↓
6. Source/evidence layer
        ↓
7. Verification engine
        ↓
8. Canonical knowledge model
        ↓
9. Embeddings + pgvector
        ↓
10. RAG explanation
        ↓
11. Flashcards
        ↓
12. Swipe experience
        ↓
13. Basic recommendations
        ↓
14. Mastery / social / scale features
```

---

# 49. Conclusion

The technically strongest version of MOSAIC is not simply a scraper, OCR tool, RAG chatbot, or flashcard application.

It is a **knowledge-processing pipeline**:

```text
Human Notes
    +
Trusted External Evidence
    ↓
MOSAIC
    ↓
Verify
    ↓
Connect
    ↓
Enrich
    ↓
Canonical Knowledge Graph
    ↓
Retrieve
    ↓
Teach
```

The most important architectural decision is to keep the following separate:

```text
RAW USER CONTENT
        ≠
EXTERNAL SOURCE CONTENT
        ≠
EXTRACTED CLAIMS
        ≠
EVIDENCE
        ≠
CANONICAL MOSAIC KNOWLEDGE
```

Maintaining these boundaries gives MOSAIC a much stronger foundation for accuracy, provenance, scalability, privacy, and future product differentiation.

---

# 50. Reference Links for Source/Licensing Research

These references are starting points for the source-policy work and should be re-checked before implementation or commercial launch:

- GitHub Acceptable Use / platform policy: https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies
- Stack Overflow licensing: https://stackoverflow.com/help/licensing
- MDN copyright and license guidance: https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Attrib_copyright_license
- Reddit Developer Terms: https://redditinc.com/policies/developer-terms
- MIT OpenCourseWare terms: https://ocw.mit.edu/pages/privacy-and-terms-of-use/
- OpenStax licensing information: https://help.openstax.org/s/article/Openstax-textbook-licensing-and-customization
- arXiv bulk data documentation: https://github.com/arXiv/arxiv-docs/blob/develop/source/help/bulk_data.md

> **Legal note:** This report is an architectural/product planning document, not legal advice. Before relying on third-party content commercially, obtain a jurisdiction-specific review of licenses, platform terms, copyright/fair-dealing/fair-use rules, privacy obligations, AI/ML usage restrictions, attribution requirements, and redistribution rights.
