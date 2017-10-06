# History and change log of kotusparser

 * 2013-02-15  1.0    First releasable version.
 * 2014-02-10  1.0.1  Simplified: doesn’t assert that a file is given because open() will raise an exception if not.
 * 2014-02-25  1.0.2  Still simplified: expects an I/O stream argument (like an open file), not a file name. Also expat’s exception will do.
 * 2014-03-24  1.0.3  Oops, can’t catch ExpatError in caller unless the expat module is imported there too. Let’s import ExpatError here and rename it to ParseError.
 * 2014-03-24  1.0.4  When called from Python 2, next() needs to be defined in addition to __next__() in the KotusParser class.
