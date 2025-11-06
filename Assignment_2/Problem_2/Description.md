# ☎️ Task 2: Modelling Call Traffic from Multiple Sources

## 🎯 Objective
To model the **aggregation of independent Poisson processes** and simulate **selective filtering (thinning)** of events.

---

## 🧩 Problem Description
We have **three call centers** — **A**, **B**, and **C** — each receiving calls as **independent Poisson processes** with the following rates:

| Call Center | Arrival Rate (λ, calls/min) |
|--------------|-----------------------------|
| A            | 2.0                         |
| B            | 1.5                         |
| C            | 0.5                         |

### Steps:
1. **Superpose** these independent processes to form a **combined arrival stream**.  
2. **Thin** the combined stream — only **priority calls** (with probability `p = 0.3`) are passed to the central operator.  
3. **Simulate** for **2 hours (120 minutes)** and estimate:
   - Mean inter-arrival time of priority calls  
   - Distribution of time between successive priority calls  
   - Verify that thinning yields a Poisson process with rate:  
     \[
     \lambda_p = p \times (\lambda_1 + \lambda_2 + \lambda_3)
     \]

---

## 📊 Expected Outcomes

- **Histogram** of inter-arrival times (should resemble an exponential distribution)  
- **Comparison** between simulated and theoretical rates  
- **Insight** into load balancing among call centers  

---

## 🧠 Implementation Hints

- Generate **inter-arrival times** for each center using:  
  `np.random.exponential(1/λi)`
- Merge and **sort** all event times (superposition)
- Use a **uniform random filter** for thinning:  
  Keep an event if `np.random.rand() < p