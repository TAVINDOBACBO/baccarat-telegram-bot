import random
from collections import defaultdict
from datetime import datetime

class BaccaratGame:
    """Lógica do jogo Baccarat com análise ao vivo"""
    
    def __init__(self):
        self.deck = self._create_deck()
        self.history = []
        self.banker_wins = 0
        self.player_wins = 0
        self.ties = 0
        self.streaks = defaultdict(int)
        self.current_streak = None
        self.max_banker_streak = 0
        self.max_player_streak = 0
    
    def _create_deck(self):
        """Cria um baralho de 8 decks (padrão Baccarat)"""
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = []
        for _ in range(8):  # 8 decks
            for suit in suits:
                for rank in ranks:
                    deck.append((rank, suit))
        random.shuffle(deck)
        return deck
    
    def _card_value(self, card):
        """Retorna o valor da carta (0-9)"""
        rank = card[0]
        if rank == 'A':
            return 1
        elif rank in ['J', 'Q', 'K', '10']:
            return 0
        else:
            return int(rank)
    
    def _calculate_score(self, cards):
        """Calcula a pontuação (módulo 10)"""
        total = sum(self._card_value(card) for card in cards)
        return total % 10
    
    def _format_cards(self, cards):
        """Formata as cartas para exibição"""
        return ' '.join([f"{card[0]}{card[1]}" for card in cards])
    
    def play_hand(self):
        """Joga uma nova mão de Baccarat"""
        if len(self.deck) < 20:
            self.deck = self._create_deck()
        
        # Distribuir cartas
        banker_cards = [self.deck.pop(), self.deck.pop()]
        player_cards = [self.deck.pop(), self.deck.pop()]
        
        banker_score = self._calculate_score(banker_cards)
        player_score = self._calculate_score(player_cards)
        
        # Lógica de terceira carta
        if player_score <= 5:
            player_cards.append(self.deck.pop())
            player_score = self._calculate_score(player_cards)
            player_drew = True
        else:
            player_drew = False
        
        if player_drew:
            third_card_value = self._card_value(player_cards[-1])
            if banker_score <= 2:
                banker_cards.append(self.deck.pop())
                banker_score = self._calculate_score(banker_cards)
            elif banker_score == 3 and third_card_value != 8:
                banker_cards.append(self.deck.pop())
                banker_score = self._calculate_score(banker_cards)
            elif banker_score == 4 and third_card_value in [2, 3, 4, 5, 6, 7]:
                banker_cards.append(self.deck.pop())
                banker_score = self._calculate_score(banker_cards)
            elif banker_score == 5 and third_card_value in [4, 5, 6, 7]:
                banker_cards.append(self.deck.pop())
                banker_score = self._calculate_score(banker_cards)
            elif banker_score == 6 and third_card_value in [6, 7]:
                banker_cards.append(self.deck.pop())
                banker_score = self._calculate_score(banker_cards)
        else:
            if banker_score <= 5:
                banker_cards.append(self.deck.pop())
                banker_score = self._calculate_score(banker_cards)
        
        # Determinar vencedor
        if banker_score > player_score:
            winner = 'banker'
            self.banker_wins += 1
            new_streak = 'banker'
        elif player_score > banker_score:
            winner = 'player'
            self.player_wins += 1
            new_streak = 'player'
        else:
            winner = 'tie'
            self.ties += 1
            new_streak = 'tie'
        
        # Atualizar streak
        if new_streak != self.current_streak:
            if new_streak == 'banker':
                self.streaks['banker'] = 1
                self.max_banker_streak = max(self.max_banker_streak, 1)
            elif new_streak == 'player':
                self.streaks['player'] = 1
                self.max_player_streak = max(self.max_player_streak, 1)
            self.current_streak = new_streak
        else:
            if new_streak == 'banker':
                self.streaks['banker'] += 1
                self.max_banker_streak = max(self.max_banker_streak, self.streaks['banker'])
            elif new_streak == 'player':
                self.streaks['player'] += 1
                self.max_player_streak = max(self.max_player_streak, self.streaks['player'])
        
        result = {
            'banker_cards': self._format_cards(banker_cards),
            'banker_score': banker_score,
            'player_cards': self._format_cards(player_cards),
            'player_score': player_score,
            'winner': winner,
            'timestamp': datetime.now()
        }
        
        self.history.append(result)
        return result
    
    def analyze(self):
        """Analisa a sequência de mãos"""
        if not self.history:
            return {
                'total_hands': 0,
                'banker_wins': 0,
                'player_wins': 0,
                'ties': 0,
                'banker_pct': 0,
                'player_pct': 0,
                'tie_pct': 0,
                'pattern': 'Nenhuma mão jogada ainda',
                'last_5': []
            }
        
        total = len(self.history)
        
        # Padrão das últimas 5
        last_5 = []
        for hand in self.history[-5:]:
            if hand['winner'] == 'banker':
                last_5.append('🏦')
            elif hand['winner'] == 'player':
                last_5.append('🎲')
            else:
                last_5.append('🤝')
        
        # Detectar padrão
        if len(self.history) >= 3:
            recent = [h['winner'] for h in self.history[-3:]]
            if recent[0] == recent[1] == recent[2]:
                if recent[0] == 'banker':
                    pattern = "🏦🏦🏦 Sequência de Banqueiro!"
                else:
                    pattern = "🎲🎲🎲 Sequência de Jogador!"
            elif recent[0] != recent[1] and recent[1] != recent[2] and recent[0] != recent[2]:
                pattern = "🎲🏦🎲 Padrão Alternado"
            else:
                pattern = "📊 Padrão Misto"
        else:
            pattern = "📊 Aguardando mais dados..."
        
        return {
            'total_hands': total,
            'banker_wins': self.banker_wins,
            'player_wins': self.player_wins,
            'ties': self.ties,
            'banker_pct': (self.banker_wins / total * 100) if total > 0 else 0,
            'player_pct': (self.player_wins / total * 100) if total > 0 else 0,
            'tie_pct': (self.ties / total * 100) if total > 0 else 0,
            'pattern': pattern,
            'last_5': last_5
        }
    
    def get_recommendation(self):
        """Retorna recomendação de aposta baseada em análise"""
        if len(self.history) < 5:
            return {
                'recommendation': '🤷 AGUARDE',
                'confidence': 0,
                'reason': 'Precisa de mais de 5 mãos para análise confiável.'
            }
        
        # Análise das últimas 20 mãos
        recent_hands = self.history[-20:]
        recent_banker = sum(1 for h in recent_hands if h['winner'] == 'banker')
        recent_player = sum(1 for h in recent_hands if h['winner'] == 'player')
        recent_ties = sum(1 for h in recent_hands if h['winner'] == 'tie')
        
        # Checkar sequência atual
        if self.current_streak == 'banker' and self.streaks['banker'] >= 2:
            recommendation = '🏦 BANQUEIRO'
            confidence = min(70 + self.streaks['banker'] * 5, 90)
            reason = f"Sequência de Banqueiro em andamento ({self.streaks['banker']} mãos)"
        elif self.current_streak == 'player' and self.streaks['player'] >= 2:
            recommendation = '🎲 JOGADOR'
            confidence = min(70 + self.streaks['player'] * 5, 90)
            reason = f"Sequência de Jogador em andamento ({self.streaks['player']} mãos)"
        elif recent_banker > recent_player + 2:
            recommendation = '🏦 BANQUEIRO'
            confidence = 65
            reason = f"Tendência: Banqueiro venceu {recent_banker} das últimas 20"
        elif recent_player > recent_banker + 2:
            recommendation = '🎲 JOGADOR'
            confidence = 65
            reason = f"Tendência: Jogador venceu {recent_player} das últimas 20"
        else:
            recommendation = '🏦 BANQUEIRO'
            confidence = 50
            reason = "Sem padrão claro. Banqueiro tem ligeira vantagem estatística."
        
        return {
            'recommendation': recommendation,
            'confidence': confidence,
            'reason': reason
        }
    
    def get_history(self):
        """Retorna histórico formatado"""
        formatted = []
        for i, hand in enumerate(self.history, 1):
            if hand['winner'] == 'banker':
                emoji = '🏦'
                winner = 'BANQUEIRO'
            elif hand['winner'] == 'player':
                emoji = '🎲'
                winner = 'JOGADOR'
            else:
                emoji = '🤝'
                winner = 'EMPATE'
            
            formatted.append(f"{emoji} Mão {i}: {winner} ({hand['banker_score']}-{hand['player_score']})")
        
        return formatted
    
    def get_stats(self):
        """Retorna estatísticas"""
        total = len(self.history)
        
        return {
            'total': total,
            'banker': self.banker_wins,
            'player': self.player_wins,
            'ties': self.ties,
            'banker_pct': (self.banker_wins / total * 100) if total > 0 else 0,
            'player_pct': (self.player_wins / total * 100) if total > 0 else 0,
            'tie_pct': (self.ties / total * 100) if total > 0 else 0,
            'max_banker_streak': self.max_banker_streak,
            'max_player_streak': self.max_player_streak
        }