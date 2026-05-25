from pathlib import Path
from ultralytics import YOLO
from minio_client import upload

BUCKET = "blu-treino"

def on_epoch_end(trainer):
    epoch = trainer.epoch
    save_dir = Path(trainer.save_dir)

    # Envia o último peso para garantir um checkpoint de recuperação
    last_pt = save_dir / "weights" / "last.pt"
    if last_pt.exists():
        upload(str(last_pt), BUCKET, f"epochs/epoch_{epoch:04d}_last.pt")

def on_train_end(trainer):
    save_dir = Path(trainer.save_dir)

    print("📤 Iniciando envio dos artefatos finais para o MinIO...")

    # 1. Envia o MELHOR modelo e o ÚLTIMO modelo definitivo (.pt)
    best_pt = save_dir / "weights" / "best.pt"
    if best_pt.exists():
        upload(str(best_pt), BUCKET, "pesos/best.pt")
        
    last_pt = save_dir / "weights" / "last.pt"
    if last_pt.exists():
        upload(str(last_pt), BUCKET, "pesos/last.pt")

    # 2. Envia metadados e gráficos gerados pelo YOLO
    # Adicionei os gráficos (png) que o YOLO gera automaticamente e que são ótimos para o orientador ver
    arquivos_para_enviar = [
        "results.csv", 
        "args.yaml", 
        "results.png", 
        "confusion_matrix.png"
    ]
    
    for arquivo in arquivos_para_enviar:
        p = save_dir / arquivo
        if p.exists():
            upload(str(p), BUCKET, f"resultados/{arquivo}")

    print("🎉 Treino concluído! Todos os artefatos salvos com segurança no MinIO.")

if __name__ == "__main__":
    model = YOLO("yolov8n.pt")
    
    # IMPORTANTE: O callback correto para o final da época de treino é "on_train_epoch_end"
    model.add_callback("on_train_epoch_end", on_epoch_end)
    model.add_callback("on_train_end", on_train_end)

    model.train(
        data="data.yaml",
        epochs=11,
        imgsz=640,
        project="runs/blu",
        name="v1"
    )