import torch
from transformers import PegasusTokenizer, PegasusForConditionalGeneration

model_name = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)

def summarize_text(user_input, model, tokenizer):

    inputs = tokenizer(
        user_input,
        truncation=True,
        padding='longest',
        return_tensors="pt"
    )

    inputs = {key: value.to(device) for key, value in inputs.items()}

    summary_ids = model.generate(**inputs)
    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True)

    return summary


user_text = input("Özetlemek istediğiniz metni giriniz:\n")

summarized_text = summarize_text(user_text, model, tokenizer)

print("\Summary:")
print(summarized_text)