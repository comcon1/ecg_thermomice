# ecg_thermomice

**Collection of jupyter notebooks for processing mice ECG data** describes the pipeline, which we used to process data of heart potential together with stimulation pulses (trigger pulses of IR laser).

Our paper in press:
> *Thermogenetics for cardiac pacing* Alexander V. Balatskiy, Alexey M. Nesterenko, Aleksandr A. Lanin, Vera S. Ovechkina, Semyon S. Sabinin, Elena S. Fetisova, Alexander A. Moshchenko, David Jappy, Rostislav A. Sokolov, Diana Z. Biglova, Georgy M. Solius, Ekaterina M. Solyus, Sergei V. Korolev, Oleg V. Podgorny, Ilya V. Kelmanson, Andrei V. Rozov, Andrei B. Fedotov, Tobias Bruegmann, Alexei M. Zheltikov, Andrey A. Mozhaev, Vsevolod V. Belousov
bioRxiv 2024.01.02.573885; doi: https://doi.org/10.1101/2024.01.02.573885 

For input we have CSV files containing one ECG potential (mostly its LR) and one trigger pulse recorded by 10MHz ADC device. For output we have picture like the following one (Fig.2 from our paper-in-press):

> ![Fig2biorxiv](https://www.biorxiv.org/content/biorxiv/early/2024/02/08/2024.01.02.573885/F3.medium.gif)
> 
> **Typical example of atrium pacing with a frequency slightly higher than the intrinsic one.**
> Pacing was at 2.5 Hz with 80 ms pulses, initial HR was ∼2 Hz. **A.** Position of the P-peak and laser pulse in relation to the R-peak in ms. Negative values mean that events occur before the reference peak. **B.** Change of complex shape (black curve) and heart rate (blue curve) during the experiment. Vertical red lines demonstrate the pulse widths of the trigger pulses. **C.** ECG signal and trigger pulses in short intervals corresponding to the beginning and ending parts of the pacing. The positions of the intervals are indicated with gray bars in panes *A* and *B*.

The most complicated thing in this image is the *A* pane; to build it, we have to go through the following steps:

- the segmentation of ECG (defining R-peaks);
- the determination of P-peak inside every R-R interval;
- the calculation of the relative position of P-peak and trigger pulse inside corresponding R-R interval.
Once you do that, you can set the relative position of P-peak and the start/end position of the trigger pulse to Y-coordinate and the number of R-R interval to the X-coordinate, then you will get a plot like shown at **Fig. 1A**.

The mostly commented code part demonstrating how to do that is located in the file ecg-commented-sample.ipynb; this file you are invited to use as a tutorial. It shows all phases of the protocol including baseline correction, ECG segmentation, P-peak annotation, phase-plot drawing. The phase analysis is done in-place by our scripts. Segmentation and peak annotation are done using [NeuroKit2](https://github.com/neuropsychology/NeuroKit). Also we demonstrate here the application of PCA-based noise filtration.

`ecg-other-samples.ipynb` demonstrates the application of the protocol to another 3 samples (without intensive comments).

`ecg-resonance-visualisation.ipynb` demonstrates how we can work with a complicated phase behaviour; in the notebook we analyze the 4:3 phase lock where every 4 laser pulses create a repeating pattern of 3 R-R intervals.

_We hope these scripts will help you in your ECG analysis!_
