
```shell
helm upgrade status-page \
  --install . \
  --namespace status-page \
  --create-namespace \
  -f values.yaml
```