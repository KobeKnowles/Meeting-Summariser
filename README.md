# Meeting-Summariser
Code to get a transcript from a video/audio file, then summarise the transcript. Useful for summarising meetings. 

## How to Run

Make sure openai is installed (pip install openai); Having an openai accound (key) is required. 

The maximum file size for audio/video files is 25 MB. If your file is larger than 25 MB then the following GitHub repository can help (https://github.com/c0decracker/video-splitter) to split the file into multiple chunks/files. 

To produce a summary of a video/audio file you will need to run main.py. You will need to enter your OPENAI_API_KEY and OPENAI_ORGANISATION_KEY (if no organisation then comment out any lines related to the organisation key). You will also need to enter values for the following variables: filepath_list, transcript_save_fp, save_fp_sum, which respresent a list of strings representing filepaths to chunks of a video/audio file (this can be a single file), the filepath you want to save the transcript of the meeting, and the filepath you want to save the produced summary. You can change the model of the audio-to-speech model by modifying variable gt_model; the language model by modifying variable lm_model, and its temperature by modifying variable temp.

This repository is currently a bare bones implementation with improvements to come!
