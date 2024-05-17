# some sketches

```mermaid

```
Noita ei saa käynnistää qthreadista koska siinä tulee iso ero
joissain toiminnallisuuksissa

https://python-watchdog.readthedocs.io/en/stable/api.html

Collections
class watchdog.observers.api.EventQueue(maxsize=0)[source]
Bases: watchdog.utils.bricks.SkipRepeatsQueue

Thread-safe event queue based on a special queue that skips adding the same event 
(FileSystemEvent) multiple times consecutively. Thus avoiding dispatching multiple event 
handling calls when multiple identical events are produced quicker than an observer can 
consume them.

eli jos otan tän eventqueuen ulos tuolta ja käytän sitä luuppina niin ei kait ole ongelmaa?
