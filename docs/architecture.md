# Framework Architecture

## Component Diagram

```mermaid
flowchart TB
    subgraph TestLayer["Test Layer"]
        Tests["Pytest Test Cases<br/>GET · POST · PUT · PATCH · DELETE"]
        Fixtures["conftest.py<br/>Client Fixtures · Auth Token Fixture"]
        Factory["Booking Payload Factory<br/>Unique and Overrideable Test Data"]
    end

    subgraph ClientLayer["API Client Layer"]
        AuthClient["AuthClient<br/>POST /auth"]
        BookingClient["BookingClient<br/>Booking CRUD Operations"]
        BaseClient["BaseClient<br/>Session · Timeout · Logging<br/>Secret Redaction · Response Truncation"]
    end

    subgraph Configuration["Configuration Layer"]
        Settings["settings.py<br/>Base URL · Timeout<br/>Username · Password"]
        Environment["Environment Variables<br/>BOOKER_*"]
    end

    subgraph ValidationLayer["Validation Layer"]
        ResponseValidators["Response Validators<br/>Status · Content Type"]
        SchemaValidator["Schema Validator"]
        Schemas["JSON Schemas<br/>Booking · Create Response · ID List"]
        BusinessAssertions["Business Assertions<br/>Values · Persistence · Lifecycle"]
    end

    API["Restful Booker API"]

    Fixtures -->|"inject clients and token"| Tests
    Factory -->|"creates payloads"| Tests
    Tests -->|"calls methods"| AuthClient
    Tests -->|"calls methods"| BookingClient
    AuthClient -->|"inherits"| BaseClient
    BookingClient -->|"inherits"| BaseClient
    Environment --> Settings
    Settings -->|"configures"| BaseClient
    BaseClient -->|"HTTP request"| API
    API -->|"HTTP response"| BaseClient
    BaseClient -->|"returns response"| Tests
    Tests --> ResponseValidators
    Tests --> SchemaValidator
    Tests --> BusinessAssertions
    SchemaValidator -->|"loads"| Schemas
```

## Request Flow

```text
Fixture → Test → Domain Client → BaseClient → Restful Booker API
                                             ↓
Test ← Response ← Safe Logging and Redaction ← Response
  ↓
Status Validation + Schema Validation + Business Validation
```

1. Pytest fixtures create reusable client objects and an authentication token.
2. A payload factory produces unique, overrideable booking data.
3. The test calls an operation on `AuthClient` or `BookingClient`.
4. The domain client delegates HTTP behavior to `BaseClient`.
5. `BaseClient` applies the base URL and timeout, reuses a session, and logs the
   request and response.
6. Passwords, tokens, and cookies are redacted, while large bodies are
   truncated before logging.
7. The response returns to the test for generic, structural, and business
   validation.

## Layer Responsibilities

| Layer | Responsibility |
| --- | --- |
| Tests | Describe scenarios and verify business behavior. |
| Fixtures | Inject clients and create shared authentication state. |
| Factories | Produce independent and customizable test data. |
| Domain clients | Represent authentication and booking API operations. |
| Base client | Centralize HTTP sessions, configuration, timeouts, and safe logging. |
| Response validators | Check generic properties such as status and content type. |
| Schema validator | Verify the structural contract of JSON responses. |
| Settings | Read environment-specific values without changing test code. |

## Validation Strategy

The framework deliberately separates three kinds of validation:

- **Generic validation:** checks status codes and response content types.
- **Schema validation:** checks required fields, data types, and nested JSON
  structure.
- **Business validation:** checks returned values, persistence, filtering, and
  resource lifecycle behavior.

Schema validation does not replace business assertions. A response can have the
correct structure while containing incorrect values.

## Interview Explanation

> The tests contain the scenario and business assertions. Pytest fixtures inject
> reusable clients and authentication. Payload factories generate independent
> test data. Domain clients describe API operations, while a shared base client
> handles HTTP sessions, environment configuration, timeouts, logging, and
> secret redaction. Responses are checked through reusable validators, JSON
> schemas, and test-specific business assertions.
