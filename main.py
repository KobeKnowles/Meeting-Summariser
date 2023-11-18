import openai

from typing import Final, Union

from models.audio_to_video import AudioToTextOpenAI
from models.language_models import LanguageModelOpenAI

OPENAI_API_KEY: Final = "" # put your key here.
OPENAI_ORGANISATION_KEY: Final = "" # NAOInstitute

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORGANISATION_KEY

def get_transcript(model, filepaths: list[str], save_transcript: bool, save_path: str="", save_mode="w") -> str:
    
    transcript: str = model.audio_to_text_m(filepath_list = filepath_list, print_otf=False)
    try:
        if save_transcript:
            model.save_string(str_=transcript, save_fp=transcript_save_fp, mode=save_mode, new_line=False)
    except Exception as e:
        print(f"Error saving the summary file!\nError: {e}")
        print(f"The transcript file is: \n\n{transcript}")
    return transcript

def get_summary(model, transcipt: str, save_summary: bool, save_path: str="", save_mode="w") -> str:
    summary: str = model.summarise_text(transcipt=transcipt, own_prompt=None)
    try: 
        if save_summary:
            model.save_string(str_=summary, save_fp=save_fp_sum, mode=save_mode, new_line=False)
    except Exception as e:
        print(f"Error saving the summary file!\nError: {e}")
        print(f"The summary file is: \n\n{summary}")
    return summary

if __name__ == "__main__":

    # do below block if need to get transcript from video/audio.
    gt_model: str = "whisper-1"
    
    '''
    get_text = AudioToTextOpenAI(gt_model)
    filepath_list = ["C:\\Users\\kkno604\\Documents\\NAOI SAIL research discussion\\16th November 2023\\GMT20231115-220006_Recording-1-of-3.m4a",
                     "C:\\Users\\kkno604\\Documents\\NAOI SAIL research discussion\\16th November 2023\\GMT20231115-220006_Recording-2-of-3.m4a",
                     "C:\\Users\\kkno604\\Documents\\NAOI SAIL research discussion\\16th November 2023\\GMT20231115-220006_Recording-3-of-3.m4a"]

    transcript_save_fp = "C:\\Users\\kkno604\\Documents\\NAOI SAIL research discussion\\16th November 2023\\gpt-4-summary\\transcript-2.txt"
    transcript: str = get_transcript(model=get_text, filepaths=filepath_list, save_transcript=True, save_path=transcript_save_fp)
    '''
    
    #'''
    #if already have a transcript then can load from file
    transcript_file: str = "C:\\Users\\kkno604\\Documents\\NAOI SAIL research discussion\\16th November 2023\\gpt-4-summary\\transcript-2.txt"
    transcript: str = ""
    with open(transcript_file, "r") as f:
        transcript = " ".join(f.readlines())
    #'''
    
    #'''
    lm_model: str = "gpt-3.5-turbo-16k"#"gpt-4"#"gpt-3.5-turbo-16k"
    temp: float = 0.7
    lm = LanguageModelOpenAI(model=lm_model, temperature=temp)
    transcript: str = "<start> "+transcript+" <end>"

    save_fp_sum = "C:\\Users\\kkno604\\Documents\\NAOI SAIL research discussion\\16th November 2023\\gpt-4-summary\\summary-gpt4-test.txt"
    summary: str = get_summary(model=lm, transcipt=transcript, save_summary=True, save_path=save_fp_sum)

    print(f"summary:\n\n{summary}")
    #'''
    
    