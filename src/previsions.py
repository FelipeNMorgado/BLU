from ultralytics import YOLO

# Carrega o modelo treinado
model = YOLO("Modelo\\best.pt")

# Faz a previsão
results = model("Fotos-estacionamento")

# Exibe resultado
results[0].show()
for i in range(28):
   results[i].save("results/saida_" + str(i) + ".jpg")