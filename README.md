# financial_summary_2
App that helps mi keep track of my spending

## Build and run
```sh
    cd financial_summary_2
    docker build . --tag financial_summary_scheduler
    docker compose -f docker-compose.yaml -f production.yaml up
```

## Test
``` sh 
    cd financial_summary_2
    python -m unittest discover test
```

## Tools
### Generate agreement
```sh
    cd financial_summary_2
    python -m tools.generate_agreement
```
### Clear requisitions
```sh
    cd financial_summary_2
    python -m tools.clear_requisitions
```