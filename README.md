- Python 3.12.3

Overview

This project analyzes market data packets received from multiple network providers (feeds) and compares their arrival times.

Each market event is identified by a unique Seqno and is delivered through multiple providers with identical content but different arrival times.
The goal is to determine:

Which provider is fastest per event

Which providers are best overall across all events

-  clone the project first
```bash
git clone https://github.com/imanbakhtiari/reporter.git && cd reporter
```

- install the requirements
```bash
python3 -m venv venv 
source venv/bin/activate
```

```bash
pip install -r requirements.txt
``` 

- and then run the project
```
python3 app.py
```


- swagger ui at http://127.0.0.1:5000/apidocs


- and then for testing the app the full ranking
```
curl http://127.0.0.1:5000/ranking
{
  "best_providers_to_keep": [
    "10.10.10.4",
    "10.10.10.3"
  ],
  "ranking": [
    {
      "average_timestamp": "2016-09-09 09:14:21",
      "fastest_count": 490,
      "provider": "10.10.10.4"
    },
    {
      "average_timestamp": "2016-09-09 09:14:21",
      "fastest_count": 296,
      "provider": "10.10.10.3"
    },
    {
      "average_timestamp": "2016-09-09 09:14:22",
      "fastest_count": 108,
      "provider": "10.10.10.2"
    },
    {
      "average_timestamp": "2016-09-09 09:14:21",
      "fastest_count": 106,
      "provider": "10.10.10.1"
    }
  ]
}
```



- and for each seqno ranking
```
curl http://127.0.0.1:5000/sorting?seqno=6
{
  "average_timestamp": "2016-09-09 09:06:08",
  "fastest_provider": "10.10.10.4",
  "fastest_timestamp": "2016-09-09 09:06:08",
  "seqno": 6,
  "slowest_provider": "10.10.10.1",
  "slowest_timestamp": "2016-09-09 09:06:09",
  "sorted_by_arrival": [
    {
      "provider": "10.10.10.4",
      "timestamp": "2016-09-09 09:06:08"
    },
    {
      "provider": "10.10.10.2",
      "timestamp": "2016-09-09 09:06:08"
    },
    {
      "provider": "10.10.10.3",
      "timestamp": "2016-09-09 09:06:09"
    },
    {
      "provider": "10.10.10.1",
      "timestamp": "2016-09-09 09:06:09"
    }
  ],
  "symbol": "APPL"
}
```
