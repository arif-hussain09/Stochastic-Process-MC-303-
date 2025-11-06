# 🏦 Task 1: Simulation of Customer Arrivals at a Bank

## 🎯 Objective
To simulate a **real-world arrival system** using a **homogeneous Poisson process** and analyze:
- Service load  
- Waiting times  
- Server utilization  

---

## 🧩 Problem Description
Customers arrive at a **bank** according to a **Poisson process** with rate **λ customers per minute**.  
Each customer requires a **random service time**, assumed to be **exponentially distributed** with mean **1/μ minutes**.  
The bank has **a single service counter**.

---

## 📋 Tasks

1. **Simulate** arrivals and departures for a working period (e.g., **4 hours**).  
2. **Track** queue length, waiting times, and server utilization.  
3. **Compare** analytical vs. simulated mean waiting time.

---

## 📊 Expected Outcomes

- **Plot:** Number of customers in system vs. time  
- **Metrics:**
  - Average waiting time  
  - Average queue length  
  - Server utilization  

---

## 🧠 Implementation Hints

- Generate **inter-arrival times** using:  
  `exponential(λ)`
- Generate **service times** using:  
  `exponential(μ)`
- Use either:
  - **Time-driven simulation**, or  
  - **Event-driven simulation**
- Libraries:  
  `numpy`, `matplotlib` (Python)  
  or random number utilities in **C++/Java**