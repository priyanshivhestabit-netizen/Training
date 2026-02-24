# Backend Architecture Overview

## Bootstrapping Order

1. Load environment variables
2. Connect database
3. Initialize express app
4. Load middlewares
5. Mount routes
6. Start server

## Separation of Concerns

- config → environment loading
- loaders → bootstrapping modules
- utils → shared utilities (logger)
- models → database schemas
- repositories → DB abstraction layer
- services → business logic
- controllers → HTTP layer
- routes → endpoint definitions