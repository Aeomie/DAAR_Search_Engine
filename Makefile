.PHONY: install

install:
	@echo "Checking for Python3..."
	@which python3 > /dev/null || (echo "Python3 not found! Please install it first." && exit 1)
	@echo "Upgrading pip..."
	python3 -m pip install --upgrade pip
	@echo "Installing required Python packages..."
	python3 -m pip install -r requirements.txt
	@echo "Installation complete."
