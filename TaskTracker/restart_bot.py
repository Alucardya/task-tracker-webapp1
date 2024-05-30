import subprocess
import time

while True:
    # Запуск бота
    process = subprocess.Popen(["python", "bot.py"])
    # Ожидание завершения процесса
    process.wait()
    # Пауза перед перезапуском
    time.sleep(5)
    print("Перезапуск бота...")
