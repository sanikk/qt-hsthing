# luonnoksia

```mermaid
block-beta
    columns 1
    block 
        main
        gui
        watchdog_watcher
    end
    
    observer 
```

```mermaid
classDiagram
    class sync {
        main
        gui
        log_service
        watchdog_provider
    }
    class qthread {
        
    }
    class observer {
        watchdog_observer
    }
```