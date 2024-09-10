#!/bin/bash
docker run -d --name rmt_data_user \
  -p 5000:5000 \
  -e MONGO_URI="mongodb://gitlab.ivl.ua:27017" \
  data-user-img

# Применять только при включенном контроле доступа
# -e MONGO_URI="mongodb://starmark:!18star28@gitlab.ivl.ua:27017" \   