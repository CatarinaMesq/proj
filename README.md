## Project structure

project/

├── app.py             # Controller

├── models.py          # Model

├── forms.py           # Form classes

├── functions.py       # Utility functions

├── templates/         # Views

│   ├── base.html      # Base template for other views to extend

│   ├── index.html     # Home page

│   ├── login.html     # Login page

│   ├── register.html  # Registration page

│   ├── search.html    # Search results page

│   ├── user_profile.html  # User profile page

│   ├── feed.html      # Feed page

│   └── error.html     # Error page

├── assets/            # Static files

│   ├── images/

│   ├── javascript/

│   └── css/


## As bibliotecas importadas são:


**base64**: Uma biblioteca que fornece funções para codificar e decodificar dados em formato base64.

**os**: Uma biblioteca que fornece funções para interagir com o sistema operacional, como criar arquivos e diretórios.

**sqlite3**: Uma biblioteca que fornece funções para trabalhar com bancos de dados SQLite.

**datetime**: Uma biblioteca que fornece funções para manipular datas e horas.

**Flask**: Um framework web em Python para construir aplicativos web.

**render_template**: Uma função do Flask para renderizar um modelo HTML.

**request**: Um objeto global do Flask que contém os dados enviados por um cliente HTTP.

**redirect**: Uma função do Flask para redirecionar um cliente HTTP para outra página.

**url_for**: Uma função do Flask para gerar URLs para as páginas de um aplicativo web.

**session**: Um objeto global do Flask que permite armazenar informações do lado do servidor para uso posterior.

**flash**: Uma função do Flask para mostrar mensagens de erro ou aviso na página.

**generate_password_hash e check_password_hash**: Funções do Werkzeug que são usadas para criptografar e verificar senhas de usuário.

**secure_filename**: Uma função do Werkzeug que retorna uma versão segura de um nome de arquivo para evitar ataques de injeção de código.

## Funções - functions.py

def register()

Esta é uma função que lida com o registo de novos utilizadores na aplicação. 

A função é chamada quando um utilizador acessa a página de registro e preenche o formulário com seu nome de utilizador, e-mail e senha.

Primeiro, a função verifica se o método da solicitação é POST, o que significa que o formulário foi enviado e os dados devem ser processados. 

Em seguida, a função extrai os valores do nome de utilizador, e-mail e senha do formulário usando a biblioteca Flask. A função também valida os dados inseridos pelos utilizador, verificando se os campos estão vazios ou se têm menos de 3 caracteres.

Em seguida, a função usa a biblioteca Werkzeug para criptografar a senha do utilizador usando o algoritmo SHA256. A função verifica se o nome de utilizador ou e-mail já estão em uso no banco de dados SQLite usando uma consulta SQL SELECT.

Se o utilizador já existe, a função renderiza novamente a página de registro com uma mensagem de erro informando que o nome de utilizador ou e-mail já existe. 

Caso contrário, a função insere as informações do novo utilizador no banco de dados SQLite usando uma consulta SQL INSERT.

Por fim, a função redireciona o usuário para a página de login usando a função redirect() do Flask. Se o método da solicitação não for POST, a função renderiza novamente a página de registro.

def login()

Esta função é responsável pelo processo de login do utilizador. 

Primeiro, cria-se uma nova instância da classe LoginForm. Depois, inicializa-se a variável de erro como None.

Se o método de pedido for POST (o que significa que o utilizador submeteu o formulário), a função obtém o nome de utilizador e a palavra-passe a partir dos dados do formulário. 

Em seguida, executa-se uma consulta SQL para obter o utilizador com o nome de utilizador fornecido. 

Se encontrar um utilizador, verifica-se se a palavra-passe fornecida corresponde à palavra-passe armazenada no banco de dados. Se as palavras-passe corresponderem, a função define as variáveis de sessão e redireciona para a página de índice.

Se as palavras-passe não corresponderem, a função define a variável de erro e renderiza o modelo de login com o formulário e a mensagem de erro. 

Se não for encontrado nenhum utilizador com o nome de utilizador fornecido, a função define a variável de erro e renderiza o modelo de login com o formulário e a mensagem de erro.

Se o método de pedido não for POST, a função renderiza o modelo de login com o formulário e a mensagem de erro (que será None).

def logout()

Esta função implementa o logout de um utilizador autenticado na aplicação web.

O que acontece é que quando o utilizador clica no botão de logout na página, a função logout() é executada. 

Em primeiro lugar, a função remove as variáveis de sessão logged_in e username, que indicam que o utilizador está autenticado e qual é o seu nome de utilizador, respetivamente. 

A remoção é feita através do método pop() do objeto session, que recebe o nome da chave a ser removida e um valor padrão a ser retornado caso a chave não exista (neste caso, None).

Após remover as variáveis de sessão, a função redireciona o utilizador para a página inicial da aplicação, que é definida pela função index(), utilizando a função redirect() e a função url_for(). 

A função url_for() gera a URL da rota correspondente à função index().

def profile()

Esta função chamada profile é responsável por renderizar a página de perfil de um usuário específico. A página exibe informações sobre o usuário, seus posts e comentários.

A função começa criando uma instância do formulário LoginForm e em seguida, faz uma consulta ao banco de dados para obter informações do usuário que tem o nome de usuário fornecido. 

Se nenhum usuário for encontrado com o nome de usuário fornecido, uma mensagem de erro será exibida com um status HTTP 404.

Se um usuário for encontrado, a função fará consultas ao banco de dados para recuperar todos os posts e comentários feitos pelo usuário, classificando-os por data de criação ou registro, respectivamente, do mais novo para o mais antigo.

Em seguida, a função itera através dos posts e cria um dicionário contendo informações relevantes sobre cada post, que é adicionado a uma lista. Se o conteúdo do post for uma string binária, ele é convertido em base64 antes de ser adicionado ao dicionário.

Finalmente, a função renderiza o modelo user_profile.html e passa as informações relevantes para serem exibidas na página, incluindo informações do usuário, lista de posts e lista de comentários, além do formulário LoginForm.

def 
