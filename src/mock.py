import sys
import json
import os
from ultralytics import YOLO

def main():
    # ---- MODO DE TESTE LOCAL (Fixo) ----
    image_path = "D:\\GitHub\\BLU\\Fotos-estacionamento\\exemplo.jpg" 
    
    if not os.path.exists(image_path):
        print(json.dumps({"erro": f"Arquivo nao encontrado: {image_path}"}))
        return

    # Descobre os caminhos automaticamente baseados na posição do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    model_path = os.path.join(project_root, "Modelo", "best.pt")

    if not os.path.exists(model_path):
        print(json.dumps({"erro": f"Modelo nao encontrado em: {model_path}"}))
        return

    # ========================================================
    # 1. CONFIGURAÇÃO DOS CAMINHOS DE SALVAMENTO
    # ========================================================
    fotos_dir = os.path.join(project_root, "results", "fotos")
    json_dir = os.path.join(project_root, "results", "json")
    
    # Cria as subpastas automaticamente se elas não existirem no disco
    os.makedirs(fotos_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    # Define o nome e o caminho final onde a foto anotada será gravada
    nome_arquivo = os.path.basename(image_path)
    nome_base, _ = os.path.splitext(nome_arquivo)
    nome_json = f"resultado1_{nome_base}.json"

    output_image_path = os.path.join(fotos_dir, f"saida1_{nome_arquivo}")
    output_json_path = os.path.join(json_dir, nome_json)

    # Carrega o modelo treinado OBB
    model = YOLO(model_path)

    # Executa a inferência em modo silencioso
    results = model(image_path, verbose=False)
    result = results[0]
    
    # ========================================================
    # 🔥 2. CÓDIGO QUE SALVA A IMAGEM ANOTADA NO DISCO
    # O result.save() da Ultralytics desenha as marcações (OBB) 
    # e grava o arquivo .jpg diretamente no caminho especificado.
    # ========================================================
    result.save(filename=output_image_path)
    # ========================================================

    # --- TRAVA DE SEGURANÇA PARA ENTRADAS VAZIAS ---
    if result.obb is None or len(result.obb) == 0:
        output = {
            "vagas_ocupadas": 0,
            "vagas_disponiveis": 0,
            "total_vagas_detectadas": 0,
            "imagem_anotada_salva_em": output_image_path,
            "json_salvo_em": output_json_path,
            "aviso": "Nenhum objeto detectado pelo modelo OBB nesta imagem.",
            "detalhes": []
        }
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=4, ensure_ascii=False)
            
        print(json.dumps(output, ensure_ascii=False))
        return
    # ----------------------------------------------

    vagas_detectadas = []
    vagas_ocupadas = 0
    vagas_livres = 0

    # Varre os objetos detectados pela YOLO OBB
    for box in result.obb:
        class_id = int(box.cls[0])
        class_name = model.names[class_id] 
        
        xywhr = box.xywhr[0].tolist()
        cx = xywhr[0]
        cy = xywhr[1]

        if "carro" in class_name.lower():
            status = "ocupada"
            vagas_ocupadas += 1
        else:
            status = "livre"
            vagas_livres += 1

        vagas_detectadas.append({
            "status": status,
            "classe_original": class_name,
            "centro_x": round(cx, 1),
            "centro_y": round(cy, 1)
        })

    # Monta o JSON de resposta estruturado
    output = {
        "vagas_ocupadas": vagas_ocupadas,
        "vagas_disponiveis": vagas_livres,
        "total_vagas_detectadas": vagas_ocupadas + vagas_livres,
        "imagem_anotada_salva_em": output_image_path,
        "json_salvo_em": output_json_path,
        "detalhes": vagas_detectadas
    }

    # Salva o arquivo JSON fisicamente para auditoria
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    # Retorna o JSON limpo em uma única linha para o Node-RED
    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()