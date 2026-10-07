# Skill: hypothesis-test-decision-maker

## Metadata
- **Name:** hypothesis-test-decision-maker
- **Version:** 1.0
- **Description:** Evaluates hypothesis tests using p-value and critical value decision rules. Computes p-value based on test statistic and test type, applies both decision rule methods (p-value method and critical value method), and provides formal statistical conclusion.
- **Category:** Statistics, Hypothesis Testing, Statistical Inference
- **Trigger Keywords:** hypothesis test decision, p-value, critical value, reject H0, fail to reject, test conclusion, statistical decision, make a decision on hypothesis test

---

## When to Use This Skill

Trigger this skill when:
- User has conducted a hypothesis test and computed a test statistic
- User provides test statistic (z or t value), alpha level, and test direction
- User asks: "Do we reject or fail to reject H0?"
- User says: "What's the p-value and what does it mean?"
- User wants to make a formal statistical conclusion
- User needs to compare p-value method vs. critical value method

Example triggers:
- "I calculated z=2.45 for an upper-tailed test with alpha=0.05. What's the decision?"
- "Test statistic is t=1.89 with df=24, two-tailed test, alpha=0.01. Should I reject H0?"
- "Calculate the p-value for this z=1.645 statistic (upper-tailed) and tell me the decision"
- "Compare p-value and critical value methods for my hypothesis test"
- "My z-score is -1.23 for a lower-tailed test. Is this significant at alpha=0.10?"

---

## Core Logic & Framework

### **Step 1: Identify Test Components**

| Component | Symbol | Definition | Example |
|-----------|--------|-----------|---------|
| Test Statistic | z or t | Computed from sample data | z = 2.45 |
| Significance Level | α (alpha) | Type I error tolerance | 0.05 |
| Test Direction | - | Upper/Lower/Two-tailed | Upper-tailed |
| Degrees of Freedom | df | n - 1 for t-tests | 24 |

### **Step 2: Understand the Decision Rules**

There are **TWO equivalent methods** to make a decision. Both should give the same conclusion:

**METHOD 1: P-Value Approach**
```
Decision Rule: If p-value ≤ α, Reject H0
              If p-value > α, Fail to Reject H0
```

**METHOD 2: Critical Value Approach**
```
Decision Rule: If |test statistic| ≥ |critical value|, Reject H0
              If |test statistic| < |critical value|, Fail to Reject H0
```

---

### **Step 3: Calculate P-Value (Based on Test Type)**

The p-value is the **probability of observing a test statistic as extreme or more extreme than what we calculated, assuming H0 is true.**

#### **UPPER-TAILED TEST (Ha: μ > μ0)**

```
P-Value = P(Z ≥ z_calculated) = 1 - Φ(z_calculated)

Where Φ(z) is the cumulative standard normal probability
```

**Example:**
- If z_calculated = 2.45
- Φ(2.45) = 0.9929 (from normal table)
- P-value = 1 - 0.9929 = 0.0071 (0.71%)

---

#### **LOWER-TAILED TEST (Ha: μ < μ0)**

```
P-Value = P(Z ≤ z_calculated) = Φ(z_calculated)
```

**Example:**
- If z_calculated = -1.75
- Φ(-1.75) = 0.0401 (from normal table)
- P-value = 0.0401 (4.01%)

---

#### **TWO-TAILED TEST (Ha: μ ≠ μ0)**

```
P-Value = 2 × P(Z ≥ |z_calculated|) = 2 × (1 - Φ(|z_calculated|))
```

**Example:**
- If z_calculated = 1.96
- Φ(1.96) = 0.9750 (from normal table)
- P(Z ≥ 1.96) = 1 - 0.9750 = 0.0250
- P-value = 2 × 0.0250 = 0.0500 (5.00%)

---

### **Step 4: Apply Decision Rule #1 (P-Value Method)**

```
Compare: p-value vs. α

If p-value ≤ α:
  → Reject H0
  → Result is "statistically significant"
  → Evidence supports Ha

If p-value > α:
  → Fail to Reject H0
  → Result is "not statistically significant"
  → Insufficient evidence to support Ha
```

---

### **Step 5: Apply Decision Rule #2 (Critical Value Method)**

**Identify the Critical Value:**

