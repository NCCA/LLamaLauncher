# TODO

## Phase 1: Web viewer

[ x] Add ability to set --host HOST  and --port PORT this should be below the api section. Default values should be 127.0.0.1 and 8080 respectively.
[ x] Update the central widget so the current UI is in a tab group called Model
[ x] Add another Tab group for Server
[ x] In the server tab group add a QWebEngineView that displays the server from above

## Phase 2 : Context Parameters

[ ] Need to set the context -c parameter this will be the conversation context size, A tool tip should be added to the context combobox to explain what it does.
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

[] need to add the other most common parameters used with llama.cpp such as including tool tips.
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
