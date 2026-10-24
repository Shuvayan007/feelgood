from django.conf import settings

from .models import Conversation, Message
from .tools import MENTOR_TOOLS


class MentorOrchestrator:
    """Central intelligence layer that coordinates user interactions with the LLM."""

    INTENTS = [
        'create_goal', 'revise_plan', 'check_in', 'log_progress',
        'ask_question', 'general_chat',
    ]

    def __init__(self, user):
        self.user = user
        try:
            self.profile = user.profile
        except Exception:
            self.profile = None

    def process_message(self, message, conversation_id=None):
        """
        Main entry point. Accepts a user message and returns a response dict.

        Flow: classify intent → build context → call LLM with tools →
              validate response → execute actions → return result.
        """
        intent = self._classify_intent(message)
        context = self._build_context(intent)

        messages = [
            {"role": "system", "content": self._system_prompt()},
            *context.get("history", []),
            {"role": "user", "content": message},
        ]

        tools = self._select_tools(intent)
        llm_response = self._call_llm(messages, tools=tools)
        validated = self._validate_response(llm_response)

        if validated.get("tool_calls"):
            action_results = self._execute_actions(validated["tool_calls"])
            validated["action_results"] = action_results

        return {
            "response": validated.get("content", "I'm here to help. Could you tell me more?"),
            "intent": intent,
            "tool_calls": validated.get("tool_calls", []),
        }

    def _classify_intent(self, message):
        """Determine what the user wants. Stub: returns 'general_chat'."""
        return "general_chat"

    def _build_context(self, intent):
        """Assemble relevant user data for the LLM context window."""
        context = {"history": []}

        if self.profile:
            context["profile"] = {
                "display_name": self.profile.display_name,
                "timezone": self.profile.timezone,
                "available_hours": float(self.profile.available_hours_per_week or 0),
            }

        try:
            from goals.models import Goal
            active_goals = Goal.objects.filter(user=self.user, status="active").values(
                "id", "title", "category", "progress_pct"
            )
            context["active_goals"] = list(active_goals)
        except Exception:
            context["active_goals"] = []

        return context

    def _system_prompt(self):
        name = ""
        if self.profile and self.profile.display_name:
            name = self.profile.display_name
        greeting = f"The user's name is {name}. " if name else ""
        return (
            "You are Feel Good, an AI personal mentor. "
            f"{greeting}"
            "Help the user define meaningful goals and guide them toward achieving "
            "those goals through personalized, actionable steps. "
            "Be warm, specific, and grounded in the user's actual data. "
            "Never invent progress or facts. If you need more information, ask."
        )

    def _select_tools(self, intent):
        """Filter available tools based on intent."""
        read_only_intents = {"ask_question", "general_chat"}
        if intent in read_only_intents:
            return [t for t in MENTOR_TOOLS if t.get("permission") == "read"]
        return MENTOR_TOOLS

    def _call_llm(self, messages, tools=None):
        """
        Placeholder for the Azure OpenAI API call.

        In production this would use:
            from openai import AzureOpenAI
            client = AzureOpenAI(
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version=settings.AZURE_OPENAI_API_VERSION,
            )
            response = client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT,
                messages=messages,
                tools=[t for t in tools] if tools else None,
            )
        """
        return {
            "content": (
                "I'd love to help you with that. To create the best plan, "
                "could you tell me a bit more about your current situation "
                "and what you'd like to achieve?"
            ),
            "tool_calls": [],
        }

    def _validate_response(self, response):
        """Validate LLM output. Pass-through stub."""
        return response

    def _execute_actions(self, tool_calls):
        """Route validated tool calls to the appropriate service methods. Stub."""
        return []
