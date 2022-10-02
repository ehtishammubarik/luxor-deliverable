# LLuxor-deliverable
Create a CRD and implement Operator to create and monitor Kubernetes resources.

# Pre-reqs 
### k8s access 
### operator-sdk installed
### available registry
## Note for Images
1. To build required images go to <applications> dir and build server image. 
2. update image registry, bearer token for cluster in helm-charts/demo/values.yaml files.
3. updated IMG_TAG_BASE in Makefile


# To build and deploy controler and CRD
```
make docker-build docker-push
make deploy
kubectl get deployment -n nginx-operator-system
```
# To create CR
edit to <config/samples/eval_v1alpha1_demo.yaml>

```
kubectl apply -f config/samples/eval_v1alpha1_demo.yaml
kubectl get pods

```
Perform any modifications in <config/samples/eval_v1alpha1_demo.yaml> and redeploy to verify changes.

# For cronjob 
to create a ping call for every pod 
```
kubectl apply -f application/cronjob.yaml
```

# CRD Resource name
demo

## Endpoints 
/ping/ /scheduler/  /pods/


