"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: w2181775, 20250479
 4. Date: 17/11/2025
****************************************************************************

"""
from graphics import *
import csv
import math

data_list = []   # data_list An empty list to load and hold data from csv file

def load_csv(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list"
    YOU DO NOT NEED TO CHANGE THIS BLOCK OF CODE
    """
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)



#************************************************************************************************************


#Task A

#valid airport dictionary 
valid_airports={
    "LHR":"London Heathrow",
    "MAD":"Madrid Adolfo Suárez-Barajas",
    "CDG":"Charles De Gaulle International",
    "IST":"Istanbul Airport International",
    "AMS":"Amsterdam Schiphol",
    "LIS":"Lisbon Portela",
    "FRA":"Frankfurt Main",
    "FCO":"Rome Fiumicino",
    "MUC":"Munich International",
    "BCN":"Barcelona International"
}

def get_valid_airport(valid_airports_dict):
    while True: 
        code_input=input("Please enter a three-letter city code: ").strip().upper()
        #check if the code is exactly 3 letters
        if len(code_input)!=3:
            print("Wrong code length - please enter a three-letter city code")
            continue 
        #check if the code exist in the valid dictionary
        if code_input not in valid_airports_dict:
            print("Unavailable city code - please enter a valid city code")
            continue
            
        return code_input

def get_valid_year():
    while True:
        year_input=input("Please enter the year required in the format YYYY: ").strip()
        #check if it has 4 digits 
        if len(year_input) !=4:
             print("Wrong data type please enter a four-digit year value")
             continue
            
        #check if it is a number
        try:
            year_int =int(year_input)
        except ValueError:
            print("Wrong data type please enter a four-digit year value")
            continue    
        #check the year range 
        year_int=int(year_input)
        if year_int <2000 or year_int > 2025:
            print("Out of range - please enter a value from 2000 to 2025")
            continue     
        return year_input


#Task B

def process_data(data_list):
    
    #Total flights on the data list 
    total_flights=len(data_list)

    #Total number of planes departing terminal 2
    terminal_2_count=0
    for row in data_list:
        if row[8] =="2":
            terminal_2_count=terminal_2_count + 1

    #Total number of departures on flights under 600 miles 
    under_600_count=0
    for row in data_list:
        distance =int(row[5])
        if distance < 600:
            under_600_count=under_600_count + 1

    #Total number of air france flights
    air_france_count=0
    for row in data_list:
        #check first two letters 
        if row[1][0:2] =="AF":
            air_france_count=air_france_count + 1

    #Total number of flights that departed under 15°C temperature 
    below_15_count=0
    for row in data_list:
        weather_string=row[10]
        words =weather_string.split() 
        for word in words:
            if "°" in word or "C" in word:
                number_str =""
                #loop to check for digits
                for char in word:
                    if char >="0" and char <="9":
                        number_str =number_str + char
                if number_str !="":
                    if int(number_str) < 15:
                        below_15_count =below_15_count + 1

    #The average number of british airways departures per hour
    ba_count=0
    for row in data_list:
        if row[1][0:2] =="BA":
            ba_count =ba_count + 1
    avg_ba =round(ba_count/12,2)        
        
    #Total percentage of total departures that are british airways 
    ba_percent=0
    if total_flights > 0:
        ba_percent =round((ba_count/total_flights)*100,2)

    #The percentage of air france with delayed departure 
    af_delayed_count=0
    for row in data_list:
        #Check the code and if the scheduled time is not equal to actual time
        if row[1][0:2] =="AF" and row[2] !=row[3]:
            af_delayed_count =af_delayed_count + 1
            
    af_delayed_percent=0
    if air_france_count >0:
        #get the precentage and rounding up
        af_delayed_percent =round((af_delayed_count/air_france_count)*100,2)

    #Total number of hours that rain in 12 hours 
    hours_where_it_rained=[]
    for row in data_list:
        scheduled_time =row[2]
        weather =row[10]
        #check for rain in row 10
        if "rain" in weather.lower():
            current_hour =scheduled_time[0:2]
            if current_hour not in hours_where_it_rained:
                hours_where_it_rained.append(current_hour)
    total_rainy_hours =len(hours_where_it_rained)

    #full name of least common destination
    all_destinations=[]
    for row in data_list:
        dest_code =row[4]
        if dest_code not in all_destinations:
            all_destinations.append(dest_code)
            
    #find the lowest number
    lowest_count =100000 
    least_common_codes=[]

    for dest_code in all_destinations:
        count=0
        for row in data_list:
            if row[4] ==dest_code:
                count =count + 1
        
        if count <lowest_count:
            lowest_count =count

    #find which codes match that number
    for dest_code in all_destinations:
        count=0
        for row in data_list:
            if row[4] ==dest_code:
                count =count + 1       
        if count ==lowest_count:
            least_common_codes.append(dest_code)

    least_common_names=[]
    for code in least_common_codes:
        if code in valid_airports:
            least_common_names.append(valid_airports[code])
        else:
            least_common_names.append(code)

    #Return all the calculated values 
    return (total_flights,terminal_2_count,under_600_count,air_france_count,below_15_count,avg_ba,ba_percent,af_delayed_percent,total_rainy_hours,least_common_names)  

