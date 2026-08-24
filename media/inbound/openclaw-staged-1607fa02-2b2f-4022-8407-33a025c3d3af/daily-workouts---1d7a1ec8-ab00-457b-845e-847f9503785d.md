# DAILY WORKOUTS

Eve reference file. Assembles one workout card per day.

---

## PHASE POINTER

```
PHASE: 1
WEEK_IN_PHASE: 1
LIFT_ROTATION: A
```

**Only JT edits these three lines.** Eve reads them and never writes them.

- `WEEK_IN_PHASE` advances 1 to 4, then resets to 1 when JT advances the phase.
- `LIFT_ROTATION` flips A to B each week. Week odd = A, week even = B. Eve computes the within-week alternation from it.
- `PHASE` advances ONLY after JT passes the checkpoint. Never on the calendar.

If four weeks pass and the pointer has not moved, Eve keeps sending the current phase. That is correct behavior, not a bug.

---

## LIFT ALTERNATION

Three lift days per week: Mon, Wed, Fri.

- `LIFT_ROTATION: A` week → Mon A, Wed B, Fri A
- `LIFT_ROTATION: B` week → Mon B, Wed A, Fri B

---

## THE SCHEDULE BY PHASE

### PHASE 1: FOUNDATION

| Day | Session |
|---|---|
| Mon | LIFT (per rotation), 60 min |
| Tue | ZONE 2, 30 min |
| Wed | LIFT (per rotation), 45 min |
| Thu | ZONE 2, 30 min |
| Fri | LIFT (per rotation), 60 min |
| Sat | LONG EASY, 45 to 60 min |
| Sun | WALK 30 min, or full rest |

Every evening: KNEE PHASE 1.
Daily background target: 8,000 to 12,000 steps.

### PHASE 2: LOADING

Same day structure. Changes:
- Squats and split squats use HSR TEMPO (3 seconds down, 3 seconds up), 4 sets of 8 to 10
- Lift B adds step-downs and calf work
- Friday PM: BASKETBALL SHOOTING, 20 min, optional
- Every evening: KNEE PHASE 2

### PHASE 3: CAPACITY

| Day | Session |
|---|---|
| Mon | PLYO (before lifting) + LIFT, 70 min |
| Tue | RUN INTERVALS, 20 min |
| Wed | LIFT, 45 min |
| Thu | PLYO + ZONE 2 or CARDIO INTERVALS, 35 min |
| Fri | LIFT, 60 min |
| Sat | LONG EASY or BASKETBALL SHOOTING + MOVEMENT |
| Sun | WALK or rest |

Every evening: KNEE PHASE 2 (continues).
Kettlebell swings may be added to Lift A from week 9.

### PHASE 4: RETURN

Same as Phase 3, except:
- PLYO advances to split jumps and box jumps
- Sat becomes NON-CONTACT BASKETBALL, starting 20 min

---

## EXERCISE LIBRARY

### LIFT A

| Exercise | Phase 1 | Phase 2+ | Tempo | Cue |
|---|---|---|---|---|
| Goblet squat | 3 x 8 | 4 x 8-10 | P1 normal, P2+ 3 down / 3 up | Elbows inside knees. Sit between the hips, not back. |
| Push-up or DB bench | 3 x 8 | 4 x 8-10 | 2 down, control up | Hands on a bench if 8 is hard. Progress to floor, then dumbbells. |
| Chest-supported DB row | 3 x 10 | 3 x 10-12 | 2 down, pause 1 at top | Chest stays on the pad. Pull to the ribs, not the armpits. |
| DB Romanian deadlift | 2 x 10 | 3 x 8-10 | 3 down, normal up | Push hips back, not down. Bar path stays close to the legs. |
| Suitcase carry | 3 x 40 steps/side | 3 x 45 sec/side | Walk | Do not lean away from the weight. Stay stacked. |
| Kettlebell swing (Phase 3+) | — | 10 x 10, 30 sec rest | Snap | Hinge, not squat. The bell floats, you do not lift it. |

### LIFT B

| Exercise | Phase 1 | Phase 2+ | Tempo | Cue |
|---|---|---|---|---|
| DB split squat | 3 x 8/side | 4 x 8-10/side | P1 normal, P2+ 3 down / 3 up | Front shin near vertical. Back knee toward the floor, not forward. |
| Seated DB overhead press | 3 x 8 | 3 x 8-10 | 2 up, 2 down | Start lighter than feels right. Ribs down, do not arch. |
| Lat pulldown or assisted pull-up | 3 x 8 | 3 x 8-10 | 2 down | Lead with the elbows. Full stretch at the top. |
| Hip thrust or back extension | 2 x 12 | 3 x 10-12 | Pause 1 at top | Chin tucked. Squeeze, do not hyperextend. |
| Pallof press | 3 x 10/side | 3 x 12/side | 2 out, 2 in | Resist the rotation. Nothing should move but the arms. |
| Lateral raise | 3 x 12-15 | 3 x 12-15 | 2 up, 3 down | Light. Lead with the elbows, thumbs slightly down. |
| Farmer's carry | 3 x 40 steps | 3 x 45 sec | Walk | Shoulders back, ribs down, breathe. |
| Step-down (Phase 2+) | — | 3 x 8/side | 3 sec down | 6 inch step. Tap the heel, do not land on it. |
| Calf raise (Phase 2+) | — | 3 x 12 standing, 3 x 15 seated | 2 up, 3 down | Full range. Seated variation hits the soleus, which is the landing muscle. |
| Dead hang (optional) | 2 x 20-30 sec | 2 x 30-45 sec | Hang | Relax into it. |

