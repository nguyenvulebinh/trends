import sys
sys.path.append('./')
from src.tools.llm import get_default_llm_model
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

translation_prompt_template = """Translate the following paragraphes from German to English:

```{text}```

TRANSLATED SENTENCE:

""" 

if __name__ == "__main__":
    translation_chain = PromptTemplate.from_template(translation_prompt_template) | get_default_llm_model(temperature=0.1) | StrOutputParser()
    print(translation_chain.invoke(input={"text": "Das Informationstechnikzentrum Bund (ITZBund) hat IONOS mit dem Aufbau einer “privaten Enterprise-Cloud“ beauftragt. Diese soll in den Rechenzentren des ..."}))