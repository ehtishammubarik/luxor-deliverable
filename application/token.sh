while ! kubectl describe secret crontab-sample-token-kcgb4 | grep -E '^token' >/dev/null; do
  echo "waiting for token..." >&2
  sleep 1
done
TOKEN=$(kubectl get secret crontab-sample-token-kcgb4 -o jsonpath='{.data.token}' | base64 --decode)

echo $TOKEN 


#works inside pod
#token.sa == $TOKEN
bearer="kubeconfig-u-ncgcgk4kk4:ghv45lhwnw52gdqzndd8n5q8rwwsp9mjvxwv8rfk8ltv4dnn5z8jts"
ips=$(curl -k -H "Authorization: Bearer $bearer" https://login.rcluster.aceso.no:9091/k8s/clusters/c-8cnzq/api/v1/namespaces/default/pods | jq '.items[] | .status.podIP')
echo $ips
#> pod_details.jsonpath