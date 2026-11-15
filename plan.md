# Mentor chat onboarding and shared personalization profile

## Goal and scope

Build a resumable, adult-only conversational questionnaire in Mentor Chat, create a trustworthy shared profile for future personalized workout and nutrition applications, and give the mentor useful, bounded conversation memory. The questionnaire must be completed and reviewed before existing or new users can access other application areas. This work prepares data for future applications; it does not build workout or meal recommendations.

Every newly created conversation starts with this exact persisted assistant message, before any other chat content:

> You are speaking with Feel Good, your AI personal mentor. I'm here to help you define meaningful goals and guide you toward achieving them through personalized, actionable steps. How can I assist you today?

## Current state

- Registration creates a user and profile; the web registration redirects to an informational onboarding page, but API registration, login and other application routes do not enforce onboarding. The landing page currently offers a skip link.
- `UserProfile` contains a few basic fields, a completion boolean and generic JSON fields. Its API serializer currently allows the completion flag to be written directly. The basic profile page does not manage a comprehensive profile.
- Chat is normally created only on the first submitted user message. Check-ins create a separate conversation with their own opening. Existing conversation history and deletion are user-scoped.
- The orchestrator receives a conversation ID but does not use it to populate history; it collects profile and active goals but does not actually include them in the LLM messages. Intent classification, response validation and tool execution are stubs.
- Conversation messages currently use creation time as model ordering; the rendered history adds the message ID as a tie-breaker. `MemoryEntry` has an optional source conversation with `SET_NULL`; conversation summaries cascade on conversation deletion. Consequently, deleting a chat does not currently delete its extracted memories.

## Decisions and boundaries

- Require the questionnaire for all users, including existing accounts. Save progress between visits; incomplete users cannot use other app features, but can sign in/out, access the onboarding chat and review or correct their own onboarding data. Enforce this on both web and APIs without redirect loops.
- While onboarding is incomplete, a new-chat attempt returns the user to their existing onboarding conversation rather than opening a parallel one. After completion, normal new conversations are available.
- Questionnaire sections are required to be visited and resolved. Basic eligibility and the minimum non-sensitive information required for a useful profile require valid answers; sensitive and other explicitly optional questions can be skipped or declined without blocking completion. Unknown is not equivalent to no.
- Sensitive health questions remain optional and editable/deletable. The user has deferred implementing a consent flow and intends to process supplied information now. Do not claim consent has been captured or treat an answer as consent. Explain processing and provider involvement transparently; treat legal/privacy review of the proposed processing and provider setup as a release prerequisite, not as an implemented consent system.
- Deleting a conversation deletes its messages, summaries and memories derived from it, but retains confirmed canonical profile data. Explain this before deletion. Users can separately edit or delete their profile details; there is no separate memory-management UI in this scope.
- For an incomplete onboarding conversation that is deleted, clear unconfirmed drafts sourced exclusively from it and detach the conversation from progress; retain independently confirmed profile values. The next onboarding entry creates a new onboarding chat with the standard greeting and resumes at unresolved questions. Deletion must never silently mark onboarding complete.

## Ordered implementation plan

### 1. Define the questionnaire and shared data contract

1. Define a versioned question catalog with stable field IDs, section order, required/optional and sensitive classifications, data types, units, validation rules, question text and completion rules. Ask manageable questions conversationally, one topic at a time, showing section progress and how to resume, review, correct, skip or decline eligible questions.
2. Cover the following categories, collecting only details useful for future personalization:
   - **Eligibility and communication:** explicit adult self-confirmation (18+), preferred name, timezone, language and communication preferences. Underage or unknown eligibility does not proceed to adult onboarding or unlock other apps; show a clear, respectful explanation.
   - **Goals and motivation:** prioritized fitness and nutrition goals, desired outcomes, motivation, target horizons and preferences; avoid promising specific outcomes. Reuse existing goal records where appropriate rather than creating duplicate canonical goals.
   - **Schedule and environment:** availability by day and duration, work/sleep schedule, access to equipment or facilities, environment and practical constraints.
   - **Activity baseline:** current activity level, training history, preferred and disliked activities, experience, mobility limitations if volunteered, and rest/recovery patterns.
   - **Food context:** dietary pattern, likes and dislikes, allergies/intolerances when volunteered, cultural or practical preferences, meal timing, cooking resources, access and budget.
   - **Optional health and safety:** user-reported injuries, relevant conditions, medications or restrictions, pregnancy-related considerations where relevant, and clinician-provided activity or dietary advice. Never infer or diagnose these; support skip/decline and avoid asking for unnecessary detail. Optional measurements such as height or weight must have clear units, relevance and valid bounds and must never be treated as mandatory.
   - **Habits and barriers:** sleep, stress, support, current routines, obstacles and readiness, without requesting unnecessary sensitive history.
