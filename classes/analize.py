''' Functions to analyze the results of the simulation
'''

import pandas as pd

from settings import SimulationSettings, GameSettings, LogSettings


class Analyzer:
    ''' Functions to analized games after the simulation
    '''

    def __init__(self):
        self.df = pd.read_csv(LogSettings.data_log_file, sep='\t')

    def remaining_players(self):
        ''' How many games had clear winner, how many players remain in tha end
        '''
        grouped = self.df.groupby('game_number').size().reset_index(name='Losers')
        result = grouped['Losers'].value_counts().reset_index()

        # {remaining players: games}
        remaining_players = {len(GameSettings.players_list) - row['Losers']: row['count']
                             for index, row in result.iterrows()}
        # Add games with no losers (all players remained)
        remaining_players[len(GameSettings.players_list)] = \
            SimulationSettings.n_games - sum(remaining_players.values())

        # Games with clear winner (1 player remains)
        clear_winner = remaining_players[1]
        print(f"Games that had clear winner: {clear_winner} / {SimulationSettings.n_games} " +
               f"({100 * clear_winner / SimulationSettings.n_games:.1f}%)")

        # Number of players by the end of simulation
        print(f"Number of remaining players after: {SimulationSettings.n_moves} turns:")
        for remaining, count in sorted(remaining_players.items()):
            print(f"  - {remaining}: {count} ({count * 100 / SimulationSettings.n_games:.1f}%)")

    def median_gamelength(self):
        ''' Median gamelength (for all an dfinite games)
        '''
        grouped = self.df.groupby('game_number')
        filtered_groups = grouped.filter(lambda x: len(x) == len(GameSettings.players_list) - 1)
        lengths_df = filtered_groups.groupby('game_number')['turn'].max().reset_index()
        lengths = lengths_df["turn"].tolist()
        all_lengths = lengths + [SimulationSettings.n_moves
                                 for _ in range(SimulationSettings.n_games - len(lengths))]
        if lengths:
            print(f"Median game length (for finished games): {lengths[len(lengths)//2]}")
        print(f"Median game length (for all games): {all_lengths[len(all_lengths)//2]}")

    def winning_rate(self):
        ''' Display winning (survival) rate of players
        '''
        loses_counts = self.df.groupby('player').size().reset_index(name='count')

        # {player: games_survived}
        survival_rate = {row['player']: row['count']
                             for index, row in loses_counts.iterrows()}
        print("Players' survival rate:")
        for player_name, loses in sorted(survival_rate.items()):
            survivals = SimulationSettings.n_games - loses
            surv_rate = survivals / SimulationSettings.n_games
            margin = 1.96 * (surv_rate * (1 - surv_rate) / SimulationSettings.n_games) ** 0.5
            print(f"  - {player_name}: {survivals} " +
                  f"({surv_rate * 100:.1f} "
                  f"+- {margin * 100:.1f}%)")

