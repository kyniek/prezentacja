# Say Hello!
:) 

**Show LMStudio.**

**Show first chat working locally and how is integrating with LMStudio**

**Show plugin Continue**

### What is LLM 
<p style="text-align: justify;">LLM (Large Language Model) is a machine learning model trained on massive text datasets, which learns statistical dependencies between tokens.
Technically, it is most commonly a transformer that predicts the next token based on context, but thanks to its scale, it can model complex linguistic and conceptual patterns.
For a programmer, an LLM is essentially a "function" that maps input text to output text, behaving like a probabilistic interpreter of natural language and code.
It does not "understand" the world in a symbolic sense, but it can very effectively approximate reasoning because it has seen millions of examples of similar structures.</p>

### What is context?
<p style="text-align: justify;">In LLMs, context is a window of tokens — a fragment of the input sequence (prompt + history + system) that the model sees simultaneously and based on which it predicts the next tokens.
Technically, context is an architectural limitation of the transformer: the self-attention mechanism has access only to tokens within this window, and everything outside of it does not exist for the model at a given inference step.
Models with small context (e.g., 4k–8k tokens) perform well on local reasoning but lose track of long-range dependencies, whereas models with very large context (e.g., 128k–260k tokens) can analyze entire code repositories, documentation, or long dialogues at once.
In practice, a larger context is not “better memory,” but rather the ability to process more data in one go — at the cost of time, memory, and often attention quality on very distant tokens.</p>

**Show second chat with context. 

### Risks when using commercial LLMs
<p style="text-align: justify;">The Samsung case you mention is an excellent example of real risk associated with public AI tools. In 2023, 
employees of this company used ChatGPT to optimize sensitive source code and summarize confidential meeting notes. This data ended up on the 
provider's servers and could have been used for further model training, resulting in an intellectual property leak 
( <a href="https://www.theverge.com/2023/5/2/23707796/samsung-ban-chatgpt-generative-ai-bing-bard-employees-security-concerns">Samsung ban for chatGPT</a>). This incident reveals 
the phenomenon known as "Shadow AI," which refers to unauthorized use of AI tools by employees and represents the main source of such threats 
( <a href="https://structured.com/blog/shadow-ai-the-hidden-threat/">AI hidden threat</a>).If a company is ChatGPT’s API, then conversations with the chatbot are not visible 
to OpenAI’s support team and are not used to train the company’s models. However, this is not true of text inputted into the general web 
interface using its default settings. In response, Samsung introduced a temporary ban on using generative AI tools on 
corporate devices.</p>


### Let's talk again about LMStudio - parameters

- ***1) Context Length (Context Window)***

    What it is:
    - The maximum number of tokens the model “remembers” (prompt + history + response).

    _Why it matters:_
    - Too small → model “forgets” earlier information
    - Too large → higher RAM/VRAM usage, slower performance

    _When to increase:_
    - Long conversations Code / document analysis / RAG, chat with files
    _Typical values:_
    - 4k – quick questions
    - 8k–16k – technical work
    - 32k+ – documents, analyses


- ***2) Temperature***

  _What it is:_
  - The randomness of selecting subsequent tokens.
  
  _How it works:_
  - 0.0–0.3 → deterministic, technical
  - 0.5–0.7 → natural, “like a human”
  - 0.9+ → creative, but chaotic
  
  _Recommendations:_
  - Code / SQL / logic → 0.1–0.3
  - Normal conversation → 0.6–0.7
  - Creative texts → 0.8–1.0


- ***3) Top-p (Nucleus Sampling)***

  _What it is:_
  - Limits token selection to the smallest set whose cumulative probability is p.
  
  _Example:_
  - top-p = 0.9 → very unlikely tokens are ignored.
  
  _Best practice:_
  - Use either temperature or aggressive top-p
    - Common range: 0.9–0.95


- ***4) Top-k***

  _What it is:_
  - Restricts token choice to the top K most probable tokens.
  
  _Typical usage:_
  - top-k = 40 → stable, safe output
    - top-k = 0 → disabled
  
  _Tip:_
  - When using top-p, keep top-k moderate (e.g. 40).


- ***5) Repeat Penalty***

  _What it is:_
  - Penalizes repeated tokens to prevent loops.
  
  _Prevents:_
  - Repetitive phrasing
  - Infinite loops
  
  _Typical values:_
  - 1.05–1.15
  
  _Too high → awkward, unnatural text._

### What you can expect when running LLM localy 

**Assumptions:**
- Quantization: Q4–Q5 (MLX / llama.cpp / vLLM)
- Context length: 8–16k
- Energy consumption: entire system under inference load
- Cost: complete platform ready for deployment
- Performance: tokens/s

| Platform                    | Gemma3 12B (tok/s) | Gemma3 27B (tok/s) | Qwen3 32B (tok/s) | Energy (W) | Efficiency* | Cost (USD) | Uwagi pamięciowe    |
|-----------------------------|--------------------|--------------------|-------------------|------------|-------------|------------|---------------------|
| Apple M4 Pro (32–48 GB)     | ~28                | ~11                | ~7                | ~35        | ~0.31       | ~2 000     | Unified memory      |
| **Apple M4 Max (128 GB)**   | **52**             | **20**             | **13**            | ~45        | **0.44**    | ~3 500     | Unified memory      |
| Apple M3 Ultra (192 GB)     | ~100               | ~38                | ~25               | ~90        | ~0.42       | ~5 500     | Unified memory      |
| Apple M5 Max (est.)         | ~68                | ~26                | ~17               | ~50        | ~0.52       | ~4 000     | Unified memory      |
| Apple M5 Ultra (est.)       | ~125               | ~48                | ~31               | ~100       | ~0.48       | ~6 500     | Unified memory      |
| AMD AI Max 395 (128 GB UMA) | ~40                | ~15                | ~10               | ~55        | ~0.27       | ~2 500     | Unified memory      |
| PC RTX 4070 (12 GB VRAM)    | ~70                | ~8                 | N/A               | ~260       | ~0.10       | ~1 800     | 27B/32B not fir     |
| PC RTX 4080 (16 GB VRAM)    | ~110               | ~30                | ~6                | ~300       | ~0.12       | ~2 500     | 32B z offload       |
| PC RTX 4090 (24 GB VRAM)    | ~130               | ~65                | ~40               | ~350       | ~0.18       | ~3 000     | 32B will fit but Q4 |
| PC RTX 6000 Ada (96 GB)     | ~140               | ~70                | ~65               | ~380       | ~0.18       | ~10 000    |                     |

* Efficiency = tokens/s/W for models ~27–32B (approximately)


### Can LLM Understand images or words?

<p style="text-align: justify;"><li>Multimodality in LLM refers to the ability of a single model to process and integrate different data modalities, such as text, images, audio, or video, within a shared spatially represented context.</li>
<li>An example is Whisper, which maps audio signals to text, demonstrating how neural networks can operate on sound as a linguistic input. </li>
<li>Google Gemma (in multimodal variants) and Qwen3-VL take it a step further, as they can jointly understand text and images—for instance, answering questions about the content of a photo or diagram. </li>  
<li>From a developer's perspective, multimodality means unifying the interface: different data types are encoded into tokens/embeddings and processed by one reasoning model that handles the entire input.</li></p>


**Show Whisper**
- english
- german
- polish

**Show Qwen3 VL on LMStudio**

ComfyUI