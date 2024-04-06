from src.tools.llm import get_default_llm_model
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

translation_prompt_template = """[INST] 
You are given a text in {src_lang}. Based only on the given text and translate the content into {tgt_lang}. You will not add any additional commentary or notes.

Given {src_lang} text:

```
{text}
```

Tranlation {tgt_lang} text:
[/INST]
""" 


summary_prompt_template = """[INST]
You are given a text. Write a concise paragraph summarizing the content of the provided text without incorporating any additional commentary or notes.

Given text:
    
```
{text}
```

Summary:
[/INST]
"""

def translate_text(text: str, src_lang="German", tgt_lang="English", stop_sequences=[], max_word=512) -> str:
    segments = []
    if len(text.split()) > max_word:
        # split the text into multiple segments
        words = text.split()
        while len(words) > 0:
            segment = []
            while len(segment) < max_word and len(words) > 0:
                segment.append(words.pop(0))
            segments.append(" ".join(segment))
        print(f"Text is too long, split into {len(segments)} segments")
    else:
        segments.append(text)

    translated_segments = []
    translation_chain = PromptTemplate.from_template(translation_prompt_template).partial(src_lang=src_lang, tgt_lang=tgt_lang) | get_default_llm_model(temperature=0., stop_sequences=stop_sequences) | StrOutputParser()
    for segment in segments:
        translated_segments.append(translation_chain.invoke(input={"text": segment}))
    return " ".join(translated_segments)

def summarize_text(text: str) -> str:
    summary_chain = PromptTemplate.from_template(summary_prompt_template) | get_default_llm_model(temperature=0.) | StrOutputParser()
    return summary_chain.invoke(input={"text": text})

if __name__ == "__main__":
    text = """
Ticker Hessen am Morgen +++ Vater schlägt Kind beim Fußballspielen +++ Frankfurt: So viele Einwohner wie noch nie +++ Meterhohe Nirvana-Skulptur auf Kreisel in …

Tschüss!

Wir hatten es gestern im Morgenticker von Elefanten in Hessen - heute möchte ich Sie deshalb ganz passend mit einem Porzellan-Laden verabschieden. Wobei, Laden stimmt nicht, Sammlung stimmt!

Ab jetzt beginnt die Sommersaison im Porzellanschlösschen in Darmstadt. Das Museum im Prinz-Georg-Palais am Herrngarten ist freitags bis sonntags zwischen 10 und 17 Uhr geöffnet. Darin zu sehen gibt es die großherzoglich-hessischen Porzellansammlung. Das Museum war wegen Bauarbeiten lange geschlossen - jetzt ist es wieder auf. Wenn Sie kein Elefant sind, könnte das sicherlich ein netter Ausflug für Sie und das Museum werden.

Das war’s von mir. Am Montag begrüßt Sie der werte Kollege Steffen Rebhahn. Ich hoffe Sie können das Wochenende genießen - wettertechnisch sollte dem nichts im Wege stehen. Machen Sie’s gut, hören Sie dabei Nirvana - oder irgendwas anders, was Sie mögen. Morgenticker out!
"""
    translation = translate_text(text, src_lang="German", tgt_lang="English")
    print("Translation:")
    print(translation)
    summary = summarize_text(translation)
    print("Summary:")
    print(summary)