import subprocess


def ask_llm(prompt: str, model: str = "llama3.1", timeout: int = 60) -> str:
    """
    Send prompt to local Ollama via CLI. Returns stdout text.
    If ollama is not installed or fails, returns an error string starting with [LLM-...].
    Expects the model to return code inside ```python blocks.
    """
    try:
        proc = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        out = proc.stdout.decode("utf-8", errors="replace")
        err = proc.stderr.decode("utf-8", errors="replace")
        if not out and err:
            return f"[LLM-error] {err}"
        return out
    except FileNotFoundError:
        return "[LLM-missing] ollama not found on PATH."
    except subprocess.TimeoutExpired:
        return f"[LLM-timeout] Model took longer than {timeout}s to respond."
    except Exception as e:
        return f"[LLM-failed] {e}"