def save_results(file_name,full_name,year,results):
    #Unpacking the results tuple to single variables for printing 
    (total_flights,terminal_2_count,under_600_count,air_france_count,below_15_count,avg_ba,ba_percent,af_delayed_percent,total_rainy_hours,least_common_names)=results
    
    #print to screen
    print(f"The total number of flights from this airport was {total_flights}")
    print(f"The total number of flights departing Terminal Two was {terminal_2_count}")
    print(f"The total number of departures on flights under 600 miles was {under_600_count}")
    print(f"There were {air_france_count} Air France flights from this airport")
    print(f"There were {below_15_count} flights departing in temperatures below 15 degrees")
    print(f"There was an average of {avg_ba} British Airways flights per hour from this airport")
    print(f"British Airways planes made up {ba_percent}% of all departures")
    print(f"{af_delayed_percent}% of Air France departures were delayed")
    print(f"There were {total_rainy_hours} hours in which rain fell")
    print(f"The least common destinations are {least_common_names}")        

#Task C
    
    #save to text file
    with open("results.txt","a") as file:
        file.write("****************************************************************************************************\n")
        file.write(f"{file_name} selected - Planes departing {full_name} {year}\n")
        file.write("****************************************************************************************************\n")
        file.write(f"The total number of flights from this airport was {total_flights}\n")
        file.write(f"The total number of flights departing Terminal Two was {terminal_2_count}\n")
        file.write(f"The total number of departures on flights under 600 miles was {under_600_count}\n")
        file.write(f"There were {air_france_count} Air France flights from this airport\n")
        file.write(f"There were {below_15_count} flights departing in temperatures below 15 degrees\n")
        file.write(f"There was an average of {avg_ba} British Airways flights per hour from this airport\n")
        file.write(f"British Airways planes made up {ba_percent}% of all departures\n")
        file.write(f"{af_delayed_percent}% of Air France departures were delayed\n")
        file.write(f"There were {total_rainy_hours} hours in which rain fell\n")
        file.write(f"The least common destinations are {least_common_names}\n")


#Task D

#valid airline dictionary
valid_airline={
    "BA":"British Airways",
    "AF":"Air France",
    "AY":"Finnair",
    "KL":"KLM",
    "SK":"Scandinavian Airlines",
    "TP":"TAP Air Portugal",
    "TK":"Turkish Airlines",
    "W6":"Wizz Air",
    "U2":"easyJet",
    "FR":"Ryanair",
    "A3":"Aegean Airlines",
    "SN":"Brussels Airlines",
    "EK":"Emirates",
    "OR":"Qatar Airways",
    "IB":"Iberia",
    "LH":"Lufthansa"
}    

