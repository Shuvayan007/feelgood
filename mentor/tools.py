MENTOR_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_user_profile",
            "description": "Retrieve the user's profile: preferences, constraints, available hours, and personal context.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sections": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["personal", "career", "health", "finance", "lifestyle", "constraints"],
                        },
                        "description": "Which profile sections to retrieve. Omit for all.",
                    }
                },
                "required": [],
            },
        },
        "permission": "read",
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_goals",
            "description": "Get the user's goals filtered by status and/or category, with progress percentages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["active", "paused", "completed", "draft"],
                    },
                    "category": {
                        "type": "string",
                        "enum": ["career", "fitness", "finance", "lifestyle", "personal_dev", "relationships"],
                    },
                },
                "required": [],
            },
        },
        "permission": "read",
    },
    {
        "type": "function",
        "function": {
            "name": "get_goal_detail",
            "description": "Get full details of a specific goal: milestones, actions, linked habits, progress history, and revisions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_id": {
                        "type": "integer",
                        "description": "The goal's database ID.",
                    }
                },
                "required": ["goal_id"],
            },
        },
        "permission": "read",
    },
    {
        "type": "function",
        "function": {
            "name": "get_available_time",
            "description": "Calculate unallocated hours in the user's weekly schedule by subtracting all active goal time budgets from declared available hours.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
        "permission": "read",
    },
    {
        "type": "function",
        "function": {
            "name": "get_habit_summary",
            "description": "Get completion rates, streaks, and consistency scores for the user's active habits.",
            "parameters": {
                "type": "object",
                "properties": {
                    "period": {
                        "type": "string",
                        "enum": ["week", "month", "quarter"],
                        "description": "Time period for the summary. Defaults to week.",
                    }
                },
                "required": [],
            },
        },
        "permission": "read",
    },
    {
        "type": "function",
        "function": {
            "name": "get_expense_summary",
            "description": "Get spending totals by category, budget adherence, and savings rate for a period.",
            "parameters": {
                "type": "object",
                "properties": {
                    "period": {
                        "type": "string",
                        "enum": ["week", "month", "quarter"],
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter to one expense category.",
                    },
                },
                "required": ["period"],
            },
        },
        "permission": "read",
    },
    {
        "type": "function",
        "function": {
            "name": "get_wellness_summary",
            "description": "Get recent wellness activity: workout frequency, measurement trends, sleep averages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "record_type": {
                        "type": "string",
                        "enum": ["workout", "measurement", "nutrition", "sleep"],
                    },
                    "period": {
                        "type": "string",
                        "enum": ["week", "month"],
                        "description": "Time period. Defaults to week.",
                    },
                },
                "required": [],
            },
        },
        "permission": "read",
    },
    {
        "type": "function",
        "function": {
            "name": "create_goal_proposal",
            "description": "Create a proposed goal with milestones and actions for user approval. Does NOT save until approved.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "category": {
                        "type": "string",
                        "enum": ["career", "fitness", "finance", "lifestyle", "personal_dev", "relationships"],
                    },
                    "time_horizon": {
                        "type": "string",
                        "enum": ["short", "medium", "long"],
                    },
                    "target_date": {
                        "type": "string",
                        "format": "date",
                    },
                    "success_criteria": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "weekly_time_budget_hours": {"type": "number"},
                    "milestones": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "target_date": {"type": "string", "format": "date"},
                                "actions": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "title": {"type": "string"},
                                            "action_type": {
                                                "type": "string",
                                                "enum": ["one_time", "recurring"],
                                            },
                                        },
                                        "required": ["title", "action_type"],
                                    },
                                },
                            },
                            "required": ["title"],
                        },
                    },
                },
                "required": ["title", "category", "time_horizon", "success_criteria", "milestones"],
            },
        },
        "permission": "write_with_approval",
    },
    {
        "type": "function",
        "function": {
            "name": "propose_weekly_plan",
            "description": "Generate a proposed weekly schedule that balances all active goals within available time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "week_start": {
                        "type": "string",
                        "format": "date",
                        "description": "Monday of the target week.",
                    }
                },
                "required": ["week_start"],
            },
        },
        "permission": "write_with_approval",
    },
    {
        "type": "function",
        "function": {
            "name": "log_habit",
            "description": "Record that the user completed a habit for a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "habit_id": {"type": "integer"},
                    "date": {
                        "type": "string",
                        "format": "date",
                        "description": "Date of completion. Defaults to today.",
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of completions. Defaults to 1.",
                    },
                    "notes": {"type": "string"},
                },
                "required": ["habit_id"],
            },
        },
        "permission": "write",
    },
    {
        "type": "function",
        "function": {
            "name": "log_progress",
            "description": "Record completion or progress notes on a specific action or milestone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action_id": {"type": "integer"},
                    "milestone_id": {"type": "integer"},
                    "notes": {"type": "string"},
                    "completed": {"type": "boolean"},
                },
                "required": [],
            },
        },
        "permission": "write",
    },
    {
        "type": "function",
        "function": {
            "name": "search_memory",
            "description": "Search the user's semantic memory for relevant past context using natural language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language description of the context needed.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results to return. Defaults to 5.",
                    },
                },
                "required": ["query"],
            },
        },
        "permission": "read",
    },
]
