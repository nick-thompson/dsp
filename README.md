# dsp

> A collection of digital signal processing concepts explored in Python.

Without the full backstory, this repository is probably very convoluted. The work here follows from an exploration
of sound design in Web Audio, which I wrote about
[on my blog](http://nickwritesablog.com/sound-design-in-web-audio-neurofunk-bass-part-1/). If you're interested,
I suggest you start there and read through the short series.

In particular, the concepts covered here revolve around an examination of the phasing, flanging characteristics of
the old school Drum n' Bass reese bass, and the application of those characteristics in modern sound design. 
That bit is explained in the blog series mentioned above. I continued down this path in search of a way to render
these characteristics in real time, learning and exploring as much of the digital signal processing world as I
could to answer such a question. That led me first into wavetable synthesis, and more recently into the more simple
digital filters.

Many of the modules written here are well documented, and can be invoked directly (e.g. `python -m filters.allpass`)
to visualize characteristics of the module and help explain its purpose.

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
