What's left in the dissertation

1. Writing
   1. vTask
      1. Section exploring the problem via measurements from the baseline experiments.
         1. Explain the setup of the experiment, the results obtained and what they are indicative of
      2. Section exploring realizable opportunity.
      3. Design of a lazy-copying framework
         1. The importance of semantic information to building such a framework.
            Describe how LAPIS provides this, and any changes that maybe necessary.
         2. Design of the buffer manager and lazy copying
      4. Evaluation
         1. Need to figure out what experiments to run
         2. Explore performance wins and trade-offs.
   2. Conclusion
      1. The pros and cons of the HIRA technique
      2. Forward looking thoughts on other directions to do DSA virtualization (maybe hybrid HW+SW approaches?)....
2. Experiments
   1. Baseline opportunity experiment:
      1. Decompress image using QATzip + run image through Tensorflow image classification (native)
         1. Might need to tune # of images for the time spent moving data become meaningful.
      2. Same experiment run with AvA
   2. Realizable opportunity experiment:
      1. Add a `do-not-copy` annotation to LAPIS.
      2. Change CAvA to elide data movement for the `do-not-copy` annotation. Instead, the generated code performs a look-up using the handle-ID and passes that pointer to the API-server.
      3. Add `do-not-copy` annotation to the relevant commands in the benchmark, and measure realizable opportunity.
   3. Building the buffer manager
      1. Any additional annotations needed in LAPIS + changes to CAvA
      2. Page table modifications + handler in KVM to detect when a demand copy has to occur.
      3. Buffer manager in host (probably in the manager user-space application with upcalls from the kernel) that tracks current state/location of buffers
   4. Evaluation experiments:
      1. Need to gather a couple of benchmarks to that use multiple frameworks and exhibit the slowdown...
      2. Tune and measure.