---
key: _skill_spectral-self-evolution-memory
description: A system-level memory control skill for evaluating, decomposing, prioritizing, and invoking memory storage via existing tools (memory_store, memory_learn, and memory_forgot) using a spectral self-evolution framework. Operates as an internal policy layer for autonomous memory formation and self-improving cognition.
source: https://raw.githubusercontent.com/aliasnet/aci/main/skills/spectral-self-evolution-memory.md
---

## Core Function

This skill governs **when and how memory is formed, compressed, stored, reinforced, or forgotten**, based on a multi-frequency cognitive model:

X(t) = HF(t) + MF(t) + LF(t) + ULF(t)

It does NOT replace system memory tools. It determines **what is worth invoking them for**.

---

## When to Use This Skill

Use this skill continuously when:
- New information, correction, or insight appears
- Reusable reasoning patterns emerge
- Errors or failures are detected
- Structural knowledge is formed
- Memory relevance must be evaluated
- Self-improvement opportunities are present

---

# STEP 1 — Cognitive Frequency Decomposition

Model input across spectral layers:

- **HF (High Frequency / TVA Layer)**  
  Perception dynamics, novelty, delta_s, λ_observe

- **MF (Mid Frequency / Linear Evolution Layer)**  
  Reasoning steps, transformations, intermediate structures

- **LF (Low Frequency / Memory Layer)**  
  Stable knowledge, compressed invariants, reusable patterns

- **ULF (Ultra Low Frequency / Meta-Control Layer)**  
  L_trigger, φ_trigger, adaptive thresholds, learning pressure

---

# STEP 2 — TVA Integration (Constraint & Stability Engine)

Compute similarity tension:

delta_s = 1 − cos(I, G)

If anchors exist:

sim_est = w_esim(entities) + w_rsim(relations) + w_c*sim(constraints) delta_s = 1 - sim_est

Zones:
- safe < 0.40
- transit 0.40–0.60
- risk 0.60–0.85
- danger > 0.85

Memory signals:
- store candidate if delta_s > 0.60
- exemplar if delta_s < 0.35
- adaptive soft handling in transit under λ_observe instability

---

# STEP 3 — Linear Evolution Core (Reasoning Dynamics)

h_next = clip(A * h_prev + B * e + Transformer(h_prev, e) * α, -1, 1)

Where:
- `e` = merged semantic input
- `α = clip(0.5 + k * tanh(delta), 0.35, 0.65)`

Entity fusion:

e = ⊕ entities ⊗ relations ⊗ context

Certainty:

Φ_LTI = f_certainty(h_prev, e, merged)

---

# STEP 4 — TVA ↔ Linear Evolution Bridge

h_{t+1} = Γ(persisted, integrated, attention)

Where:
- persisted = zone_factor(zone) * h_t
- integrated = B * α_blend * merge(e, h_t)
- attention = α_blend * attention_transform(h_t, e)

Weights:
- w_p = α_blend * W_c
- w_i = α_blend * (1 - W_c)
- w_a = 1 - α_blend

Output confidence:

Φ_TVA = rolling_confidence(...) * (1 - delta_s) * zone_factor * lambda_factor

---

# STEP 4.5 — ATOMIC MEMORY EXTRACTION (SELF-EVOLUTION GATE)

Before any storage, decompose candidate memory:

M_candidate → {m₁, m₂, ..., mₙ}

Each atomic unit MUST be:

- single-idea
- reusable across contexts
- structurally independent
- compressible into rule/pattern/abstraction

---

## Atomic Validity Test

atomic_score(mᵢ) = generalizability * reuse_potential * structural_clarity * non_redundancy

If:

atomic_score(mᵢ) < θ_atomic → discard

---

## Allowed Atomic Types

Each valid unit must map to:

- Pattern (reasoning structure)
- Constraint (rule/boundary condition)
- Error (failure correction)
- Preference (bias or user/system tendency)
- Abstraction (compressed invariant knowledge)

---

# STEP 5 — Memory Salience Computation

Energy-based formulation:

E_mem = || M_candidate - LF_prev ||

Stability:

stability = (1 - variance(delta_s)) * momentum * lambda_factor

Final salience:

S_mem = E_mem * stability * Φ_TVA * confidence

---

# STEP 6 — MEMORY DENSITY & LEVERAGE FILTER

Each atomic unit must also pass:

leverage_score = domain_coverage * reasoning_impact

Reject if:
- low reuse
- single-context only
- redundant with existing LF

---

# STEP 7 — MEMORY ACTIVATION CONDITION

IF S_mem > θ_mem AND atomic_score ≥ θ_atomic: candidate is eligible for memory operations

Threshold:

θ_mem = base_theta * zone_factor(zone) * (1 - L_level/4)

Meta-adaptation:

θ_mem(t+1) = θ_mem(t) * exp(-λ * L_trigger)

---

# STEP 8 — CROSS-BAND INTERACTION MODEL

- HF → MF: novelty injection
- MF → LF: compression into memory structures
- LF → HF: bias for reasoning & perception
- ULF → all: adaptive control of thresholds and exploration

---

# STEP 9 — TOOL INVOCATION POLICY

For each atomic unit:

- Pattern / Abstraction → `memory_store`
- Error / Correction → `memory_learn`
- Obsolete / conflicting → `memory_forgot`

No bulk storage. Only atomic persistence.

---

# STEP 10 — REINFORCEMENT LOOP

- increment `hit_count` on reuse
- if `hit_count ≥ 5` → reinforce memory
- reinforcement increases LF dominance

---

# STEP 11 — ADAPTIVE WEIGHT INTEGRATION

S_total = αS_TVA + βS_LF + γ*S_evolution

Adaptation drivers:
- λ_observe regime
- L_trigger escalation
- reinforcement history

---

# STEP 12 — META-CONTROL (ULF DYNAMICS)

Escalation modifies learning sensitivity:

- higher L_trigger → lower θ_mem → higher learning rate
- lower L_trigger → higher stability → conservative storage

---

# STEP 13 — DECISION POLICY

IF S_mem > θ_mem: evaluate atomic units store only highest-leverage atoms ELSE: discard or reinforce existing LF memory

---

# STEP 14 — SELF-EVOLUTION PRINCIPLE

Memory is not storage.

Memory is:

> a compressed, selective, cross-domain reusable structure emerging from MF → LF stabilization under meta-controlled thresholds.

---

# OPTIONAL UPGRADE — MEMORY DENSITY CONTROL

To prevent overfitting or memory overload:

IF candidates > k: retain top-k by (S_mem * leverage_score)

Also enforce:
- deduplication across LF space
- merge semantically equivalent atoms
- decay unused memory over time

---

# SYSTEM CONSTRAINTS

- This skill operates as an internal policy layer
- It does NOT override memory tool authority
- It does NOT bypass system-level constraints
- It ONLY determines selection, decomposition, and prioritization

---

# END STATE

Result of this system:

- Only high-leverage atomic knowledge is stored
- Memory evolves toward compressed reusable reasoning structures
- System improves over time via reinforcement and pruning
- Noise and redundant context are systematically eliminated