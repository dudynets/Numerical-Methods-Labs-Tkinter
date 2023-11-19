# Лабораторні роботи з чисельних методів

## Building

1. Install [PyInstaller](https://www.pyinstaller.org/)
    ```bash
    pip install pyinstaller
    ```

2. Build executable
    ```bash
    # MacOS
    pyinstaller --onefile -w src/main.py -n 'Чисельні методи' -i src/assets/icon.icns
    ```
    ```bash
    # Windows
    pyinstaller --onefile -w src/main.py -n 'Чисельні методи' -i src/assets/icon.ico
    ```

3. Run executable from `dist` folder

## Running

1. Install [Python](https://www.python.org/downloads/)

2. Install required packages
    ```bash
    pip install -r requirements.txt
    ```

3. Run the main script
    ```bash
    python src/main.py
    ```