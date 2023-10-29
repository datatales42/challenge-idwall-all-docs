# Frontend Styles
https://github.com/datatales42/challenge-idwall-all-docs/assets/69640514/f28b7d31-81e7-41f7-80f3-6353c3051137

https://github.com/datatales42/challenge-idwall-all-docs/assets/69640514/e1c33da3-652f-4ae2-a86d-f6e16dd82a49

# <img src='https://github.com/datatales42/challenge-idwall-all-docs/assets/69640514/36710913-1c77-4faa-a718-bdb66f453c87' width='30'> <img src='https://github.com/datatales42/challenge-idwall-all-docs/assets/69640514/98653fc5-fc98-4267-b7d6-a39859184f22' width='30'> Description
This is a repository for presenting submission for a challenge presented by IdWall in conjunction with FIAP college, by the contributing members of this project. Every documentation file, videos, and scripts to populate the database may be found.

## 🤔❓ Challenge 
### Context References

**Anti-Money Laundering (AML)** refers to a set of procedures, laws, and regulations designed to stop illegal generation of income. Its main goal is to help detect and report money laundering and financing of terrorist practices. AML also combats crimes like securities fraud and market manipulation.

**Federal Bureau of Investigation (FBI)**: An American entity that investigates and pursues individuals connected to crimes. It exposes information about wanted individuals and important details of the crimes.

**International Criminal Police Organization (Interpol)**: An intergovernmental organization with 195 member countries that assists the police from all these countries in working together to make the world a safer place.

### Steps
<ol>
  <li> Data Acquisition: We will use advanced techniques such as Web Scraping and Web Crawling [or API calls] to gather relevant data. Our focus will be to extract information about criminals, their images, and the crimes committed directly from the official pages of the FBI and Interpol. This data will be subsequently used to enrich the database we built in the previous phase.</li>
  <li> API Dynamism: This is where our API evolves from a prototype to a functional system. We will establish the connection between the API and the newly updated database with the extracted data. This will allow the system to come to life and provide real-time information, offering a dynamic experience to users.</li>
</ol>

### Delivery Requirements
The delivery of this challenge will be divided into two parts:

**Part 1: Technical Documentation**<br/>
Each team should create a detailed documentation (PPT or PDF) of the Web Scraping and Web Crawling techniques they plan to use. This should include a step-by-step description of how these techniques will be implemented, the libraries that will be used, and the expected challenges during the data extraction process. Additionally, details about the database structure should also be provided.

**Part 2: Implementation and Presentation**<br/>
Upon completing the implementation, each team should provide the source code (zip) that demonstrates the data acquisition from the FBI and Interpol websites, the database update, and the integration with the API. Furthermore, prepare a presentation (video) to demonstrate how the API is now active and offering dynamic information to users (Oracle Database / Java or .NET).