#get the data for histrogram
def draw_histogram(data_list,full_airport_name,selected_year):
    airline_code=""
    while True:
        airline_code=input("Enter a two-character Airline code to plot a histogram: ").strip().upper()
        if airline_code in valid_airline:
            break
        print("Unavailable Airline code please try again.")

    full_airline_name=valid_airline[airline_code]

    #create the list for the 12 hours
    hourly_counts =[0,0,0,0,0,0,0,0,0,0,0,0]

    for row in data_list:
        flight_num=row[1]
    
        #Get the airline code  
        first_two_letters =flight_num[0:2]
        if first_two_letters ==airline_code:

           #get the hour
           time_str =row[2]
        
           digit1=time_str[0]
           digit2=time_str[1]
        
           hour_string =digit1+digit2
        
           # Convert that string into number
           hour_index =int(hour_string)
        
           # Add 1 to the correct slot in the list 
           if hour_index < 12:
              hourly_counts[hour_index] =hourly_counts[hour_index]+1

    #Finding the Maximum 
    max_count=0
    for count in hourly_counts:
        if count > max_count:
           max_count=count


    if max_count==0:
       max_count=1

    try:
        win=GraphWin("histrogram",800,800)
        win.setBackground("white")
        title_text=f"Departures by hour for {full_airline_name} from {full_airport_name} {selected_year}"
        title=Text(Point(400,30), title_text)
        title.setSize(20)
        title.setStyle("bold")
        title.draw(win)
        left_margin = 100
        top_margin = 80
    
        y_axis_label =Text(Point(40,300),"Hours\n00:00\nto\n12:00")
        y_axis_label.setSize(10)
        y_axis_label.draw(win)

        p1=Point(left_margin,top_margin)
        p2=Point(left_margin,550) 
        axis_line=Line(p1,p2)
        axis_line.draw(win)

        max_bar_width=600 
        for hour in range(12):
            count =hourly_counts[hour]
            y_pos =top_margin+(hour*40) 
        
            hour_label_str =str(hour)
            if len(hour_label_str)<2:
               hour_label_str ="0"+hour_label_str 
            
            hour_text= Text(Point(left_margin-20,y_pos+15),hour_label_str)
            hour_text.draw(win)
            if count>0:
               bar_width=(count/max_count)*max_bar_width
               rect_p1=Point(left_margin,y_pos) 
               rect_p2 = Point(left_margin+bar_width,y_pos+30)
            
               bar =Rectangle(rect_p1,rect_p2)
               bar.setFill("pink") 
               bar.setOutline("black")
               bar.draw(win)
               count_text =Text(Point(left_margin+bar_width+15,y_pos+15),str(count))
               count_text.setSize(10)
               count_text.draw(win)
               
        win.getMouse()
        win.close()
    except:
        pass

#Task E    
    
def main():
    
    #Main Loop to control the program flow and allow restarting.
    while True:
        # Get User Input
        selected_airport =get_valid_airport(valid_airports)
        selected_year =get_valid_year()
        
        #Load File(Task A)
        selected_data_file =f"{selected_airport}{selected_year}.csv"
        full_airport_name =valid_airports[selected_airport]
        
        print("****************************************************************************************************\n")
        print(f"{selected_data_file} selected - Planes departing {full_airport_name} {selected_year}")
        print("****************************************************************************************************\n")

        #Clear the global list before loading new data
        data_list.clear()

        #load the selected data file 
        load_csv(selected_data_file)

        if len(data_list) > 0:
            #Capture the results returned by process_data (Task B)
            results =process_data(data_list)
            
            #Pass the results to save_results (Task C)
            save_results(selected_data_file,full_airport_name,selected_year,results)
            
            #Histogram(Task D)
            draw_histogram(data_list,full_airport_name,selected_year)

        #Restart Loop(Task E)
        restart = input("Do you want to select a new data file? Y/N: ").strip().upper()
        if restart =="N":
            print("Thank you. End of run")
            break

# Run the program
main()


    
    
        
        
        
        
    
    
    
    
    






      














  






