import openai

from typing import Final, Union

OPENAI_API_KEY: Final = "" # put your key here.
OPENAI_ORGANISATION_KEY: Final = "" # NAOInstitute

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORGANISATION_KEY


class LanguageModelOpenAI(object):

    Prompt_improve_gen_text: Final = "In-between <start> and <end> will be a transcript from a meeting generated from audio. The generated text is imperfect; your objective is to improve the generated text to make it more readable and to fix any errors in the transcript. After <end> output a revised transcript."
    Prompt_summary: Final = "In-between <start> and <end> will be a transcipt from a meeting. You objective is summarise the transcript and extract all important information so that a human can read the summary and understand the whole meeting. After <end> output a summary of the transcript."

    def __init__(self, model: str, temperature: float=0.7):
        
        self.model: str = model
        assert temperature <= 1.0 and temperature >= 0, f"temperature values should be between 0 and 1, got {temperature}!"
        self.temperature: float = temperature

    def model_completion(self, messages: list) -> str:
        completion = openai.ChatCompletion.create(
            model = self.model,
            messages = messages,
            temperature = self.temperature
        )
        
        return completion['choices'][0]['message']['content']

    def improve_generated_text_from_audio(self, transcipt: str, own_prompt: Union[None, str]=None) -> str:
        
        # don't harcode this as user can provide own prompt and specify different way to indicate start and end of 
        # transcript. This is expected to be done to the transcript before input to this funcion. 
        #transcipt = "<start> " + transcipt + " <end>"

        messages = []
        messages.append({"role": "system", "content": self.Prompt_improve_gen_text if own_prompt is None else own_prompt})
        messages.append({"role": "user", "content": transcipt})
        return self.model_completion(messages)

    def summarise_text(self, transcipt: str, own_prompt: Union[None, str]=None) -> str:
        messages = []
        messages.append({"role": "system", "content": self.Prompt_summary if own_prompt is None else own_prompt})
        messages.append({"role": "user", "content": transcipt})
        return self.model_completion(messages)

    def save_string(self, str_: str, save_fp: str, mode: str="w", new_line: bool=False):
        if new_line: str_ = str_ + "\n"
        with open(save_fp, mode) as f:
            f.write(str_)

if __name__ == "__main__":
    
    transcript_file: str = "C:\\Users\\kkno604\\Documents\\audio_to_text_files\\test\\test1.txt"
    transcript: str = ""
    with open(transcript_file, "r") as f:
        transcript = " ".join(f.readlines())
    #print(transcript)

    lm = LanguageModelOpenAI(model="gpt-3.5-turbo-16k", temperature=0.7)
    
    '''
    transcript_improved: str = lm.improve_generated_text_from_audio(transcipt="<start> "+transcript+" <end>", own_prompt=None)
    save_fp_imp = "C:\\Users\\kkno604\\Documents\\audio_to_text_files\\test\\test1_improved.txt"
    lm.save_string(str_ = transcript_improved, 
                   save_fp=save_fp_imp,
                   mode="w", new_line=False)
    
    transcript_improved2: str = ""
    with open(save_fp_imp, "r") as f:
        transcript_improved2 = " ".join(f.readlines())

    #assert transcript_improved == transcript_improved2, f"transcript_improved: {transcript_improved}\n\ntranscript_improved2: {transcript_improved2}"
    '''
    #summarised_text = lm.summarise_text(transcipt="<start> "+transcript_improved+" <end>", own_prompt=None)
    summarised_text = lm.summarise_text(transcipt="<start> "+transcript+" <end>", own_prompt=None)
    save_fp_sum = "C:\\Users\\kkno604\\Documents\\audio_to_text_files\\test\\test1_summary_orig.txt"
    lm.save_string(str_ = summarised_text, 
                   save_fp=save_fp_sum,
                   mode="w", new_line=False)

    summarised_text2: str = ""
    with open(save_fp_sum, "r") as f:
        summarised_text2 = " ".join(f.readlines())

    #assert summarised_text == summarised_text2, f"summarised_text: {summarised_text}\n\nsummarised_text2: {summarised_text2}"

    