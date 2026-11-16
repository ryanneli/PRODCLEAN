import shutil
import os

# Pega o diretório onde o script está e sobe UM nível para a raiz do projeto, assim ele acha a node_modules que está na pasta principal
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODE_DIR = os.path.join(BASE_DIR, 'node_modules')
STATIC_VENDORS = os.path.join(BASE_DIR, 'static', 'vendors')

def setup_vendors():
    # 1. Criar a pasta vendors se não existir
    if not os.path.exists(STATIC_VENDORS):
        os.makedirs(STATIC_VENDORS)
        print(f"✅ Pasta criada: {STATIC_VENDORS}")

    # Lista de mapeamento (Origem no Node -> Destino na Static)
    mappings = {
        'bootstrap/dist': 'bootstrap',
        'bootstrap-icons/font': 'bootstrap-icons',
        'htmx.org/dist': 'htmx',
        'jquery/dist': 'jquery'
    }

    for src, dest in mappings.items():
        src_path = os.path.join(NODE_DIR, src)
        dest_path = os.path.join(STATIC_VENDORS, dest)
        
        if os.path.exists(src_path):
            # Remove a pasta antiga se existir para atualizar
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            
            shutil.copytree(src_path, dest_path)
            print(f"🚀 {dest} copiado com sucesso!")
        else:
            print(f"⚠️ Atenção: {src} não encontrado em node_modules. Rode 'npm install {src.split('/')[0]}'")

if __name__ == "__main__":
    setup_vendors()