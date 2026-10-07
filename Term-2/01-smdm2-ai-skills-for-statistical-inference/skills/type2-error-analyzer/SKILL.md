# Skill: type2-error-analyzer

## Metadata
- **Name:** type2-error-analyzer
- **Version:** 1.0
- **Description:** Calculates Type II error probability (beta) and statistical power for hypothesis tests given baseline mean, hypothesized mean, standard deviation, sample size, and significance level.
- **Category:** Statistics, Hypothesis Testing
- **Trigger Keywords:** Type II error, beta, power analysis, power of test, statistical power

---

## When to Use This Skill

Trigger this skill when:
- User provides mu0 (baseline mean), mu1 (hypothesized mean), sigma (standard deviation), n (sample size), and alpha (significance level)
- User asks: "What's the power of this test?" or "Calculate beta for this scenario"
- User requests: "What's the probability of Type II error?"
- User wants to assess: "How likely are we to detect the effect if it exists?"

Example triggers:
- "Calculate the Type II error probability given mu0=100, mu1=110, sigma=15, n=50, alpha=0.05"
- "What's the power of this test for an upper-tailed hypothesis?"
- "Find beta for these parameters: baseline 50, alternative 55, std dev 8, sample 60, alpha 0.01"

---

## Core Logic & Formulas

### **Step 1: Determine Critical Mean Under H0**
For an upper-tailed test:
```
x_crit = mu0 + z_alpha * (sigma / sqrt(n))
```

Where:
- `mu0` = baseline/null hypothesis mean
- `z_alpha` = critical z-value at significance level alpha (e.g., z_0.05 = 1.645)
- `sigma` = population standard deviation
- `n` = sample size

### **Step 2: Standardize Critical Mean Under Alternative Hypothesis**
Calculate z-value for the critical mean if the true mean is mu1:
```
z = (x_crit - mu1) / (sigma / sqrt(n))
```

Where:
- `x_crit` = critical mean from Step 1
- `mu1` = hypothesized/alternative mean

### **Step 3: Calculate Type II Error (Beta)**
```
beta = P(Z < z)
```
Look up the cumulative probability in standard normal table or use CDF function.

### **Step 4: Calculate Power of Test**
```
Power = 1 - beta
```

---

## Example Calculation

**Given:**
- mu0 = 100 (baseline mean)
- mu1 = 110 (alternative mean)
- sigma = 15 (standard deviation)
- n = 50 (sample size)
- alpha = 0.05 (significance level, upper-tailed test)

**Step 1: Critical Mean**
```
z_0.05 = 1.645
x_crit = 100 + 1.645 * (15 / sqrt(50))
x_crit = 100 + 1.645 * 2.121
x_crit = 100 + 3.489 = 103.489
```

**Step 2: Standardize Under Alternative**
```
z = (103.489 - 110) / (15 / sqrt(50))
z = -6.511 / 2.121
z = -3.071
```

**Step 3: Calculate Beta**
```
beta = P(Z < -3.071) ≈ 0.0011
```

**Step 4: Calculate Power**
```
Power = 1 - 0.0011 = 0.9989 (or 99.89%)
```

**Interpretation:** The test has a 99.89% probability of detecting the effect if the true mean is 110.

---

## Parameter Guide

| Parameter | Symbol | Definition | Example |
|-----------|--------|-----------|---------|
| Baseline/Null Mean | mu0 | Mean under null hypothesis | 100 |
| Alternative Mean | mu1 | Mean we want to detect | 110 |
| Std Deviation | sigma | Population standard deviation | 15 |
| Sample Size | n | Number of observations | 50 |
| Significance Level | alpha | Probability of Type I error | 0.05 |
| Critical Value | z_alpha | Z-score for alpha level | 1.645 (upper), 1.960 (two-sided) |

---

## Interpretation Guide

**Power Levels:**
- **Power < 0.80:** Weak ability to detect effect (underpowered)
- **Power 0.80–0.90:** Acceptable power
- **Power > 0.90:** Strong power (highly likely to detect effect)
- **Power > 0.95:** Very strong power

**Beta Levels:**
- **Beta > 0.20:** High Type II error risk (reject only if effect is obvious)
- **Beta 0.10–0.20:** Moderate risk
- **Beta < 0.10:** Low risk (good chance of detection)

**Effect Size Impact:**
- Larger effect (mu1 - mu0) → Lower beta → Higher power
- Larger sample size (n) → Lower beta → Higher power
- Larger sigma → Higher beta → Lower power

---

## Common Test Types

**Upper-Tailed Test (H1: μ > μ0):**
- Use z_alpha (one-sided)
- Example: z_0.05 = 1.645

**Lower-Tailed Test (H1: μ < μ0):**
- Use -z_alpha (one-sided)
- Example: -z_0.05 = -1.645

**Two-Tailed Test (H1: μ ≠ μ0):**
- Use z_alpha/2 for each tail
- Example: z_0.025 = 1.960 (for alpha = 0.05)

---

## Output Format

When applying this skill, provide:
1. **Given Parameters:** mu0, mu1, sigma, n, alpha
2. **Critical Mean:** x_crit (calculated)
3. **Z-Value Under Alternative:** z (calculated)
4. **Type II Error (Beta):** Probability as decimal and percentage
5. **Power of Test:** Probability as decimal and percentage
6. **Interpretation:** What this means for the hypothesis test

**Example Output:**
```
Given: mu0=100, mu1=110, sigma=15, n=50, alpha=0.05 (upper-tailed)

Critical Mean: 103.49
Z-Value Under H1: -3.07
Beta (Type II Error): 0.0011 (0.11%)
Power of Test: 0.9989 (99.89%)

Interpretation: This test has 99.89% probability of detecting 
a true effect size of 10 units. Very strong power.
```

---

## Related Concepts

- **Type I Error (Alpha):** Rejecting H0 when it's true (false positive)
- **Type II Error (Beta):** Failing to reject H0 when it's false (false negative)
- **Power:** Probability of correctly detecting an effect (1 - Beta)
- **Effect Size:** Difference between mu0 and mu1; larger differences = higher power
- **Sample Size Planning:** Choosing n to achieve desired power level

---

## Notes for Users

1. **Always specify test direction:** upper-tailed, lower-tailed, or two-tailed
2. **Standard deviation assumption:** Formula assumes known population sigma; use sample s with t-distribution for small samples
3. **Normal distribution:** This skill assumes underlying normality; Central Limit Theorem applies for large n
4. **Power trade-offs:** Increasing power requires either larger sample size, smaller sigma, larger effect size, or higher alpha (not recommended)

