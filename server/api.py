import os
from fastapi import FastAPI
from pyresparser import ResumeParser
from server.routes import router as ResumeParserRoute

app = FastAPI()
app.include_router(ResumeParserRoute, prefix="/parse")


@app.get("/", tags=["Root"])
async def engine(resume_list: list[dict]):
    json_list = []
    error_list = []

    for resume in resume_list:

        try:
            if resume["fileName"] == "":
                error_list += [f"Resume of index {resume_list.index(resume)} has an empty file name"]
                continue
            else:
                file_name = resume["fileName"]
        except Exception as ex:
            error_list += [f"Resume of index {resume_list.index(resume)} does not have the file name key"
                           f"and {str(ex)}"]
            continue

        try:
            if resume["fileExtension"] == "":
                error_list += [f"Resume of index {resume_list.index(resume)} has an empty file extension"]
                continue
            else:
                file_extension = resume["fileExtension"]
        except Exception as ex:
            error_list += [f"Resume of index {resume_list.index(resume)} does not have the file extension key"
                           f"and {str(ex)}"]
            continue

        try:
            if resume["encodedFile"] == "":
                error_list += [f"Resume of index {resume_list.index(resume)} has an empty base 64 encoded string"]
                continue
            elif b'{encoded_file}' != bytes:
                error_list += [f"Resume of index {resume_list.index(resume)} doesn't have a valid bytes-like object"]
                continue
            else:
                encoded_file = resume["encodedFile"]
        except Exception as ex:
            error_list += [f"Resume of index {resume_list.index(resume)} does not have the encoded file key"
                           f"and {str(ex)}"]
            continue

        try:
            file = open(f"{file_name}{file_extension}", 'wb')
            file.write(encoded_file)
            file.close()

            cv_data = ResumeParser(f"{file_name}{file_extension}").get_extracted_data()
            json_list += [cv_data]
            os.remove(f"{file_name}{file_extension}")
        except Exception as ex:
            error_list += [f"Unable to parse the resume with the index {resume_list.index(resume)}"
                           f"because {str(ex)}"]

    return {
        "cvData": json_list,
        "errorList": error_list
    }
