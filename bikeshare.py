import time
import pandas as pd
import numpy as np
import glob

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze, or "all" to apply no filter on city
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hey there! Time for digging some bikeshare data!')

    #Gets user's input for city (chicago, new york city, washington or all)
    cities = list(CITY_DATA.keys())
    cities.append('all')
    city = input('\nWould you like to filter the data by city? \n\nSelect from Chicago, New York, Washington or all? >> ').lower()
    #Handles not supported inputs by the user
    while city not in cities:
        city = input('\nThat\'s not a valid city. \n\nPlease, enter Chicago, New York, Washington or all. >> ')

    #Gets user's input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input('\nWould you like to filter the data by month? \n\nSelect from January, February, March, April, May, June or all. >> ').lower()
    #Handles not supported inputs by the user
    while month not in months:
        month = input('\nThat\'s not a valid month. \n\nPlease, select from January, February, March, April, May, June or all. >> ')

    #Gets user's input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = input('\nWould you like to filter the data by day? \n\nSelect from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all. >> ').lower()
    #Handles not supported inputs by the user
    while day not in days:
        day = input('\nThat\'s not a valid entry. \n\nSelect from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all. >> ')

    print("_"*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city or cities and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze or "all" if no filter is applicable
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day, if applicable
    """

    #Loads data from all cities if user chooses no filter
    if city == 'all':
        df = pd.concat([pd.read_csv(f) for f in glob.glob('*.csv')], ignore_index = True, sort=False)
    #Loads data from specified city
    else:
        df = pd.read_csv(CITY_DATA[city])

    #Converts the Start & End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #Extracts month, day of the week and hour from Start Time df to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        #Need to fix this in order to get the str instead of int
        #Refactoring may be required
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Displays the most common month
    top_month = df['month'].mode()[0]
    print('\nThe month in which services were most used is: ', top_month)

    #Display the most common day of week
    top_day = df['day'].mode()[0]
    print('\nThe day of the week in which services were most used is: ', top_day)

    #Display the most common start hour
    top_hour = df['hour'].mode()[0]
    print('\nThe hour in which services were most used is: ', top_hour)

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    top_start_station = df['Start Station'].mode()[0]
    print('\nThe starting station most used is: ', top_start_station)

    #Display most commonly used end station
    top_end_station = df['End Station'].mode()[0]
    print('\nThe ending station most used is: ', top_end_station)

    #Display most frequent combination of start station and end station trip
    top_route = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print('\nThe route most used is: ', top_route)


    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    df['travel_time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['travel_time'].sum()
    print('\nTotal travel time is: ', total_travel_time)

    #Display mean travel time
    avg_travel_time = df['travel_time'].mean()
    print('\nThe average travel time is: ', avg_travel_time)

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_type = df['User Type'].value_counts()
    print('\nCount of different types of users:\n', user_type)

    #Display counts of gender and, if no data is available, avoids crashing the code
    gender = []
    if "Gender" in df.columns:
        gender = df['Gender'].value_counts()
        print('\nCount of users by gender:\n', gender)
    else:
        print('\nThere\'s no data on user gender. Sorry.\n')

    #Display information on birth year of user, and, if no data is available, avoids crashing the code
    birth_year = []
    if "Birth Year" in df.columns:
        birth_year = df['Birth Year']
    #Display earliest, most recent, and most common year of birth
        min_year = df['Birth Year'].min()
        print('\nEarliest year of birth: ', min_year)
        max_year = df['Birth Year'].max()
        print('\nMost rescent year of birth: ', max_year)
        most_common_year = df['Birth Year'].mode()
        print('\nMost common year of birth: ', most_common_year)
    else:
        print('\nThere\'s no data on user\'s date of birth. Sorry.\n')

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Core code
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #Offer users the option of visualizing some raw data
        raw_data = input('Would you like to see some raw data?\nEnter yes or no.\n>>').lower()
        if raw_data == 'yes':
            i = 0
            while True:
                print(df.iloc[i:i+5])
                i += 5
                more_raw_data = input('Would you like to see 5 more lines of raw data?\nEnter yes or no.\n>> ').lower()
                if more_raw_data == 'no':
                    break
        else:
            print('Done.')

        #Offer users the option of restarting
        restart = input('\n\nWould you like to restart?\nEnter yes or no.\n>> ').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
