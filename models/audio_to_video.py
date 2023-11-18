import openai

from typing import Final

OPENAI_API_KEY: Final = "" # put your key here.
OPENAI_ORGANISATION_KEY: Final = "" # NAOInstitute

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORGANISATION_KEY

class AudioToTextOpenAI(object):
    
    def __init__(self, model_name: str):
        
        self.model_name: str = model_name # assumption is that the user inputs the correct model_name, no checks are going to be done.

    # process audio/video input
    # supported files for OpenAI models: mp3, mp4, mpeg, mpga, m4a, wav, webm
    def audio_to_text_s(self, filepath: str) -> str: # _s stands for single file. 
        f = open(filepath, "rb")
        transcript = openai.Audio.transcribe(self.model_name, f)
        f.close()
        return transcript["text"]

    def audio_to_text_m(self, filepath_list: list[str], print_otf: bool=False) -> str:
        
        transcript_lst: list[str] = []

        for fp in filepath_list:
            t = self.audio_to_text_s(filepath=fp)
            if print_otf: print(f"transcript: {t}")
            transcript_lst.append(t)

        return " ".join(transcript_lst)

    def convert_file_into_chunks(self, filepath_orig: str, filepath_writeto: str, suffix: str, tofilename: str,
                                 chunk_size: int=25000000):
        # byte_size should be equal to the maximum filesize that openai supports. 

        # adapted from https://www.tutorialspoint.com/How-to-spilt-a-binary-file-into-multiple-files-using-Python#:~:text=To%20split%20a%20big%20binary,the%20end%20of%20original%20file.

        print(f"Warning! the last file won't be converted correctly.")

        f = open(filepath_orig, "rb")
        print(f"f: {f}")
        chunk = f.read(chunk_size)
        file_num = 1
        while chunk:
            with open(filepath_writeto + f"{tofilename}_{file_num}.{suffix}", "wb") as chunk_file:
                chunk_file.write(chunk)
            file_num += 1
            chunk = f.read(chunk_size)
        f.close()

    #def save_string(self, str_: str, save_fp: str, mode: str="w", new_line: bool=False):
    #    if new_line: str_ = str_ + "\n"
    #    with open(save_fp, mode) as f:
    #        f.write(str_)
            
    def save_string(self, str_: str, save_fp: str, mode: str = "w", new_line: bool = False):
        if new_line:
            str_ += "\n"
        with open(save_fp, mode, encoding='utf-8') as f:  # Ensure text mode with UTF-8 encoding
            f.write(str_)




if __name__ == "__main__":
    
    get_text = AudioToTextOpenAI("whisper-1")
    #video_audio_filepath = "C:\\Users\\kkno604\\Documents\\Reading Group Recordings\\18th April 2023\\GMT20230417-213530_Recording.mp3"
    #video_audio_tofilepath = "C:\\Users\\kkno604\\Documents\\Reading Group Recordings\\18th April 2023\\chunks2\\"
    #suffix = "mp3" # period should NOT be included here.
    #tofilename = "GMT20230417-213530_Recording"

    #get_text.convert_file_into_chunks(filepath_orig=video_audio_filepath, filepath_writeto=video_audio_tofilepath,
    #                                  suffix=suffix, tofilename=tofilename)

    #video_audio_filepath = "C:\\Users\\kkno604\\Documents\\Reading Group Recordings\\18th April 2023\\GMT20230417-213530_Recording.mp3"


    filepath_list = ["C:\\Users\\kkno604\\Documents\\Reading Group Recordings\\11th July 2023\\reading-group-rec-1-of-2.m4a",
                     "C:\\Users\\kkno604\\Documents\\Reading Group Recordings\\11th July 2023\\reading-group-rec-2-of-2.m4a"]
    #print(f"filepath_list: {filepath_list}")

    transcript = get_text.audio_to_text_m(filepath_list = filepath_list, print_otf=False)

    #filepath = "C:\\Users\\kkno604\\Documents\\Reading Group Recordings\\18th April 2023\\chunks\\GMT20230417-213530_Recording_1.mp3"
    #transcript = get_text.audio_to_text_s(filepath=filepath)
    
    save_fp = "C:\\Users\\kkno604\\Documents\\audio_to_text_files\\test\\test1.txt"
    get_text.save_string(str_=transcript, save_fp=save_fp, mode="w", new_line=False)