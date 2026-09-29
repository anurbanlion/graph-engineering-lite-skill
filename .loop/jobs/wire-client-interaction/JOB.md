# Wire Client Interaction

## Input

- The UI source contract, typed Demo props, direct named browser use case when present, target rule, and hook conventions.

## Process

1. Keep user-triggered interaction in a Client Component hook or shell.
2. Import a named browser use case directly by file path, never through a use-case barrel.
3. Keep route-provided initial sources separate from interaction-derived sources and pass their object to Marketplace UI unchanged.
4. Implement only client state, debounce, stale-response protection, callbacks, and navigation required by the rule.

## Output

- Interactive client wiring and separate source groups passed to Marketplace UI.
