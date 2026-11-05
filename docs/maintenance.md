# Bruno Universe

README de perfil para Bruno Souza. Arte vetorial original em pixel art, sem fontes externas, imagens rasterizadas ou JavaScript no README.

## Conteúdo e regeneração

Edite `profile.json` para atualizar contatos, tecnologias e missões. As cenas e a paleta estão em `scripts/generate-assets.py` e `scripts/art.py`.

```sh
python scripts/generate-assets.py
python scripts/update-stats.py
python scripts/validate.py
```

Python 3.12 e GitHub CLI autenticado são suficientes; os geradores não precisam de pacotes Python externos. Para regerar somente o visual das estatísticas, sem rede, use `python scripts/update-stats.py --cached`.

## Estatísticas

O workflow `Update profile statistics` consulta a API oficial do GitHub diariamente às 09:23 UTC (06:23 em Brasília), no push de alterações nos geradores e por execução manual em Actions. Os SVGs resultantes ficam no próprio repositório, em vez de depender de widgets de terceiros. O horário agendado pode atrasar conforme a fila do GitHub.

O workflow usa o `GITHUB_TOKEN` fornecido automaticamente pelo GitHub. Nenhum token pessoal é necessário ou salvo no repositório. O token tem permissão de escrita apenas no conteúdo deste repositório, para salvar os SVGs.

- **Repositórios públicos:** repositórios pertencentes ao perfil, incluindo forks e arquivados.
- **Estrelas recebidas:** soma das estrelas dos repositórios públicos originais, incluindo arquivados; exclui forks.
- **Contribuições:** calendário dos últimos 12 meses retornado pelo GitHub para a credencial que faz a consulta. Segue a visibilidade e as regras do GitHub; pode incluir contagens anônimas de contribuições privadas se o perfil as exibir. Não representa todos os commits realizados. Nenhum nome ou conteúdo de repositório privado é consultado ou publicado.
- **Linguagens:** proporção de bytes de código nos repositórios públicos originais e ativos; exclui forks e arquivados. Não é uma avaliação de proficiência. Cinco linguagens e o restante agrupado como “Outras”.
- **Seguidores no GitHub:** pessoas que seguem o perfil.

O snapshot auditável está em `assets/github-data.json`. Se a API falhar, o workflow falha antes de salvar os resultados; o último SVG válido permanece disponível.

Fontes técnicas: [autenticação no Actions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token), [GraphQL do GitHub](https://docs.github.com/en/graphql/reference) e [agendamentos do Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

## Animação e acessibilidade

Um único sprite mestre define o astronauta loiro de olhos azuis, com traje azul e branco e a letra B. Os quatro quadros de caminhada são usados em todas as cenas; o hero usa a pose inicial e o registro usa a pose sentado.

As animações usam CSS dentro dos SVGs: caminhada com passos discretos, respiração, flutuação do planeta e ativação lenta do portal. `prefers-reduced-motion` mantém as cenas estáticas e escolhe o primeiro quadro de caminhada. Os assets também continuam legíveis sem animações.

O README usa `<picture>` para versões de celular, `alt` com conteúdo significativo e links HTML externos aos SVGs. Links dentro de um SVG carregado como imagem não são interativos no README. Os títulos pixelados são paths; o texto corrido usa fontes de sistema.

A apresentação, localização e formação são compostas dentro dos SVGs de ABOUT, com quebras próprias para desktop e celular. O texto completo também permanece no `alt`. As navegações usam botões SVG de 136 × 48 px em âncoras HTML, centralizados e com quebra natural em duas colunas no celular ou uma coluna em telas muito estreitas. Assim, cada destino continua clicável sem depender de links internos a SVGs.

Não há controle pelo scroll nem sincronização garantida entre imagens independentes. A posição do astronauta e o caminho pontilhado constroem a sequência narrativa.
