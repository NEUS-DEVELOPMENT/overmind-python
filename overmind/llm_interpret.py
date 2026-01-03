"""
overmind/llm_interpret.py - Example usage of interpret_threat with an LLM object

This module demonstrates how to use an LLM (such as OpenAI) to interpret or explain a threat received from the Sentinel system.
"""

class LLMInterface:
    """
    Abstract class representing an LLM interface (e.g., OpenAI, Azure, etc.).
    In practice, this should implement a generate() or complete() method.
    """
    def generate(self, prompt: str) -> str:
        raise NotImplementedError("Implement LLM client logic here.")


def interpret_threat(threat: dict, llm: LLMInterface) -> str:
    """
    Given a threat object (as received from Sentinel), use LLM to provide an interpretation/explanation.

    :param threat: dict, the threat object as received from Sentinel
    :param llm: an instance of LLMInterface (e.g., wrapping OpenAI API)
    :return: str, the LLM's interpretation/explanation
    """
    threat_str = str(threat)
    prompt = (
        "Received the following threat object from Sentinel (as dict):\n"
        f"{threat_str}\n\n"
        "Please provide a clear and professional explanation of this threat for a security analyst."
    )
    return llm.generate(prompt)

# Example Usage (requires implementing a subclass of LLMInterface that connects to an actual LLM):
# from openai_llm import OpenAILLM  # hypothetical module
# threat = {"id": 123, "type": "malware", "details": "Suspicious file detected on endpoint."}
# llm = OpenAILLM(api_key="sk-...")
# explanation = interpret_threat(threat, llm)
# print(explanation)
