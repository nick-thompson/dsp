# wavetable

> A small experiment with linear interpolation in wavetable synthesis.

This project serves largely as a proof of concept implementation of what I believe to be an "alternative"
approach to linear interpolation in wavetable synthesis. I say "alternative" because it may well have been done
before, and it may well be a silly idea!

The idea here builds upon a previous exploration of sound design and audio synthesis which I wrote about
[on my blog](http://nickwritesablog.com/sound-design-in-web-audio-neurofunk-bass-part-1/) (see part two), and for
which the code is also available here on my GitHub profile, in a project named
[neuro](https://github.com/nick-thompson/neuro). In particular, it examines the phase artifacts introduced by using
resampling to produce a detuned pair of sawtooth waveforms, and how those artifacts might be rendered in real time.
Ultimately, I intend to use the results of this experiment in building a VST software synthesizer capable of
generating this "gritty" detuned output.

I also hope for this project to serve as a well-written, well-documented reference implementation for wavetable
synthesis in Python, because the subject has a lot of interesting details and nuances that are not necessarily
easy for someone new to audio programming to come across. So with that in mind, if you feel any part of the code
is poorly written, missing important details, or could be better explained in the comments, please open an issue!

## License

Copyright (c) 2015 Nick Thompson

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
