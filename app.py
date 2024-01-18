import sys
sys.path.insert(0, './service/query_agent')

from service.query_agent.query_agent_server import serve

# Main Function
if __name__ == "__main__":
    serve()


