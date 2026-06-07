# 🎲 Bot Telegram - Baccarat (Bác Bộ)

Bot inteligente do Telegram para jogar Baccarat com análise ao vivo e recomendações de apostas.

## 🎯 Funcionalidades

- **Análise ao vivo**: Avalia a sequência de mãos e identifica padrões
- **Recomendação de lado**: Sugere se deve apostar no Banqueiro, Jogador ou Empate
- **Suporte a dados**: Rastreia histórico de mãos e gera estatísticas
- **Simulação de cartas**: Embaralha e distribui cartas realistas
- **Pontuação Baccarat**: Cálculo automático de pontos (módulo 10)

## 📋 Comandos

- `/start` - Inicia o bot
- `/jogar` - Começa uma nova mão
- `/analise` - Mostra análise da sequência atual
- `/recomendacao` - Recomendação baseada em padrões
- `/historico` - Mostra últimas 10 mãos
- `/stats` - Estatísticas gerais
- `/reset` - Limpa o histórico
- `/ajuda` - Mostra todos os comandos

## 🚀 Deploy no Render

1. Acesse render.com
2. Conecte seu repositório GitHub
3. Crie um novo **Web Service**
4. Configure a variável de ambiente:
   - `TELEGRAM_BOT_TOKEN=8698797816:AAHANQTdKwZ5pGL-1fpZKIVmldgUg6vhBo0`
5. Deploy!

## 📊 Análise do Jogo

O bot analisa:
- Sequência de vitórias (Banqueiro vs Jogador)
- Taxa de Empates
- Padrões de Alternância
- Tendências recentes (últimas 20 mãos)
- Recomendação ponderada com confiança

## 🎲 Regras do Baccarat

- **Objetivo**: Acertar qual lado terá mais pontos (0-9)
- **Pontuação**: Soma das cartas módulo 10
- **Lados**: 🏦 Banqueiro, 🎲 Jogador, 🤝 Empate
- **Cartas**: A=1, 2-9=valor, 10/J/Q/K=0

---

Desenvolvido para análise inteligente de Baccarat! 🎯