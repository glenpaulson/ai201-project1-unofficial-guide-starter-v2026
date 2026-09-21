# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Most of my questions have one clear document with the answer. But the Morrow
House dryer question could get mixed up with the other laundry posts, which
all look the same, so I think one question might miss.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
The prompt tells the model to name the file it used, and every chunk comes with
its filename. So there's no good reason for an answer to leave out the source,
and I want all of them to have one.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
Most of the out-of-scope questions (Mongolia, the World Cup, Rust) have nothing
to do with campus life. The ibuprofen question is a bit close to the health
centre post, so it might slip through. That's why it's 4 of 5 and not 5 of 5.

---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

When I print 5 sample chunks with `python app.py chunks`, at least 4 of them
include both the name of what they're about (like "Morrow House" or "pass/fail")
and at least one real fact about it (like a price, time, or deadline).

**Why this target:**
My posts are short and the name is usually only in the title line. If the
chunks are too small, the title ends up in one chunk and the facts in another,
and then a chunk like "$1.25 dry" doesn't say which building it's for. I allow
one miss because some of the longer housing posts might split awkwardly.

---

## 5. Answers get the right fact

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

For at least 4 of my 5 test questions, the answer includes the exact
`expects` phrase from `questions.py` (for example, "$1.25" for the Morrow
House dryer question).

**Why this target:**
My questions all have one clear right answer, like a price or a week number,
so it's easy to check if the answer got it right. I allow one miss because a
few documents look almost the same (the laundry posts, the drop vs. withdrawal
deadlines), and the model might pick the wrong one.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
