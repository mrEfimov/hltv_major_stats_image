import pandas as pd
from pandas import DataFrame
from pandas.io.formats.style import Styler
import dataframe_image as dfi
from abc import ABC, abstractmethod

from services.functions import get_css_styles


class MajorsStats(ABC):
    """Abstract class that defines base methods for interacting with Major statistics"""
    def __init__(
            self,
            stats_path: str,
            css_path: str
    ) -> None:
        self.df: DataFrame = pd.read_csv(stats_path)
        self.css: list[dict[str, str]] = get_css_styles(css_path)

    @staticmethod
    def _drop_invalid_rating(
            df: DataFrame
    ) -> DataFrame:
        """Return the DataFrame w/o rating column that wasn't used during this Major"""
        if any(df.loc[:, 'Rating1.0'].isna()):
            return df.drop(columns=['Rating1.0'])
        return df.drop(columns=['Rating2.0'])

    @staticmethod
    def _style_df(
            styler: Styler,
            major_name: str
    ) -> Styler:
        """Return Styler that makes DataFrame prettier"""
        styler.set_caption(major_name)
        styler.hide(axis=0)
        styler.hide(axis=1, subset='Event ID')
        styler.format(precision=2)
        styler.map(lambda v:
                   'color: #09c100;' if (isinstance(v, float) and v >= 1.05) or (isinstance(v, int) and v > 0) else
                   'color: #fc1d1d;' if (isinstance(v, float) and v <= 0.95) or (isinstance(v, int) and v < 0) else
                   'color: #929a9e')
        return styler

    @abstractmethod
    def get_major_dfi(
            self,
            major_id: int,
            majors_df: DataFrame,
            dir_path: str
    ) -> None:
        """Export Major player/team stats DataFrame into file"""
        ...

    def get_majors_dfis(
            self,
            majors: DataFrame,
            dir_path: str
    ) -> None:
        """Export player/team stats DataFrame of all Majors into file"""
        major_ids = majors.index
        for major_id in major_ids:
            self.get_major_dfi(major_id=major_id,
                               majors_df=majors,
                               dir_path=dir_path)


class MajorsTeamStats(MajorsStats):
    """A class that allows you to interact with TEAM statistics"""
    def _style_df(
            self,
            styler: Styler,
            major_name
    ) -> Styler:
        super()._style_df(styler, major_name)
        styler.set_table_styles(self.css)
        return styler

    def get_major_dfi(
            self,
            major_id: int,
            majors_df: DataFrame,
            dir_path: str
    ) -> None:
        df: DataFrame = self.df.loc[self.df.loc[:, 'Event ID'] == major_id]
        correct_df: DataFrame = self._drop_invalid_rating(df)
        major_name: str = majors_df.loc[major_id, 'Event']
        df_style: Styler | DataFrame = self._style_df(correct_df.style, major_name)
        dfi.export(obj=df_style,
                   filename=f'{dir_path}/{major_id}_team_stats.png',
                   dpi=250)


class MajorsPlayerStats(MajorsStats):
    """A class that allows you to interact with PLAYER statistics"""
    def _style_df(
            self,
            styler: Styler,
            major_name
    ) -> Styler:
        super()._style_df(styler, major_name)
        styler.hide(axis=1, subset=['Event ID', 'Rounds'])
        styler.set_table_styles(self.css)
        return styler

    def get_major_dfi(
            self,
            major_id: int,
            majors_df: DataFrame,
            dir_path: str
    ) -> None:
        df: DataFrame = self.df.loc[self.df.loc[:, 'Event ID'] == major_id]
        correct_df: DataFrame = self._drop_invalid_rating(df)
        major_name: str = majors_df.loc[major_id, 'Event']
        for slice_index, df_slice in enumerate([slice(16),
                                                slice(16, 32),
                                                slice(32, 48),
                                                slice(48, 64),
                                                slice(64, df.shape[0])], start=1):
            correct_df_slice: DataFrame = correct_df.iloc[df_slice]
            df_style: Styler | DataFrame = self._style_df(correct_df_slice.style, major_name)
            dfi.export(obj=df_style,
                       filename=f'{dir_path}/{major_id}_{slice_index}_player_stats.png',
                       dpi=250)
