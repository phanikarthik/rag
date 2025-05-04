1) Goto https://ollama.com/ and download OllamaSetup 

2) Open windows cmd anywhere and run the below commands:
 ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
 ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\Windows\system32>ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
pulling manifest
pulling 74aebb552ea7... 100% ▕████████████████████████████████████████████████████████▏  68 MB
pulling ef1438627c47... 100% ▕████████████████████████████████████████████████████████▏  190 B
verifying sha256 digest
writing manifest
success

C:\Windows\system32>ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
pulling manifest
pulling 6f85a640a97c... 100% ▕████████████████████████████████████████████████████████▏ 807 MB
pulling 948af2743fc7... 100% ▕████████████████████████████████████████████████████████▏ 1.5 KB
pulling 6c0b08d96525... 100% ▕████████████████████████████████████████████████████████▏   65 B
pulling 60f68b1aefd0... 100% ▕████████████████████████████████████████████████████████▏  193 B
verifying sha256 digest
writing manifest
success

C:\Windows\system32>pip install ollama
Collecting ollama
  Downloading ollama-0.4.7-py3-none-any.whl.metadata (4.7 kB)
Requirement already satisfied: httpx<0.29,>=0.27 in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from ollama) (0.28.1)
Requirement already satisfied: pydantic<3.0.0,>=2.9.0 in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from ollama) (2.10.6)
Requirement already satisfied: anyio in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from httpx<0.29,>=0.27->ollama) (4.9.0)
Requirement already satisfied: certifi in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from httpx<0.29,>=0.27->ollama) (2025.1.31)
Requirement already satisfied: httpcore==1.* in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from httpx<0.29,>=0.27->ollama) (1.0.7)
Requirement already satisfied: idna in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from httpx<0.29,>=0.27->ollama) (3.10)
Requirement already satisfied: h11<0.15,>=0.13 in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from httpcore==1.*->httpx<0.29,>=0.27->ollama) (0.14.0)
Requirement already satisfied: annotated-types>=0.6.0 in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from pydantic<3.0.0,>=2.9.0->ollama) (0.7.0)
Requirement already satisfied: pydantic-core==2.27.2 in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from pydantic<3.0.0,>=2.9.0->ollama) (2.27.2)
Requirement already satisfied: typing-extensions>=4.12.2 in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from pydantic<3.0.0,>=2.9.0->ollama) (4.12.2)
Requirement already satisfied: sniffio>=1.1 in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from anyio->httpx<0.29,>=0.27->ollama) (1.3.1)
Downloading ollama-0.4.7-py3-none-any.whl (13 kB)
Installing collected packages: ollama
Successfully installed ollama-0.4.7

[notice] A new release of pip is available: 24.3.1 -> 25.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3) Install a Python debugger like VSCode. and install python packages in VSCode.
Python
v2025.4.0
Microsoft
microsoft.com
163,745,936
(609)
Python language support with extension access points for IntelliSense 


4) Then follow as explained in "Loading the dataset" in BKM.

reference :BKM downloaded from https://huggingface.co/blog/ngxson/make-your-own-rag

5) install faiss
pip install faiss-cpu

Collecting faiss-cpu
  Using cached faiss_cpu-1.10.0-cp313-cp313-win_amd64.whl.metadata (4.5 kB)
Collecting numpy<3.0,>=1.25.0 (from faiss-cpu)
  Using cached numpy-2.2.4-cp313-cp313-win_amd64.whl.metadata (60 kB)
Collecting packaging (from faiss-cpu)
  Using cached packaging-24.2-py3-none-any.whl.metadata (3.2 kB)
Downloading faiss_cpu-1.10.0-cp313-cp313-win_amd64.whl (13.7 MB)
   ---------------------------------------- 13.7/13.7 MB 3.8 MB/s eta 0:00:00
Using cached numpy-2.2.4-cp313-cp313-win_amd64.whl (12.6 MB)
Using cached packaging-24.2-py3-none-any.whl (65 kB)
Installing collected packages: packaging, numpy, faiss-cpu
Successfully installed faiss-cpu-1.10.0 numpy-2.2.4 packaging-24.2

