# 8.08-project

This is my final project for 8.08 taken in IAP 2024. In recitation on 2024-01-26, we looked at the kinematic wave model, equivalent/similar to the Lighthill-Whitham-Richards (LWR) traffic model, simulated via TASEP. Today, we'll be exploring the Nagel-Schreckenberg (NS) model of traffic.

The model consists of list of particles (cars) occupying discrete positions (on the road) with periodic boundary conditions, each associated with a velocity that changes based on rules that are applied in parallel. The model has an associated maximum velocity $v_m$ for a particle. In order, the following four rules are applied for particle $j$ with velocity $v_j$ to simulate movement:
- Acceleration: add 1 to $v_j$ if this does not exceed $v_m$.
- Braking: set $v_j$ to at most the distance between this particle and the next particle.
- Randomization: with probability $p$, subtract 1 from $v_j$ if this does not make velocity negative.
- Driving: add $v_j$ to the position of car $j$.
Notice that $v_j$ is an integer.

From what I understand, for $v_m > 1$, the dynamics of the system are not fully solved and has only been approximated. To match my results against theory, we look at $f(c)$, the average current across the system at steady-state as a function of $c$, the density of particles in the system.

In the simple case of the simple case of $v_m = 1$, the system is essentially TASEP with parallel update, which can be solved to give
$$
    f(c) = \frac{1}{2} \left(1 - \sqrt{1 - 4(1-p)c(1-c)}\right)
$$
as in [here](https://arxiv.org/pdf/cond-mat/9902170.pdf), so we can directly check against this curve. This is seen in files NS-v_m=1-p=0.3.png and NS-v_m=1-p=0.5.png.

For higher $v_m$, we seek to only recreate the observation/theory that flow will instead be maximized at smaller $c$. This is seen in NS-v_ms.png.

Links to some general sources and other ideas I considered:
- [General LWR Model](https://sboyles.github.io/teaching/ce392d/5-lwrmodel.pdf)
- [General LWR Model 2](https://mtreiber.de/Vkmod_Skript/Lecture06_Macro_LWR.pdf)
- [On/Off Ramps with TASEP](https://link.springer.com/article/10.1007/s10955-019-02380-7)
- [Merger TASEP with three phases](http://archive.sciendo.com/JRP/jrp.2011.35.issue-1/v10242-012-0007-x/v10242-012-0007-x.pdf)