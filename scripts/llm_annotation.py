import ollama
import re
import pandas as pd
import json
class ollamaAgent:
    def __init__(self, model_name, context_size, temperature, max_tokens):
        super().__init__()
        self.model_name = model_name
        self.options = {'num_ctx': context_size, # max number of tokens allowed in context
                        'temperature': temperature, # sampling temperature
                        'num_predict': max_tokens, # max number of decoded tokens before interrupt
                        'keep_alive': "2h"
                        } 
    
    def get_action(self, prompt, context):
        return ollama.generate(model=self.model_name,
                        prompt=prompt,
                        options=self.options,
                        context = context)
    
def extract_classification(answer_identifier, response, allowed_responses):
    """
    Params
    answer_identifier : str
        The special string indicating where the answer begins (e.g., "sentiment:").
    response : str
        The text output from the model.
    allowed_responses : list of str
        List of allowed classification answers (case-insensitive).

    Returns
    str or None
        The extracted answer (normalized to lowercase), or None if not found or not allowed.
    """
    if not response or not answer_identifier:
        return None

    # Use regex to find the answer after the identifier
    pattern = re.escape(answer_identifier) + r"\s*([^\s.,;:!?\n\r]+)"
    match = re.search(pattern, response, flags=re.IGNORECASE)
    if not match:
        print("ERROR ANSWER IDENTIFIER NOT IN RESPONSE")
        return None

    # Extract and normalize the answer
    answer = match.group(1).strip().lower()

    # Normalize allowed responses for case-insensitive comparison
    allowed_set = {a.lower() for a in allowed_responses}
    if answer not in allowed_set:
        print("ERROR ANSWER NOT IN ALLOWED SET")
        return None
    return answer

if __name__ == "__main__":
    agent = ollamaAgent(model_name='qwen3:4b', context_size=40000, temperature=0.5, max_tokens=2500)
    csv_path = "../data/open_coding_articles.tsv"
    df = pd.read_csv(csv_path, sep='\t')
    categories = ["positive", "negative", "neutral"]
    context_prompt = "You are going to be doing sentiment classification. \
        The inputs will be in the format of a title and a description of a news article. \
        You must classify wether the article is positive, negative or neutral about Mark Carney who is the Current Prime Minister of Canada.\n\
        To classify something as positive about Mark Carney, it needs to involve a positive opinion about him, one of his policies, or to be discussing his successes.\n\
        To classify something as negative about Mark Carney, it needs to involve a negative opinion aobut him, one of his policies or to be discussing his failures.\n\
        To classify something as neutral, it must either not relate directly to him or his policies or not offer an opinion on him or his policies.\n\
        Make sure to only respond in the format 'sentiment:' followed by one of positive, negative or neutral\n"
    tot = 0
    incorrect = 0
    resp = agent.get_action(context_prompt, [])
    context = resp["context"]
    agent_preds = []
    for i, row in df.iterrows():
        #print(row)
        desc_str = f"title: {row['title']}\n description: {row['description']}"
        prompt = f"Below is the title description pair to classify:\n" + desc_str
        response = agent.get_action(prompt, context)
        pred_class = extract_classification("sentiment:", response["response"], categories)
        print("AGENT:", pred_class)
        print('LABEL:', row['sentiment'].lower())
        tot += 1
        if pred_class != row['sentiment'].lower():
            incorrect += 1
            print("AGENT OUTPUTTING BAD CLASS")
        agent_preds.append(pred_class)
    print('AGENT WAS WRONG ', incorrect, " on ", tot, ' entries')

    outfile = "qwen3_4b_open_coding_sentiment.json"
    with open(outfile, 'w') as fp:
        json.dump(agent_preds, fp)