[notice] A new release of pip is available: 24.3.1 -> 25.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip


6) initialize repo
$ ls -al ~/.ssh
ls: cannot access '/c/Users/MSI/.ssh': No such file or directory

MSI@DESKTOP-8P7LIVV MINGW64 ~
$ ssh-keygen -t ed25519 -C "phanikartcs@gmail.com"

In powershell admin prompt:
PS C:\Windows\system32> Get-Service -Name ssh-agent | Set-Service -StartupType Manual
PS C:\Windows\system32> Start-Service ssh-agent
PS C:\Windows\system32> ssh-add c:/Users/MSI/.ssh/id_ed25519
Identity added: c:/Users/MSI/.ssh/id_ed25519 (xxxx@gmail.com)

Then in gitbash: ssh-keyscan github.com >>  ../../Users/MSI/.ssh/known_hosts

Copied id_ed25519.pub contents and pasted in github.

$ pip install tqdm
Requirement already satisfied: tqdm in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (4.67.1)
Requirement already satisfied: colorama in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from tqdm) (0.4.6)

[notice] A new release of pip is available: 24.3.1 -> 25.1
[notice] To update, run: python.exe -m pip install --upgrade pip

$ pip install nltk (not using)
Collecting nltk
  Using cached nltk-3.9.1-py3-none-any.whl.metadata (2.9 kB)
Collecting click (from nltk)
  Using cached click-8.1.8-py3-none-any.whl.metadata (2.3 kB)
Collecting joblib (from nltk)
  Using cached joblib-1.4.2-py3-none-any.whl.metadata (5.4 kB)
Collecting regex>=2021.8.3 (from nltk)
  Using cached regex-2024.11.6-cp313-cp313-win_amd64.whl.metadata (41 kB)
Requirement already satisfied: tqdm in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from nltk) (4.67.1)
Requirement already satisfied: colorama in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from click->nltk) (0.4.6)
Using cached nltk-3.9.1-py3-none-any.whl (1.5 MB)
Downloading regex-2024.11.6-cp313-cp313-win_amd64.whl (273 kB)
Using cached click-8.1.8-py3-none-any.whl (98 kB)
Using cached joblib-1.4.2-py3-none-any.whl (301 kB)
Installing collected packages: regex, joblib, click, nltk
Successfully installed click-8.1.8 joblib-1.4.2 nltk-3.9.1 regex-2024.11.6

[notice] A new release of pip is available: 24.3.1 -> 25.1
[notice] To update, run: python.exe -m pip install --upgrade pip


$ pip install textblob
Collecting textblob
  Downloading textblob-0.19.0-py3-none-any.whl.metadata (4.4 kB)
Requirement already satisfied: nltk>=3.9 in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from textblob) (3.9.1)
Requirement already satisfied: click in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from nltk>=3.9->textblob) (8.1.8)
Requirement already satisfied: joblib in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from nltk>=3.9->textblob) (1.4.2)
Requirement already satisfied: regex>=2021.8.3 in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from nltk>=3.9->textblob) (2024.11.6)
Requirement already satisfied: tqdm in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from nltk>=3.9->textblob) (4.67.1)
Requirement already satisfied: colorama in c:\users\msi\appdata\local\programs\python\python313\lib\site-packages (from click->nltk>=3.9->textblob) (0.4.6)
Downloading textblob-0.19.0-py3-none-any.whl (624 kB)
   ---------------------------------------- 624.3/624.3 kB 3.0 MB/s eta 0:00:00
Installing collected packages: textblob
Successfully installed textblob-0.19.0

[notice] A new release of pip is available: 24.3.1 -> 25.1
[notice] To update, run: python.exe -m pip install --upgrade pip

