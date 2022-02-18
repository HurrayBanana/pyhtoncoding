### Wav file viewer

A simple application to load and view wav files, so you can see the effects of altering the sampling frequency.

It only looks for wav files in the same folder as the python file.

The original wav file is rendered at the bottom of the screen in red
An adjustable version is rendered at the top of the screen in yellow

Program will automatically get you to pick a file, there are a few wav files to get you going

#### File Select mode

**up cursor** - move up list  
**down cursor** - move down list  
**return/enter** - select highlighted file, if no wav files exist exits the program

#### Wav display mode

**f** - choose a different file  
**b** - toggle between amplitude blocks or amplitude line for adjusted waveform  
**o** - toggle adjusted wave overaly on original waveform (only shows once samples reduced)  
**s** - toggle sample points from adjusted wav displayed on top of original waveform  

**q** - increase sample skipping (lower sample frequency)  
**a** - decrease sample skipping (increase sample frequency)  
**left/right cursor** - move view of waveform shown on screen  
**up/down cursors** - alter scale of waveform views (increasing/decreasing number of samples shown on screen)  

