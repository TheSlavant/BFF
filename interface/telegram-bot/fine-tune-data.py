import json
import os
from transformers import pipeline

class ConversationEvaluator:
    def __init__(self, llm_model, output_file):
        """
        Initialize the ConversationEvaluator class.

        Args:
            llm_model (str): The name of the LLM model to use (e.g. "t5-base")
            output_file (str): The path to the output JSONL file
        """
        self.llm_model = llm_model
        self.output_file = output_file
        self.llm = pipeline("text-generation", model=llm_model)

    def evaluate_conversation(self, conversation):
        """
        Evaluate a conversation and generate question-answer pairs.

        Args:
            conversation (str): The conversation to evaluate

        Returns:
            list: A list of question-answer pairs
        """
        # Send the conversation to the LLM to evaluate and generate question-answer pairs
        output = self.llm(conversation, max_length=100, num_return_sequences=10)

        # Extract the question-answer pairs from the LLM output
        qa_pairs = []
        for item in output:
            prompt = item["generated_text"].split("\n")[0].strip()
            completion = item["generated_text"].split("\n")[1].strip()
            qa_pairs.append({"prompt": prompt, "completion": completion})

        return qa_pairs

    def save_to_jsonl(self, qa_pairs):
        """
        Save the question-answer pairs to a JSONL file.

        Args:
            qa_pairs (list): The list of question-answer pairs
        """
        with open(self.output_file, "a") as f:
            for pair in qa_pairs:
                json.dump(pair, f)
                f.write("\n")

    def process_conversation(self, conversation):
        """
        Process a conversation by evaluating it and saving the output to a JSONL file.

        Args:
            conversation (str): The conversation to process
        """
        qa_pairs = self.evaluate_conversation(conversation)
        self.save_to_jsonl(qa_pairs)

# Example usage
if __name__ == "__main__":
    conversation = "What's up? Not much, how about you?"
    evaluator = ConversationEvaluator("t5-base", "output.jsonl")
    evaluator.process_conversation(conversation)