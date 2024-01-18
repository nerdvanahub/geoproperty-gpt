import grpc
import pyfiglet
from concurrent import futures
import time
from config.database_config import get_connection
from service.query_agent.query_agent_pb2 import Response
from service.query_agent.query_agent_pb2_grpc import PromptServiceServicer, add_PromptServiceServicer_to_server

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_sql_query_chain
from langchain.sql_database import SQLDatabase
import re
from dotenv import load_dotenv
load_dotenv()

PG_URI = get_connection()

llm = ChatGoogleGenerativeAI(model="models/gemini-pro")
db = SQLDatabase.from_uri(PG_URI)
chain = create_sql_query_chain(llm, db)

class PromptServiceServicer(PromptServiceServicer):
    def GetQuery(self, request, context):
        response = Response()
        prompt = request.prompt.lower() + " di table property dan pilih kolom id saja dan batasi 100 data."

        # log prompt
        print("Propmpt : ", prompt)

        response.response = chain.invoke({"question":prompt})

        # clean markdown sql and remove unnecessary characters
        match = re.search(r'```sql(.*?)```', response.response, re.DOTALL)
        
        if match:
            sql_code = match.group(1).strip()
            response.response = sql_code[:-1].strip()
            
            # remove enter and new line
            response.response = response.response.replace('\n', ' ')

            # log response
            print("Response : ", response.response)

            return response
        
        return None


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PromptServiceServicer_to_server(PromptServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started at 50051")

    banner = pyfiglet.figlet_format("Geoproperty GPT")
    print(banner)

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)