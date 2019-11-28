import time
import numpy as np
import pandas as pd
import datetime as dt
import click


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities = ('chicago', 'new york city', 'washington')
months = (
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
    'all',
    )
months_names = {
    '1': 'january',
    '2': 'february',
    '3': 'march',
    '4': 'april',
    '5': 'may',
    '6': 'june',
    }
days = (
    'saturday',
    'sunday',
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'all',
    )

# washington city indicator
dc_flag = False


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nFor which city do you want to select Data from New York City, Chicago or Washington?\n").lower()
    while city not in cities:
        print("\nSomething is not right in the input!\n")
        city = input("\nPlease choose a valid City:\n")

    # get user input for month (all, january, february, ... , june)
    month = input("\nFor which month do you want to select Data from January, February,.. ,June or all?\n").lower()
    while month not in months:
        print("\nSomething is not right in the input!\n")
        month = input("\nPlease enter a valid month or all:\n")
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nFor which day do you want to select Data from Sunday, Monday,...Saturday or all?\n").lower()
    while day not in days:
        print("\nSomething is not right in the input!\n")
        day = input("\nPlease enter a valid day or all:\n")
        
    if city == 'washington':
        dc_flag = True
    else:
        dc_flag = False

    print("\n\nApplying Filters....\nCity: {}\nMonth: {}\nDay: {}\n".format(city, month, day).title())
    
    return city, month, day, dc_flag

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

    # convert the Start and The End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    #df['month_name'] = df['month'].apply(lambda x: calendar.month_abbr[x])

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

    return df
    
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = str(df['month'].mode()[0])
    popular_month = months_names.get(popular_month).title()
    print("\nThe Most Frequent Month: {}\n".format(popular_month))

    # display the most common day of week
    popular_day = str(df['day_of_week'].mode()[0])
    print("\nThe Most Frequent Day of Week: {}\n".format(popular_day))

    # display the most common start hour
    popular_hour = str(df['hour'].mode()[0])
    print("\nThe Most Frequent Hour: {}\n".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = str(df['Start Station'].mode()[0])
    print("\nMost Popular Start Station is: {}\n".format(popular_start_station))

    # display most commonly used end station
    popular_end_station = str(df['End Station'].mode()[0])
    print("\nMost Popular End Station is: {}\n".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']
    popular_trip = str(df['Trip'].mode()[0])
    print("\nMost Popular Trip: {}\n".format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    total_days = str(int(total_time//(60*60*24)))
    total_hours = str(int((total_time%(60*60*24)) //(60*60)))
    total_mins = str(int(((total_time%(60*60*24)) %(60*60)) //60))
    total_secs = str(int(((total_time%(60*60*24)) %(60*60)) %60))
    print("\nTotal Travel Time is: {} Day(s), {} hour(s), {} min(s) and {} sec(s)\n".format(total_days, total_hours, total_mins, total_secs))

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    avg_mins = str(int(avg_time // 60))
    avg_secs = str(int(avg_time % 60))
    print("\nAverage Trip Duration is: {} min(s) and {} sec(s)\n".format(avg_mins, avg_secs))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, dc_flag):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print("\nUser Type Distribution is: \n{}\n".format(user_types_count))
    
    # Check if city == 'washington'
    if dc_flag != True:
        # Display counts of gender
        genders_count = df['Gender'].value_counts()
        print("\nGender Distribution of Bike Riders is: \n{}\n".format(genders_count))

        # Display earliest, most recent, and most common year of birth
        oldest_year = str(int(df['Birth Year'].min()))
        print("\nOldest Biker was born in {}\n".format(oldest_year))
        newest_year = str(int(df['Birth Year'].max()))
        print("\nYoungest Biker was born in {}\n".format(newest_year))
        popular_year = str(int(df['Birth Year'].mode()[0]))
        print("\nMost Bikers were born in {}\n".format(popular_year))
        
    else:
        print('\nSorry! This Data is not available for Washington.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df, marker):
    print("\nYou chose to show Raw Data.\n")
    
    # Check if user want to get data from were it stopped last time
    if marker > 0:
        print("\nWould you like to continue from last stop or not?\n")
        indicator = input("type 'yes' or 'no'")
        if indicator == 'no':
            marker = 0
    
    # Sortingorting Data
    if marker == 0:
        # Sort Raw Data or not
        sort_df = input("How would you like to sort displayed data?\n [st] for Start time\n [et] for End time\n [td] for Trip Duration\n [ss] for Start Station\n "
                         "[es] for End Station\n [ns] for No Sorting\n\n")
                         
        choices = ['st', 'et', 'td', 'ss', 'es', 'ns']       
        while sort_df not in choices:
            sort_df = input("\nMake Sure you selected right\nPlease Select again:\n [st] for Start time\n [et] for End time\n [td] for Trip Duration\n [ss] for Start Station\n "
                         "[es] for End Station\n [ns] for No Sorting\n\n")
        
        # Sort in Ascending or Descending order
        asc_desc_sort = input("\nWould you like to sort in ascending order or in descending order?\n"
                               " [a] for Ascending\n [d] for Descending\n\n")
        sorted_ways = ['a', 'd']
        while asc_desc_sort not in sorted_ways:
            asc_desc_sort = input("\nMake Sure you selected right\nPlease Select again:\n [a] for Ascending\n [d] for Descending\n\n")
                               
        if asc_desc_sort == 'a':
            asc_desc_sort = True
        else:
            asc_desc_sort = False
            
        if sort_df == 'st':
            df = df.sort_values(['Start Time'], ascending=asc_desc_sort)
        elif sort_df == 'et':
            df = df.sort_values(['End Time'], ascending=asc_desc_sort)
        elif sort_df == 'td':
            df = df.sort_values(['Trip Duration'], ascending=asc_desc_sort)
        elif sort_df == 'ss':
            df = df.sort_values(['Start Station'], ascending=asc_desc_sort)
        elif sort_df == 'es':
            df = df.sort_values(['End Station'], ascending=asc_desc_sort)
        elif sort_df == 'ns':
            pass
        
        # Printing five rows a time
        while True:
            for counter in range(marker, len(df.index)):
                print("\n")
                print(df.iloc[marker:marker+5].to_string())
                print("\n")
                marker += 5
                
                if input("Keep going?\n[y]Yes\n[n]No\n\n") == 'y':
                    continue
                else:
                    break
            break
            
    return marker

#raw_data

def main():
    while True:
        click.clear()
        city, month, day, dc_flag = get_filters()
        df = load_data(city, month, day)
        marker = 0
        
        while True:
            data_selection = input("\nWhat Data do you want to get?\n\n"
                                    "[ts] Time Stats\n"
                                    "[ss] Station Stats\n"
                                    "[tds] Trip DuratioN Stats\n"
                                    "[us] User Stats\n"
                                    "[rd] Display Raw Data\n"
                                    "[r] Restart\n\n")
            
            data_selections = ['ts', 'ss', 'tds', 'us', 'rd', 'r']
            while data_selection not in data_selections:
                data_selection = input("\nMake Sure you selected right\nPlease Select again:\n[ts] Time Stats\n"
                                    "[ss] Station Stats\n"
                                    "[tds] Trip DuratioN Stats\n"
                                    "[us] User Stats\n"
                                    "[rd] Display Raw Data\n"
                                    "[r] Restart\n\n")
            click.clear()
            if data_selection == 'ts':
                time_stats(df)
            elif data_selection == 'ss':
                station_stats(df)
            elif data_selection == 'tds':
                trip_duration_stats(df)
            elif data_selection == 'us':
                user_stats(df, dc_flag)
            elif data_selection == 'rd':
                raw_data(df, marker)
            elif data_selection == 'r':
                break

        restart = input('\nWould you like to restart?\n\n[y] Yes\n[n] No\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()