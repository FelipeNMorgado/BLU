import os
from pathlib import Path
from dotenv import load_dotenv
import torch
import mlflow
from ultralytics import YOLO
from minio_client import upload

# Carrega as variáveis do .env
load_dotenv()

BUCKET = "blu-treino"
CONF_THRESHOLD = 0.35

def on_epoch_end(trainer):
    """Backup de segurança a cada 5 épocas no MinIO"""
    epoch = trainer.epoch
    if epoch % 5 == 0:
        save_dir = Path(trainer.save_dir)
        last_pt = save_dir / "weights" / "last.pt"
        if last_pt.exists():
            upload(str(last_pt), BUCKET, f"epochs/epoch_{epoch:04d}_last.pt")

def on_train_end(trainer):
    """MANTIDO E MELHORADO: Envia todos os artefatos finais para o MinIO e MLflow"""
    save_dir = Path(trainer.save_dir)
    print("📤 Iniciando envio dos artefatos finais para o MinIO e MLflow...")

    best_pt = save_dir / "weights" / "best.pt"
    last_pt = save_dir / "weights" / "last.pt"

    # 1. Envia os pesos para a sua estrutura original no MinIO
    if best_pt.exists():
        upload(str(best_pt), BUCKET, "pesos/best.pt")
        # Novidade: Também registra o melhor peso dentro do MLflow
        mlflow.log_artifact(str(best_pt), artifact_path="pesos")

    if last_pt.exists():
        upload(str(last_pt), BUCKET, "pesos/last.pt")
        mlflow.log_artifact(str(last_pt), artifact_path="pesos")

    # 2. Envia os relatórios e gráficos para o MinIO e MLflow
    arquivos_para_enviar = [
        "results.csv",
        "args.yaml",
        "results.png",
        "confusion_matrix.png",
        "confusion_matrix_normalized.png",
    ]

    for arquivo in arquivos_para_enviar:
        p = save_dir / arquivo
        if p.exists():
            # Mantém seu envio direto para a pasta 'resultados/' no MinIO
            upload(str(p), BUCKET, f"resultados/{arquivo}")
            # Também guarda no histórico do experimento atual do MLflow
            mlflow.log_artifact(str(p), artifact_path="resultados")

    print("🎉 Todos os artefatos salvos com segurança no MinIO e MLflow!")

if __name__ == "__main__":
    # Configuração do MLflow
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("YOLOv8_Vagas_MinIO")
    os.environ["MLFLOW_ARTIFACT_URI"] = f"s3://{BUCKET}/mlflow_artifacts"

    model = YOLO("yolov8n.pt")
    
    print(f"CUDA Disponível: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    # REGISTRANDO OS DOIS CALLBACKS NOVAMENTE 
    model.add_callback("on_train_epoch_end", on_epoch_end)
    model.add_callback("on_train_end", on_train_end)

    # Inicia o treino dentro do gerenciador de contexto do MLflow
    with mlflow.start_run(run_name="v1_conf_0.35"):
        model.train(
            data="data.yaml",
            epochs=20,
            imgsz=640,
            project="runs/blu",
            name="v1",
            device=0,
            workers=0,
            conf=CONF_THRESHOLD,
        )