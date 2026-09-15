# P104-100 LLM benchmarks

Measured local Ollama / Qwen3-Coder results for the Huanan test system.

## PCIe link comparison — 2× P104-100

Same `qwen3-coder:30b` model on the same two P104-100 cards.

| Configuration | Prompt | Generation | Total |
|---|---:|---:|---:|
| Direct, Gen1 ×4 | 14.51 tok/s | 29.66 tok/s | 22.8 s |
| Chinese mining riser, Gen1 ×1 | 1.03 tok/s | 9.48 tok/s | 114.3 s |
| Slowdown / loss | ~14× slower prompt | ~3.1× slower generation | ~5× longer |

Conclusion: PCIe Gen1 ×1 mining risers cause a major performance loss for this multi-GPU LLM workload. Future multi-P104 hardware should target at least the native Gen1 ×4 link per GPU.

## 3× P104-100 mixed-link test

Physical configuration:
- P104 #1: direct/native link
- P104 #2: direct/native link
- P104 #3: Chinese mining riser (×1)

Ollama runner reported three CUDA devices.

| Model | Prompt | Generation | Total | Context setting | Runner VRAM |
|---|---:|---:|---:|---:|---:|
| qwen3-coder:30b | 71.34 tok/s | 37.24 tok/s | 19.04 s | 32768 | 20.2 GiB |

The prompt workload differs from the earlier 2-GPU comparison, so prompt rates should not be compared as a strict scaling benchmark. The generation result is retained as a useful measured reference.

## Hardware implication

P104-100 cards in this test platform report/use a native Gen1 ×4-class link. For a six-GPU build, the design target is therefore six independent ×4 links (24 lanes total), rather than mining-style ×1 links. x8/x16 per P104 is not required unless a separate PCIe-link modification proves useful.
