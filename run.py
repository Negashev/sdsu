import asyncio
import os

import aiodocker
from aiodocker.exceptions import DockerError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

image = os.getenv('SERVICE_IMAGE', None)
service_id = os.getenv('SERVICE_ID', None)


async def upgrade_service():
    print("Connect to Docker")
    docker = aiodocker.Docker()
    try:
        print(f"Get inspect for service {service_id}")
        inspect = await docker.services.inspect(
            service_id=service_id
        )
        try:
            image_data = await docker.images.get(image)
        except DockerError as e:
            if e.status == 404:
                print(f"Pull image {image}")
                await docker.pull(image)
                image_data = await docker.images.get(image)
            else:
                print(f'Error retrieving {image} image.')
                await docker.close()
                return
        print(f"Upgrade service {service_id} with image {image_data['RepoDigests'][0]}")
        update = await docker.services.update(
            service_id=service_id,
            version=inspect['Version']['Index'],
            image=image_data['RepoDigests'][0]
        )
        if update:
            print(f"Service {service_id} success update")
        else:
            print(f"Service {service_id} fail update")
    except Exception as e:
        print(e)
    print("Close connection to Docker")
    await docker.close()


if __name__ == '__main__':
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(upgrade_service, 'interval', seconds=int(os.getenv('SERVICE_INTERVAL_UPGRADE', 3600)),
                      max_instances=1)
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
