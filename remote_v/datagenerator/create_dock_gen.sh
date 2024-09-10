#!/bin/bash
docker run -d --name rmt_data_generator \
  --network host \
  -e MONGO_URI="mongodb://gitlab.ivl.ua:27017" \
  data-generator-img

# Применять только при включенном контроле доступа
# -e MONGO_URI="mongodb://starmark:!18star28@gitlab.ivl.ua:27017" \  