| Test Type | H0 | Ha | Critical Region | z_crit (α=0.05) |
|-----------|----|----|-----------------|-----------------|
| **Upper-Tailed** | μ = μ0 | μ > μ0 | z > z_α | 1.645 |
| **Lower-Tailed** | μ = μ0 | μ < μ0 | z < -z_α | -1.645 |
| **Two-Tailed** | μ = μ0 | μ ≠ μ0 | \|z\| > z_α/2 | ±1.96 |

**Apply the Rule:**
```
Compare: |test statistic| vs. |critical value|

If |test statistic| ≥ |critical value|:
  → Reject H0 (test statistic falls in critical region)
  → Result is "statistically significant"

If |test statistic| < |critical value|:
  → Fail to Reject H0 (test statistic does NOT fall in critical region)
  → Result is "not statistically significant"
```

---

## Example Applications

### **Example 1: Upper-Tailed Test (z-test)**

**Scenario:**
A company claims their new process improves production time. Historical average = 50 minutes.
Sample of 100 units shows mean = 48.5 minutes, σ = 8 minutes.
Test at α = 0.05 (upper-tailed test: we want to show time DECREASED, or equivalently, μ is LESS than 50)

Wait, let me reconsider. Upper-tailed means Ha: μ > μ0 (value increased). Let me revise:

A company wants to show their new process reduces production time. Historical average = 50 minutes.
Sample of 100 units shows mean = 48.5 minutes, σ = 8 minutes.
Test at α = 0.05

Actually, if they want to show time reduced (goes DOWN), that's lower-tailed. Let me use upper-tailed properly:

A company wants to show their advertising increases sales. Historical average = $50,000.
Sample of 60 stores shows mean = $52,800, σ = $10,000.
Test at α = 0.05 (upper-tailed: Ha: μ > $50,000)

**Step 1: Compute Test Statistic**
```
z = (x̄ - μ0) / (σ / √n)
  = (52,800 - 50,000) / (10,000 / √60)
  = 2,800 / 1,291
  = 2.17
```

**Step 2: Calculate P-Value (Upper-Tailed)**
```
P-value = P(Z ≥ 2.17) = 1 - Φ(2.17) = 1 - 0.9850 = 0.0150 (1.50%)
```

**Step 3: Decision Rule #1 (P-Value Method)**
```
p-value (0.0150) ≤ α (0.05)?
YES → Reject H0
```

**Step 4: Critical Value (Upper-Tailed, α=0.05)**
```
z_crit = 1.645
|z_calculated| (2.17) ≥ |z_crit| (1.645)?
YES → Reject H0
```

**Step 5: Formal Conclusion**
```
Decision: REJECT H0

Interpretation: At the 0.05 significance level, we have sufficient evidence 
to conclude that the advertising campaign increased average sales above $50,000. 
The result is statistically significant (p = 0.0150).
```

---

### **Example 2: Two-Tailed Test (t-test)**

**Scenario:**
A restaurant claims their average service time is 20 minutes. A consumer group suspects this claim is inaccurate (either faster or slower).
Sample of 25 customers shows mean = 22.5 minutes, s = 5 minutes.
Test at α = 0.05 (two-tailed: Ha: μ ≠ 20 minutes)

**Step 1: Compute Test Statistic**
```
t = (x̄ - μ0) / (s / √n)
  = (22.5 - 20) / (5 / √25)
  = 2.5 / 1
  = 2.50
```

**Step 2: Calculate P-Value (Two-Tailed, df = 24)**
```
Using t-distribution with df = 24:
P(t ≥ 2.50) ≈ 0.0116 (upper tail)
P-value = 2 × 0.0116 = 0.0232 (2.32%)

[From t-table: t_0.0116, df=24 is between t_0.01 (2.492) and t_0.02 (2.164)]
```

**Step 3: Decision Rule #1 (P-Value Method)**
```
p-value (0.0232) ≤ α (0.05)?
YES → Reject H0
```

**Step 4: Critical Value (Two-Tailed, α=0.05, df=24)**
```
t_crit = ±2.064
|t_calculated| (2.50) ≥ |t_crit| (2.064)?
YES → Reject H0
```

