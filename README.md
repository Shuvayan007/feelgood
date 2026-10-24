# Feel Good 🌱
### Your AI-Powered Personal Mentor

**Turn your ambitions into actionable plans. Build better habits. Make meaningful progress.**

Feel Good is an AI-powered personal mentor designed to help people understand themselves, define meaningful life goals, and achieve them through personalized guidance, structured planning, and continuous progress tracking.

Rather than treating habits, wellness, finances, and personal development as isolated activities, Feel Good brings them together under one intelligent mentoring experience. It learns about the user's goals, preferences, circumstances, and constraints to recommend practical actions that fit their life.

The vision is simple: **help people become the person they want to be, one achievable step at a time.**

> *Your life. Your goals. Your pace. One mentor to help you move forward.*

---

## ✨ Vision

Everyone has ambitions, but turning those ambitions into consistent action is difficult. Goals can feel overwhelming, priorities compete for attention, and motivation naturally fluctuates.

Traditional productivity applications help track tasks. Habit trackers measure consistency. Fitness applications monitor workouts. Expense managers categorize spending.

**Feel Good aims to connect these activities to a bigger picture: the user's life goals.**

Through conversational AI, structured personal memory, goal planning, and data-driven insights, Feel Good acts as a personal mentor that helps users:

- Understand their current situation and identify areas for improvement.
- Define short-term, medium-term, and long-term goals.
- Break ambitious goals into milestones, weekly priorities, and daily actions.
- Build sustainable habits and track progress over time.
- Improve wellness, fitness, and nutritional routines.
- Understand spending patterns and develop better financial habits.
- Reflect on setbacks, adapt plans, and stay accountable.
- Balance competing priorities across different areas of life.

Feel Good is not intended to replace the user's judgment. It helps users make informed decisions and take ownership of their progress.

---

## 🎯 Core Philosophy

Feel Good is built around five principles.

| Principle | Description |
|---|---|
| **Mentor-first** | The AI mentor is the central experience. Tracking modules support the mentor rather than operating as disconnected products. |
| **Personalization** | Recommendations reflect the user's goals, preferences, available time, resources, and constraints. |
| **Action over advice** | Broad aspirations are translated into specific, measurable, achievable actions. |
| **Progress over perfection** | Setbacks are opportunities to reassess and improve a plan, not reasons to abandon it. |
| **User ownership** | Users control their goals, approve meaningful plan changes, and manage what the system remembers. |

---

## 🧠 Key Features

### 1. AI Personal Mentor

The central interface is a conversational AI mentor that helps users plan, reflect, and make progress.

Users can communicate naturally instead of navigating complicated forms for every interaction.

**Capabilities:**
- Conversational onboarding and progressive profile creation.
- Personalized guidance based on relevant user context.
- Goal creation, clarification, and revision.
- Daily check-ins and weekly reviews.
- Context-aware suggestions and explanations.
- Identification of stalled goals and conflicting commitments.
- Personalized recommendations grounded in recorded progress.
- Conversation history and controlled long-term memory.

The mentor uses an LLM for reasoning and generating proposals, while application services validate data, enforce business rules, and execute approved actions.

### 2. Personal Profile and Memory

The mentor builds an evolving understanding of the user.

Profile information is collected progressively, only when it is relevant to the conversation or a proposed plan.

**Profile domains:**
- Personal circumstances and preferences.
- Career, skills, and learning ambitions.
- Fitness, activity, and nutritional preferences.
- Financial priorities and spending constraints.
- Lifestyle, routines, and commitments.
- Available time, resources, and practical limitations.

Feel Good uses three complementary forms of memory:

- **Structured memory:** Goals, deadlines, preferences, approved plans, and progress records stored in PostgreSQL.
- **Conversation memory:** Summaries of previous discussions and decisions.
- **Semantic memory:** Optional retrieval of relevant context from journal entries and previous conversations using vector embeddings.

Structured records remain the source of truth for factual questions. Conversation summaries and semantic retrieval provide context, not authoritative numerical answers.

Users should be able to inspect, correct, and delete stored memories and manage memory consent.

