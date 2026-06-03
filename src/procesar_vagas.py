import sys
import json
import os
from ultralytics import YOLO

def main():
    # ---- MODO DE PRODUÇÃO (NODE-RED) ----
    # Verifica se o Node-RED passou o caminho da imagem como argumento
    if len(sys.argv) < 2:
        print(json.dumps({"erro": "Nenhum caminho de imagem fornecido."}))
        return

    image_path = sys.argv[1] 
    
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

    # Mapeamento das Novas Pastas solicitadas
    fotos_dir = os.path.join(project_root, "results", "fotos")
    json_dir = os.path.join(project_root, "results", "json")
    
    # Cria as subpastas automaticamente se elas não existirem
    os.makedirs(fotos_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    # Extrai o nome do arquivo recebido (Ex: foto2.jpg) e define o nome do JSON
    nome_arquivo = os.path.basename(image_path)
    nome_base, _ = os.path.splitext(nome_arquivo)
    nome_json = f"resultado_{nome_base}.json"

    # Define os caminhos completos de gravação final
    output_image_path = os.path.join(fotos_dir, f"saida_{nome_arquivo}")
    output_json_path = os.path.join(json_dir, nome_json)

    # Carrega o modelo treinado OBB
    model = YOLO(model_path)

    # Executa a inferência forçando modo 100% silencioso
    results = model(image_path, verbose=False)
    result = results[0]
    
    # Salva a imagem com as caixas rotacionadas na pasta correta
    result.save(filename=output_image_path)

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
        # Grava o JSON de erro na pasta de registros
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=4)
            
        # Responde para o Node-RED de forma compacta
        print(json.dumps(output))
        return
    # ----------------------------------------------

    vagas_detectadas = []
    vagas_ocupadas = 0
    vagas_livres = 0

    # Varre os objetos detectados pela YOLO OBB
    for box in result.obb:
        class_id = int(box.cls[0])
        class_name = model.names[class_id] 
        
        # xywhr nos entrega: [centro_x, centro_y, largura, altura, rotacao]
        xywhr = box.xywhr[0].tolist()
        cx = xywhr[0]
        cy = xywhr[1]

        # Lógica de status baseada nas suas classes reais ('carro' e 'vaga')
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

    # 💾 SALVA O ARQUIVO FISICAMENTE NA PASTA JSON (com identação para leitura humana fácil)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    # 🚀 SAÍDA PARA O NODE-RED: Limpa o buffer de saída e imprime estritamente em uma única linha
    sys.stdout.write(json.dumps(output) + "\n")
    sys.stdout.flush()

if __name__ == "__main__":
    main()