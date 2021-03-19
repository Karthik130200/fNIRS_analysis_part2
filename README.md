# fNIRS_analysis_part2

Currently, we are comparing:
- True synchrony in the TOG condition; the true synchrony is obtained by computing the synchrony between the signals of M and F while listening to the SAME audio stimulus
- Control synchrony in the TOG condition; the control synchrony is obtained by computing the synchrony between the signals of M and F while listening to DIFFERENT audio stimulus (specifically M/F listening to an audio stimulus, and F/M listening to static noise).

Our current task will be to adapt the code to compare:
- True synchrony in the TOG condition; the true synchrony is obtained by computing the synchrony between the signals of M and F while listening to the SAME audio stimulus
- Control synchrony in the SEP condition; the control synchrony is obtained by computing the synchrony between the signals of M and F while listening to SAME audio stimulus

Note that the True synchrony is the same as before.
Only the Control synchrony changes: since in our new control M and F are in the SEP condition, in this second analysis we will focus on the synchrony that is due only to the fact that M and F were together (co-presence effect).

At the moment, we will be focusing on the cc metric.
