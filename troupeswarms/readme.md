# TroupeSwarms: A TinyTroupe / Swarms Integration

Check back later for updates to this repository!  

Current challenges: Pipelining dictionaries from OpenAI to TinyTroupe, extracting relevant message data from agents (massively verbose at the moment), and prompt stabilizing unique agent sessions in swarms.  

The current outlined workflow of this subproject:

```mermaid
flowchart TD
    A[Target Image] --> B[Primary LLM]
    B --> C[Swarms Agents]
    C --> D[Tinytroupe Task Forces]
    D --> E[Generate Models]
    E --> A
```

Note that a more linear approach may be taken:  

```mermaid
flowchart TD
    A[Target Image] --> B[Primary LLM]
    B --> C[Swarms Agents]
    C --> D[Tinytroupe Task Forces]
    D --> E[Generate Models]
```

![TroupeSwarms](../media/troupeswarms.webp)
