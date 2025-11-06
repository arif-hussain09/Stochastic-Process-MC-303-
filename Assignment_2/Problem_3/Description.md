# ⚙️ Task 3: Machine Replacement Policy (Renewal Process)

## 🎯 Objective
Model equipment life cycles and maintenance schedules using a **renewal process** (Weibull lifetimes) and study the long-run replacement rate and cost-optimal preventive replacement interval.

---

## 🧩 Problem Description
A factory operates a machine whose lifetime \(X\) (months) follows a **Weibull** distribution with parameters:
- Shape: \(\alpha = 2\)  
- Scale: \(\beta = 10\)

When a machine fails it is **immediately replaced** by a new identical machine.

### Tasks
1. Simulate the renewal process for **10 years (120 months)**.  
2. Estimate:
   - Number of renewals up to time \(t\): \(N(t)\)  
   - Long-run renewal rate: \(N(t)/t\)  
3. Compare empirical renewal rate with theoretical value \(1/\mathbb{E}[X]\).  
4. **Extension:** Add a preventive replacement policy that replaces a machine at time \(T_p = 8\) months if it hasn’t failed earlier. Compute expected cost per month using:
   - Failure replacement cost = ₹5000  
   - Preventive replacement cost = ₹3000

---

## 📐 Theory (useful formulas)
- If \(X \sim \text{Weibull}(\alpha,\beta)\) with shape \(\alpha\) and scale \(\beta\), the mean is
  \[
  \mathbb{E}[X] = \beta \, \Gamma\!\left(1 + \frac{1}{\alpha}\right).
  \]
- Theoretical long-run renewal rate:
  \[
  r_{\text{theory}} = \frac{1}{\mathbb{E}[X]}.
  \]
- For the thinned preventive policy, treat replacement times as renewals (either failure time \(<T_p\) or preventive at \(T_p\)).

---

## 🧠 Implementation Hints
- `numpy.random.weibull(a)` returns samples from a Weibull with shape `a` and **scale = 1**. Multiply by `β` to get scale `β`.  
  Example: `lifetime = np.random.weibull(alpha) * beta`
- Simulate renewals by repeatedly sampling lifetimes and accumulating time until the time horizon `t_max` is exceeded.
- For preventive replacement at `T_p`, use `min(lifetime, T_p)` as the actual time-in-service and record whether it was a failure or preventive replacement.
- Run many Monte Carlo trials to stabilize estimates.


