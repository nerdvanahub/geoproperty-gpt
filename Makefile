generate:
	python -m grpc_tools.protoc -I./proto --python_out=./service --pyi_out=./service --grpc_python_out=./service ./proto/*.proto

run:
	python -W ignore app.py

test:
	python -m unittest discover -s tests -p '*_test.py'