from ray import serve
import socket
import os
import asyncio


@serve.deployment(
    ray_actor_options={
        "num_cpus": 1
    },

    autoscaling_config={
        "min_replicas": 1,
        "max_replicas": 10,
        "target_ongoing_requests": 1
    }
)
class Hello:

    def __init__(self):
        self.hostname = socket.gethostname()
        self.pod_ip = os.environ.get("MY_POD_IP", "unknown")

    async def __call__(self):

        # 故意慢一点，方便触发 autoscaling
        await asyncio.sleep(5)

        return (
            f"hello rayserve\n"
            f"host={self.hostname}\n"
            f"pod_ip={self.pod_ip}"
        )


deployment_graph = Hello.bind()
