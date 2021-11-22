The goal is to find an input that makes the positive and negative results of the forward function match.
However, if the input is too different from `src`, the condition `np.linalg.norm(diff, 0) > L0_THRES or np.linalg.norm(diff, 2) > L2_THRES` cannot be satisfied.

This can be solved by using the [simulated annealing](https://en.wikipedia.org/wiki/Simulated_annealing) method with an appropriate score function.

[Payload](./misc-collision-payload.txt).

Flag: `n1ctf{why_not_pytorch_55a1904048a51661ffa5eca6678d636435ab70d2}`