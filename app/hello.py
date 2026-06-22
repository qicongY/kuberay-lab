from ray import serve
import socket
import os
import time

@serve.deployment(
    autoscaling_config={
        "min_replicas":1,
        "max_replicas":10,
        "target_ongoing_requests":2
    }
)

class Hello:
    def __init__(self):
        # 缓存主机名，避免每次请求都调用系统函数
        self.hostname = socket.gethostname()
        # 如果需要具体的 Pod IP，可以通过环境变量获取
        self.pod_ip = os.environ.get("MY_POD_IP", "unknown")

    async def __call__(self):
            time.sleep(5)
            return f"hello rayserve:v2, running on host: {self.hostname}, pod_ip: {self.pod_ip}"

deployment_graph = Hello.bind()
