import os
import subprocess

def run_rq_worker():
    # Load environment variables if .env file exists
    if os.path.exists('.env'):
        print("Loading .env file")
        with open('.env') as f:
            for line in f:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
    else:
        print("No .env file")

    # Make sure the DATABASE_URL is set
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print(f"Using DATABASE_URL: {database_url}")
    else:
        raise ValueError("DATABASE_URL not set")

    # Run alembic upgrade
    subprocess.run(["python", "-m", "alembic", "upgrade", "head"], check=True)

    # Set default RQ_POOL_SIZE if not set
    rq_pool_size = os.getenv('RQ_POOL_SIZE', '5')
    print(f"RQ_POOL_SIZE: {rq_pool_size}")

    # Set the queues if not set
    queues = os.getenv('QUEUES', 'load-xml')
    print(f"QUEUES: {queues}")

    # Run the RQ worker
    command = [
        "rq", "worker-pool",
        "-n", rq_pool_size,
        "-u", os.getenv('REDIS_URL'),
        "-w", "app.worker.AppWorker",
        queues
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    run_rq_worker()
