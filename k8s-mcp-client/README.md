# Usage

See `MCP_URL` 

```
python k8s-loop.py gpt-5-mini
```


## K8S MCP Servers Tested

### kubernetes-mcp-server (golang)

See https://github.com/containers/kubernetes-mcp-server

```
mfranz@hp-desktop-g2:~$ ~/kubernetes-mcp-server-linux-amd64 --read-only --port 8000  --log-level 3
I0101 15:19:36.673544 1220913 root.go:280] "Starting kubernetes-mcp-server"
I0101 15:19:36.673574 1220913 root.go:281] " - Config: "
I0101 15:19:36.673582 1220913 root.go:282] " - Toolsets: core, config, helm"
I0101 15:19:36.673589 1220913 root.go:283] " - ListOutput: table"
I0101 15:19:36.673597 1220913 root.go:284] " - Read-only mode: true"
I0101 15:19:36.673605 1220913 root.go:285] " - Disable destructive tools: false"
I0101 15:19:36.673612 1220913 root.go:286] " - Stateless mode: false"
I0101 15:19:36.673620 1220913 root.go:293] " - ClusterProviderStrategy: auto-detect (it is recommended to set this explicitly in your Config)"
I0101 15:19:36.674451 1220913 envvar.go:172] "Feature gate default state" feature="ClientsAllowCBOR" enabled=false
I0101 15:19:36.674494 1220913 envvar.go:172] "Feature gate default state" feature="ClientsPreferCBOR" enabled=false
I0101 15:19:36.674517 1220913 envvar.go:172] "Feature gate default state" feature="InOrderInformers" enabled=true
I0101 15:19:36.674522 1220913 envvar.go:172] "Feature gate default state" feature="InOrderInformersBatchProcess" enabled=true
I0101 15:19:36.674544 1220913 envvar.go:172] "Feature gate default state" feature="InformerResourceVersion" enabled=true
I0101 15:19:36.674548 1220913 envvar.go:172] "Feature gate default state" feature="WatchListClient" enabled=true
I0101 15:19:36.681303 1220913 kubeconfig.go:78] "Started kubeconfig watcher (debounce: 100ms)"
I0101 15:19:36.681340 1220913 cluster.go:89] "Started cluster state watcher (poll interval: 30s, debounce: 5s)"
I0101 15:19:36.681396 1220913 http.go:57] "Streaming and SSE HTTP servers starting on port 8000 and paths /mcp, /sse, /message"
```