**Step 5: Formal Conclusion**
```
Decision: REJECT H0

Interpretation: At the 0.05 significance level, we have sufficient evidence 
to conclude that the average service time differs from the claimed 20 minutes 
(specifically, appears to be longer). The result is statistically significant 
(p = 0.0232).
```

---

### **Example 3: Lower-Tailed Test**

**Scenario:**
A manufacturing plant wants to show that a new quality control process reduces defect rates. 
Historical defect rate = 8%.
Sample of 200 units shows 12 defects (6% rate), α = 0.05 (lower-tailed)

**Step 1: Compute Test Statistic (using proportion)**
```
p̂ = 12 / 200 = 0.06
SE = √[p0(1-p0)/n] = √[0.08 × 0.92 / 200] = √0.000368 = 0.0192

z = (p̂ - p0) / SE = (0.06 - 0.08) / 0.0192 = -0.02 / 0.0192 = -1.04
```

**Step 2: Calculate P-Value (Lower-Tailed)**
```
P-value = P(Z ≤ -1.04) = Φ(-1.04) = 0.1492 (14.92%)
```

**Step 3: Decision Rule #1 (P-Value Method)**
```
p-value (0.1492) ≤ α (0.05)?
NO → Fail to Reject H0
```

**Step 4: Critical Value (Lower-Tailed, α=0.05)**
```
z_crit = -1.645
z_calculated (-1.04) < z_crit (-1.645)?
NO → Fail to Reject H0
```

**Step 5: Formal Conclusion**
```
Decision: FAIL TO REJECT H0

Interpretation: At the 0.05 significance level, we do NOT have sufficient 
evidence to conclude that the new quality control process reduces defect rates 
below 8%. The observed difference (8% vs 6%) could be due to random sampling 
variation. The result is not statistically significant (p = 0.1492).
```

---

## Output Format

When applying this skill, provide:

```
HYPOTHESIS TEST DECISION ANALYSIS

TEST INFORMATION:
  - Test Type: [Upper-tailed / Lower-tailed / Two-tailed]
  - Null Hypothesis (H0): [state H0]
  - Alternative Hypothesis (Ha): [state Ha]
  - Significance Level (α): [value]
  - Sample Size (n): [value]
  - Degrees of Freedom (if t-test): [value]

TEST STATISTIC:
  - Value: [z or t] = [calculated value]
  - Type: [z-statistic / t-statistic]

P-VALUE CALCULATION:
  - Formula: [which formula for test direction]
  - Calculation: [steps]
  - Result: p-value = [value] ([percentage])

DECISION RULE #1: P-VALUE METHOD
  - p-value ([value]) vs. α ([value])
  - Comparison: p-value ≤ α? [YES / NO]
  - Decision: [REJECT H0 / FAIL TO REJECT H0]

CRITICAL VALUE:
  - [z_α or t_α (df)] = [value]
  - |test statistic| ([value]) vs. |critical value| ([value])
  - Comparison: |test stat| ≥ |critical| ? [YES / NO]

DECISION RULE #2: CRITICAL VALUE METHOD
  - Decision: [REJECT H0 / FAIL TO REJECT H0]

CONCLUSION:
  Decision: [REJECT H0 / FAIL TO REJECT H0]
  
  Interpretation: At the α = [value] significance level, we [have/do not have] 
  sufficient evidence to conclude that [state the alternative claim in plain language]. 
  The result is [statistically significant / not statistically significant] (p = [value]).
```

**Example Output:**
```
HYPOTHESIS TEST DECISION ANALYSIS

TEST INFORMATION:
  - Test Type: Upper-tailed
  - H0: μ = $50,000 (historical average sales)
  - Ha: μ > $50,000 (new advertising increases sales)
  - Significance Level (α): 0.05
  - Sample Size (n): 60 stores

TEST STATISTIC:
  - z = 2.17
  - Type: z-statistic (σ known)

P-VALUE CALCULATION:
  - Formula: P(Z ≥ z_calculated)
  - Calculation: P(Z ≥ 2.17) = 1 - Φ(2.17) = 1 - 0.9850
  - Result: p-value = 0.0150 (1.50%)

DECISION RULE #1: P-VALUE METHOD
  - p-value (0.0150) vs. α (0.05)
  - Is p-value ≤ α? YES
  - Decision: REJECT H0

CRITICAL VALUE:
  - z_0.05 = 1.645
  - |2.17| vs. |1.645|
  - Is 2.17 ≥ 1.645? YES

DECISION RULE #2: CRITICAL VALUE METHOD
  - Decision: REJECT H0

CONCLUSION:
  Decision: REJECT H0
  
  Interpretation: At the α = 0.05 significance level, we have sufficient 
  evidence to conclude that the advertising campaign increased average store 
  sales above $50,000. The result is statistically significant (p = 0.0150 < 0.05).
```

