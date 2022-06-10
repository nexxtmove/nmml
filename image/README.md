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