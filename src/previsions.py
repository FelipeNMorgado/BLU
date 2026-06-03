from ultralytics import YOLO

# Carrega o modelo treinado
model = YOLO("runs/detect/runs/blu/v1-3/weights/best.pt")

# Faz a previsão
results = model("dataset/previsions")

# Exibe resultado
results[0].show()
for i in range(28):
   results[i].save("dataset/results/saida_" + str(i) + ".jpg")
