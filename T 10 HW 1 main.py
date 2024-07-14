import asyncio
import aiofiles
import aiopath
import argparse
import logging
from aiopath import AsyncPath
# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
async def copy_file(source: AsyncPath, dest: AsyncPath):
    try:
        await dest.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(source, mode='rb') as src, aiofiles.open(dest, mode='wb') as dst:
            await dst.write(await src.read())
        logging.info(f"Скопійовано: {source} -> {dest}")
    except Exception as e:
        logging.error(f"Помилка при копіюванні {source}: {str(e)}")
async def read_folder(source: AsyncPath, dest: AsyncPath):
    try:
        async for entry in source.iterdir():
            if await entry.is_file():
                extension = entry.suffix.lower()[1:]  # Отримуємо розширення без крапки
                if not extension:
                    extension = "no_extension"
                output_dir = dest / extension
                await copy_file(entry, output_dir / entry.name)
            elif await entry.is_dir():
                await read_folder(entry, dest)
    except Exception as e:
        logging.error(f"Помилка при читанні папки {source}: {str(e)}")
async def main(source_folder: str, output_folder: str):
    source = AsyncPath(source_folder)
    dest = AsyncPath(output_folder)
    if not await source.exists():
        logging.error(f"Вихідна папка {source} не існує")
        return
    await dest.mkdir(parents=True, exist_ok=True)
    await read_folder(source, dest)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням")
    parser.add_argument("source", help="Шлях до вихідної папки")
    parser.add_argument("output", help="Шлях до папки призначення")
    args = parser.parse_args()
    asyncio.run(main(args.source, args.output))



Щоб запустити скрипт, використовуйте команду:

python script_name.py /шлях/до/вихідної/папки /шлях/до/папки/призначення 

