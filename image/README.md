# Runtime

De runtime zorgt ervoor dat de modellen uitgevoerd worden en dat de resultaten teruggestuurd worden naar de control
server.

## File bundle

To execute a model, a folder structure will be created in the executors working directory.

The following structure will be created:

```
├── repository
│   ├── model.pickle
│   ├── requirements.txt
│   └── ...
├── config
│   ├── key.pub
│   ├── key
│   ├── .env
│   └── google_credentials.json
├── Dockerfile
└── run.py
```