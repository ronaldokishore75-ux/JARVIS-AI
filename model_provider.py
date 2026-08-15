# =========================================================
# JARVIS V6.8 - MODEL PROVIDER WITH FALLBACK
# =========================================================

import os

from dotenv import load_dotenv

from ai import ask_ai
from local_llm import ask_local


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "gemini"
).strip().lower()


FALLBACK_PROVIDER = os.getenv(
    "LLM_FALLBACK",
    "gemini"
).strip().lower()


# =========================================================
# GET ACTIVE PROVIDER
# =========================================================

def get_provider():

    return LLM_PROVIDER


# =========================================================
# GET FALLBACK PROVIDER
# =========================================================

def get_fallback_provider():

    return FALLBACK_PROVIDER


# =========================================================
# ASK GEMINI
# =========================================================

def _ask_gemini(prompt):

    return ask_ai(
        prompt
    )


# =========================================================
# ASK OLLAMA
# =========================================================

def _ask_ollama(prompt):

    return ask_local(
        prompt
    )


# =========================================================
# ASK SELECTED MODEL
# =========================================================

def ask_model(prompt):

    if not prompt or not prompt.strip():

        raise ValueError(
            "Prompt cannot be empty."
        )

    provider = get_provider()

    fallback = get_fallback_provider()


    # =====================================================
    # GEMINI
    # =====================================================

    if provider == "gemini":

        return _ask_gemini(
            prompt
        )


    # =====================================================
    # OLLAMA
    # =====================================================

    if provider == "ollama":

        try:

            return _ask_ollama(
                prompt
            )

        except Exception as error:

            print(
                f"V6.8 OLLAMA ERROR: {error}"
            )


            # ---------------------------------------------
            # Fallback to Gemini
            # ---------------------------------------------

            if fallback == "gemini":

                print(
                    "V6.8 FALLBACK: Switching to Gemini."
                )

                return _ask_gemini(
                    prompt
                )


            raise


    # =====================================================
    # UNKNOWN PROVIDER
    # =====================================================

    raise ValueError(
        f"Unknown LLM_PROVIDER: {provider}"
    )