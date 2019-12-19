import time
import pandas as pd
import numpy as np
from datetime import date


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
df=CITY_DATA

def get_filters(welcome=True):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #Welcome message isn't displayed if user input is incorrect and the user is asked to reenter information"
    if welcome:
        print('Hello! Let\'s explore some US bikeshare data!')

    city=input("Which city would you like to explore?").lower().strip()

    month=input("Which month are you going to explore; January, February, March, April, May or June?").lower().strip()

    day=input("Which day of the week are you going to explore?").lower().strip()
    return [city, month, day]


def load_data(city, month, day):
    """
    Creates a dataframe with filtered data based on user input.
    If user input is incorrect or other than expected an empty object None is returned instead of a dataframe.
    """

    # load data from the correct csv file based on user choice #
    if city in CITY_DATA:
        folder='/Users/theresesvensson/Documents/Other projects/Udacity/bikeshare-2/'
        path=folder+CITY_DATA[city]
        df=pd.read_csv(path)
    else:
        print('No data available for {}. Please choose between chicago, washington, new york city. Please make sure your spelling is correct.'.format(city))
        return None
    # convert the Start Time column to datetime
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    # controll that user input is correct #
    if month in months:
        pass
    else:
        print('No data available for {}. Please choose between the available months. Please make sure your spelling is correct.'.format(month))
        return None
    if day in ['monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']:
        pass
    else:
        print('No data available for {}. Please make sure your spelling is correct'.format(day))
        return None
    # extract month and day of week from Start Time to create new columns #
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    month=months.index(month)+1
    df=df[df['month']==month]
    df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations."""

    print('\nCalculating The Most Popular Stations...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station=df['Start Station']
    print('The most popular start station in {} on {}s in {} is: '.format(city, day, month))
    print(start_station.value_counts().head(1))

    # display most commonly used end station
    end_station=df['End Station']
    print('The most popular end station in {} on {}s in {} is: '.format(city, day, month))
    print(end_station.value_counts().head(1))

    # display most frequent combination of start station and end station trip
    mytable = df.groupby(['Start Station','End Station']).size()
    pop_stations=df.groupby(['Start Station','End Station']).size().reset_index().rename(columns={0:'count'})
    most_popular=pop_stations.sort_values(by='count', ascending=False).head(1)
    print('The most popular trip is:')
    print(most_popular)

    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_duration=df['Trip Duration']
    print('The total travel time for {}s in {} in {} is {} seconds'.format(day, month, city, int(sum(trip_duration))))

    corr_days=sum(trip_duration)/(60*60*24)
    print('This corresponds to {} days'.format(int(corr_days)))

    # display mean travel time
    print('The avarage travel time per trip for the choosen period is {0:.0f} seconds'.format((sum(trip_duration)/len(trip_duration))))


    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The distribution of users using our service in this period is the following:')
    print(df['User Type'].value_counts())


    # Display counts of gender
    if city != 'washington':
        most_common_gender=df['Gender'].mode().values
        print('Most of our users in this period are {}'.format(most_common_gender))
        # Display earliest, most recent, and most common year of birth
        today=date.today()
        latest_byear=df['Birth Year'].max()
        earliest_byear=df['Birth Year'].min()
        most_common_byear=df['Birth Year'].mode().values
        print('The most senior user during the choosen period was born {0:.0f}'.format(earliest_byear))
        print('The youngest user during the choosen period was born {0:.0f}'.format(latest_byear))
        print('Our service seem to be most popular among users born in {} based upon that is the most common birth year among users during the choosen period'.format(most_common_byear))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def passenger_stats(df,city):
    """
    Calculates the mean age of passengers travelling during the period choosen by the user
    """
    if city != 'washington':
        print('\nCalculating statistics about travellers...\n')
    #Calculate the avarage birth date, thereafter calculate how old people born that year are today #
        today=date.today()
        accum_age=0
        agelist=[]
        mean_birth_year=df['Birth Year'].mean()
        age=today.year - mean_birth_year
        print('The avarage age for passengers travelling during this period in this region is {0:.0f} years'.format(age))


def main():
    #First time when called apon; define df and set display welcome message variable to true. #
    #This so that welcome message isn't displayed if user makes a mistake and has to reenter values#
    df=None
    disp_welcome_msg=True
    #While loop to give users the possiblity to reenter values when incorrect input has been recognized #
    while df is None:
        input=get_filters(welcome=disp_welcome_msg)
        city, month, day = input
        disp_welcome_msg=False
        df=load_data(city,month,day)
    station_stats(df, city, month, day)
    trip_duration_stats(df, city, month, day)
    user_stats(df,city)
    passenger_stats(df,city)
    #print(df.head(5))



if __name__ == "__main__":
  	main()