### 3. Goal Planning and Execution

Feel Good helps transform abstract ambitions into structured plans.

For example:

> "I want to become highly proficient in AI engineering."

The mentor can help clarify the user's current skills, desired outcome, available study time, and target date. It then proposes a personalized roadmap with milestones and weekly actions.

**Goal hierarchy:**

```text
Life Direction
└── Long-Term Goal
    ├── Milestone 1
    │   ├── Action 1
    │   └── Action 2
    ├── Milestone 2
    │   ├── Action 3
    │   └── Linked Habit
    └── Milestone 3
        └── Action 4
```

**Goal management capabilities:**
- Short-term, medium-term, and long-term goals.
- Life directions and personal priorities.
- Milestones with target dates and success criteria.
- Daily actions and recurring habits.
- Goal progress aggregation and historical tracking.
- Time-budget validation and scheduling conflict detection.
- Stalled-goal detection.
- Plan revision history with explanations.

The LLM proposes plans, application services validate them, and users approve consequential changes before they are saved.

### 4. Habit Tracking

Habits are recurring behaviors that support broader life goals.

Users can create habits, record completions, and monitor consistency. Habits can be linked to specific goals so that daily actions contribute to the user's larger objectives.

**Capabilities:**
- Custom habit creation and scheduling.
- Daily completion logging.
- Current and longest streaks.
- Completion rates and consistency scores.
- Historical progress charts.
- Goal-linked habits.
- Mentor recommendations for improving consistency.

The mentor can use actual habit data to identify patterns and suggest realistic adjustments.

### 5. Wellness and Fitness

The wellness module helps users monitor their physical well-being and develop sustainable routines.

**Planned capabilities:**
- Workout logging and training frequency.
- Workout plans and exercise records.
- Body measurements and progress trends.
- Meal logging and nutritional estimates.
- Sleep and activity consistency.
- Fitness goal tracking.
- Personalized workout and nutrition suggestions.

Recommendations should reflect the user's goals, preferences, experience, available equipment, and constraints.

Wellness guidance is intended for general education and habit support, not medical diagnosis or treatment.

### 6. Personal Finance and Expense Management

Feel Good helps users understand their spending behavior and develop better financial habits.

**Planned capabilities:**
- Income and expense logging.
- Custom expense categories.
- Monthly spending summaries.
- Budget creation and tracking.
- Savings goals and progress.
- Spending trends and category comparisons.
- Budget adherence and savings-rate analytics.
- Personalized suggestions for reducing unnecessary expenses.

For example, the mentor might identify a recurring discretionary expense and suggest a realistic adjustment that supports a user's savings goal.

Financial recommendations should be transparent, grounded in recorded data, and focused on budgeting and financial habits rather than unsupported investment advice.

### 7. Unified Progress Dashboard

The dashboard connects individual activities to the user's broader objectives.

It should help users answer:

- What am I trying to achieve?
- What should I focus on today?
- Am I making progress?
- Which habits are helping me?
- What is getting in my way?
- What should I change next?

The dashboard will bring together active goals, milestones, upcoming actions, habit consistency, wellness trends, financial summaries, and insights from the mentor.

The emphasis is on meaningful progress rather than displaying as many metrics as possible.

### 8. Daily Check-ins and Weekly Reviews

The mentor helps users reflect on their actions and adapt their plans.

A daily check-in can explore:

- What did I accomplish today?
- What prevented me from completing my planned actions?
- How much time and energy do I have tomorrow?
- What is the most useful next step?

Weekly reviews summarize actual progress, highlight patterns, identify obstacles, and propose adjustments.

Plans remain editable and user-controlled.

---

## 🏗️ System Architecture

Feel Good follows a **mentor-first, modular monolith architecture**.

The application uses a single Django backend deployment containing separate domain applications. These applications communicate through Python service functions rather than independent network services.

This approach keeps the initial system straightforward to develop, test, deploy, and maintain while preserving clear boundaries between business domains.

### High-Level Architecture