MSI@DESKTOP-8P7LIVV MINGW64 /d/2105_family/panu/code/workspace/rag_repo/rag (main)
$ python -m textblob.download_corpora
[nltk_data] Downloading package brown to
[nltk_data]     C:\Users\MSI\AppData\Roaming\nltk_data...
[nltk_data]   Unzipping corpora\brown.zip.
[nltk_data] Downloading package punkt_tab to
[nltk_data]     C:\Users\MSI\AppData\Roaming\nltk_data...
[nltk_data]   Unzipping tokenizers\punkt_tab.zip.
[nltk_data] Downloading package wordnet to
[nltk_data]     C:\Users\MSI\AppData\Roaming\nltk_data...
[nltk_data] Downloading package averaged_perceptron_tagger_eng to
[nltk_data]     C:\Users\MSI\AppData\Roaming\nltk_data...
[nltk_data] Error downloading 'averaged_perceptron_tagger_eng' from
[nltk_data]     <https://raw.githubusercontent.com/nltk/nltk_data/gh-p
[nltk_data]     ages/packages/taggers/averaged_perceptron_tagger_eng.z
[nltk_data]     ip>:   HTTP Error 429: Too Many Requests
[nltk_data] Downloading package conll2000 to
[nltk_data]     C:\Users\MSI\AppData\Roaming\nltk_data...
[nltk_data]   Unzipping corpora\conll2000.zip.
[nltk_data] Downloading package movie_reviews to
[nltk_data]     C:\Users\MSI\AppData\Roaming\nltk_data...
[nltk_data]   Unzipping corpora\movie_reviews.zip.
Finished.

MSI@DESKTOP-8P7LIVV MINGW64 /d/2105_family/panu/code/workspace/rag_repo/rag (main

$ pip install pymupdf -------------not using
Collecting pymupdf
  Downloading pymupdf-1.25.5-cp39-abi3-win_amd64.whl.metadata (3.4 kB)
Downloading pymupdf-1.25.5-cp39-abi3-win_amd64.whl (16.6 MB)
   ---------------------------------------- 16.6/16.6 MB 8.4 MB/s eta 0:00:00
Installing collected packages: pymupdf
Successfully installed pymupdf-1.25.5

[notice] A new release of pip is available: 24.3.1 -> 25.1
[notice] To update, run: python.exe -m pip install --upgrade pip


$ pip install pdfminer.six
Collecting pdfminer.six
  Downloading pdfminer_six-20250416-py3-none-any.whl.metadata (4.1 kB)
Collecting charset-normalizer>=2.0.0 (from pdfminer.six)
  Using cached charset_normalizer-3.4.1-cp313-cp313-win_amd64.whl.metadata (36 kB)
Collecting cryptography>=36.0.0 (from pdfminer.six)
  Downloading cryptography-44.0.2-cp39-abi3-win_amd64.whl.metadata (5.7 kB)
Collecting cffi>=1.12 (from cryptography>=36.0.0->pdfminer.six)
  Downloading cffi-1.17.1-cp313-cp313-win_amd64.whl.metadata (1.6 kB)
Collecting pycparser (from cffi>=1.12->cryptography>=36.0.0->pdfminer.six)
  Downloading pycparser-2.22-py3-none-any.whl.metadata (943 bytes)
Downloading pdfminer_six-20250416-py3-none-any.whl (5.6 MB)
   ---------------------------------------- 5.6/5.6 MB 11.1 MB/s eta 0:00:00
Using cached charset_normalizer-3.4.1-cp313-cp313-win_amd64.whl (102 kB)
Downloading cryptography-44.0.2-cp39-abi3-win_amd64.whl (3.2 MB)
   ---------------------------------------- 3.2/3.2 MB 13.1 MB/s eta 0:00:00
Downloading cffi-1.17.1-cp313-cp313-win_amd64.whl (182 kB)
Downloading pycparser-2.22-py3-none-any.whl (117 kB)
Installing collected packages: pycparser, charset-normalizer, cffi, cryptography, pdfminer.six
Successfully installed cffi-1.17.1 charset-normalizer-3.4.1 cryptography-44.0.2 pdfminer.six-20250416 pycparser-2.22

[notice] A new release of pip is available: 24.3.1 -> 25.1
[notice] To update, run: python.exe -m pip install --upgrade pip
