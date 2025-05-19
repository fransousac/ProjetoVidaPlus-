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
ProjetoVidaPlus/
│
├── app.py                 # Arquivo principal da aplicação
├── database.py            # Conexão com o banco SQLite
├── models.py              # Modelos de criação de tabelas
├── banco.db               # Banco de dados local
├── routes/                # Blueprints separados por módulo
│   ├── pacientes.py
│   ├── profissionais.py
│   ├── consultas.py
│   └── prescricoes.py
└── README.md             
```