```text
┌──────────────────────────────────────────┐
│              Client Layer                │
│                                          │
│     React + TypeScript (Web)             │
│     Kotlin + Jetpack Compose (Future)    │
└────────────────────┬─────────────────────┘
                     │
              HTTPS / REST / WS
                     │
┌────────────────────▼─────────────────────┐
│          Django REST Framework           │
│                                          │
│ Authentication · Permissions · APIs      │
│ Validation · Rate Limiting               │
└────────────────────┬─────────────────────┘
                     │
┌────────────────────▼─────────────────────┐
│          Mentor Orchestration            │
│                                          │
│ Intent Classification                    │
│ Context Building                         │
│ LLM + Tool Registry                      │
│ Response Validation                      │
│ Approval Management                      │
│ Action Execution                         │
└───────────┬──────────────────┬───────────┘
            │                  │
┌───────────▼──────────┐ ┌─────▼────────────┐
│   Goal Planning      │ │  Domain Services │
│   Profile            │ │                  │
│   Conversations      │ │  Habits          │
│   Memory             │ │  Finance         │
│                      │ │  Wellness        │
└───────────┬──────────┘ └─────┬────────────┘
            │                  │
            └────────┬─────────┘
                     │
┌────────────────────▼─────────────────────┐
│              PostgreSQL                  │
│                                          │
│ Structured Records · JSONB · pgvector     │
└────────────────────┬─────────────────────┘
                     │
┌────────────────────▼─────────────────────┐
│         LLM Provider Adapter              │
│                                          │
│ Azure OpenAI / Compatible Providers       │
└──────────────────────────────────────────┘
```

The architecture is conceptual. Actual deployment and component availability will depend on the implementation phase.

### Core Backend Services

| Service | Responsibility |
|---|---|
| Mentor Orchestrator | Coordinates user interactions, context retrieval, LLM calls, tool execution, and response validation. |
| Goal Planning Service | Manages goal hierarchies, milestones, actions, progress, and plan revisions. |
| User Profile Service | Maintains structured user context, preferences, and constraints. |
| Conversation Service | Persists messages, manages conversation threads, and summarizes history. |
| Memory Service | Retrieves relevant historical context and manages user-controlled memory. |
| Habit Service | Records habit completions and calculates consistency metrics. |
| Finance Service | Manages financial records, budgets, and spending analytics. |
| Wellness Service | Manages workout, measurement, nutrition, and sleep records. |

Each service owns its business logic and exposes narrowly defined functions to the mentor orchestrator.

---

## 🤖 LLM Integration and Tool Framework

The LLM is a reasoning engine, not a database or an unrestricted action executor.

Feel Good uses controlled tool calling to allow the mentor to retrieve relevant user information and interact with application services.

### Request Processing Flow

```text
User Message
     │
     ▼
Intent Classification
     │
     ▼
Context Builder
     │
     ▼
LLM + Approved Tool Definitions
     │
     ▼
Response and Tool-Call Validation
     │
     ▼
Permission and Approval Checks
     │
     ▼
Application Service Execution
     │
     ▼
Persisted Result and User Response
```

Not every request requires the entire pipeline. A simple factual question can use a focused database query, while a complex goal-planning request may require additional context and validation.

### Tool Permissions

| Permission Level | Behavior | Examples |
|---|---|---|
| Read | Retrieve information belonging to the authenticated user. | `get_user_goals`, `get_expense_summary` |
| Write | Execute validated, low-consequence actions. | `log_habit`, `log_progress` |
| Write with approval | Prepare a proposed change and wait for user confirmation. | `create_goal_proposal`, `propose_weekly_plan` |

Every tool must have typed inputs, ownership checks, and an explicit permission level.

The LLM must never receive unrestricted database access. All writes are handled by application code, with appropriate validation, transaction handling, and audit records.

### Initial Tool Registry

Representative tools include:

- `get_user_profile`
- `get_user_goals`
- `get_goal_detail`
- `get_available_time`
- `get_habit_summary`
- `get_expense_summary`
- `get_budget_status`
- `get_wellness_summary`
- `get_measurement_trend`
- `create_goal_proposal`
- `propose_weekly_plan`
- `log_progress`
- `log_habit`
- `search_memory`

