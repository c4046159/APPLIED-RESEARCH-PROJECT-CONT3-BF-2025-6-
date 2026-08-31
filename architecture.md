# Architecture

```text
                         +----------------------+
                         |  Streamlit interface |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | normalized prompting |
                         +----------+-----------+
                                    |
               +--------------------+--------------------+
               |                    |                    |
               v                    v                    v
        +-------------+      +-------------+      +--------------+
        | Gemini API  |      | GroqCloud   |      | OpenRouter   |
        | Gemini 3.1  |      | GPT-OSS120B |      | Nemotron 3   |
        +------+------+      +------+------+      +------+-------+
               |                    |                    |
               +--------------------+--------------------+
                                    |
                                    v
                         +----------------------+
                         | unified run metadata |
                         | latency/tokens/errors|
                         +----------+-----------+
                                    |
                         +----------+-----------+
                         | CSV + JSONL raw logs |
                         +----------------------+
```

The benchmark runner bypasses the UI but calls the same `engine.run_bot()` function,
so interactive tests and formal evaluation use the same provider adapters and logging path.
