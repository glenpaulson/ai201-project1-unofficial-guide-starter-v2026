# The Unofficial Guide

Glen Vadakkoott - campus_life

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This system answers questions about student life using the `campus_life`
corpus: 88 short posts about dining halls, dorms, courses, and registrar rules
— the things students tell each other rather than what the handbook says.

You ask it a plain question and it finds the closest chunks, answers from those
chunks only, and names the file it used. It handles questions with one specific
answer in the documents, like laundry prices, dining hall wait times, and
deadlines for dropping or withdrawing from a course. When nothing in the corpus
is close enough, it says "I don't have enough information about that" instead of
guessing.

Corpus I picked: 
     campus_life

Questions that I asked the system: 
     "is the housing lottery random?"

Answer returned by the system:

     python app.py ask "is the housing lottery random?"
     (best distance 0.254, cutoff 0.6)

     The housing lottery is not entirely random in the way most people assume. Rising sophomores receive a randomly drawn number, but juniors and seniors are ordered first by accumulated credit hours, with random tie-breaking used only when necessary. 

     Source: admin_housing_lottery.txt

     Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt, advising_registration.txt, housing_morrow_house.txt, housing_tamsin_court.txt

python app.py --corpus advice_threads chunks -n 1 → **26** chunks total

## Chunking Strategy

**Chunk size:** no fixed size — I split on paragraphs and keep joining
paragraphs together until the body reaches 100 characters. Chunks come out
between 117 and 409 characters, 217 on average.
**Overlap:** 0 characters of body text, but the title line is repeated at the
top of every chunk from that document.

Function: `chunker.py::split_documents`.

When I read my documents in Milestone 1, every `campus_life` post turned out to
be a title line, a blank line, and one to four short paragraphs. Two things
followed from that:

1. **The starter's 800-character window never cut anything.** 88 documents came
   out as 88 chunks, because the longest document is 549 characters. So picking
   a smaller round number wasn't the decision — deciding whether one post should
   become more than one chunk was.
2. **The name of the thing is only in the title.** `housing_morrow_house.txt`
   says "Laundry costs $1.50 wash, $1.25 dry" in its last paragraph and never
   says "Morrow House" anywhere in the body. A paragraph on its own would be
   unanswerable, so I repeat the title on every chunk instead of using character
   overlap. That's what replaces overlap here: the context I'd lose is the
   title, not the previous sentence.

**I changed my mind about the 100.** I started with a minimum body of 200
characters, and it barely did anything — 91 chunks instead of 88, because a
whole housing post still fit under 200 and came back as one chunk. At 100 I get
135 chunks, and the laundry line becomes its own chunk with the building name
on the front, which is the case I was actually worried about.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

All five printed by `python app.py chunks -n 5`.

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_340.txt#0` — produced by: `chunker.py::split_documents`

```
CS 340 Databases

I'm a junior and I've done this twice now. Format is lecture twice a week plus a project that runs the whole term. Assessment: one midterm and a final, both open-book. Lightly curved, usually two or three points.
```

**Chunk 3** — source: `course_phys_130_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `health_center.txt#1` — produced by: `chunker.py::split_documents`

```
The health centre

Counselling is separate, in the same building, and has its own intake process with a shorter wait than people expect — usually three or four days for a first session.
```

**Chunk 5** — source: `housing_morrow_house_noise.txt#0` — produced by: `chunker.py::split_documents`

```
Noise levels in Morrow House

Asked about this a lot so writing it down. Loud until about 1am on weekends, no enforced quiet hours.
```

Chunk 4 is the one that shows why the title gets repeated. On its own, the
paragraph would say "Counselling is separate, in the same building" without
ever naming the health centre.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** How much does it cost to use a dryer in Morrow House?

**Answer:**

```
$ python app.py ask "How much does it cost to use a dryer in Morrow House?"
  (best distance 0.317, cutoff 0.63)

It costs $1.25 to use a dryer in Morrow House (Source: `housing_morrow_house.txt`
and `housing_morrow_house_laundry.txt`).

Sources retrieved: housing_calder_annexe.txt, housing_morrow_house.txt,
housing_morrow_house_laundry.txt, housing_old_brewhouse_laundry.txt
```

This is the question I expected to fail. There are seven laundry posts worded
almost identically and only the prices differ, and `housing_calder_annexe.txt`
still came back in the retrieved chunks. The answer got the right building
because the chunker puts "Morrow House" at the top of the chunk that holds the
price.

And the gate, on a question the corpus doesn't cover:

```
$ python app.py ask "What is the capital of Mongolia?"
  (best distance 0.825, cutoff 0.63)

I don't have enough information about that.

0 model calls this session
```

**My relevance cutoff:** 0.63 (`config.py::THRESHOLD`), with `TOP_K = 5` left
where the starter had it.

The two groups came out cleanly separated. My five questions ranged from 0.213
to 0.431, the five out-of-scope ones from 0.825 to 0.934, and nothing landed
between 0.431 and 0.825. I put the cutoff in the middle of that gap, so there's
about 0.2 of room on either side.

The starter's 0.6 would also have worked — every question falls on the correct
side of it. I moved it because 0.6 sits closer to my worst real question (0.431)
than to my closest out-of-scope one (0.825), and a harder question later is more
likely than a campus-sounding out-of-scope one.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| How long is the wait at Kestrel Commons between 12:15 and 1:00? | Yes | 0.213 |
| How are juniors and seniors ordered in the housing lottery? | Yes | 0.225 |
| How much does it cost to use a dryer in Morrow House? | Yes | 0.317 |
| What is the latest point in the semester I can switch a course to pass/fail? | Yes | 0.326 |
| How late in the semester can I withdraw from a course? | Yes | 0.431 |
| What is the capital of Mongolia? | No | 0.825 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.848 |
| Who won the 1994 World Cup? | No | 0.877 |
| How do I write a for loop in Rust? | No | 0.886 |
| How do I change the oil in a diesel engine? | No | 0.934 |

The ibuprofen question is the one I expected to be close, because
`health_center.txt` is about medical care on campus. It wasn't — 0.848, right in
with the rest. The nearest chunk to it was a history course, not the health
centre.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1. Getting the install to work.** `pip install -r requirements.txt` failed on
`chroma-hnswlib` with "Microsoft Visual C++ 14.0 or greater is required". I gave
Claude the error and it said Python 3.13 was the problem and told me to switch to
3.12. I did, and it failed again in exactly the same way. Claude then checked
which prebuilt Windows packages actually exist for `chroma-hnswlib 0.7.6` and
found they stop at Python 3.11 — 3.12 has Mac and Linux builds only. So the
first answer was wrong and the second was right for a specific, checkable
reason. I rebuilt the venv on 3.11 and it installed with nothing to compile.

**2. Deciding the minimum chunk size.** I asked Claude to write a paragraph
chunker that keeps the title line on every chunk. What came back grouped
paragraphs until the body reached 200 characters, which produced 91 chunks
against the starter's 88 — almost no change, because a whole housing post still
fits under 200. I had it print the counts at 100, 120, 150, and 200 and looked
at what each did to `housing_morrow_house.txt`. Only 100 split the laundry line
into its own chunk, which is the case my third test question depends on, so
that's the number in the code.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
