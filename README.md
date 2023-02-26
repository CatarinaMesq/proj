## [URL]: (https://sarcasticnetwork.pythonanywhere.com)


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


# As bibliotecas importadas são:


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



# Funções - functions.py

## def register()

Esta é uma função que lida com o registo de novos utilizadores na aplicação. 

A função é chamada quando um utilizador acessa a página de registro e preenche o formulário com seu nome de utilizador, e-mail e senha.

Primeiro, a função verifica se o método da solicitação é POST, o que significa que o formulário foi enviado e os dados devem ser processados. 

Em seguida, a função extrai os valores do nome de utilizador, e-mail e senha do formulário usando a biblioteca Flask. A função também valida os dados inseridos pelos utilizador, verificando se os campos estão vazios ou se têm menos de 3 caracteres.

Em seguida, a função usa a biblioteca Werkzeug para criptografar a senha do utilizador usando o algoritmo SHA256. A função verifica se o nome de utilizador ou e-mail já estão em uso no banco de dados SQLite usando uma consulta SQL SELECT.

Se o utilizador já existe, a função renderiza novamente a página de registro com uma mensagem de erro informando que o nome de utilizador ou e-mail já existe. 

Caso contrário, a função insere as informações do novo utilizador no banco de dados SQLite usando uma consulta SQL INSERT.

Por fim, a função redireciona o usuário para a página de login usando a função redirect() do Flask. Se o método da solicitação não for POST, a função renderiza novamente a página de registro.

## def login()

Esta função é responsável pelo processo de login do utilizador. 

Primeiro, cria-se uma nova instância da classe LoginForm. Depois, inicializa-se a variável de erro como None.

Se o método de pedido for POST (o que significa que o utilizador submeteu o formulário), a função obtém o nome de utilizador e a palavra-passe a partir dos dados do formulário. 

Em seguida, executa-se uma consulta SQL para obter o utilizador com o nome de utilizador fornecido. 

Se encontrar um utilizador, verifica-se se a palavra-passe fornecida corresponde à palavra-passe armazenada no banco de dados. Se as palavras-passe corresponderem, a função define as variáveis de sessão e redireciona para a página de índice.

Se as palavras-passe não corresponderem, a função define a variável de erro e renderiza o modelo de login com o formulário e a mensagem de erro. 

Se não for encontrado nenhum utilizador com o nome de utilizador fornecido, a função define a variável de erro e renderiza o modelo de login com o formulário e a mensagem de erro.

Se o método de pedido não for POST, a função renderiza o modelo de login com o formulário e a mensagem de erro (que será None).

## def logout()

Esta função implementa o logout de um utilizador autenticado na aplicação web.

O que acontece é que quando o utilizador clica no botão de logout na página, a função logout() é executada. 

Em primeiro lugar, a função remove as variáveis de sessão logged_in e username, que indicam que o utilizador está autenticado e qual é o seu nome de utilizador, respetivamente. 

A remoção é feita através do método pop() do objeto session, que recebe o nome da chave a ser removida e um valor padrão a ser retornado caso a chave não exista (neste caso, None).

Após remover as variáveis de sessão, a função redireciona o utilizador para a página inicial da aplicação, que é definida pela função index(), utilizando a função redirect() e a função url_for(). 

A função url_for() gera a URL da rota correspondente à função index().

## def profile()

Esta função chamada profile é responsável por renderizar a página de perfil de um usuário específico. A página exibe informações sobre o usuário, seus posts e comentários.

A função começa criando uma instância do formulário LoginForm e em seguida, faz uma consulta ao banco de dados para obter informações do usuário que tem o nome de usuário fornecido. 

Se nenhum usuário for encontrado com o nome de usuário fornecido, uma mensagem de erro será exibida com um status HTTP 404.

Se um usuário for encontrado, a função fará consultas ao banco de dados para recuperar todos os posts e comentários feitos pelo usuário, classificando-os por data de criação ou registro, respectivamente, do mais novo para o mais antigo.

