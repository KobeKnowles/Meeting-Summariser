import openai

from typing import Final, Union

from models.audio_to_video import AudioToTextOpenAI
from models.language_models import LanguageModelOpenAI

OPENAI_API_KEY: Final = "" # put your key here.
OPENAI_ORGANISATION_KEY: Final = "" # NAOInstitute

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORGANISATION_KEY

def get_transcript(model, filepaths: list[str], save_transcript: bool, save_path: str="") -> str:
    
    transcript: str = model.audio_to_text_m(filepath_list = filepath_list, print_otf=False)
    try:
        if save_transcript:
            model.save_string(str_=transcript.encode("utf-8"), save_fp=transcript_save_fp, mode="w", new_line=False)
    except:
        pass 
    return transcript

def get_summary(model, transcipt: str, save_summary: bool, save_path: str="") -> str:
    summary: str = model.summarise_text(transcipt=transcipt, own_prompt=None)
    try: 
        if save_summary:
            model.save_string(str_=summary.encode("utf-8"), save_fp=save_fp_sum, mode="w", new_line=False)
    except:
        pass
    return summary

if __name__ == "__main__":

    # do below block if need to get transcript from video/audio.
    gt_model: str = "whisper-1"
    get_text = AudioToTextOpenAI(gt_model)
    filepath_list = ["C:\\Users\\kkno604\\Documents\\Reading Group Recordings\\4th July 2023\\4th july SAIL reading group-1-of-4.m4a",
                     "C:\\Users\\kkno604\\Documents\\Reading Group Recordings\\4th July 2023\\4th july SAIL reading group-2-of-4.m4a",
                     "C:\\Users\\kkno604\\Documents\\Reading Group Recordings\\4th July 2023\\4th july SAIL reading group-3-of-4.m4a",
                     "C:\\Users\\kkno604\\Documents\\Reading Group Recordings\\4th July 2023\\4th july SAIL reading group-4-of-4.m4a"]

    transcript_save_fp = "C:\\Users\\kkno604\\Documents\\audio_to_text_files\\test\\4th_july_rg\\transcript.txt"
    transcript: str = get_transcript(model=get_text, filepaths=filepath_list, save_transcript=True, save_path=transcript_save_fp)

    # if already have a transcript then can load from file
    #transcript_file: str = "C:\\Users\\kkno604\\Documents\\audio_to_text_files\\test\\main_test2\\transcript.txt"
    #transcript: str = ""
    #with open(transcript_file, "r") as f:
    #    transcript = " ".join(f.readlines())

    lm_model: str = "gpt-3.5-turbo-16k"
    temp: float = 0.7
    lm = LanguageModelOpenAI(model=lm_model, temperature=temp)
    transcript: str = "<start> "+transcript+" <end>"

    save_fp_sum = "C:\\Users\\kkno604\\Documents\\audio_to_text_files\\test\\4th_july_rg\\summary.txt"
    summary: str = get_summary(model=lm, transcipt=transcript, save_summary=True, save_path=save_fp_sum)

    print(f"summary:\n\n{summary}")
    
    