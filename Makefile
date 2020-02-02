
TARGET	=	accounting
DEPS	=	main.py \
			database.py \
			importer.py \
			utility.py

all: $(TARGET)

$(TARGET): $(DEPS)
	pyinstaller -F -n $(TARGET) main.py

clean:
	rm -rf *.spec dist build __pycache__ *.db