Em seguida, a função itera através dos posts e cria um dicionário contendo informações relevantes sobre cada post, que é adicionado a uma lista. Se o conteúdo do post for uma string binária, ele é convertido em base64 antes de ser adicionado ao dicionário.

Finalmente, a função renderiza o modelo user_profile.html e passa as informações relevantes para serem exibidas na página, incluindo informações do usuário, lista de posts e lista de comentários, além do formulário LoginForm.

## def feed()

Este código define uma função chamada feed() que busca posts e comentários de uma base de dados, formata-os e retorna-os para serem renderizados num modelo HTML chamado feed.html.

Em primeiro lugar, a função executa duas consultas SQL para buscar todos os posts e todos os comentários da base de dados, respetivamente, ordenando cada um por um campo relevante em ordem decrescente. Os resultados destas consultas são armazenados nas variáveis posts e comments.

Em seguida, é criado um novo objeto LoginForm.

Uma lista vazia chamada post_list é criada para armazenar os posts e comentários formatados. A função, em seguida, itera através de cada post em posts.

Para cada post, a função verifica se o campo picture é uma string de bytes ou uma string. Se for uma string de bytes, é codificada como base64 e decodificada para uma string utf-8. Caso contrário, é codificada como utf-8 e, em seguida, como base64. Esta string codificada é armazenada na variável encoded_string.

A função, em seguida, executa outra consulta SQL para buscar todos os comentários para este post na base de dados, filtrando por post_id, e ordenando-os por timestamp em ordem decrescente. Os resultados desta consulta são armazenados na variável post_comments.

Uma lista vazia chamada comment_list é criada para armazenar os comentários formatados para este post. A função, em seguida, itera através de cada comentário em post_comments.

Para cada comentário, um dicionário é criado para armazenar os dados do comentário, incluindo os campos id, user_id, post_id, content, timestamp e upvotes. Este dicionário é armazenado na variável comment_dict, e é adicionado à comment_list para este post.

Depois de todos os comentários terem sido processados, é criado um dicionário para armazenar os dados do post, incluindo os campos id, user_id, picture, content, created_at e comments. O campo picture é definido como um URI de dados codificado em base64 que contém o encoded_string.

Este dicionário é armazenado na variável post_dict e é adicionado à post_list.

Finalmente, a função renderiza o modelo feed.html com as variáveis post_list, form e comments. Estas variáveis estarão disponíveis no modelo como posts, form e comments, respetivamente.

## def post():

A função post() implementa a funcionalidade de criar um novo post na aplicação.

Ela começa inicializando um formulário de login e checando se o utilizador está logado. Se o usuário não estiver logado, a função redireciona para a página de login com uma mensagem de erro.

Em seguida, a função recupera todos os posts e comentários do base de dados. Se a requisição HTTP for um POST, o utilizador enviou um novo post. A função então valida a imagem enviada, salva-a em um arquivo temporário, insere o novo post no banco de dados, e deleta o arquivo temporário.

Independentemente do método da requisição, a função sempre redireciona o utilizador para a página do feed após o processamento da requisição.

A função retorna uma instância do objeto redirect do Flask que redireciona o utilizador para a página especificada no argumento url_for().

Note que o código também utiliza o módulo os para lidar com o armazenamento temporário do arquivo da imagem e o módulo secure_filename para garantir que o nome do arquivo é seguro.

## def comment():

A função comment() é responsável por adicionar um comentário a uma postagem específica no feed.

Em primeiro lugar, a função verifica se o utilizador está logado. Se não estiver, o utilizador é redirecionado para a página de login.

Em seguida, a função recupera o ID da postagem à qual o comentário está sendo adicionado, o ID do usuário logado e o conteúdo do comentário do formulário enviado pelo utilizador.

A função insere o comentário no banse de dados, usando a função execute() do objeto c, que é uma conexão com o banco de dados. A consulta SQL utilizada inclui a inserção do ID da postagem, ID do utilizador, conteúdo do comentário e um carimbo de data/hora da criação do comentário.

Em seguida, a função recupera todas as postagens e comentários do base de dados, ordenando-os em ordem decrescente de data/hora de criação.

Por fim, a função redireciona o utilizador para a página do feed.


