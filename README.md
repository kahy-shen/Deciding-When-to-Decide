# Understanding Prior Bias and Choice Paralysis in Transformer-based Language Representation Models through Four Experimental Probes

### Data Resources
---
The "OriginalBenchmarks" folder contains the two original benchmarks (HellaSwag and Social IQA) used in the experimental study, including the corresponding training and dev sets. The "PerturbedBenchmarks" folder includes NQ-, WQ-, and NRA-perturbed dev sets for benchmarks. For each instance in the dev sets of both the original and perturbed benchmarks, we have provided the confidence score obtained from the RoBERTa ensemble model in "Output" folders.


### Data processing
---
We also include a data processing file that demonstrates how to apply the NQ, WQ, and NRA perturbation functions to a given instance. Note that we never apply the perturbation functions to any of the training instances in two benchmarks. They were solely applied to the instances in the dev sets. It is worth mentioning that these perturbation functions can also be applied to dev instances in other commonsense reasoning benchmarks.