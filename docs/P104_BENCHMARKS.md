# P104-100 LLM benchmarks

Measured local Ollama / llama.cpp results on P104-100 systems.

## Overall benchmark table

| System | Model | GPUs | Context | Prompt | Generation | Total | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| Huanan | qwen3-coder:30b | 2× P104-100, direct Gen1 ×4 | — | 14.51 tok/s | 29.66 tok/s | 22.8 s | Native/direct PCIe links |
| Huanan | qwen3-coder:30b | 2× P104-100, mining riser Gen1 ×1 | — | 1.03 tok/s | 9.48 tok/s | 114.3 s | Large PCIe penalty |
| Huanan | qwen3-coder:30b | 3× P104-100 mixed links | 32768 | 71.34 tok/s | 37.24 tok/s | 19.04 s | 2 direct + 1 ×1 riser; different prompt workload |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 2× P104-100 | 8192 | 13.43 tok/s | 11.45 tok/s | 46.14 s | ~7.77 GiB VRAM/GPU under load |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 3× P104-100 | 24576 | 11.46 tok/s | 11.93 tok/s | 44.56 s | ~5.60–5.65 GiB VRAM/GPU idle after load |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 3× P104-100 | 32768 | 11.38 tok/s | 11.93 tok/s | 44.58 s | Same 512-token generation test |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 3× P104-100 | 65536 | 11.35 tok/s | 11.89 tok/s | 44.72 s | ~6.46–6.55 GiB VRAM/GPU |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 3× P104-100 | 98304 | 11.17 tok/s | 11.88 tok/s | 44.81 s | ~7.15–7.26 GiB VRAM/GPU |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 6× P104-100 | 24576 | 10.45 tok/s | 12.07 tok/s | 44.25 s | ~3.0 GiB VRAM/GPU |

The AI6 rows use the same short benchmark prompt and `n_predict=512`, so the generation numbers are directly useful for 2-vs-3-vs-6 GPU scaling. The Huanan rows were measured earlier with different workloads and should not be treated as strict apples-to-apples model comparisons.

## AI6 3+3 parallel serving test — 2026-09-16

Two independent `llama-server` instances were run simultaneously:

- GPU 0,1,2: Qwen3.8-27B Q4_K_M, 65,536 context, port 8096.
- GPU 3,4,5: Qwen3.8-27B Q4_K_M, 98,304 context, port 8097.

| Worker | GPUs | Context | Generation | Prompt | VRAM/GPU |
|---|---|---:|---:|---:|---:|
| 8096 | 0,1,2 | 65536 | 12.01 tok/s | 11.36 tok/s | ~6.46–6.55 GiB |
| 8097 | 3,4,5 | 98304 | 11.95 tok/s | 6.33 tok/s* | ~7.15–7.26 GiB |
| Combined | 6 GPUs as 3+3 | mixed | **23.96 tok/s** | — | ~41 GiB total |

\*The 8097 prompt sample was only 18 tokens and is not comparable to the standard short-prompt measurements. A later cached request reused the LCP and should also not be used as a prompt-throughput benchmark.

During simultaneous generation all six GPUs were ~96–97% loaded and the AI6 monitor showed about **656.5 W total GPU power**. The key result is that two 3-GPU workers preserve roughly 12 tok/s each, while one 6-GPU worker only reaches about 12.07 tok/s. For concurrent coding-agent work, 3+3 therefore provides roughly double the aggregate generation throughput.

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

P104-100 cards in the Huanan test platform report/use a native Gen1 ×4-class link. For a six-GPU build, the design target is therefore six independent ×4 links (24 lanes total), rather than mining-style ×1 links. x8/x16 per P104 is not required unless a separate PCIe-link modification proves useful.

For the current AI6 Qwen3.8-27B Q4_K_M workload, adding GPUs to a single tensor-split instance scales poorly: 2 GPUs measured 11.45 tok/s, 3 GPUs 11.93 tok/s, and 6 GPUs 12.07 tok/s. The six-card rig is therefore more useful as two independent 3-GPU inference workers than as one 6-GPU worker for this model.