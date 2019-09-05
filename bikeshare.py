import time
import pandas as pd

#controls debugging print statements
lets_debug = False

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    is_valid = True

    while True:
        # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = str(input('\nWhich city would you like to explore: Chicago, New York City or Washington:\n').lower())

        # TO DO: get user input for month (all, january, february, ... , june)
        month = str(input('\nWhich month (january, february, ..., june or all):\n').lower())

        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = str(input('\nWhich day of week (sunday, monday, ..., saturday or all):\n').lower())

        # determine if user inputs are valid before calculate statistics
        is_valid = validate_inputs(city, month, day)

        if is_valid == True:
            print('You selected City: {}; Month: {}; Day: {}'.format(city.title(), month.title(), day.title()))
            #valid input breaks and returns back to main program
            break
        else:
            print('-'*40)
            print('Please enter a proper value that matches the prompt.')

    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # store total trip time end - start
    #df = df.assign(end_minus_start = df['End Time'] - df['Start Time'])
    df['end_minus_start'] = df['End Time'] - df['Start Time']

    # combine start/end stations to create new column
    df['start_end_station'] = df['Start Station'] + ' : ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #debug information, only display if lets_debug is set True
    if lets_debug:
        print('Shape: ', df.shape)
        print('Size: ', df.size)
        print('Ndim: ', df.ndim)
        print('End load_data if debug')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].value_counts().idxmax()
    print('Most Frequent Month:\n', popular_month)

    # TO DO: display the most common day of week
    popular_dow = df['day_of_week'].value_counts().idxmax()
    print('Most Frequent day of week:\n', popular_dow)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].value_counts().idxmax()  #solution from quiz was .mode()[0]
    print('Most Frequent Start Hour(0-23):\n', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('Most popular start station:\n', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('Most popular end station:\n', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = df['start_end_station'].value_counts().idxmax()
    print('Most popular round trip:\n', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['end_minus_start'].sum()
    print('Total travel time:\n', total_travel)

    # TO DO: display mean travel time
    avg_travel = df['end_minus_start'].mean()
    print('Average travel time:\n', avg_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Counts per user type:\n', user_type)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('Counts per user gender:\n', gender)
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year_min = df['Birth Year'].min()
        print('Birth year of oldest user:\n',birth_year_min)
        birth_year_max = df['Birth Year'].max()
        print('Birth year of youngest user:\n',birth_year_max)
        birth_year_common = df['Birth Year'].value_counts().idxmax()
        print('Most popular user birth year:\n',birth_year_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(city, df):
    """
    Interacts with user to output raw data until user stops

    Args:
        (str) city - name of the city to analyze
        (DataFrame) - raw_results based on Output df from load_data(city, month, day)

    Returns:
        None - Only Screen output results presented of raw data stored in a Pandas DataFrame
    """
    start = 0
    stop = 5
    to_display = 'yes'
    while to_display == 'yes':
        to_display = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower()
        if to_display == 'no':
            return
        elif to_display =='yes':
            if city == 'chicago':
                print(df.iloc[start:stop,1:9])
            else:
                # non-chicago cities have less columns of data in raw source
                print(df.iloc[start:stop,1:7])
        else:
            print('Sorry, that is not an option. Please restart.')

        start = start + 5
        stop = stop + 5
        print('-'*40)

def validate_inputs(city, month, day):
    """
    Verify user input exists within the valid dictionary & list

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        is_valid - boolean value: True indicates valid input, False indicates invalid input
    """
    # months list
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june']
    valid_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    if city in CITY_DATA and (month in valid_months or month == 'all') and (day in valid_days or day == 'all'):
        is_valid = True
    else:
        is_valid = False
        if lets_debug:
            print('validate_inputs city: ', city)
            print('validate_inputs month: ', month)
            print('validate_inputs months list: ', valid_months)
            print('validate_inputs day: ', day)
            print('validate_inputs days list: ', valid_days)
            print('validate_inputs is_valid returned: ', is_valid)

    return is_valid

def main():
    print('Welcome to the US Bikeshare interactive program!')

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(city,df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
    print('Thank you, hope you enjoyed the interactive experience!')
