from openai import AsyncOpenAI

from logger import logger

errors_dict = {
    "The file could not be parsed because it is empty.": "Документ не читаемый. Попробуйте сделать OCR и загрузить снова"
}


class IncorrectFilesException(Exception):
    """Exception raised when files are in an incorrect format or state.

    Attributes:
        files -- list of problematic files
        message -- explanation of the error
    """

    def __init__(self, files_ids: list[str], errors: list[tuple[str, str]], message="Некорректные файлы"):
        self.files = [(filename, errors_dict.get(error, error)) for filename, error in errors]
        self.message = message
        self.files_ids = files_ids
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {', '.join(f"{filename}: {error}" for filename, error in self.files)}"


async def create_vector_store(client: AsyncOpenAI) -> str:
    vector_store = await client.vector_stores.create(
        name="AI_funds_application",
    )
    return vector_store.id


async def add_files(client: AsyncOpenAI, vector_store_id: str, files: list[str]) -> list[str]:
    errors = []
    files_ids = []
    for file in files:
        with open(file, "rb") as f:
            file_content = (file.split("/")[-1], f.read())
        try:
            file_response = await client.vector_stores.files.upload_and_poll(vector_store_id=vector_store_id,
                                                                             file=file_content)
        except Exception as e:
            errors.append((file, e))
        else:
            files_ids.append(file_response.id)
            if file_response.status == "failed":
                errors.append((file, file_response.last_error.message))
    if errors:
        raise IncorrectFilesException(files_ids, errors)
    return files_ids


async def delete_files(client: AsyncOpenAI, files_ids: list[str]) -> None:
    for file_id in files_ids:
        try:
            await client.files.delete(file_id)
        except:
            continue


async def delete_vector_store(client: AsyncOpenAI, vector_store_id: str):
    try:
        await client.vector_stores.delete(vector_store_id=vector_store_id)
    except:
        pass


async def clear_openai_storage(client: AsyncOpenAI, files_ids, vector_store_id):
    if files_ids:
        await delete_files(client, files_ids)
        logger.info("files deleted")
    if vector_store_id:
        await delete_vector_store(client, vector_store_id)
        logger.info("vector store deleted")
