# TODO

## Phase 1: Web viewer

[ x] Add ability to set --host HOST  and --port PORT this should be below the api section. Default values should be 127.0.0.1 and 8080 respectively.
[ x] Update the central widget so the current UI is in a tab group called Model
[ x] Add another Tab group for Server
[ x] In the server tab group add a QWebEngineView that displays the server from above

## Phase 2 : Context Parameters

[X ] Need to set the context -c parameter this will be the conversation context size, A tool tip should be added to the context combobox to explain what it does.
| Display name | Value passed to `--ctx-size` | Use case |

|---|---:|---|

| Auto (model default) | `0` | Recommended default; uses GGUF model context |

| 2K | `2048` | Very small models / low memory |

| 4K | `4096` | Basic chat, small coding tasks |

| 8K | `8192` | General purpose |

| 16K | `16384` | Better coding/chat history |

| 32K | `32768` | Large files, coding assistants |

| 64K | `65536` | Long documents, repo context |

| 128K | `131072` | Modern long-context models |

[X] need to add the other most common parameters used with llama.cpp such as including tool tips.
| Parameter | Purpose | Typical Value |

|---|---|---|

| `--temp` | Temperature; randomness of token selection | `0.1–0.4` |

| `--top-k` | Restrict to K highest probability tokens | `20–50` |

| `--top-p` | Nucleus sampling probability cutoff | `0.8–0.95` |

| `--min-p` | Remove very unlikely tokens | `0.05–0.1` |

| `--typical-p` | Select tokens near the “typical” probability distribution | `0.9–1.0` |

| `--repeat-penalty` | Penalise repeated tokens | `1.05–1.15` |

| `--repeat-last-n` | How many previous tokens to check for repetition | `64–256` |

| `--presence-penalty` | Penalise tokens that already appeared | `0–0.5` |

| `--frequency-penalty` | Penalise frequent tokens | `0–0.5` |

| `--mirostat` | Adaptive sampling algorithm | Usually off |

| `--mirostat-lr` | Mirostat learning rate | `0.1` |

| `--mirostat-ent` | Target entropy for Mirostat | `5–7` |

## Performance

- [ X] Configure GPU acceleration

  - [ X] Set GPU layer offload

    | Parameter | Purpose | Typical Value |

    |---|---|---|

    | `-ngl` / `--n-gpu-layers` | Number of model layers offloaded to GPU | `99` (full offload if memory allows) |

  - [ X] Configure CPU threading

    | Parameter | Purpose | Typical Value |

    |---|---|---|

    | `-t` / `--threads` | Number of CPU threads used for generation | Number of performance cores or auto |

    | `--threads-batch` | CPU threads used during prompt processing | Higher than generation threads |

  - [ X] Tune batching

    | Parameter | Purpose | Typical Value |

    |---|---|---|

    | `-b` / `--batch-size` | Number of tokens processed per batch | `512–2048` |

    | `-ub` / `--ubatch-size` | Physical micro-batch size | `128–512` |

  - [ X] Configure context size

    | Parameter | Purpose | Typical Value |

    |---|---|---|

    | `-c` / `--ctx-size` | Maximum context window size | `8192–131072` depending on model |

    | `--n-predict` | Maximum tokens generated | `2048–8192` |

  - [ X] Enable attention optimisations

    | Parameter | Purpose | Typical Value |

    |---|---|---|

    | `--flash-attn` | Enable Flash Attention to reduce memory use and improve speed | `on` |

  - [ X] Optimise KV cache

    | Parameter | Purpose | Typical Value |

    |---|---|---|

    | `--cache-type-k` | KV cache key precision | `f16`, `q8_0`, `q4_0` |

    | `--cache-type-v` | KV cache value precision | `f16`, `q8_0`, `q4_0` |

  - [ X] Configure memory handling

    | Parameter | Purpose | Typical Value |

    |---|---|---|

    | `--mmap` | Memory-map model file | Enabled |

    | `--mlock` | Lock model into RAM to prevent swapping | Enable if enough RAM |

  - [ X] Configure server batching

    | Parameter | Purpose | Typical Value |

    |---|---|---|

    | `--cont-batching` | Enable continuous batching for multiple requests | `on` |

    | `--parallel` | Number of concurrent sequences | `1–8+` |

    | `--defrag-thold` | KV cache defragmentation threshold | `0.1–0.5` |

---

# Advanced Generation

- [x] Configure speculative decoding / MTP support

  | Parameter | Purpose | Typical Value |

  |---|---|---|

  | `--draft-model` | Small draft model used for speculative decoding | Smaller compatible model |

  | `--draft-max` | Maximum number of draft tokens | `4–8` |

  | `--draft-min` | Minimum number of draft tokens | `1–2` |

- [ ] Configure adaptive sampling

  | Parameter | Purpose | Typical Value |

  |---|---|---|

  | `--mirostat` | Adaptive sampling algorithm | `0` (off), `1` or `2` (enabled) |

  | `--mirostat-lr` | Mirostat learning rate | `0.1` |

  | `--mirostat-ent` | Target entropy level | `5–7` |

- [ ] Configure deterministic generation

  | Parameter | Purpose | Typical Value |

  |---|---|---|

  | `--seed` | Random seed for reproducible output | Fixed integer (e.g. `42`) |

- [ ] Configure structured output constraints

  | Parameter | Purpose | Typical Value |

  |---|---|---|

  | `--grammar` | Apply grammar constraints to generation | JSON / custom grammar file |

  | `--json-schema` | Force JSON schema compliant output | Schema file |

- [ ] Configure model behaviour

  | Parameter | Purpose | Typical Value |

  |---|---|---|

  | `--rope-scaling` | Extend model context length using RoPE scaling | Model dependent |

  | `--rope-freq-base` | Modify RoPE frequency base | Model dependent |

  | `--rope-freq-scale` | Adjust positional scaling | Model dependent |

## Phase 3 : Testing

[ ] Not test we need to add them with pytest

## Phase 4 : Configuration save and load

[ ] add the ability to save configuration to a json file
[ ] add the ability to load configuration from a json file
[ ] Use QSettings to save/load the last setup

## Phase 5 : exit management

[ ] if the server is running as to quit and stop the server before doing so.

## Phase 6 : exe location

[ ] Add the ability to set the executable location
[ ] Save the executable location in the configuration

## Phase 7 : Optional CLI support 
[ ] Add optional CLI support 
[ ] Create own terminal for the cli in app