---

## P-Value Interpretation Guide

| P-Value Range | Interpretation | Strength of Evidence |
|---------------|----------------|----------------------|
| p < 0.001 | Extremely strong evidence against H0 | Very significant |
| 0.001 ≤ p < 0.01 | Very strong evidence against H0 | Highly significant |
| 0.01 ≤ p < 0.05 | Strong evidence against H0 | Significant |
| 0.05 ≤ p < 0.10 | Moderate evidence against H0 | Marginally significant |
| p ≥ 0.10 | Weak or no evidence against H0 | Not significant |

**Note:** The boundary α = 0.05 is conventional but not universal. Some fields use α = 0.01 or α = 0.10.

---

## Decision Framework Summary

```
STEP 1: State H0 and Ha
        ↓
STEP 2: Choose α (significance level)
        ↓
STEP 3: Collect data and compute test statistic
        ↓
STEP 4: Calculate p-value OR identify critical value
        ↓
STEP 5: Apply decision rule
        ├─ If p-value ≤ α → REJECT H0
        └─ If p-value > α → FAIL TO REJECT H0
        ↓
STEP 6: Interpret in context of original claim
```

---

## Common Mistakes & Clarifications

❌ **MISTAKE:** "The p-value is the probability that H0 is true"
✓ **CORRECT:** "The p-value is the probability of observing this statistic IF H0 is true"

❌ **MISTAKE:** "We accept H0" 
✓ **CORRECT:** "We fail to reject H0" (subtle but important—H0 is never "accepted," only not rejected)

❌ **MISTAKE:** "Fail to reject means the claim is false"
✓ **CORRECT:** "Fail to reject means we lack sufficient evidence; it doesn't prove H0"

❌ **MISTAKE:** "A small p-value means a big effect size"
✓ **CORRECT:** "A small p-value indicates statistical significance; effect size is separate"

❌ **MISTAKE:** "p < 0.05 means the result is important or practically meaningful"
✓ **CORRECT:** "p < 0.05 means the result is statistically significant; practical significance is different"

---

## Decision vs. Conclusion

**DECISION (Statistical):**
- "Reject H0" or "Fail to Reject H0"
- Based purely on p-value vs. α comparison

**CONCLUSION (Practical/Business):**
- "We have evidence that [management claim]"
- Translates the statistical decision into business language
- Acknowledges that rejecting H0 supports Ha, not that Ha is proven

---

## Relating to Other Skills

**Workflow Through the Statistical Toolkit:**

1. **hypothesis-framer** → Define H0 and Ha from business scenario
2. **confidence-interval-builder** → Understand the parameter and variability
3. **type2-error-analyzer** → Assess test power before collecting data
4. **hypothesis-test-decision-maker** → Use calculated test statistic to make decision (this skill)

---

## Notes for Users

1. **P-value ≠ Type I Error Probability:** α is the Type I error rate we tolerate; p-value is what we observed
2. **Statistical vs. Practical Significance:** A result can be statistically significant but practically small
3. **Sample Size Matters:** Large samples can detect tiny effects; use confidence intervals for context
4. **Direction Matters:** Upper, lower, and two-tailed tests have different p-value calculations
5. **Both Methods Agree:** P-value method and critical value method always reach the same conclusion
6. **Report Both:** Best practice is to report p-value AND confidence interval, not just reject/fail to reject

---

## Related Skills

- **hypothesis-framer:** Frame H0 and Ha from business scenario
- **confidence-interval-builder:** Provide confidence bounds alongside hypothesis test
- **type2-error-analyzer:** Assess power (ability to detect true effects)
- **sample-point-estimator:** Calculate the test statistic from raw data

