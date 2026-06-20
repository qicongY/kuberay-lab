from ray import serve
import socket
import os

@serve.deployment(num_replicas=1)
class Hello:
    def __init__(self):
        # 缓存主机名，避免每次请求都调用系统函数
        self.hostname = socket.gethostname()
        # 如果需要具体的 Pod IP，可以通过环境变量获取
        self.pod_ip = os.environ.get("MY_POD_IP", "unknown")

    def __call__(self):
        return f"hello rayserve, running on host: {self.hostname}, pod_ip: {self.pod_ip}"

deployment_graph = Hello.bind()
