import os
import asyncio
from asyncio import Semaphore
import logging
from models.Real_ESRGAN import process_input

from config import UPLOAD_FOLDER, RESULT_FOLDER, LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

MAX_N_THREADS = 3
DELAY = 5
async def async_process_input(f_path):
    return asyncio.run(process_input(f_path))

async def async_file_delete(f_path):
    return asyncio.run()


async def task_wrapper(semaphore: Semaphore, f_path, *args):
    await semaphore.acquire()
    try:
        #new_f_path = await async_process_input(f_path)
        new_f_path = process_input(f_path)
        logger.info(f'{f_path} processed to {new_f_path}')
        res = os.remove(f_path)
        logger.info(f'{f_path} deleted')
    except Exception as ex:
        pass
    finally:
        semaphore.release()


async def main():
    while True:
        img_list = os.listdir(UPLOAD_FOLDER)
        if len(img_list) == 0:
            await asyncio.sleep(DELAY)
            continue
        max_threads_nbr = min(MAX_N_THREADS, len(img_list))

        semaphore = Semaphore(max_threads_nbr)
        tasks = []
        for f_name in img_list:
            f_path = os.path.join(UPLOAD_FOLDER, f_name)
            #await asyncio.create_task(task_wrapper(semaphore, f_path))
            task = asyncio.create_task(task_wrapper(semaphore, f_path))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())