Idwall's reference service 
![image](https://github.com/datatales42/challenge-idwall-all-docs/assets/69640514/e25ef7d9-bf2a-4f57-bf37-079fe3faea7f)

## 💡 Solution Architecture

**Relational Database**: Oracle 19g (from FIAP college)<br/>

**API**:<br/>
- Programming Language: Java
- Framework: Spring Boot
- Additional Libraries/Frameworks: Spring Security, Spring Data JPA, Hibernate, Spring Doc
- Dependency Manager: Maven
- Testing: Postman
- API Documentation: Swagger [YAML](https://github.com/datatales42/challenge-idwall-all-docs/blob/main/api_docs/swagger-api-doc.yaml), Swagger [Site](https://app.swaggerhub.com/apis/cgodevs/challenge-idwall/1.0.0)
  
**Data Pipeline**: ETL Model. The scripts are written in Python and are intended for periodic execution using an automation tool (suggestion: weekly, using Jenkins or Airflow).
  <ul>
    <li> <b> Extraction </b>
      <ul>
        <li>extract-fbi-api.py script: Extracts the complete FBI database and inserts it into the FBI_CRIMINALS_DATABASE table. Some identified unused columns are discarded.</li>
        <li>extract-interpol-api.py script: Extracts the complete Interpol database and inserts it into the INTERPOL_CRIMINALS_DATABASE table. It's common for nested data in some attributes to be "exploded" into new columns.</li>
      </ul>
    </li>
    <li> <b> Transformation and Loading </b>
      <ul>
        <li>transform-load.py script: Re-collects data from both FBI_CRIMINALS_DATABASE and INTERPOL_CRIMINALS_DATABASE tables into Pandas dataframes for transformations, such as renaming columns to establish identified equivalences between them or converting lists into strings of items separated by semicolons. It combines both datasets and saves the union into two different tables: one to maintain a history of criminals and another to keep the most updated list from the last execution in a production table, used for consumption by the API.
        </li>
      </ul>
    </li>
  </ul>

*Note: It's important to install the cx_Oracle Python module and the Oracle client on your machine to execute the scripts, as well as to change the path to your unzipped folder directly in the code (indication in the code itself).*



<hr>

# <img src='https://github.com/datatales42/challenge-idwall-all-docs/assets/69640514/08582651-b02a-418a-8794-5b90b91dd28a' width='30'> <img src='https://github.com/datatales42/challenge-idwall-all-docs/assets/69640514/655c122a-0724-4c5c-8478-784d668a5b35' width='30'> Descrição
Este é um repositório para exposição da entrega para um desafio apresentado pela empresa IdWall em conjunto com a faculdade FIAP, pelos membros contribuidores deste projeto. Aqui estão todos os arquivos de documentação, vídeos e scripts para popular os banco de dados.

## 🤔❓ Desafio 
### Referências de Contexto
**Anti-Money Laundering (AML)** refere-se a um conjunto de procedimentos, leis e regulamentos destinados a interromper a prática de geração ilegal de renda. Seu objetivo principal é ajudar a detectar e relatar a lavagem de dinheiro e financiamento das práticas terroristas. A AML também combate crimes como fraude de títulos e manipulação de mercado.<br/><br/>
**Federal Bureau of Investigation (FBI)**: Uma entidade norte-americana que investiga e busca pessoas ligadas a crimes. Expõe as informações de pessoas procuradas e detalhes importantes dos crimes.<br/><br/>
**International Criminal Police Organization (Interpol)**: Uma organização intergovernamental com 195 países membros e ajudamos a polícia de todos eles a trabalhar em conjunto para tornar o mundo um lugar mais seguro.<br/><br/>

### Etapas
<ol>
  <li> Aquisição de Dados: Vamos utilizar técnicas avançadas de WebScraping e WebCrawler [ou chamadas de API] para coletar dados relevantes. Nosso foco será extrair informações sobre criminosos, suas imagens e os crimes cometidos, diretamente das páginas oficiais do FBI e Interpol. Esses dados serão posteriormente utilizados para enriquecer o banco de dados que construímos na fase anterior. </li>
  <li> Dinamismo da API: Aqui é onde a nossa API evolui de um protótipo para um sistema funcional. Iremos estabelecer a conexão entre a API e o banco de dados recém-atualizado com os dados extraídos. Isso permitirá que o sistema ganhe vida e possa fornecer informações em tempo real, oferecendo uma experiência dinâmica aos usuários. </li>
</ol>

### Requisitos para entrega
A entrega deste desafio será dividida em duas partes:<br/>

**Parte 1: Documentação Técnica**<br/>
Cada equipe deve criar uma documentação detalhada (PPT ou PDF) das técnicas de WebScraping e WebCrawler que planejam utilizar. Isso deve incluir uma descrição passo a passo de como essas técnicas serão implementadas, as bibliotecas que serão utilizadas e os desafios esperados durante o processo de extração de dados. Além disso, detalhes sobre a estrutura do banco de dados também devem ser fornecidos.<br/>

**Parte 2: Implementação e Apresentação**<br/>
Após a conclusão da implementação, cada equipe deve fornecer o código-fonte (zip) que demonstre a aquisição de dados dos sites do FBI e Interpol, a atualização do banco de dados e a integração com a API. Além disso, preparem uma apresentação (vídeo) para demonstrar como a API agora está ativa e oferecendo informações dinâmicas aos usuários (Banco de Dados Oracle / Java ou .NET).<br/><br/>

Serviço análogo de referência da IdWall
![image](https://github.com/datatales42/challenge-idwall-all-docs/assets/69640514/e25ef7d9-bf2a-4f57-bf37-079fe3faea7f)


## 💡 Arquitetura da Solução

**Banco de Dados Relacional**: Oracle 19g (da faculdade FIAP)<br/>

**API**:<br/>
- Linguagem de Programação: Java
- Framework: Spring Boot
- Bibliotecas/Frameworks Adicionais: Spring Security, Spring Data JPA, Hibernate, Spring Doc
- Gerenciador de Dependências: Maven
- Testes: Postman
- Documentação da API: Swagger [YAML](https://github.com/datatales42/challenge-idwall-all-docs/blob/main/api_docs/swagger-api-doc.yaml), Swagger [Site](https://app.swaggerhub.com/apis/cgodevs/challenge-idwall/1.0.0)
  
**Pipeline de Dados**: Modelo ETL. Os scripts são escritos em python e destinados para execução periódica em ferramenta de automação (sugestão: semanal, Jenkins ou Airflow).<br/>
  <ul>
    <li> <b> Extração </b>
      <ul>
        <li>Script extract-fbi-api.py: Realiza extração da base de dados completa do FBI e os insere na tabela FBI_CRIMINALS_DATABASE. Alguma colunas sem utilidade identificada são abandonadas.</li>
        <li>Script extract-interpol-api.py: Realiza extração da base de dados completa da Interpol e os insere na tabela INTERPOL_CRIMINALS_DATABASE. Alguma colunas sem utilidade identificada são abandonadas. É comum que dados aninhados em alguns atributos sejam "explodidos" para novas colunas.</li>
      </ul>
    </li>
      <li> <b> Transformação e Carregamento </b>
      <ul>
        <li>Script transform-load.py: Recoleta os dados de ambas tabelas FBI_CRIMINALS_DATABASE e INTERPOL_CRIMINALS_DATABASE em dataframes pandas para realizar transformações, como renomear suas colunas para estabelecer as equivalências identificadas entre ambas ou converter listas para strings de itens separados por ponto e vírgula. Faz a união de ambas e salva a união em 2 tabelas diferentes: uma para manter o histórico de criminosos, outra para manter a lista mais atualizada da última execução em uma tabela de produção, utilizada para consumo pela API.
        </li>
      </ul>
    </li>
  </ul>

*Obs.: É importante instalar o módulo python cx_Oracle e o client Oracle em sua máquina para conseguir executar os scripts, assim como alterar o caminho para sua pasta descompactada diretamente no código (indicação no próprio código).* <br/>
