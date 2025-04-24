from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# Load the pre-trained Pegasus model and tokenizer
tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

def summarize_text(text):
    """
    Summarizes the provided text using the pre-trained Pegasus model.
    """
    # Encode the text into the format the model understands
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)

    # Generate the summary using the model
    summary_ids = model.generate(
        inputs["input_ids"], 
        max_length=250,       # Increase max length
        min_length=50,        # Ensure minimum summary length
        num_beams=8,          # Higher beams for better quality
        early_stopping=True
    )

    # Decode the generated summary and return it
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
