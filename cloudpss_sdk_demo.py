SDK_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjQ5NiwidXNlcm5hbWUiOiJTdGV2ZW4wMTI4Iiwic2NvcGVzIjpbXSwidHlwZSI6ImFwcGx5IiwiZXhwIjoxNzEwMzg4NjQ3LCJpYXQiOjE2NzkyODQ2NDd9.bn-opCnMyy7Fgj8oIKPdeyaUTvcTxNLgdmC4TUv-MEigA6xiStlAJrsdOOpUDTB_ccH1ERIs292gUjLaXnLt9ZJ4ncrCeq0Pf_nTsSHWYXwDXjZU4xhJ66zk917N0Cr-cEiiLU-iHBZhmovhg6RHnfGKMoToALWqszHbMXDGlcQ'


"""

# Plan on creating APIs for algo services

- [create openapi doc annotation](https://fastapi.tiangolo.com/tutorial/schema-extra-example/) with fastapi
- use [BackgroundTasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) or [celery](https://docs.celeryq.dev/en/stable/userguide/tasks.html) (check [fastapi-celery](https://github.com/GregaVrbancic/fastapi-celery/blob/master/app/main.py)) to handle comp intensive tasks
- [investigate cloudpss sdk](https://docs.cloudpss.net/sdk/instruction_manual/guide) to design the overall APIs

"""

import cloudpss

# cloudpss.ModelTopology