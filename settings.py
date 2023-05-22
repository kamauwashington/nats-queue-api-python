import os
import dotenv

dotenv.load_dotenv()

HOST : str = os.environ.get("HOST") or "localhost"
HOST_PORT : str = os.environ.get("HOST_PORT") or "8000"
SERVER : str = os.environ.get("SERVER") or "localhost"
NATS_SUBJECT : str = os.environ.get("NATS_SUBJECT") or "queue.balancer"
PORT : int = 8000 if not os.environ.get("PORT") else int(os.environ.get("PORT"))
DURATION : float = .100 if not os.environ.get("DURATION") else float(os.environ.get("DURATION"))
NATS_QUEUE_NAME : str = os.environ.get("NATS_QUEUE_NAME") or "nats_default_queue"


