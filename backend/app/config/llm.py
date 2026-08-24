from pydantic_settings import BaseSettings


class LLMSettings(BaseSettings):
    """Model routing configuration.

    Each use case gets its own ordered list of litellm model ids
    ("provider/model"). The first entry is the preferred model; the rest are
    failover targets served by other providers, so a pipeline step keeps
    working when a provider is down, rate limited or returns garbage.
    Override any group with LLM_<USE_CASE>_MODELS in the environment.
    """

    # 5 SOTA models across 5 providers, routed per use case
    architecture_models: str = "anthropic/claude-sonnet-5,openai/gpt-5.1,gemini/gemini-3-pro,xai/grok-4"
    critique_models: str = "openai/gpt-5.1,anthropic/claude-opus-5,gemini/gemini-3-pro"
    roadmap_models: str = "gemini/gemini-3-pro,anthropic/claude-sonnet-5,deepseek/deepseek-chat"
    costs_models: str = "openai/gpt-5.1,deepseek/deepseek-chat,gemini/gemini-3-pro"
    edit_models: str = "anthropic/claude-sonnet-5,openai/gpt-5.1,xai/grok-4"

    # router behaviour
    request_timeout: float = 180.0
    num_retries: int = 2
    cooldown_time: int = 30

    # .env is shared with the app settings, so ignore keys that are not ours
    model_config = {"env_file": ".env", "env_prefix": "LLM_", "extra": "ignore"}


llm_settings = LLMSettings()
