import pandas as pd
from services.classes import MajorsPlayerStats, MajorsTeamStats


def main():
    majors = pd.read_csv('data/majors.csv', index_col=0)
    majors_player_stats = MajorsPlayerStats(stats_path='data/majors_player_stats.csv',
                                            css_path='css/player_stats.css')
    majors_team_stats = MajorsTeamStats(stats_path='data/majors_team_stats.csv',
                                        css_path='css/team_stats.css')

    majors_player_stats.get_majors_dfis(majors=majors,
                                        dir_path='img/player_stats')
    majors_team_stats.get_majors_dfis(majors=majors,
                                      dir_path='img/team_stats')


if __name__ == '__main__':
    main()
