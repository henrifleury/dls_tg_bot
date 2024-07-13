import os
import asyncio
import logging
import requests

from asyncio import Semaphore
from aiofiles.os import remove, listdir
from environs import Env
from config import RESULT_FOLDER, API_URL, LOG_LEVEL
from config import SENDER_MAX_N_THREADS as MAX_N_THREADS
from config import SENDER_DELAY as DELAY


logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")


async def task_wrapper(semaphore: Semaphore, f_path, *args):
    await semaphore.acquire()
    try:
        f_name = f_path.split(os.sep)[-1]
        (_, message_id, chat_id) = f_name.split("_")[:3]

        # TODO check file size and raise exception if > 10Mb
        #  (tg limit 10Mb - will not be send)

        data = {"chat_id": chat_id, "caption": "enhanced photo"}
        url = f"{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}"
        with open(f_path, "rb") as img_f:
            # res =
            requests.post(url, data=data, files={"photo": img_f})
        # TODO check res.json() and raise exception if something wrong
        logger.info(
            f"{f_name} send to chat: {chat_id}, "
            f"as reply to message: {message_id}"
        )
        await remove(f_path)
        logger.info(f"{f_path} deleted")
    except Exception as ex:
        logger.error(f"exc: {ex}")
        if os.path.isfile(f_path):
            await remove(f_path)
            logger.error(f"{f_path} deleted by exception")
            semaphore.release()
    finally:
        semaphore.release()


async def main(
    img_dir=RESULT_FOLDER,
    max_n_threads=MAX_N_THREADS,
    wrapper=task_wrapper,
    delay=DELAY,
):
    logger.info(f"{__name__} startung")
    semaphore = Semaphore(max_n_threads)
    while True:
        img_list = sorted(await listdir(img_dir))
        if len(img_list) == 0:
            await asyncio.sleep(delay)
            continue
        threads_nbr = min(MAX_N_THREADS, len(img_list))
        tasks = []
        logger.info(
            f"start processing list: {img_list[:threads_nbr]}, "
            f"{len(img_list)} images in queue"
        )
        for f_name in img_list[:threads_nbr]:
            f_path = os.path.join(img_dir, f_name)
            task = asyncio.create_task(wrapper(semaphore, f_path))
            tasks.append(task)

        await asyncio.gather(*tasks)
        logger.info(f"finish processing list: {img_list[:threads_nbr]}")


if __name__ == "__main__":
    asyncio.run(main())
