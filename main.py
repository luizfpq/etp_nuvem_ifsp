import os
import subprocess
import time

def print_menu():
    print("\n" + "="*40)
    print(" Menu Principal - Processamento de UASGs ")
    print("="*40)
    print("1. Obter dados da API (get_uasg.py)")
    print("2. Processar dados com Ollama (process_uasg_ollama.py)")
    print("3. Processar dados sem IA (process_uasg_no_ai.py)")
    print("x. Sair")
    print("="*40)

def main():
    while True:
        print_menu()
        choice = input("Por favor, selecione uma opção: ")

        if choice == '1':
            print("Executando o script para obter os dados da API...")
            try:
                subprocess.run(["python", "get_uasg.py"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Ocorreu um erro ao executar 'get_uasg.py': {e}")
            except FileNotFoundError:
                print("Erro: O interpretador Python ou o script 'get_uasg.py' não foi encontrado.")

        elif choice == '2':
            data_file = "uasgs_raw_data.json"
            if os.path.exists(data_file):
                print("Executando o script para processar os dados com Ollama...")
                try:
                    subprocess.run(["python", "process_uasg_ollama.py"], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Ocorreu um erro ao executar 'process_uasg.py': {e}")
                except FileNotFoundError:
                    print("Erro: O interpretador Python ou o script 'process_uasg.py' não foi encontrado.")
            else:
                print(f"Erro: O arquivo de dados '{data_file}' não foi encontrado.")
                print("Por favor, execute a opção 1 primeiro para obter os dados.")

        elif choice == '3':
                    data_file = "uasgs_raw_data.json"
                    if os.path.exists(data_file):
                        print("Executando o script para processar os dados sem IA...")
                        try:
                            subprocess.run(["python", "process_uasg_no_ai.py"], check=True)
                        except subprocess.CalledProcessError as e:
                            print(f"Ocorreu um erro ao executar 'process_uasg_no_ai.py': {e}")
                        except FileNotFoundError:
                            print("Erro: O interpretador Python ou o script 'process_uasg_no_ai.py' não foi encontrado.")
                    else:
                        print(f"Erro: O arquivo de dados '{data_file}' não foi encontrado.")
                        print("Por favor, execute a opção 1 primeiro para obter os dados.")

        elif choice == 'x':
            print("Saindo do programa. Até mais!")
            break
            
        else:
            print("Opção inválida. Por favor, escolha 1, 2, 3 ou x.")
            
        time.sleep(2) # Tempinho pra ler a saida

if __name__ == "__main__":
    main()