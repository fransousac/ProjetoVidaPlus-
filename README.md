# ProjetoVidaPlus

API RESTful para gerenciamento de um sistema hospitalar simples. Desenvolvido com Flask, SQLite e autenticação via JWT. Permite o cadastro e controle de pacientes, profissionais da saúde, consultas médicas e prescrições.

Principais funcionalidades:
- Cadastro e listagem de pacientes e profissionais
- Agendamento de consultas médicas
- Registro e edição de prescrições
- Proteção com login/autenticação JWT
- Testes de endpoints via Postman

## 📚 Como Executar o Projeto

### ✅ Pré-requisitos

Certifique-se de ter o **Python 3.10+** instalado em sua máquina.

### 📦 Bibliotecas necessárias

Instale as dependências executando:

```bash
pip install flask flask-jwt-extended flask-cors
```

---

## 🚀 Executando a API

No terminal, dentro da pasta do projeto, execute:

```bash
python app.py
```

A aplicação será iniciada em:  
📍 `http://localhost:5000`

---

## 🔐 Autenticação JWT

A maioria dos endpoints exige **token JWT**.  
Faça o login na rota `/login` para obter o token e utilize no cabeçalho das próximas requisições:

```
Authorization: Bearer <seu_token>
```

---

## 🧪 Exemplos de Testes com Postman

### Criar Paciente (POST /pacientes/)
```json
{
  "nome": "João da Silva",
  "idade": 35,
  "telefone": "99999-0000"
}
```

### Criar Consulta (POST /consultas/)
```json
{
  "id_paciente": 1,
  "id_profissional": 1,
  "data": "2025-05-20 14:00",
  "status": "agendada"
}
```

---

## 📂 Estrutura do Projeto

```
projeto-back/
│
├── app.py                  # Arquivo principal para inicialização da aplicação Flask
├── database.py             # Conexão e utilitários do banco de dados
├── models.py               # Criação das tabelas do banco de dados
├── reset_db.py             # Script para resetar o banco de dados (opcional)
├── banco.db                # Arquivo SQLite contendo os dados
├── usuarios.py             # Registro de usuários no sistema
├── ver_usuarios.py         # Utilitário para listar usuários
│
├── routes/                 # Pasta contendo as rotas organizadas por módulo
│   ├── __init__.py
│   ├── auth.py             # Rota de autenticação JWT
│   ├── consultas.py        # Rotas relacionadas a consultas
│   ├── pacientes.py        # Rotas de pacientes
│   ├── prescricoes.py      # Rotas de prescrições
│   ├── profissionais.py    # Rotas de profissionais da saúde


```
