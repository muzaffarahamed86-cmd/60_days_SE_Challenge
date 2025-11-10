from transformers import pipeline
generator = pipeline('text-generation', model='gpt2')

result = generator("Once upon a time in chennai.", max_length=20, num_return_sequences=1)

print(result[0]['generated_text'])