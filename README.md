# A Formalism and Approach for Improving Robustness of Large Language Models Using Risk-Adjusted Confidence Scores

### Data Resources
---
The "OriginalBenchmarks" folder contains the four original benchmarks used in the experimental study, including the corresponding training and dev sets. The "RiskInjectedBenchmarks" folder includes NQ-, WQ-, and NRA-injected dev sets for benchmarks. For each instance in the dev sets of both the original and perturbed benchmarks, we have provided the confidence score obtained from the RoBERTa ensemble model in Output folders.


### Data processing
---
We also include a data processing file that demonstrates how to apply the NQ, WQ, and NRA perturbation functions to a given instance. Note that we never apply the risk injection functions to any of the training instances in the benchmarks. They were solely applied to the instances in the dev sets. It is worth mentioning that these RIFs can also be applied to dev instances in other commonsense reasoning benchmarks.