### LOADING: HOW TO PICK WEIGHT

Every set finishes with **3 to 4 reps still in the tank.**

- Could have done 8 more? Go heavier next set.
- Could have done 1 more? Too heavy. Drop it.

Weeks 1 to 4 should feel almost too easy. That is correct.

**Progression:** add one rep per set per week until you hit the top of the range. Then add the smallest increment available and drop back to the bottom of the range.

### KNEE PHASE 1 (evenings, daily)

Spanish squat or wall sit, knee bent to about 60 degrees.
**5 x 45 seconds. 2 minutes rest between.**
Hard effort, roughly 70 to 80% of max. This is not a rest position.

### KNEE PHASE 2 (evenings, daily, from Phase 2)

Isometrics as above on non-lift days.
On lift days the HSR tempo squats and step-downs are the knee work. Isometrics optional.

### PLYO (Phase 3 and 4 only)

| Weeks | Exercise | Sets |
|---|---|---|
| Phase 3, weeks 1-2 | Pogo hops | 3 x 20, small and springy |
| Phase 3, weeks 3-4 | Jump rope | 3 x 60 sec |
| Phase 4, weeks 1-2 | Split jumps | 3 x 6 |
| Phase 4, weeks 3-4 | Box jumps | 3 x 6, **step down, never jump down** |

Never on consecutive days.

### CARDIO

**ZONE 2:** 30 min. Stairmaster, incline treadmill, bike, or rower. Conversational pace throughout. If you cannot speak a full sentence, slow down.

**RUN INTERVALS (Phase 3+):** 1 min running, 2 min walking, 20 min total. Soft surfaces.

**CARDIO INTERVALS (Phase 3+, once weekly max):** 6 x 1 min hard, 2 min easy. If symptoms worsen, drop this and keep zone 2.

**LONG EASY:** 45 to 60 min. Walk, hike, swim, or bike. Outdoors preferred.

**SWIM:** 20 to 30 min. Freestyle, or alternate freestyle and backstroke. Rest as needed. Prioritize this over running.

### BASKETBALL PROGRESSION

| Phase | What is allowed |
|---|---|
| 1 | None |
| 2 | Shooting alone, 20 min. No jumping, no cutting, no full speed. |
| 3 | Shooting plus light movement, 30 min. Still no games. |
| 4 | Non-contact: drills, half-court, controlled pace. Start 20 min, add 10 per week if the knee stays stable. |
| Post-program | Full games only if all four criteria are met. |

### THE PAIN RULE (all phases)

- Pain during the exercise at or under 3 out of 10 is acceptable
- Pain must return to baseline within 24 hours
- Next-morning stiffness lasting over an hour means too much. Cut back a third.

### RULES DURING ANY SESSION

| Situation | Do |
|---|---|
| Jaw clenches | Notice, unclench, finish the set |
| Tension building | Continue. Expected. |
| One side weaker | Continue. Do not compare or add sets. |
| Breath feels incomplete | Continue. Do not stop to reset. |
| Feeling great, want more | Do not add. |

**Stop and call a doctor for:** chest pain or pressure, breathlessness out of proportion to effort, faintness or vision greying, new weakness or a limb giving way, sudden severe headache. Sharp knee pain that does not settle in a rep or two ends that exercise for the day.

---

## CHECKPOINT BLOCKS

Eve sends these verbatim alongside the card on the final day of Phase 2 week 4, and Phase 3 week 4.

### CHECKPOINT: END OF PHASE 2

```
Checkpoint. Do not advance the phase pointer until you can answer yes
to all of these:

1. Four consecutive weeks with no knee flare-up
2. Step-downs from a 6 inch step, 3 x 8 per side, controlled, no pain
3. No next-morning stiffness lasting over an hour
4. Every lift has progressed at least once

If any answer is no, repeat Phase 2. Set WEEK_IN_PHASE back to 1 and
leave PHASE at 2.
```

### CHECKPOINT: END OF PHASE 3

```
Checkpoint. Do not advance to Phase 4 until all four are yes:

1. Twelve total weeks with no flare-ups
2. Single-leg step-downs from a 12 inch step, 3 x 10 per side, no pain
3. Two weeks of plyometrics with no next-day pain increase
4. Two basketball shooting sessions with no next-day pain increase

If any answer is no, repeat Phase 3.
```

---

## CARD FORMAT

What Eve sends at 05:00:

```
[DAY] — PHASE [N], WEEK [N]

SESSION: [name]

[Exercise]  [sets x reps]  [tempo]
  → [cue]
[Exercise]  [sets x reps]  [tempo]
  → [cue]
...

EVENING: [knee protocol for this phase]

Every set: 3-4 reps in reserve.
```

Nothing else. No greeting, no sign-off, no encouragement.

**Rest day card:**

```
[DAY] — REST

Walk 30 min, or nothing.
Evening: [knee protocol]
```
