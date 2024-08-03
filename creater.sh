#!/bin/bash

echo "    -----------------------------------------------------------"
echo "    Генерация данных, запись в MongoDB и чтения с выводом"
echo "    сustomer: IVL Equipment & Engineering"
echo "    -----------------------------------------------------------"
echo "    author: Старых ЛН"
echo "    e-mail: ln.kornilovstar@gmail.com"
echo "    e-mail: ln.starmark@ekatra.io"
echo "    github: https://github.com/KornilovLN"
echo "    tel:    +380 66 9805661"
echo "    ------------------------------------------------------------"

echo "Выберите действие: "
echo "1) Полная пересборка (с удалением старых контейнеров и созданием новых)"
echo "2) Перезапуск (только перезапуск контейнеров)"
read -p "Введите 1 или 2: " ACTION

# Удаление висячих контейнеров
docker container prune -f

# Удаление висячих образов
docker image prune -f

# Папки проекта
PROJECT_DIR="$(pwd)"
SOURCE_GENERATOR="$PROJECT_DIR/source_generator"
SOURCE_USER="$PROJECT_DIR/source_user"
DATA_GENERATOR="$PROJECT_DIR/datagenerator"
DATA_USER="$PROJECT_DIR/datauser"
PORT_HOST=8989
PORT_CONT=5000

# Функция для проверки и создания папок
create_folder() {
  local folder="$1"
  if [ ! -d "$folder" ]; then
    echo "Create folder $folder"
    mkdir -p "$folder"
  else
    echo "Folder $folder already exists"
  fi
}

copy_files() {
  local src_dir="$1"
  local dest_dir="$2"
  local files=("*.py" "Dockerfile")

  for file in "${files[@]}"; do
    if compgen -G "$src_dir/$file" > /dev/null; then
      echo "Copying $file from $src_dir to $dest_dir"
      cp "$src_dir"/$file "$dest_dir/"
    else
      echo "$file not found in $src_dir"
    fi
  done
}

# Функция для создания Docker сетей
create_network() {
  local network_name="$1"
  if ! docker network ls --filter name="$network_name" --format "{{ .Name }}" | grep -q "$network_name"; then
    echo "Create Docker network $network_name"
    docker network create "$network_name"
  else
    echo "Docker network $network_name already exists"
  fi
}

# Функция для остановки и удаления контейнеров
cleanup_containers() {
  local containers=("data_user" "data_generator" "my_mongo")

  for container in "${containers[@]}"; do
    if docker ps -q --filter name="$container" | grep -q .; then
      echo "Stopping container $container"
      docker stop "$container"
    fi
    if docker ps -a -q --filter name="$container" | grep -q .; then
      echo "Removing container $container"
      docker rm "$container"
    fi
  done
}

# Функция для пересборки и запуска контейнеров
build_and_run() {
  # Создание папок
  create_folder "$DATA_GENERATOR"
  create_folder "$DATA_USER"

  # Копирование файлов
  copy_files "$SOURCE_GENERATOR" "$DATA_GENERATOR"
  copy_files "$SOURCE_USER" "$DATA_USER"

  # Создание Docker сетей
  create_network "net_gen_db"
  create_network "net_db_user"

  # Построение Docker образов
  echo "Building data_generator image..."
  cd "$DATA_GENERATOR" && docker build -t data_generator . && echo "data_generator image built successfully." && cd "$PROJECT_DIR"

  echo "Building data_user image..."
  cd "$DATA_USER" && docker build -t data_user . && echo "data_user image built successfully." && cd "$PROJECT_DIR"


  # Запуск контейнеров
  docker run --name my_mongo \
             --network net_gen_db \
             --network-alias mongo_gen \
             --network net_db_user \
             --network-alias mongo_user \
             -v mongo_data:/data/db \
             -d mongo:latest

  sleep 10 # Ждем, пока MongoDB контейнер запустится

  docker run --name data_generator \
             --network net_gen_db \
             -d data_generator
  sleep 5

  docker run --name data_user \
             --network net_db_user \
             -p $PORT_HOST:$PORT_CONT \
             -d data_user
}

# Функция для перезапуска контейнеров
restart_containers() {
  cleanup_containers
  build_and_run
}

# Выполнение выбранного действия
case $ACTION in
  1)
    build_and_run
    ;;
  2)
    restart_containers
    ;;
  *)
    echo "Неверный выбор. Пожалуйста, введите 1 или 2."
    exit 1
    ;;
esac

# Открытие терминалов для логов (настраивается под вашу ОС)
#gnome-terminal -- docker logs -f data_generator
#gnome-terminal -- docker logs -f data_user

xterm -hold -e "docker logs -f data_generator" &
xterm -hold -e "docker logs -f data_user" &

#gnome-terminal -- bash -c "docker logs -f data_generator"
#gnome-terminal -- bash -c "docker logs -f data_user"

# Открытие терминалов для логов (настраивается под вашу ОС)
#if command -v gnome-terminal &> /dev/null
#then
#    gnome-terminal -- bash -c "docker logs -f data_generator; exec bash" &
#    gnome-terminal -- bash -c "docker logs -f data_user; exec bash" &
#elif command -v xterm &> /dev/null
#then
#    xterm -hold -e "docker logs -f data_generator" &
#    xterm -hold -e "docker logs -f data_user" &
#elif command -v konsole &> /dev/null
#then
#    konsole --noclose -e "docker logs -f data_generator" &
#    konsole --noclose -e "docker logs -f data_user" &
#else
#    echo "Не удалось найти подходящий терминал для вывода логов. Проверьте установленные терминалы."
#fi

echo "Setup complete. Check the new terminal windows for logs."

