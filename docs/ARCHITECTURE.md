# How a decision reaches contract state

```mermaid
flowchart TD
    A["Public write request"] --> B["Check signer and inputs"]
    B --> C{"Judgment needed?"}
    C -- Yes --> D["Leader evaluates evidence"]
    D --> E["Validators check result"]
    E -- Agreement --> F["Apply deterministic rules"]
    E -- Disagreement --> G["No state update"]
    C -- No --> F
    F --> H["Store record or transition"]
```

OpenFieldMap illustrates the boundary. The model judges whether an open-data column matches a canonical definition. A validated `MATCH` allows the proposal's signer to activate it. From then on, `normalize()` applies a predefined integer multiplier to the values a caller supplies. Comparing documentation, authorizing an active mapping, and converting a measurement are three distinct operations.

DonationAllocation uses the same boundary for an eligibility decision. Activation instead reserves units, and completion moves those units to either distributed or available. The capacity invariant is checked through the remaining, reserved, and distributed counts.