3. Give each value a typed value plus `unknown`, `skipped`, `declined` or `confirmed` status, source, timestamp, question version and units as applicable. Explicitly distinguish “none” from unavailable or declined. Expose field-level provenance and freshness where appropriate, without retaining sensitive free-text excerpts unnecessarily.
4. Define a versioned, authenticated, user-scoped profile read contract for future apps, including units, statuses, update time and enough completeness/safety flags to identify missing or stale inputs. A status is not a medical clearance. Document the contract, field ownership, optional fields and migration/versioning policy.

### 2. Establish canonical storage and migrate safely

1. Extend the existing profile and introduce only the structured onboarding/answer models needed for the contract and progress state; use validated fields or a documented versioned schema rather than unchecked arbitrary JSON. Define ownership clearly: canonical confirmed profile values live in one place; `Goal` owns actual goals; conversation messages and memory are context, not competing sources of truth.
2. Model questionnaire version, current section/question, in-progress/completed status, and a nullable owner-scoped onboarding conversation reference. Preserve confirmed user values during upgrades; track drafts and their source so deleting a conversation handles unfinished answers as specified.
3. Migrate existing users without discarding existing profile, goals, chats or memories. Backfill compatible existing fields only as existing user-provided data, never invent answers. Require all accounts to complete the current questionnaire, including accounts with an old completion flag; retain prior data for review.
4. Make completion server-controlled and derived from current questionnaire version, adult eligibility, required answers, resolved optional questions and explicit review/confirmation. Remove direct write access to the completion flag; keep APIs and profile edits consistent with the canonical service.

### 3. Implement onboarding access and lifecycle

1. Replace the skip-to-dashboard experience with a concise introduction explaining topics, optional sensitive questions, saving/resuming, and the need to finish before accessing other apps. Respect the current plan to defer consent UI, but do not imply consent has been given.
2. Apply one shared access policy consistently across frontend routes and authenticated API endpoints, including direct links, registration, login, dashboard, chat/check-in and other app endpoints. Allow only authentication/logout, onboarding and the profile review/correction operations needed to finish. APIs return a documented actionable incomplete-onboarding response instead of HTML redirects.
3. Initialize or resume exactly one active onboarding conversation per user, with concurrency-safe creation and a persisted greeting. New-chat and check-in entry points during onboarding route back to it. A refresh or repeat request must not create another conversation or duplicate the greeting.
4. Create new conversations through an explicit, idempotent server operation rather than on a read-only page load. After onboarding, new chat and check-in conversations receive the exact greeting first; keep any existing check-in-specific prompt as a subsequent assistant message. Do not retroactively alter existing conversations or their ordering.
5. Handle age ineligibility and incomplete eligibility explicitly; avoid bypass through direct API calls or profile writes. Clearly show progress and a supported return path after sign-in, session loss, refresh or navigation.

### 4. Build the conversational questionnaire

1. Use a server-owned state machine and catalog to determine the next question and validate answers. Let the mentor phrase follow-ups naturally, but never let model text alone advance completion, assert unknown facts, or write a canonical profile.
2. Extract possible structured answers with a constrained output schema and validate types, units, ranges, cross-field relationships and question applicability on the server. Ask clarifying questions for ambiguous/conflicting answers; preserve a correction path. Reject or re-ask invalid values with helpful feedback.
3. Save each accepted answer durably before advancing. Support explicit skip/decline on optional questions, distinguish unresolved answers, and offer the ability to return and edit. Partial results survive interruption; a provider error cannot corrupt state or fabricate an assistant response.
4. Show a readable review of all captured information and missing/declined statuses. Require explicit user confirmation before promoting drafts to canonical values and setting completion; support individual correction or deletion later via the existing profile experience and authenticated profile API.
5. Show a completion screen and unlock other application areas only after server-side validation. Explain that missing safety information may limit future personalization.

### 5. Connect reliable chat context and memory

