# Model Weights License

The KorvaTTS model weights and voice style files published at [huggingface.co/dogenthq/KorvaTTS](https://huggingface.co/dogenthq/KorvaTTS) are released under the **Apache License 2.0**, the same license as the source code in this repository (see `LICENSE`).

## Provenance

- The weights were **trained from scratch** by dogenthq using our own re-implementation of the Supertonic 3 architecture. No Supertonic checkpoint was loaded, fine-tuned, or distilled. Supertonic's OpenRAIL-M model license therefore does not apply to these weights.
- The vocoder follows the BlueCodec design from [BlueTTS](https://github.com/maxmelichov/BlueTTS) (MIT).
- Training data: [PhoAudiobook](https://huggingface.co/datasets/thivux/phoaudiobook) plus a private Vietnamese/English code-switching corpus collected by the authors. See the dataset page for PhoAudiobook's own terms.

## What you can do

Use, copy, modify, fine-tune, redistribute, and build commercial products — under the standard Apache-2.0 conditions (keep the license and attribution notices; state your changes).

## Responsible use

Only clone or imitate voices you own or have explicit permission to use. Generated speech must not be used to deceive, defraud, harass, or impersonate. Compliance with law and consent from voice owners are your responsibility.

## Future checkpoints

Each checkpoint's model card on Hugging Face states the license that applies to it. Checkpoints from later roadmap phases may be released under different terms.
