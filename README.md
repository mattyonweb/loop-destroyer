# loop-destroyer

A loop destroyer, in a similar vein of William Basinsky.

## Requirements

+ `sox`, which you can download from here [sox.sourceforge](http://sox.sourceforge.net/)
+ (optionally) `ffmpeg`, to generate a spectrogram video; you can download it from [github](https://github.com/FFmpeg/FFmpeg)

## Installation

	pip install --user loop-destroyer

## How does it sound?

Listen on [youtube](https://youtu.be/iYZJCHTh-3s)!

## Usage example

Suppose you have the following directory hierarchy:

	.
	├── samples-piano
	    ├── piano-01.wav
	    ├── piano-02.wav
	    ├── piano-03.wav
	    └── piano-04.wav


The simplest way to destroy these samples is:

	loop-destroyer -o out_dir --quiet samples-piano/
	
This command will take each sample, repeat it a number of times (progressively destroying it), and then mix this "degradation chain" with the degradation chains from the other samples.

The resulting directory structure will be:

	.
	├── out_dir
	│   ├── disintegrated.mp3
	│   ├── piano-01.wav
	│   ├── piano-02.wav
	│   ├── piano-03.wav
	│   └── piano-04.wav
	└── samples-piano
		├── piano-01.wav
		├── piano-02.wav
		├── piano-03.wav
		└── piano-04.wav
		
`out_dir` contains the disintegrated mix (`disintegrated.mp3`) and the various degradation chains (named after the sample they destroyed, eg. `piano-01.wav`).



	
