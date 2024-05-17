## sum qthredd nuts, no bolts

```mermaid

```
Noita ei saa käynnistää qthreadista koska siinä tulee iso ero
joissain toiminnallisuuksissa. Varmaan event-luuppi tms? Toi pistää jonkun 
virtuaalithredin pystyyn ja ajaa siellä event luuppia (arvaus). Luuppi on jo 
käynnissä siellä niin ei voi käynnistää uutta, vanha jää pyörimään sinne.

https://doc.qt.io/qt-6/threads-technologies.html

https://doc.qt.io/qt-6/threads.html





qtconcurrent
 In run with promise mode, the function passed to QtConcurrent::run() can make use of the 
additional QPromise API, which enables _multiple result reporting_, _*progress reporting*_, 
suspending the computation when requested by the caller, or stopping the computation on 
the caller's demand.

hijack progress reports to send log lines? LOL NOPE



