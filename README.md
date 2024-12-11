# 📆 RotinaPy
![Python Version](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white) ![License](https://img.shields.io/badge/License-MIT-green) ![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange) ![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

RotinaPy is an application developed with Streamlit to assist in personal organization and the management of daily routines, study monitoring, flashcards, and more. This project is an evolution of [🤺 LUX](https://www.github.com/silveirinhajuan/LUX), with improved features and planned future integration with it.

## ✨ Features

- **🗓️ Daily Routines**: View and organize your daily tasks according to the days of the week.
- **🤖 Chat with LLMs**: Use language models running locally with Ollama.
- **📊 Study Metrics**: Monitor your academic progress and analyze your performance.
- **📚 Flashcards**: Efficiently review content.
- **🧮 Formula Management**: Integrate formulas for quick and direct study.
- **✅ TO-DO List**: Manage your tasks with a simple and effective list.

## 📂 Project Structure

```
|-csvs
 |  -domingo.csv 
 |  -quarta.csv 
 |  -quinta.csv 
 |  -segunda.csv 
 |  -sexta.csv
 |  -sábado.csv
 |  -terça.csv
|-pages
 |  -Chat.py
 |  -Estudos.py 
 |  -Flashcards.py  
 |  -Fórmulas.py 
 |  -Tarefas.py  
|.gitignore
|LICENSE
|README.md
|Rotina.py
|estudos_tracker.db
|formulas.csv
|pomodoro_tracking.csv
|requirements.txt
|style.css
|tarefas.txt
|utils.py 
|video
 |  -RotinaPy.mp4
```

## 🛠️ Installation

1. Clone the repository:

```bash
$ git clone https://github.com/silveirinhajuan/RotinaPy.git
```

2. Navigate to the project directory:

```bash
$ cd RotinaPy
```

3. Create a virtual environment and activate it:

```bash
$ python -m venv venv
$ source venv/bin/activate # Linux/MacOS
$ venv\Scripts\activate # Windows
```

4. Install the dependencies:

```bash
$ pip install -r requirements.txt
```

5. **Ensure Ollama is installed** and that at least one model is downloaded on your machine. For more information, visit [Ollama's official website](https://ollama.ai/).

6. Run the application:

```bash
$ streamlit run Rotina.py
```

## 🧩 Dependencies

The project's dependencies are listed in the `requirements.txt` file:

- `ollama==0.4.1`
- `pandas==2.0.3`
- `plotly==5.24.1`
- `streamlit==1.40.0`

## 🎥 Demo Video

You can find a demonstration of the project in the following file:

[Video demonstration](./video/RotinaPy.mp4)

## 🤝 Contributing

Contributions are welcome! Feel free to open issues and submit pull requests.

## 📜 License

This project is licensed under the [MIT](./LICENSE) license.

---

Developed with ❤️ by Juan Guerra.
