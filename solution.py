import time
import pandas as pd
import numpy as np

# Bike share systems data for three major cities in the United States—Chicago, New York City, and Washington. It will be used for computing descriptive statistics.

CITY_DATA = { 'Chicago': '/Users/okyay/Desktop/Project2/chicago.csv',
              'New York': '/Users/okyay/Desktop/Project2/new_york_city.csv',
              'Washington': '/Users/okyay/Desktop/Project2/washington.csv'
            }
month_check = ["January","February","March","April","May","June","all","All","ALL","aLL"]
day_check = {"1": "Sunday","2": "Monday","3": "Tuesday","4": "Wednesday","5": "Thursday","6": "Friday","7": "Saturday","All": "*","all":"*","ALL":"*","aLL":"*"}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('"\n\n"Hello! Let\'s explore some US bikeshare data!\n\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city =input("\nWould you like to see data for Chicago, New York or Washington: ").title().strip()
        if city in CITY_DATA.keys():
            break
        else:
            print("You have entered wrong city name .Please try again ")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWould you like to filter the data by month.\nPlease type out the full month name: \n January, February, March, April , May ,June or the all: ").title().strip()
        if month in month_check:# month_check list is mentioned at the top of the code , It is first 6 months and name all
            month = month_check.index(month) + 1
            break
        else:
            print("You have entered wrong month name .Please try again ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWould you like to filter the data by day of week.\nPlease type your response as an integer(e.g., 1 = Sunday) or type all: ").title().strip()
        if day in day_check.keys(): # day_check list is mentioned at the top of the code , It is day number of weeks and name all
            day = day_check[day]
            break
        else:
            print("You have entered wrong day number .Please try again ")
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

    df = pd.read_csv(CITY_DATA[city])

    df['Start Date'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Date'].dt.month

    df['day_of_week'] = df['Start Date'].dt.day_name()

    if month != 8: # if the user select all option for month , there will not a filter
        df = df[df['month'] == month]

    if day != '*': # if the user select all option for day , there will not a filter
        df = df[df['day_of_week'] == day.title()]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Date'].dt.month
    popular_month = df['month'].mode()[0]
    counts_1 = df['month'].value_counts().max()

    # display the most common day of week
    df['day_of_week'] = df['Start Date'].dt.day_name()
    popular_day_of_week = df['day_of_week'].mode()[0]
    counts_2 = df['day_of_week'].value_counts().max()
    # display the most common start hour
    df['hour'] = df['Start Date'].dt.hour
    popular_hour = df['hour'].mode()[0]
    counts_3 = df['hour'].value_counts().max()

    print("The most popular month for travelling: {} , counts: {}".format(popular_month,counts_1))
    print("The most popular weekday for travelling: {} , counts: {}".format(popular_day_of_week,counts_2))
    print("The most popular hour for travelling: {} , counts: {}".format(popular_hour,counts_3))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start_sit = df['Start Station'].mode()[0]
    counts_1 = df['Start Station'].value_counts().max()
    # display most commonly used end station
    most_used_end_sit = df['End Station'].mode()[0]
    counts_2 = df['End Station'].value_counts().max()
    # display most frequent combination of start station and end station trip

    df['Trip'] = df['Start Station'] + str(" -  -> ")+ df['End Station']
    most_used_trip = df['Trip'].mode()[0]
    counts_3 = df.groupby(['Start Station','End Station'])['Start Station'].count().max()

    print("Most commonly used start station is: {} , counts: {}".format(most_used_start_sit,counts_1))
    print("Most commonly used end station is: {} , counts: {}".format(most_used_end_sit,counts_2))
    print("Most Popular Trip is : {} , counts: {} ".format(most_used_trip,counts_3))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    count =df['Trip Duration'].count()

    # display mean travel time
    average_duration = df['Trip Duration'].mean()

    print("Total Duration : {} , counts : {} , Average Duration : {} ".format(total_duration,count,average_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))
    print("\n")

    if (len(df.columns)) != 12: # control if the city is washington or not, washington has 12 dataframe column, it hasnt gender and birth data which cause error
        # Display counts of gender
        print("Counts of gender:\n")
        gender_counts  = df['Gender'].value_counts()
        for index,gender_count   in enumerate(gender_counts):
            print("  {}: {}".format(gender_counts.index[index], gender_count))
        print("\n")

        # Display earliest, most recent, and most common year of birth
        youngest = df['Birth Year'].min()
        oldest =  df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        count  = df['Birth Year'].value_counts().max()

        print("Earliest year of birth: ",youngest)
        print("Recents year of birth: ",oldest)
        print("Most Common year of birth : {} , counts : {}".format(most_common , count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        start_loc = 0
        end_loc = 5

        if view_data == 'yes':
            while end_loc <= df.shape[0] - 1:

                print(df.iloc[start_loc:end_loc,:])
                start_loc += 5
                end_loc += 5
                end_display = input("Do you wish to continue?: ").lower()
                if end_display == 'no':
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
