# Abra o terminal e instale as seguintes bibliotecas:
# pip install img2pdf
# pip install selenium
# pip install webdriver_manager
# pip install pypdf2


import os
import img2pdf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from PyPDF2 import PdfMerger
import time  # Importação adicional para esperar manualmente


# Configuração do driver do Selenium
def setup_selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Modo sem interface gráfica
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Configurando o serviço com o nome correto 'Service'
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    return driver


# Função para capturar uma página web como imagem e depois converter para PDF
def convert_page_to_pdf(url, output_path, delay=400):
    driver = setup_selenium()
    try:
        driver.get(url)
        driver.implicitly_wait(delay)

        # Espera explícita para garantir que a página esteja totalmente carregada
        WebDriverWait(driver, 250).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
            # Pode alterar para um seletor específico, se necessário
        )

        # Espera adicional para garantir que todos os scripts e conteúdo sejam carregados
        time.sleep(10)  # Aguarda 5 segundos adicionais; ajuste conforme necessário

        # Calcula a altura total da página
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1300, total_height)

        # Salva a página completa como imagem temporariamente
        temp_image = output_path.replace('.pdf', '.png')
        driver.save_screenshot(temp_image)

        # Usa img2pdf para converter a imagem salva em PDF
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(temp_image))

        # Verifique se o arquivo PDF foi criado com sucesso
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Failed to create PDF file: {output_path}")

        # Remove o arquivo de imagem temporário
        os.remove(temp_image)

        print(f"PDF saved successfully to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


# Função para combinar múltiplos PDFs em um único PDF
def merge_pdfs(pdf_list, output_path):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()


if __name__ == "__main__":
    # URLs do site que você deseja converter para PDF
    urls = [
        # Substitua pelo URL do site
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/in%C3%ADcio",  # Substitua pelo URL do site
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/facti",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/qualifacti",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/coordena%C3%A7%C3%A3o-geral",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/mediadores",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/mediadores/adriana-pereira-da-silva",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/mediadores/ana-paula-rodrigues",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/mediadores/fabr%C3%ADcio-kleinicke-gomes",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/mediadores/francisco-conti-bauke",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/mediadores/j%C3%BAlio-c%C3%A9sar-leit%C3%A3o-j%C3%BAnior",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/mediadores/larissa-de-oliveira-figueira",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/mediadores/marcelo-de-almeida-viana",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/mediadores/peterson-gomes-de-moura-barros",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/mediadores/thais-angela-cavalheiro-de-azevedo",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/introdu%C3%A7%C3%A3o",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-inspirar",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-conceitualizar",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-conceitualizar/a-computa%C3%A7%C3%A3o-em-nuvem",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-conceitualizar/baas-e-mbaas",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-conceitualizar/baas-com-o-firebase",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-conceitualizar/baas-com-o-firebase/baas-na-pr%C3%A1tica-via-projetos-firebase",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-conceitualizar/baas-com-o-firebase/adicionando-o-firebase-a-projetos-de-apps-j%C3%A1-existentes",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-conceitualizar/baas-com-o-firebase/configurando-os-servi%C3%A7os-principais-do-firebase",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-conceitualizar/baas-com-o-firebase/projeto-de-demonstra%C3%A7%C3%A3o-do-firebase-para-apps-android-e-ios",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-conceitualizar/estudo-de-casos-pr%C3%A1ticos",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-consolidar",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/etapa-avaliar",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-1",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-2",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-3",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-4",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-5",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-6",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-7",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-8",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-9",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-10",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-11",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-12",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-13",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-14",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-15",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-16",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-17",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-18",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-19",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-20",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/sugest%C3%B5es-de-resposta/atividade-de-experimenta%C3%A7%C3%A3o-21",
        "https://sites.google.com/facti.com.br/aplicacoes-escalaveis-na-nuvem/material-did%C3%A1tico/refer%C3%AAncias",


        # Adicione outras URLs conforme necessário
    ]

    # Diretório temporário para salvar PDFs intermediários
    temp_dir = "temp_pdfs"
    os.makedirs(temp_dir, exist_ok=True)

    pdf_files = []
    for i, url in enumerate(urls):
        output_file = os.path.join(temp_dir, f"output_{i}.pdf")
        convert_page_to_pdf(url, output_file, delay=25)  # Ajuste o tempo de espera conforme necessário
        if os.path.exists(output_file):
            pdf_files.append(output_file)

    # Nome do arquivo PDF combinado de saída
    final_output_file = "Mais um teste.pdf"
    merge_pdfs(pdf_files, final_output_file)

    # Limpeza dos arquivos temporários
    for pdf in pdf_files:
        os.remove(pdf)

    print(f"Combined PDF saved successfully to {final_output_file}")
