import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from flask import Flask, request
from game import BaccaratGame
import json

# Carregar variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
RENDER_URL = os.getenv('RENDER_URL', 'https://baccarat-telegram-bot.onrender.com')

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Dicionário global para rastrear usuários
user_games = {}
application = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia o bot"""
    user_id = update.effective_user.id
    user_games[user_id] = BaccaratGame()
    
    welcome = """
🎲 Bem-vindo ao Bot Baccarat! 🎲

Aqui você pode:
✅ Jogar Baccarat com análise ao vivo
✅ Receber recomendações inteligentes
✅ Ver padrões e tendências
✅ Acompanhar histórico de mãos

Use /ajuda para ver todos os comandos!
    """
    await update.message.reply_text(welcome)

async def jogar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Começa uma nova mão"""
    user_id = update.effective_user.id
    if user_id not in user_games:
        user_games[user_id] = BaccaratGame()
    
    game = user_games[user_id]
    result = game.play_hand()
    
    message = f"""
🎴 NOVA MÃO 🎴

📊 Banqueiro: {result['banker_cards']} = {result['banker_score']} pontos
🎲 Jogador: {result['player_cards']} = {result['player_score']} pontos

🏆 RESULTADO:
"""
    
    if result['winner'] == 'banker':
        message += "🏦 BANQUEIRO VENCE!"
    elif result['winner'] == 'player':
        message += "🎲 JOGADOR VENCE!"
    else:
        message += "🤝 EMPATE!"
    
    await update.message.reply_text(message)

async def analise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Análise ao vivo da sequência"""
    user_id = update.effective_user.id
    if user_id not in user_games:
        user_games[user_id] = BaccaratGame()
    
    game = user_games[user_id]
    analysis = game.analyze()
    
    message = f"""
📈 ANÁLISE AO VIVO 📈

Total de mãos: {analysis['total_hands']}

🏦 Vitórias Banqueiro: {analysis['banker_wins']} ({analysis['banker_pct']:.1f}%)
🎲 Vitórias Jogador: {analysis['player_wins']} ({analysis['player_pct']:.1f}%)
🤝 Empates: {analysis['ties']} ({analysis['tie_pct']:.1f}%)

📊 Padrão Atual:
{analysis['pattern']}

Últimas 5 mãos: {' → '.join(analysis['last_5'])}
    """
    
    await update.message.reply_text(message)

async def recomendacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recomendação de aposta baseada em análise"""
    user_id = update.effective_user.id
    if user_id not in user_games:
        user_games[user_id] = BaccaratGame()
    
    game = user_games[user_id]
    rec = game.get_recommendation()
    
    message = f"""
🎯 RECOMENDAÇÃO DE APOSTA 🎯

👉 Aposte em: {rec['recommendation']}
📊 Confiança: {rec['confidence']:.0f}%

Análise:
{rec['reason']}

⚠️ Lembre-se: Isto é análise estatística, não garantia!
    """
    
    await update.message.reply_text(message)

async def historico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra histórico das últimas mãos"""
    user_id = update.effective_user.id
    if user_id not in user_games:
        user_games[user_id] = BaccaratGame()
    
    game = user_games[user_id]
    history = game.get_history()
    
    if not history:
        await update.message.reply_text("📋 Nenhuma mão jogada ainda!")
        return
    
    message = "📋 HISTÓRICO DE MÃOS 📋\n\n"
    for i, hand in enumerate(history[-10:], 1):
        message += f"{i}. {hand}\n"
    
    await update.message.reply_text(message)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra estatísticas gerais"""
    user_id = update.effective_user.id
    if user_id not in user_games:
        user_games[user_id] = BaccaratGame()
    
    game = user_games[user_id]
    stats = game.get_stats()
    
    message = f"""
📊 ESTATÍSTICAS 📊

Total de mãos: {stats['total']}
🏦 Banqueiro: {stats['banker']} vitórias
🎲 Jogador: {stats['player']} vitórias
🤝 Empates: {stats['ties']}

Maior sequência Banqueiro: {stats['max_banker_streak']}
Maior sequência Jogador: {stats['max_player_streak']}

Taxa de vitória Banqueiro: {stats['banker_pct']:.1f}%
Taxa de vitória Jogador: {stats['player_pct']:.1f}%
Taxa de Empates: {stats['tie_pct']:.1f}%
    """
    
    await update.message.reply_text(message)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reseta o histórico"""
    user_id = update.effective_user.id
    user_games[user_id] = BaccaratGame()
    await update.message.reply_text("✅ Histórico limpo! Comece uma nova sessão com /jogar")

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra ajuda com todos os comandos"""
    help_text = """
🎮 COMANDOS DO BOT 🎮

/start - Inicia o bot
/jogar - Começa uma nova mão
/analise - Análise ao vivo da sequência
/recomendacao - Recomendação de aposta 👈 PRINCIPAL
/historico - Últimas 10 mãos jogadas
/stats - Estatísticas gerais
/reset - Limpa o histórico
/ajuda - Mostra esta mensagem

💡 DICAS:
1. Use /jogar para simular novas mãos
2. Use /analise para ver os padrões
3. Use /recomendacao para obter sugestões inteligentes
4. Mantenha histórico com /historico

⚠️ AVISO IMPORTANTE:
Este bot faz análise estatística baseada em padrões passados.
NÃO é uma garantia de ganho. Use com responsabilidade! 🎯
    """
    await update.message.reply_text(help_text)

# Webhook
@app.route(f'/{TOKEN}', methods=['POST'])
async def webhook():
    """Recebe updates do Telegram via webhook"""
    try:
        data = request.get_json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return 'ok', 200
    except Exception as e:
        logger.error(f'Erro no webhook: {e}')
        return 'error', 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return {'status': 'ok'}, 200

@app.route('/', methods=['GET'])
def index():
    """Index"""
    return 'Bot Baccarat rodando! 🎲', 200

async def set_webhook():
    """Configura o webhook"""
    await application.bot.set_webhook(url=f'{RENDER_URL}/{TOKEN}')
    logger.info(f'Webhook configurado: {RENDER_URL}/{TOKEN}')

def init_app():
    """Inicializa o bot e o Flask"""
    global application
    
    application = Application.builder().token(TOKEN).build()

    # Handlers dos comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jogar", jogar))
    application.add_handler(CommandHandler("analise", analise))
    application.add_handler(CommandHandler("recomendacao", recomendacao))
    application.add_handler(CommandHandler("historico", historico))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("ajuda", ajuda))
    
    logger.info("Bot inicializado com webhook!")
    
    return app

# Inicializa para o Gunicorn
if __name__ != '__main__':
    app = init_app()
    logger.info("App criado para Gunicorn")

if __name__ == '__main__':
    app = init_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
