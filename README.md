# pdf_summarizer

pdf_summarizer is a tool that, when PDF files are provided as a prompt, summarizes their contents and generates headlines for each file.
It was developed as part of the dissertation project for the MSc Computational and Data Journalism course at Cardiff University.

The tool implemented LLM model [Llama-3-ELYZA-JP-8B-GGUF](https://huggingface.co/elyza/Llama-3-ELYZA-JP-8B-GGUF).

## How to run the tool

1. Install all the requirements by running `pip install -r requirements.txt` in the terminal.
2. Run `python main.py`
3. To upload PDF, type "PDF " then paste relative paths of the files. Make sure the files are in the same folder as the python file.

##Referemces

- Masato Hirakawa, Shintaro Horie, Tomoaki Nakamura, Daisuke Oba, Sam Passaglia, Akira Sasaki. [elyza/Llama-3-ELYZA-JP-8B](https://huggingface.co/elyza/Llama-3-ELYZA-JP-8B), 2024.
