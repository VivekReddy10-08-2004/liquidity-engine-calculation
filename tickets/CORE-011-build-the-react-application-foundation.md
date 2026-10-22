# CORE-011 — Build the React application foundation

**Status:** Ready  
**Release:** Core MVP  
**Depends on:** None

## Outcome

Provide a runnable frontend connected to the existing FastAPI backend.

## Work to do

- Initialize React, TypeScript, and Vite under frontend/ with one documented Node version and committed package-manager lockfile.
- Configure Tailwind/component primitives, routing, TanStack Query, and typed API access; use a development API proxy or explicit local CORS configuration.
- Create navigation for overview, timeline, policies, scenarios, and audit; add shared money/date formatting and error/loading components.

## Acceptance criteria

- [ ] A clean frontend install, type check, and production build succeed.
- [ ] The app reaches /health through its configured backend connection and displays a useful unavailable state.
- [ ] Navigation and forms are keyboard accessible; UI consistently identifies synthetic data and non-execution behavior.
- [ ] Document root-versus-frontend commands and environment variables.

## Out of scope

No product calculations in the browser; no AI panel yet.

## Source requirements

MVP: Technical Approach, Suggested Repository Layout. See the [source map and shared completion rules](README.md).
