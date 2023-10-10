# Rubbrband: Monitoring for Stable Diffusion

Rubbrband detects deformities in your images generated by Stable Diffusion at scale.

## Installation

```bash
pip install rubbrband
```

## Usage

```python
import rubbrband
rubbrband.init("YOUR_API_KEY")
evals = rubbrband.eval("https://example.com/image.png", prompt="Prompt used to generate image")
```

## Uploading Images to Rubbrband

1. Using a URL

```python
evals = rubbrband.eval(image="https://example.com/image.png", prompt="Prompt used to generate image")
```

2. Using a PIL Image

```python
from PIL import Image
evals = rubbrband.eval(image=Image.open("/path/to/image.png"), prompt="Prompt used to generate image")
```

3. Using a path

```python
evals = rubbrband.eval(image="/path/to/image.png", prompt="Prompt used to generate image")
```

4. Using a context manager

```python
with open("/path/to/image.png", "rb") as f:
    evals = rubbrband.eval(image=f, prompt="Prompt used to generate image")
```

## Evaluation features

Rubbrband by default returns the `rating` feature, which returns either `normal` or `deformed`.

Other available features are `["nsfw"]`.

```python
response = rubbrband.eval(
    "https://replicate.delivery/mgxm/85f53415-0dc7-4703-891f-1e6f912119ad/output.png",
    prompt="A woman wearing a strange hat",
    "features": ["nsfw"]
)

is_deformed = response["nsfw_detected"]
```