1. Load only the authenticated user's requested conversation, ordered by `(created_at, id)`, and feed bounded recent messages to the orchestrator exactly once per turn; avoid adding the just-persisted user message twice. Include a relevant, minimized subset of confirmed profile and active goals in the actual LLM context, not merely in an unused dictionary.
2. Use a token/message budget and an optional conversation summary for older context. Define a stable summary coverage boundary based on message IDs, avoid duplicating covered messages, and regenerate or discard summaries when their source changes. Do not include another user's chat or unchecked memory in context.
3. Extract only useful, validated facts/preferences/constraints with provenance and verification state. Avoid blindly promoting model inferences into the canonical profile; deduplicate or supersede conflicting facts and honor expiration. Keep summaries and memories user-scoped, bounded and relevant. Sensitive facts receive the same minimization and deletion protections as profile data.
4. Change conversation deletion transactionally so its messages, summaries and source-derived `MemoryEntry` rows are removed before `SET_NULL` can orphan them; retain canonical confirmed profile values. Cover any multi-source memory explicitly: use source-specific provenance or do not combine sources in a way that defeats deletion. Show a confirmation explaining what is deleted and retained. Existing memory API remains user-scoped; no new standalone memory UI.

### 6. Make delivery, privacy and safety robust

1. Serialize each conversation's turns or otherwise prevent overlapping sends; persist client-generated idempotency keys and turn status so retries, timeouts, double-clicks and reconnects do not duplicate user messages, greetings or replies. Do not hold a database transaction open over the external provider call. Explicitly represent pending/failed turns, offer safe retry, and recover after interrupted requests.
2. Protect profile, messages, memories, summaries and all related APIs with owner-scoped queries; enforce CSRF/authentication for web requests, validate payload sizes, avoid sensitive content in logs/errors, and review database backups and provider retention/access settings. Show clear failure states and do not send unrelated historical or sensitive data to the provider.
3. Preserve keyboard access, screen-reader announcements for new responses, sensible focus, responsive layout and reduced-motion behavior. Clearly indicate saved, sending, retry and completion states.
4. Do not infer safety from questionnaire completion. Future consumers must be able to identify missing allergy, injury, condition or clinician-guidance information and withhold or limit recommendations as appropriate. Do not diagnose, prescribe, promise safety, or generate detailed workout/meal plans in this phase; medical red flags require appropriate professional guidance.
5. Before any release processing real sensitive data, review applicable privacy/legal requirements, lawful basis and provider agreements/retention with the responsible owner. The planned omission of consent collection is not evidence that processing is legally permitted; resolve any required safeguards before release.

### 7. Validate and roll out

1. Add focused Django/service/API tests for existing and new account gates, all allowed escape paths, adult eligibility, optional skip/decline versus unknown, validation, review/correction, deletion, completion tampering, questionnaire-version migration and resumption.
2. Test new-chat/check-in greetings for exact text and first position; refresh, concurrent initiation and retry must not duplicate conversations, messages or greetings. Verify older conversations remain unchanged, deterministic ordering survives timestamp ties, and onboarding new-chat requests resume the existing chat.
3. Test context contains only the correct ordered, bounded conversation and permitted profile/goal data, with no duplicated current turn or cross-user exposure. Test memory extraction, verification, expiration, summary boundaries and deletion including orphan prevention and retained canonical values.
4. Simulate provider errors, timeouts, duplicate submission, interruptions and retry; confirm explicit errors, durable progress and no duplicated replies. Test owner isolation, profile edit/deletion, and authenticated frontend/API gate bypass attempts.
5. Run relevant existing chat tests and new targeted tests, migration checks and project checks; perform browser flows for desktop/mobile, keyboard/screen reader semantics, refresh, resume, delete, confirm and later edit. Verify a sample authenticated profile response matches the documented versioned contract and that existing records survive migration.
6. Roll out migrations before enabling the gate, with a staged deployment/feature flag and a reversible application rollout. Back up data, monitor non-sensitive operational metrics for completion, failed turns and deletion errors, and document migration/rollback limitations. Never log questionnaire answers for analytics.

## Acceptance criteria

- All eligible existing and new users are guided into the same resumable questionnaire and cannot bypass completion via a web or API route.
- Every newly created chat begins with exactly the specified greeting once, including after retries; old chats remain intact and in sequence.
- The reviewed profile is typed, validated, user-scoped, editable/deletable and consumable through a documented versioned contract; unknown, skipped, declined and confirmed are distinct.
- Deleting a conversation removes its messages, summaries and conversation-derived memories while retaining confirmed profile values, as explained to the user.
- Chat memory uses relevant, bounded user-owned context; failures and retries are visible and do not corrupt progress or create duplicates.
- No workout/nutrition recommendation engine or separate memory-management interface is delivered as part of this plan. Consent collection is deferred and legal/privacy review remains a release prerequisite.
