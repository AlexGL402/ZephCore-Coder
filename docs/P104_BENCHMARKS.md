# P104-100 LLM benchmarks

Measured local Ollama / llama.cpp results on P104-100 systems.

## Overall benchmark table

| System | Model | GPUs | Context | Split | Prompt | Generation | Total | Notes |
|---|---|---:|---:|---|---:|---:|---:|---|
| Huanan | qwen3-coder:30b | 2× P104-100, direct Gen1 ×4 | — | — | 14.51 tok/s | 29.66 tok/s | 22.8 s | Native/direct PCIe links |
| Huanan | qwen3-coder:30b | 2× P104-100, mining riser Gen1 ×1 | — | — | 1.03 tok/s | 9.48 tok/s | 114.3 s | Large PCIe penalty |
| Huanan | qwen3-coder:30b | 3× P104-100 mixed links | 32768 | — | 71.34 tok/s | 37.24 tok/s | 19.04 s | 2 direct + 1 ×1 riser; different prompt workload |
| Huanan | Qwen3.8-27B Q4_K_M | 2× P104-100 direct | 8192 | tensor, ngl=63 | 15.36 tok/s | 10.30 tok/s | 50.91 s | Same 20-token prompt + 512-token generation |
| Huanan | Qwen3.8-27B Q4_K_M | 2× P104-100 direct | 8192 | tensor, ngl=64 | 17.69 tok/s | 11.49 tok/s | 45.62 s | One more GPU layer gives a clear gain |
| Huanan | Qwen3.8-27B Q4_K_M | 2× P104-100 direct | 8192 | tensor, ngl=65 | 20.56 tok/s | 12.53 tok/s | 41.76 s | Best measured Huanan 2×P104 result so far |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 2× P104-100 | 8192 | tensor | 13.43 tok/s | 11.45 tok/s | 46.14 s | Full GPU offload; ~7.77 GiB VRAM/GPU under load |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 2× P104-100 | 8192 | tensor, ngl=63 | 9.61 tok/s | 7.46 tok/s | 70.56 s | Matching partial-offload test against Huanan |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 3× P104-100 | 24576 | tensor | 11.46 tok/s | 11.93 tok/s | 44.56 s | ~5.60–5.65 GiB VRAM/GPU idle after load |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 3× P104-100 | 24576 | layer | 14.95 tok/s | 9.90 tok/s | 52.97 s | Same 20-token prompt + 512-token generation; layer is slower overall |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 3× P104-100 | 32768 | tensor | 11.38 tok/s | 11.93 tok/s | 44.58 s | Same 512-token generation test |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 3× P104-100 | 65536 | tensor | 11.35 tok/s | 11.89 tok/s | 44.72 s | ~6.46–6.55 GiB VRAM/GPU |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 3× P104-100 | 98304 | tensor | 11.17 tok/s | 11.88 tok/s | 44.81 s | ~7.15–7.26 GiB VRAM/GPU |
| AI6 | Qwen3.8-27B-UD-Q4_K_M | 6× P104-100 | 24576 | tensor | 10.45 tok/s | 12.07 tok/s | 44.25 s | ~3.0 GiB VRAM/GPU |

The AI6 rows use the same short benchmark prompt and `n_predict=512`, so the generation numbers are directly useful for 2-vs-3-vs-6 GPU scaling and for tensor-vs-layer comparison at 24K context. The Huanan qwen3-coder rows were measured earlier with different workloads and should not be treated as strict apples-to-apples model comparisons.

## Huanan GPU-layer scaling — 2026-09-16

On 2× P104-100 with 8,192 context and tensor split, increasing GPU layers produced a large and very consistent gain:

| `-ngl` | Prompt | Generation | Total |
|---:|---:|---:|---:|
| 63 | 15.36 tok/s | 10.30 tok/s | 50.91 s |
| 64 | 17.69 tok/s | 11.49 tok/s | 45.62 s |
| 65 | 20.56 tok/s | 12.53 tok/s | 41.76 s |

From `ngl=63` to `ngl=65`, prompt throughput improved by about 34%, generation throughput by about 22%, and total completion time dropped by about 18%. This confirms that even a very small CPU-offload portion has a large cost on this workload, and that maximizing GPU-resident layers is important on P104 systems.

## Huanan vs AI6 matched partial-offload test — 2026-09-16

Both systems were tested with 2× P104-100, 8,192 context, tensor split, `-ngl 63`, the same 20-token prompt, and `n_predict=512`.

| System | Prompt | Generation | Total |
|---|---:|---:|---:|
| Huanan | 15.36 tok/s | 10.30 tok/s | 50.91 s |
| AI6 | 9.61 tok/s | 7.46 tok/s | 70.56 s |

With the matched `-ngl 63` configuration, Huanan was about 60% faster in prompt processing, about 38% faster in token generation, and about 28% faster in total completion time. This is consistent with a substantial platform / PCIe-topology advantage for Huanan in this partial-offload multi-GPU workload. The Huanan model blob and the AI6 UD-Q4_K_M file are both Q4_K_M-class but are not guaranteed to be byte-identical, so this should be treated as a strong platform comparison rather than a perfectly controlled binary-identical model test.

## AI6 tensor vs layer split — 2026-09-16

On 3× P104-100 at 24,576 context, `-sm layer` improved prompt processing from 11.46 to 14.95 tok/s, but reduced generation from 11.93 to 9.90 tok/s and increased total runtime from 44.56 s to 52.97 s. For this Qwen3.8-27B Q4_K_M coding workload, `-sm tensor` is the preferred split mode.

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
