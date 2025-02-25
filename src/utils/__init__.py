from .helpers import setup_cors
from .prompts import (teaching_design_prompt, exercise_prompt, answer_explanation_prompt,
                      online_test_prompt, text_polishing_prompt,
                      integrated_recommendation_prompt, ppt_outline_prompt)

__all__ = [
    "setup_cors",
    "teaching_design_prompt",
    "exercise_prompt",
    "answer_explanation_prompt",
    "online_test_prompt",
    "text_polishing_prompt",
    "integrated_recommendation_prompt",
    'ppt_outline_prompt'
]

