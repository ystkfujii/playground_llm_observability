

portkey config

```json
{
  "strategy": {
    "mode": "loadbalance"
  },
  "targets": [
    {
      "virtual_key": "cohere-XXXXX",
      "override_params": {
        "model": "command-r"
      },
      "weight": 0.5
    },
    {
      "virtual_key": "open-ai-virtual-XXXX",
      "override_params": {
        "model": "gpt-4o-mini"
      },
      "weight": 0.5
    }
  ],
  "retry": {
    "attempts": 3
  },
  "cache": {
    "mode": "simple",
    "max_age": 60
  }
}
```