The final tool registry and schemas will be defined during implementation.

### Model Strategy

The initial implementation will use prompt engineering, structured context, tool calling, and schema validation rather than fine-tuning.

LLM integrations will be isolated behind a provider-independent interface. Azure OpenAI is the intended starting point, but the application should remain adaptable to other compatible model providers.

A single mentor orchestrator will coordinate domain-specific tools. Multiple autonomous agents are not required for the initial release.

---

## 🧠 Context Management and Memory

The context builder assembles the information relevant to each user request while keeping token usage manageable.

Context is prioritized approximately as follows:

1. System instructions and behavioral constraints.
2. Active goals and progress summaries.
3. Relevant profile information and available resources.
4. Recent conversation history.
5. Summaries of previous conversations.
6. Relevant retrieved memories.
7. Domain-specific analytics when needed.

The exact allocation will depend on the selected model and request type.

Older conversation history can be summarized, while important facts are extracted into structured fields. Relevant semantic memories can be retrieved when a request benefits from historical context.

**Important:** Numerical claims and factual answers must be grounded in authoritative records. For example, monthly workout counts must be calculated from workout records, not inferred from conversation summaries.

---

## 🗄️ Data Architecture

PostgreSQL is the primary database. The schema is organized around identity, goals, domain tracking, conversations, and memory.

The `pgvector` extension is planned for semantic retrieval where appropriate.

### Core Data Models

| Domain | Models | Purpose |
|---|---|---|
| Identity | `User`, `UserProfile` | Authentication, preferences, and user context. |
| Goals | `LifeDirection`, `Goal`, `Milestone`, `Action` | Goal hierarchy, planning, and execution. |
| Conversations | `Conversation`, `Message` | Message history, conversation purpose, and summaries. |
| Memory | `Memory`, `ConversationSummary` | Structured facts, summaries, and optional semantic memories. |
| Habits | `Habit`, `HabitLog` | Habit definitions, completions, and consistency. |
| Finance | `ExpenseCategory`, `FinancialRecord`, `Budget` | Income, expenses, categories, and budget tracking. |
| Wellness | `WellnessRecord` | Workout, measurement, nutrition, and sleep records. |

These are the planned core models. Additional models and relationships may be introduced as implementation requirements become clearer.

All user-owned records must enforce ownership at the application and API layers.

Financial values should use decimal-safe numeric types and explicit currency information. Dates, timestamps, and recurring schedules should respect the user's timezone.

---

## 🔌 API Design

The backend will expose versioned REST endpoints for web and mobile clients.

Representative endpoint groups:

| Endpoint | Responsibility |
|---|---|
| `/api/v1/auth/` | Authentication and token management. |
| `/api/v1/profile/` | Profile and preference management. |
| `/api/v1/goals/` | Goals, milestones, actions, and progress. |
| `/api/v1/conversations/` | Conversation and message management. |
| `/api/v1/mentor/` | Mentor interactions and planning workflows. |
| `/api/v1/memory/` | Memory inspection and user controls. |
| `/api/v1/habits/` | Habit definitions and completion logs. |
| `/api/v1/finance/` | Financial records, budgets, and analytics. |
| `/api/v1/wellness/` | Wellness records and summaries. |
| `/api/v1/dashboard/` | Aggregated progress and insights. |

WebSocket communication is planned for streaming mentor responses. REST remains the primary interface for persisted application data.

The final API contract, authentication details, and request/response schemas will be documented as the endpoints are implemented.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Web frontend | React | Interactive web application. |
| Language | TypeScript | Type safety for frontend development. |
| Backend | Python | Application and AI orchestration logic. |
| API framework | Django REST Framework | REST APIs, serialization, permissions, and validation. |
| Database | PostgreSQL | Relational data and transactional consistency. |
| Vector search | pgvector | Optional semantic memory retrieval. |
| LLM integration | Azure OpenAI initially | Conversational reasoning and structured proposals. |
| API communication | REST + WebSocket | Data access and streaming responses. |
| Mobile | Kotlin + Jetpack Compose | Planned native Android application. |
| Cloud hosting | Azure App Service | Backend hosting. |
| Managed database | Azure Database for PostgreSQL | Hosted relational database. |
| Secrets | Azure Key Vault | Secure secret management where applicable. |
| Monitoring | Azure Monitor / Application Insights | Operational monitoring and diagnostics. |
| Version control | Git + GitHub | Source control and collaborative development. |

