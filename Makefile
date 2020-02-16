
TARGET	=	accounting
DEPS	=	main.py \
			database.py \
			dialogs.py \
			importer.py \
			utility.py \
			notebk.py \
			events.py \
			form_widgets.py \
			setup_form.py \
			setup_notebook.py \
			import_form.py \
			contact_form.py

all: $(TARGET)

$(TARGET): $(DEPS)
	pyinstaller -F -n $(TARGET) main.py

clean:
	rm -rf *.spec dist build __pycache__ *.db