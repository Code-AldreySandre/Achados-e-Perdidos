# Sistema de Achados e Perdidos

## Descrição
Este repositório contém a implementação de um sistema de achados e perdidos, permitindo o cadastro, busca e listagem de itens perdidos e encontrados.

## Diagramas UML
Foram criados diagramas UML para representar os casos de uso e fluxo de atividades do sistema:

- **Diagrama de Caso de Uso:** Representa as interações entre os usuários (Usuário Comum e Administrador) e o sistema.
   - Ator Usuário Comum: Cadastrar item perdido, consultar itens e realizar login.
   - Ator Administrador: Realizar todas as funções do usuário comum, além de gerenciar usuários e itens.
  ![Diagrama de Caso de Uso](Imagens/UML_caso_uso.png)

- **Diagrama de Atividade:** Demonstra o fluxo de operações do sistema, como cadastro e busca de itens.
  ![Diagrama de Atividade](Imagens/UML_Atividade.png)

## Modelagem de Software
O sistema adota a arquitetura MVC (Model-View-Controller) para separar responsabilidades e facilitar a manutenção. A estrutura detalhada é a seguinte:

### Model (Modelo)
Responsável pela lógica de negócios e manipulação de dados. Utiliza o SQLite3 para persistência, com tabelas como `usuarios`, `itens_perdidos` e `itens_encontrados`.
- `Usuario`: Representa um usuário com atributos como `id`, `nome`, `email`, `senha` e `permissao`.
- `Item`: Representa um item com atributos como `id`, `descricao`, `localizacao`, `status` e `data`.

### View (Visão)
Interface gráfica desenvolvida com Tkinter. Exibe dados e captura interações do usuário.
- Telas de login, cadastro de itens, listagem e busca de itens.
- Interface amigável e intuitiva, com feedback visual.

### Controller (Controlador)
Intermediário entre a View e o Model. Processa entradas da View e aciona métodos do Model.
- Controla autenticação e permissões.
- Realiza operações de CRUD (Create, Read, Update, Delete) e busca de itens.

## Funcionalidades
- Cadastro de usuários com autenticação (login e senha)
- Cadastro de itens encontrados e perdidos
- Consulta por categorias, descrição ou localização
- Interface gráfica amigável e interativa
- Controle de permissões (admin e usuário comum)
- Geração de relatórios e históricos de devoluções

## Estrutura do Projeto
O projeto utiliza a linguagem Python e a biblioteca Tkinter para interface gráfica, com persistência de dados utilizando SQLite3. A arquitetura é baseada no padrão MVC (Model-View-Controller), garantindo separação de responsabilidades e facilidade de manutenção.

## Requisitos
- Python 3.10+
- Bibliotecas: Tkinter, SQLite3

## Como Executar
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-achados-perdidos.git
   ```
2. Acesse o diretório do projeto:
   ```bash
   cd sistema-achados-perdidos
   ```
3. Instale as dependências necessárias (caso existam):
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   python main.py
   ```

## Contribuição e Equipe
O projeto foi desenvolvido em colaboração com a equipe abaixo:
- **Aldrey Sandre** [(GitHub)](https://github.com/aldreysandre) - Modelagem de Diagramas UML; Análise do Código; Revisão Final
- **Arthur Daniel** [(GitHub)](https://github.com/arthurdanielp) - Desenvolvimento e Estruturação do Código
- **Ismael Farias** [(GitHub)](https://github.com/ismlfq) - Testes de Usabilidade
- **Jean Lucas** [(GitHub)](https://github.com/jeanlucas) - Modelagem e Organização do Relatório
- **Renata Galvão** [(GitHub)](https://github.com/RehGal) - Revisão e Documentação do Artigo; Plano de Apresentação
- **Wendreo Tauan** [(GitHub)](https://github.com/wendreotauan) - Desenvolvimento das Funcionalidades

## Orçamento
O projeto teve um custo estimado de R$ 3.910,00, considerando horas trabalhadas e custo por hora dos membros da equipe.

## Licença
Este projeto é open-source e está licenciado sob a MIT License.





   ```

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).


