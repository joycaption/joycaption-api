# JoyCaption API — Python client

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Hosted on Synexa](https://img.shields.io/badge/hosted%20on-Synexa-6366f1.svg)](https://synexa.ai/explore/yorickvp/llava-13b?utm_source=github&utm_medium=ugc&utm_campaign=joycaption&utm_content=readme-badge&utm_term=tier-a)

JoyCaption is an open image captioning model built to write the kind of dense, literal descriptions that diffusion-model training sets need. This package is a JoyCaption-style captioning API client for Python: one `pip install` lets you send an image and a prompt to a hosted vision-language model and get a caption, tag list or answer back as text, with no weights to download and no GPU to provision.

You get a blocking `run()` that returns the generated text, a submit-and-poll path for large batches, webhook delivery on completion, and one runtime dependency (`httpx`). It is meant for dataset builders, alt-text pipelines and anyone who needs image descriptions at scale without running an 8B–13B parameter model themselves.

> **Try it now:** [https://synexa.ai/explore/yorickvp/llava-13b](https://synexa.ai/explore/yorickvp/llava-13b?utm_source=github&utm_medium=ugc&utm_campaign=joycaption&utm_content=readme-top&utm_term=tier-a) — the hosted model behind this client. New accounts get a free trial credit.

## Contents

- [Why this client](#why-this-client)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Hosted models](#hosted-models)
- [Parameters](#parameters)
- [Advanced usage](#advanced-usage)
- [About JoyCaption](#about-joycaption)
- [Use cases](#use-cases)
- [FAQ](#faq)
- [License](#license)

## Why this client

- **No GPU to provision.** A captioning VLM pairs a vision encoder with a multi-billion-parameter language model; running one at useful throughput needs a data-centre class card or heavy quantisation. The hosted endpoint runs on managed GPUs.
- **No environment to maintain.** No transformers/CUDA version matching, no multi-gigabyte checkpoint downloads, no tokenizer or projector mismatches. Install, set a key, call `run()`.
- **No cold starts on your side.** Loading a 13B model takes tens of seconds; keeping it warm costs money around the clock. Here you pay per prediction only.
- **Very low cost per image.** `yorickvp/llava-13b` is $0.0005 per run, so captioning ten thousand images costs about $5.

## Installation

```bash
pip install git+https://github.com/joycaption/joycaption-api.git
```

Then set your API key (create one at [synexa.ai](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=joycaption&utm_content=readme-apikey&utm_term=tier-a)):

```bash
export SYNEXA_API_KEY="sk-..."
```

## Quickstart

```python
import joycaption_api

output = joycaption_api.run({
    "image": "https://example.com/input.png",
    "prompt": "Are you allowed to swim here?"
})
print(output)   # URL(s) of the generated result
```

Or with an explicit client:

```python
from joycaption_api import Client

client = Client(api_key="sk-...")
output = client.run({"image": "https://example.com/input.png", "prompt": "Are you allowed to swim here?"})
```

## Hosted models

| Model | Category | What it does | Price / run |
|---|---|---|---|
| [`yorickvp/llava-13b`](https://synexa.ai/explore/yorickvp/llava-13b?utm_source=github&utm_medium=ugc&utm_campaign=joycaption&utm_content=readme-models&utm_term=tier-a) | text-recognition-ocr | Visual instruction tuning towards large language and vision models with GPT-4 level capabilities | $0.0005 |

The default model is **`yorickvp/llava-13b`**; pass `model="owner/name"` to `run()` to use another one from the table.

## Parameters

### `yorickvp/llava-13b`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `image` | file | yes | `https://synexa.s3.us-east-005.backblazeb…` | — | Input image |
| `top_p` | number | no | `1` | 0, 1 | When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens |
| `prompt` | string | yes | `Are you allowed to swim here?` | — | Prompt to use for text generation |
| `max_tokens` | integer | no | `1024` | 0, 1024 | Maximum number of tokens to generate. A word is generally 2-3 tokens |
| `temperature` | number | no | `0.2` | 0, 1 | Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic |

## Advanced usage

**Submit without blocking, then poll:**

```python
prediction = client.run(input, wait=False)      # returns immediately
prediction = client.wait(prediction, timeout=300)
print(prediction["output"])
```

**Webhook on completion:**

```python
client.run(input, wait=False, webhook="https://your-app.example/hooks/synexa")
```

**Errors:**

```python
from joycaption_api import ModelError, PredictionTimeout

try:
    output = client.run(input)
except ModelError as e:
    print("failed:", e, e.prediction and e.prediction.get("id"))
except PredictionTimeout:
    print("still running — poll later")
```

Status values you will see on a prediction: `starting` → `processing` → `succeeded` | `failed`.

## About JoyCaption

JoyCaption is an image captioning model published by fpgaminer under an open licence with weights on Hugging Face. It was created to fill a gap: existing captioners were either closed, filtered, or wrote short marketing-style text, none of which is useful for training text-to-image models. JoyCaption aims for full coverage of what is in the frame, including content that commercial models refuse, and it offers several fixed output styles: descriptive captions of controllable length, Stable Diffusion style prompts, and booru-style tag lists.

Architecturally it is a standard vision-language model: a SigLIP image encoder feeds a projector into a Llama 3.1 8B language model, fine-tuned on a large captioned corpus. The project went through Pre-Alpha, Alpha One, Alpha Two and Beta One releases, each improving accuracy and instruction following. Outputs are plain text; typical use is one caption per image at a few hundred tokens.

Limits: like every captioner it hallucinates on small text, counts and fine spatial relations, and its fixed modes are tuned for training-data captions rather than conversational Q&A.

The hosted endpoint used by this client is `yorickvp/llava-13b`, which provides the same image-to-text capability; it serves LLaVA 1.5 13B (Haotian Liu and colleagues, 2023), a Vicuna-13B language model with a CLIP ViT-L/14 vision encoder. It is a general instruction-following VLM, so the caption style is controlled by your prompt rather than by JoyCaption's named modes. The original JoyCaption weights are available at https://github.com/fpgaminer/joycaption if you want to self-host.

**Official project:** https://github.com/fpgaminer/joycaption

## Use cases

- **Training-set captions** — loop over a folder of images and call `run({"image": url, "prompt": "Write a detailed, literal description of this image."})` to produce captions for a LoRA or fine-tune.
- **Alt text for a CMS** — generate one-sentence accessible descriptions on upload with `max_tokens=60`.
- **Tag extraction** — prompt for a comma-separated list of objects, styles and colours and index the result for search.
- **Content moderation triage** — ask a yes/no question about the image and route on the answer with `temperature=0`.
- **Product attribute extraction** — describe material, colour and pattern of catalogue photos into structured fields.
- **Bulk backfill** — submit tens of thousands of `wait=False` predictions and collect captions by webhook for about $0.50 per thousand images.

## FAQ

**Is there a JoyCaption API?**

There is no official hosted JoyCaption API; the project ships weights for self-hosting. This client gives you the same image-to-text capability through a hosted VLM endpoint (`yorickvp/llava-13b`) that you call over HTTPS.

**How much does the JoyCaption API cost?**

The hosted `yorickvp/llava-13b` model is $0.0005 per run. Billing is per prediction; there is no hourly GPU charge, so 1,000 captions cost roughly $0.50.

**Can I run JoyCaption without a GPU?**

With this client, yes: inference runs on the hosted service and your code only makes HTTP requests. Self-hosting JoyCaption itself needs a CUDA GPU with enough memory for an 8B language model plus a vision encoder.

**Does this client work with the original JoyCaption repo or ComfyUI?**

No. It does not load the fpgaminer/joycaption checkpoints and it is not a ComfyUI node. It is a network client for the hosted endpoint. To use JoyCaption's exact modes and weights, run the official repository locally.

**What input formats does it accept?**

Two required fields: `image` (a publicly reachable image URL) and `prompt` (the instruction, e.g. a caption request or a question). Optional `max_tokens`, `temperature` and `top_p` control length and randomness. The output is plain text.

**Is this the official JoyCaption SDK?**

No. This is an independent, community-maintained client and is not affiliated with the JoyCaption author. The official project lives at https://github.com/fpgaminer/joycaption.

## Related

- [JoyCaption (official repository)](https://github.com/fpgaminer/joycaption) — model weights, modes and training notes.
- [Synexa Python client](https://github.com/synexa-ai/synexa-python) — the general-purpose client this package wraps.
- [yorickvp/llava-13b](https://synexa.ai/explore/yorickvp/llava-13b) — the hosted LLaVA 1.5 13B endpoint behind this client.

## License

MIT. This is an independent, community-maintained client and is not affiliated with or endorsed by the authors of JoyCaption. Model weights and trademarks belong to their respective owners.

_Last reviewed: 2026-09-22_
