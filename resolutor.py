import os
import asyncio
from asyncio import Semaphore
import logging
from models.Real_ESRGAN import process_input
from aiofiles.os import remove, listdir

from config import UPLOAD_FOLDER, RESULT_FOLDER, LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

MAX_N_THREADS = 3
DELAY = 5

async def task_wrapper(semaphore: Semaphore, f_path, *args):
    await semaphore.acquire()
    try:
        # new_f_path = await async_process_input(f_path)
        new_f_path = process_input(f_path)
        # TODO check file size and raise exception if > 10Mb/4 (tg limit 10Mb - will not be send)
        # TODO
        logger.info(f'{f_path} processed to {new_f_path}')
        await remove(f_path)
        logger.info(f'{f_path} deleted')
    except Exception as ex:
        logger.info(f'exc: {ex}')
        pass
    finally:
        semaphore.release()


async def main():
    logger.info('resolutor starting')
    semaphore = Semaphore(MAX_N_THREADS)
    while True:
        img_list = sorted(await listdir(UPLOAD_FOLDER))
        if len(img_list) == 0:
            #logger.info(f'delay {DELAY}')
            await asyncio.sleep(DELAY)
            continue
        max_threads_nbr = min(MAX_N_THREADS, len(img_list))
        tasks = []
        logger.info(f'start processing list: {img_list[:max_threads_nbr]}, {len(img_list)} images in queue')
        for f_name in img_list[:max_threads_nbr]:
            f_path = os.path.join(UPLOAD_FOLDER, f_name)
            task = asyncio.create_task(task_wrapper(semaphore, f_path))
            tasks.append(task)

        await asyncio.gather(*tasks)
        logger.info(f'finish processing list: {img_list[:max_threads_nbr]}')


if __name__ == "__main__":

    asyncio.run(main())


'''
import asyncio
from asyncio import Semaphore
#from concurrent.futures import ThreadPoolExecutor

async def process_image(f_path):
    logger.info(f'process {f_path}')
    res_f_name = await async_process_input(f_path)


async def check_images(img_path: str = RESULT_FOLDER) -> None:
    MAX_N_THREADS = 3
    while True:
        img_list = os.listdir(img_path)
        if len(img_list)==0:
            await asyncio.sleep(5)
        n_threads = min(MAX_N_THREADS, len(img_list))
        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            f_path = [os.path.join(img_path, img_list[i])]
            executor.map(process_image,f_path)
'''
