import math
import pandas as pd
import numpy as np
import datetime as dt

pd.set_option('display.max_columns', None)


def ds_demand_cat(df):
    # note: Mere modified this so it would take a df (so we can drop Nov DST before aggregating)
    """
    **(Downstream Demand - Categorized)**: 
    This function takes a dataframe containing the hourly consumption 
    and zoning category (resdential, business, or commercial) of each meter in a specific portion of the grid 
    (usually specfied by taking all meters downstream of a certain transformer), 
    where the hourly consumption appears in the column `kWh` 
    and the zoning category appears in the column `type_of_consumer`. 
    It returns a `pandas` dataframe with three columns indexed by hour: 
    `ds_kWh_comm` (total commercial/business consumption downstream of a given meter), 
    `ds_kWh_res` (total residential consumption downstream of a given meter), and 
    `ds_kWh_ind` (total industrial consumption downstream of a specfic meter.) 
    It would be possible to restrict (e.g.) to residential consumers 
    by using a command like `ds_demand_cat(sql_query)['ds_kWh_res']`.
    """
    # This line switches over to the DataFrame() that returns three columns.
    df = df.groupby(['timestamp', 'type_of_consumer'])['kWh'].sum().reset_index()\
            .pivot(index=['timestamp'], columns='type_of_consumer', values='kWh')\
            .rename_axis(None, axis=1).reindex(columns=['business', 'residential', 'industrial'], fill_value=0)\
            .rename(columns = {'business': 'comm', 'residential':'res', 'industrial':'ind'}).add_prefix('ds_kWh_')
    return df

# a rolling average
def avg(df, period = 'M'):
    """
    **(Averaging Function)**: 
    Takes (i) a data frame with integer entries and (ii) an averaging period (either 'M' for monthly or 'kD' where k is numeric for every k days).
    Returns a data frame of averages which is indexed by the midpoint of each averaging period (or the rough midpoint in the monthly case). 
    This can accept dataframes with any column names, and adds a period+`_avg_` prefix to the columns. 
    Default behaviour (i.e. if we only give the `df` argument) is to return monthly averages.
    """
    if period == 'M': 
        av = df.resample(period).mean().add_prefix(period + '_avg_').apply(lambda x: x.shift(-15, freq='D'))
    if len(period) == 1 and period[-1] == 'D': 
        av = df.resample(period).mean().add_prefix(period + '_avg_')\
                .apply(lambda x: x.shift(12, freq='H'))
    if len(period) > 1 and period[-1] == 'D': 
        av = df.resample(period).mean().add_prefix(period + '_avg_')\
                .apply(lambda x: x.shift(int(period[:-1])*12, freq='H'))


# choose and manipulate relevant data from a df:

def get_timeframe():
    # User input for the time frame.
    user_start = input('Enter start date: ')
    user_end = input('Enter end date (inclusive): ')

    start_date = pd.to_datetime(user_start)
    end_date = pd.to_datetime(user_end) + dt.timedelta(hours=23)

    return (start_date, end_date)

def timeframe_df(df, start_date, end_date):
    """
    Takes a dataframe of usage data indexed by timestamp
    and returns a copy dataframe with added columns for
        year
        week of year
        hour of week
    """
    # choose the time series from the aggregated residential data 
    # that is in this time frame:
    tf_usage = df[start_date:end_date].copy().reset_index()

    # add in relevant columns to consider weeks and hour of week for the shift
    tf_usage['week'] = tf_usage.timestamp.dt.isocalendar().week
    tf_usage['isoyear'] = tf_usage.timestamp.dt.isocalendar().year
    tf_usage['weekhour'] = tf_usage['timestamp'].dt.dayofweek*24\
                            + tf_usage['timestamp'].dt.hour
    
    return tf_usage

def pivot_strip_spare(df):
    """
    Takes a dataframe containing usage data as 'kWh' and columns for
        year
        week of year
        hour of week
    and returns a tuple containing
        a pivot table of usage data with hour of the week as columns
        and week of the year as rows, stripping out spare days so there is no NaN
        (If the start date isn't on a Monday and/or the end date isn't on a Sunday,
        this pivot table will contain NaN for the missing usage. We drop those partial weeks)
    and
        a df containing usage data from the spare days dropped from the pivot table
    """
    # make a pivot table:
    df_pivot = df.pivot_table('kWh', 
                                index=['week','isoyear'], 
                                columns='weekhour')
    
    # check if first and last weeks are full weeks,
    # if not, filter out from full ts so we can potentially 
    # do a daily shift on those days.
    # potentially need to worry about other weeks too, 
    # but I think not in this dataset
    # so I'm reducing the number of potential loops by 
    # just checking first and last
    spare_days = pd.DataFrame()
    first_week_no = min(df.week.unique())
    last_week_no = max(df.week.unique())
    for weekno in [first_week_no, last_week_no]:
        if df_pivot.loc[weekno,:,:].isnull().values.any():
            # Preserve spare days
            spare_days = pd.concat([spare_days, df[(df['week'] == weekno)]])
            # Drop partial weeks
            df_pivot.drop(weekno, axis=0, inplace=True)
                
    # to handle other potential missing values (eg DST), interpolate
    # between columns (since those are the hours)
    # df_pivot.interpolate(axis=1, inplace=True)
    # alternatively, just fill with zeros
    df_pivot.fillna(0, inplace=True)
    
    return (spare_days, df_pivot)


# interesting aggregations

def daily_max(df):
    """
    **(Daily Maximum)**: 
    Takes a time-indexed dataframe, with numerical entries and whose timestamps occur at least once daily (e.g. hourly works), 
    and returns a data frame of daily maxima which is indexed by the day. 
    Note that this takes the daily maximum of each column, 
    so there's no need to expect that (for example) the daily maximum consumption 
    and the daily maximum anomaly occur at precisely the same hour. 
    """
    return df.groupby(pd.Grouper(freq='D')).max().add_prefix('max_')

def daily_tot(df):
    """
    **(Daily Total)**: Takes a time-indexed dataframe, with numerical entries 
    and whose timestamps occur at least once daily (e.g. hourly works), and returns a data frame, 
    indexed by day, whose entries are the sums of the absolute values of the entries of the original dataframe 
    over the relevant time period. 
    This is useful, for example, when dealing with anomalies, 
    as the daily total of a given day represents twice the amount of consumption 
    which would need to be shifted from high-consumption hours to low-consumption hours 
    in order to achieve totally flat/constant consumption over the course of a day. 
    """
    return df.abs().groupby(pd.Grouper(freq = 'D')).sum().add_prefix('tot_')

def avg_week(df):
    """
    **(Average for Each Hour in a Week)**: Takes a time-indexed dataframe, whose timestamps occur hourly,
      and returns a dataframe with 168 rows, where each row corresponds to an hour of the week. 
      The entries of this new dataframe are averages of the original dataframe over the given hour 
      (for example, entry 8 will correspond to an average over all Monday 8AMs which appear in the dataset).
    Defined by Mo
    """
    df['weekhour'] = df.index.dayofweek*24 + df.index.hour
    df = df.groupby(['weekhour']).mean().reset_index().set_index('weekhour')
    return df