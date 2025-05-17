from typing import Dict

FOO1_KEY="FOO_KEY"
FOO1_VALUE="FOO_VALUE"

FOO2_KEY="event-planner"
FOO2_VALUE="""
Plan an event titled {{Event Name}}. The event will be about: {{Event Description}}.
The event will be held in {{Location}} on {{Date}}.
Consider the following factors: audience, budget, venue, catering options, and entertainment.
Provide a detailed plan including potential vendors and logistics.
"""

ITEM1: Dict[str, str] = {
    FOO1_KEY: FOO1_VALUE,
    FOO2_KEY: FOO2_VALUE,
}