The stack is intentionally designed around managed services and a modular backend to minimize infrastructure overhead during early development.

---

## 🔐 Security, Privacy, and Responsible AI

Feel Good may handle sensitive personal, financial, and wellness information. Privacy and security are fundamental requirements.

The implementation will prioritize:

- Secure authentication and authorization.
- Strict per-user data isolation.
- HTTPS for network communication.
- Validation of all API requests and LLM tool arguments.
- Rate limiting and configurable LLM usage limits.
- Secure secret storage and managed identities where supported.
- Minimal disclosure of personal information to external models.
- Configurable retention of conversation and operational logs.
- User-controlled memory inspection, correction, and deletion.
- Explicit approval for meaningful goal and plan changes.
- Audit trails for consequential actions.
- Database backups and recovery procedures.

The mentor is intended to support personal development, general wellness education, and budgeting habits. It is not a substitute for medical care, mental health treatment, or qualified financial advice.

LLM outputs will be treated as proposals and validated against application rules before execution. Generated recommendations will be evaluated for relevance, feasibility, factual grounding, and consistency with user preferences.

---

## 🚀 Development Roadmap

Development is planned in four phases.

### Phase 1 — Foundation

- Establish the Django backend and React frontend.
- Implement authentication and profile management.
- Build conversational onboarding.
- Persist conversations and structured profile information.
- Integrate the initial LLM provider.
- Implement the basic mentor orchestration pipeline.

**Success criterion:** A user can create an account, build a profile through conversation, and interact with the mentor.

### Phase 2 — Goal Intelligence

- Implement the complete goal hierarchy.
- Generate structured goal and milestone proposals.
- Add weekly planning and daily actions.
- Implement approval workflows and plan history.
- Add context management and conversation summaries.
- Implement daily check-ins and progress logging.

**Success criterion:** A user can turn a broad ambition into an approved, structured plan and track progress over time.

### Phase 3 — Goal and Habit Integration

- Implement habit creation and completion tracking.
- Link habits to goals.
- Build the unified progress dashboard.
- Add goal progress aggregation and stalled-goal detection.
- Implement time-budget checks and scheduling conflict detection.
- Add weekly reviews and adaptive recommendations.

**Success criterion:** Completing linked habits updates relevant progress metrics, and the mentor can use actual activity data to recommend next steps.

### Phase 4 — Domain Expansion and Mobile

- Implement finance and wellness modules.
- Add semantic memory with pgvector.
- Introduce advanced analytics and weekly reports.
- Build an LLM evaluation framework.
- Develop the native Android application.
- Optimize performance and conduct a security review.

**Success criterion:** The mentor can use relevant data across all three domains, while the mobile application shares the same backend and business logic.

The phases describe the intended delivery sequence, not a commitment to a specific release date.

---

## 🧪 Testing and Evaluation

Feel Good requires both conventional software testing and LLM-specific evaluation.

### Application Testing
- Unit tests for business logic and analytics.
- API tests for validation and permissions.
- Integration tests for database transactions and tool execution.
- Tests for user ownership and data isolation.
- Tests for approval workflows and plan revisions.

### Mentor Evaluation
- Goal specificity and completeness.
- Feasibility against available time and resources.
- Consistency with stored profile information.
- Accuracy of numerical claims.
- Correct selection and execution of tools.
- Appropriate handling of missing information.
- Quality of plan adaptations after setbacks.
- Privacy and safety boundary adherence.

### Product Success Metrics
- Goal proposal acceptance and editing rates.
- Completion of planned actions.
- Milestone progression.
- Usefulness of recommendations.
- Quality of adaptation during weekly reviews.
- User trust and satisfaction.
- LLM latency and cost per interaction.

The objective is not simply to make the mentor sound intelligent. It is to make its guidance useful, grounded, and capable of supporting measurable progress.

---

## 📁 Proposed Repository Structure

```text
feel-good/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── mentor/
│   │   │   ├── goals/
│   │   │   ├── habits/
│   │   │   ├── finance/
│   │   │   └── wellness/
│   │   ├── pages/
│   │   ├── api/
│   │   ├── hooks/
│   │   └── types/
│   └── package.json
│
├── backend/
│   ├── config/
│   ├── apps/
│   │   ├── users/
│   │   ├── profiles/
│   │   ├── goals/
│   │   ├── conversations/
│   │   ├── memory/
│   │   ├── mentor/
│   │   ├── habits/
│   │   ├── finance/
│   │   └── wellness/
│   ├── services/
│   │   ├── llm/
│   │   ├── tools/
│   │   └── planning/
│   ├── tests/
│   ├── manage.py
│   └── requirements.txt
│
├── android/                 # Planned
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── development.md
├── .env.example
├── .gitignore
└── README.md
```

This structure is a proposed starting point. It may evolve as the implementation takes shape.

---

## 💻 Local Development

The following tools are expected to be needed for local development:

- Python and a virtual environment.
- Node.js and npm.
- PostgreSQL with the required extensions.
- Git.
- An API key and access to the selected LLM provider.

### Environment Configuration

Create environment files for local development and keep credentials out of source control.

A future `.env.example` may include variables such as:

```dotenv
DJANGO_SECRET_KEY=
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=

LLM_PROVIDER=azure_openai
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_API_VERSION=
```

These are illustrative configuration names. The actual settings will be defined by the implementation.

**Do not commit real API keys, database credentials, or production secrets.** Production secrets should be managed through Azure's supported secret-management and identity mechanisms.

Detailed installation, migration, test, and run instructions will be added once the initial application scaffold is in place.

---

## ⚖️ Key Architecture Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Backend architecture | Modular Django monolith | Clear domain boundaries without unnecessary microservice complexity. |
| Goal management | Dedicated planning service | Keeps structural rules and progress calculations outside the LLM. |
| LLM coordination | Single mentor orchestrator | Simplifies tool access, context selection, and action control. |
| Database | PostgreSQL | Strong relational modeling and transactional consistency. |
| Semantic memory | PostgreSQL + pgvector | Avoids introducing a separate vector database prematurely. |
| AI strategy | Prompts, tools, and retrieval | Establishes a measurable baseline before considering fine-tuning. |
| Model integration | Provider-independent adapter | Reduces dependence on one model provider. |
| Conversation history | Persistence + summarization | Maintains useful context without passing unbounded history to the LLM. |
| User approvals | Explicit proposal workflow | Keeps consequential decisions under user control. |
| Hosting | Azure App Service + managed PostgreSQL | Reduces infrastructure management for an early-stage application. |

---

## 🧭 Long-Term Vision

Feel Good aims to become a trusted personal mentoring companion that helps people make progress across different areas of life.

Over time, the platform may evolve to include:

- More advanced personalized planning.
- Better detection of behavioral patterns and obstacles.
- Cross-domain prioritization and time allocation.
- Deeper integrations with supported health and activity platforms.
- Financial data import and additional analytics.
- Native mobile notifications and offline-friendly tracking.
- Longitudinal personal progress reports.
- More sophisticated recommendation evaluation and personalization.

These are future possibilities, not commitments for the initial release.

The long-term ambition is to help users understand not only what they want to achieve, but also what actions consistently move them closer to it.

---

## 🌱 The Feel Good Promise

You don't need to transform your entire life overnight.

You need to understand where you are, decide where you want to go, and take the next meaningful step.

Feel Good is being built around that idea: **a personal mentor that helps you turn intentions into action, action into progress, and progress into lasting change.**

*Build a better life, one step at a time.*

---

## 📌 Project Status

**Stage:** Architecture and planning

The architecture, technology choices, and phased roadmap describe the intended system. Features should be considered planned until they have been implemented, tested, and documented as available.
