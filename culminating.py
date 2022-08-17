#-------------------------------------------------------------------------------
# Name:        culminating.py
# Purpose:     Video Renting program
#
# Author:      Atharva Mishra
#
# Created:     11/01/2022
# Copyright:   (c) Atharva Mishra 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import subprocess
import sys
import os.path
try: 
    from tkinter import *
    from tkinter.font import Font
    from tkcalendar import Calendar,DateEntry
    import json
    import datetime
    from PIL import Image, ImageTk
    import ast 
    import random
    import yagmail

except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yagmail", "keyring", "pillow", "tkcalendar"])

#post-rent commands
class rented:
    
    #asking the user how many days they want to rent the movie for.
    def date_limit(movie1, genre):
        global limit, time_limit
        genre = genre
        movie = movie1
        try:
            horrorscreen.destroy()
        except:
            try:
                romancescreen.destroy()
            except:
                try:
                    comedyscreen.destroy()
                except:
                    try:
                        adventurescreen.destroy()
                    except:
                        try:
                            fictionscreen.destroy()
                        except:
                            pass
        
        #window
        limit = Tk()
        limit.geometry('250x250')
        
        #title
        #entry for dates box.
        #sumbit button
        title = Label(limit, text='How many days are you \ngoing to rent the movie for?')
        title.pack()
        time_limit = Entry(limit, width = 20)
        time_limit.pack()
        sumbit = Button(limit, text='Sumbit!', command = lambda:[rented.rent(movie, genre), rental.user_interface()])
        sumbit.pack()

    #checking wether the movie has already been rented by the user.
    def checking(movie1, genre):
        genre = genre
        movie = movie1
        file = open("information", 'r')
        info = file.readline()
        info = ast.literal_eval(info)
        file.close()
        user = info['user'].index(current_user)
        if len(info['Rented'][user]) >= 1:
            for i in range(len(info['Rented'][user])):
                if info['Rented'][1][i][0] == movie:
                    rental.user_interface()
                    break
            else: 
                rented.date_limit(movie, genre)
        else:
            rented.date_limit(movie, genre)

    #renting the movie
    def rent(movie1, genre):
        movie = movie1
        file = open("information", 'r')
        info = file.readline()
        info = ast.literal_eval(info)
        file.close()

        user = info['user'].index(current_user)
        
        with open('moviedata', 'r') as file:
            movie_data = file.readline()
            file.close()
        movie_data = ast.literal_eval(movie_data)
    
        movie = [i for i in range(len(movie_data[genre])) if movie_data[genre][i][0] == movie]
        movie = movie[0]
        
        #removing 1 amount from the movie when renting it.
        if movie_data[genre][movie][1] != 0:
            movie_data[genre][movie][1] -= 1
            with open('moviedata', 'w') as file:
                file.write(json.dumps(movie_data))
                file.close()
                
        time = datetime.datetime.now()
        time = time.strftime("%x")
        if time[0] == "0":
            time = time[1:]

        info['Rented'][user].append([movie1, time, int(time_limit.get())])  
        info['Transaction'][user].append([movie1, time, int(time_limit.get())])  

        with open('information', 'w') as file:
            file.write(json.dumps(info))
            file.close()
        
        # tosend = current_email
        # receiver = tosend 
        # body = f"You have rented {movie1} please make sure to return it on time!"
        # user_information = yagmail.SMTP("@gmail.com", 'password')
        # user_information.send(to=receiver,subject="Video Rental payment",contents=body)

    #check 
    def check(date1, date2, moviename):
        global movie_name
        movie_name = moviename
        time = datetime.datetime.now()
        time = time.strftime("%x")
        if time[0] == '0':
            time = time[1:]
        file = open("information", 'r')
        info = file.readline()
        info = ast.literal_eval(info)
        file.close()
        user = info['user'].index(current_user)
        position = 0
        for i in range(len(info['Rented'][user])):
            if moviename == info['Rented'][user][i][0]:
                position = i
                break
            else:
                pass
        datecheck = info['Rented'][user][position].index(date1)
        if date1 == info['Rented'][user][position][datecheck]:
            print("Checks out!")
            if date2 == time:
                rented.pay(date1, date2)
            else:
                print("error1")
        else:
            print("error")

    #calculating how much the user has to pay.
    def pay(date1, date2):

        #storing dates.
        returning = date2
        purchase = date1
        returning_month = ""
        returning_date = ""
        returning_year = ""
        purchase_month = ""
        purchase_date = ""
        purchase_year = ""
        previous = ""

        #storing date, month and year for returing and purchase.
        for i in range(len(returning)):
            if returning[i] != "/": 
                returning_month += returning[i]
            else:
                previous = returning[i] 
                break

        for x in range(returning.index(previous)+1, len(returning)):
            if returning[x] != "/":
                returning_date += returning[x]
            else:
                previous = x
                break
        
        for y in range(x+1, len(returning)):
            returning_year += returning[y]
        
        for j in range(len(purchase)):
            if purchase[j] != "/": 
                purchase_month += purchase[j]
            else:
                previous = purchase[j] 
                break

        for k in range(purchase.index(previous)+1, len(purchase)):
            if purchase[k] != "/":
                purchase_date += purchase[k]
            else:
                previous = k
                break
        
        for l in range(x+1, len(purchase)):
            purchase_year += purchase[l]

        returning_month = int(returning_month)
        returning_date = int(returning_date)
        returning_year = int(returning_year)
        purchase_year = int(purchase_year)
        purchase_date = int(purchase_date)
        purchase_month = int(purchase_month)
        days = 0

        #calculating the amount of days the movie was taken for to compare it with the amount of days the user said he/she wanted to take the movie for.
        if returning_month - purchase_month > 0 and returning_year - purchase_year == 0:
            for length in range((returning_month-(returning_month-purchase_month)), returning_month):
                if returning_month == 1:
                    days += 31
                elif returning_month == 2:
                    days += 28
                elif returning_month == 3:
                    days += 31
                elif returning_month == 4:
                    days += 30
                elif returning_month == 5:
                    days += 31
                elif returning_month == 6:
                    days += 30
                elif returning_month == 7:
                    days += 31
                elif returning_month == 8:
                    days += 31
                elif returning_month == 9:
                    days += 30
                elif returning_month == 10:
                    days += 31
                elif returning_month == 11:
                    days += 30
                elif returning_month == 12:
                    days += 31
        else:
            pass
        
        with open('information','r') as file:
            info = file.readline()
            file.close()
        info = ast.literal_eval(info)

        user = info['user'].index(current_user)
        position = 0

        #findin the movie to get it's information.
        for i in range(len(info['Rented'][user])):
            if movie_name == info['Rented'][user][i][0]:
                position = i
                break
            else:
                print("movie doesn't exist")
        
        movie_rent = info['Rented'][user][position][2]

        info['Rented'][user].pop(position)
        with open('information', 'w') as file:
            file.write(json.dumps(info))
            file.close()

        with open('moviedata', 'r') as file:
            movie_data = file.readline()
            file.close()
        movie_data = ast.literal_eval(movie_data)

        genre_list = ['Horror', 'Romance', 'Adventure', 'Comedy', 'Fiction']
        genre = 0
        for x in genre_list:
            for i in range(len(movie_data[x])):
                if movie_data[x][i][0] == movie_name:
                    movie_location = i
                    genre = x
        
        #when the movie is being returned add 1 to the amount of movie.
        if movie_data[genre][movie_location][1] <= 1:
            movie_data[genre][movie_location][1] += 1
            with open('moviedata', 'w') as file:
                file.write(json.dumps(movie_data))
                file.close()
        else:
            pass
        
        if (days+1) <= movie_rent and returning_year - purchase_year == 0:

            #if the user is in time at returning the movie then.
            with open('information', 'r') as f:
                info = f.readline()
                info = ast.literal_eval(info)
                f.close()

            money = (days+1) * info['price']
            
            info['revenue'].append(money)
            
            with open('information', 'w') as f:
                f.write(json.dumps(info))
                f.close()

            #send user email for how much money has been charged on their card.
            # tosend = current_email
            # receiver = tosend 
            # body = f"${money} has been charged on your card! For returning the rented movie!"
            # user_information = yagmail.SMTP("@gmail.com", 'password')
            # user_information.send(to=receiver,subject="Video Rental payment",contents=body)

        else:
            with open('information', 'r') as f:
                info = f.readline()
                info = ast.literal_eval(info)
                f.close()
            
            #if the user is late at returning the movie then 10 extra for each day.
            money = (days+1) * info['late_price']

            info['revenue'].append(money)

            with open('information', 'w') as f:
                f.write(json.dumps(info))
                f.close()
            
            #send user email for how much money has been charged.
            # tosend = current_email
            # receiver = tosend 
            # body = f"${money} has been charged on your card! For returning the rented movie! You have been charged more because you had returned the movie late!"
            # user_information = yagmail.SMTP("@gmail.com", 'password')
            # user_information.send(to=receiver,subject="Video Rental payment",contents=body)
        
    #returning the rented movie
    def returning():
        global returningscreen, movie_info
        try:
            screen3.destroy()
        except:
            pass

        file = open("information", 'r')
        info = file.readline()
        info = ast.literal_eval(info)
        file.close()

        #window
        returningscreen = Tk()
        returningscreen.geometry('250x250')

        #design layout for reutning the movie.
        #selection box for the movie.
        #selection box for the date the user rented the movie.
        #selection box for the date the user is returning the movie.
        #sumbit button for when finished filling out the information.
        user = info['user'].index(current_user)
        if len(info['Rented'][user]) > 0:
            movie_list = []

            for i in info['Rented'][user]:
                movie_list.append(i[0])
            
            movie = Label(returningscreen, text='Movie Name:')
            movie.pack()
            setting = StringVar(returningscreen)
            setting.set("Pick movie!")
            movie_info = OptionMenu(returningscreen, setting, *movie_list)
            movie_info.pack()
            dateinfo = Label(returningscreen, text='Purchase date:')
            dateinfo.pack()
            cal = DateEntry(returningscreen,width=30,bg="darkblue",fg="white",year=2021)
            cal.pack()
            dateinfo1 = Label(returningscreen, text='Return date!')
            dateinfo1.pack()
            cal1 = DateEntry(returningscreen,width=30,bg="darkblue",fg="white",year=2021)
            cal1.pack()
            btn = Button(returningscreen, text='submit!', command= lambda: [rented.check(cal.get(), cal1.get(), setting.get()), rental.user_interface()])
            btn.pack()
            
        else:
            #if there are no movies rented by the user then don't do anything.
            #button to go back to the movie selection screen.
            error = Label(returningscreen, text='You haven\'t rented any movie!', bg='white')
            error.pack()
            goback = Button(returningscreen, text='Go back!', command =rental.user_interface)
            goback.pack()

#different movies inside of different genre
class genre:

    #horror movies.
    def horror():
        global horrorscreen
        try:
            screen3.destroy()
        except NameError:
            pass

        with open('moviedata', 'r') as file:
            movie_data = file.readline()
            file.close()
        movie_data = ast.literal_eval(movie_data)

        #window
        horrorscreen = Tk()
        horrorscreen.geometry("250x250")

        for amount_of_movies in movie_data['Horror']:
            btn = Button(horrorscreen, text=amount_of_movies[0], bg='white', command= lambda name = amount_of_movies[0]:rented.checking(name, "Horror"))
            btn.pack()

    #romance genre
    def romance():
        global romancescreen
        try:
            screen3.destroy()
        except NameError:
            pass

        with open('moviedata', 'r') as file:
            movie_data = file.readline()
            file.close()
        movie_data = ast.literal_eval(movie_data)

        #window
        romancescreen = Tk()
        romancescreen.geometry('250x250')
        
        for amount_of_movies in movie_data['Romance']:
            btn = Button(romancescreen, text=amount_of_movies[0], bg='white', command= lambda name = amount_of_movies[0]:rented.checking(name, "Romance"))
            btn.pack()

    #adventure genre
    def adventure():
        global adventurescreen
        try:
            screen3.destroy()
        except NameError:
            pass

        with open('moviedata', 'r') as file:
            movie_data = file.readline()
            file.close()
        movie_data = ast.literal_eval(movie_data)

        #window
        adventurescreen = Tk()
        adventurescreen.geometry('250x250')
        
        for amount_of_movies in movie_data['Adventure']:
            btn = Button(adventurescreen, text=amount_of_movies[0], bg='white', command= lambda name = amount_of_movies[0]:rented.checking(name, "Adventure"))
            btn.pack()

    #comedy genre
    def comedy():
        global comedyscreen
        try:
            screen3.destroy()
        except NameError:
            pass

        with open('moviedata', 'r') as file:
            movie_data = file.readline()
            file.close()
        movie_data = ast.literal_eval(movie_data)

        #window
        comedyscreen = Tk()
        comedyscreen.geometry('250x250')
        
        for amount_of_movies in movie_data['Comedy']:
            btn = Button(comedyscreen, text=amount_of_movies[0], bg='white', command= lambda name = amount_of_movies[0]:rented.checking(name, "Comedy"))
            btn.pack()
        
    #fiction genre
    def fiction():
        global fictionscreen
        try:
            screen3.destroy()
        except NameError:
            pass
        with open('moviedata', 'r') as file:
            movie_data = file.readline()
            file.close()
        movie_data = ast.literal_eval(movie_data)

        #window
        fictionscreen = Tk()
        fictionscreen.geometry('250x250')
        
        for amount_of_movies in movie_data['Fiction']:
            btn = Button(fictionscreen, text=amount_of_movies[0], bg='white', command= lambda name = amount_of_movies[0]:rented.checking(name, "Fiction"))
            btn.pack()

#this is the rental screen where the users can decided what movie they want to rent.
class rental:
    
    #movie rental screen.
    def user_interface():
        try:
            returningscreen.destroy()
        except: 
            try:
                limit.destroy()
            except:
                try:
                    horrorscreen.destroy()
                except:
                    try:
                        romancescreen.destroy()
                    except:
                        try:
                            comedyscreen.destroy()
                        except:
                            try:
                                adventurescreen.destroy()
                            except:
                                try:
                                    fictionscreen.destroy()
                                except:
                                    pass

        global screen3

        #window
        screen3 = Tk()
        screen3.geometry('1000x1000')
        screen3.config(bg="white")

        #Button for each genre of movie
        title = Label(screen3, text='DSC\'s Video Rental Store!\n\n\n', bg = "white")
        title.pack()

        subtitle = Label(screen3, text="Pick a Genre: \n\n", bg='white')
        subtitle.pack()

        gener1 = Button(screen3, text='Horror', bg='white', command=genre.horror)
        gener1.pack()
        
        gener2 = Button(screen3, text='Romance', bg='white', command=genre.romance)
        gener2.pack()

        gener3 = Button(screen3, text="Adventure", bg='white', command=genre.adventure)
        gener3.pack()

        gener4 = Button(screen3, text='Comedy', bg='white',command=genre.comedy)
        gener4.pack()

        gener5 = Button(screen3, text="Fiction", bg='white',command=genre.fiction)
        gener5.pack()

        returning = Button(screen3, text='Return Movie', bg='White', command=rented.returning)
        returning.pack()

        screen3.mainloop()

#manager screen where the manager can see all the users and their information and he can delete the users.
class manager:

    #when the delete button is clicked the user gets deleted.
    def delete_user(user):  
               
        managerscreen.destroy()

        info_list = ['user', 'Email', 'credit', 'Login-Code', 'Rented','Transaction']
        file = open("information", 'r')
        info = file.readline()
        info = ast.literal_eval(info)
        file.close()
        for i in info_list:
            info[i].pop(user)

        with open('information', 'w') as file:
            file.write(json.dumps(info))
            file.close()
        manager.portal()

    #get movie name and genre
    def add_movie():
        global add_screen
        try:
            managerscreen.destroy()
        except:
            pass
            
        add_screen = Tk()
        add_screen.geometry('250x250')
        genre_list = ['']
        genre = Label(add_screen, text='Pick Genre')
        genre.pack()
        genre_list = ['Horror', 'Romance', 'Adventure', 'Comedy', 'Fiction']
        setting = StringVar(add_screen)
        setting.set("Pick Genre!")
        genre_choice = OptionMenu(add_screen, setting, *genre_list)
        genre_choice.pack()

        movies_info = Label(add_screen, text='Movie name')
        movies_info.pack()
        movie_entry = Entry(add_screen)
        movie_entry.pack()
        btn = Button(add_screen, text='Submit!', command=lambda:manager.add(setting.get(), movie_entry.get()))
        btn.pack()
    
    #add movie to moviedata file
    def add(genre, movie):

        with open('moviedata', 'r') as f:
            movie_data = f.readline()
            movie_data = ast.literal_eval(movie_data)
            f.close()
        
        movie_data[genre].append([movie, 2])

        with open('moviedata', 'w') as f:
            f.write(json.dumps(movie_data))
            f.close()
        
        manager.portal()

    #change the price of in-time price and late price
    def price(price, late_price):
        try:
            change_screen.destroy()
        except:
            pass

        with open('information', 'r') as f:
            info = f.readline()
            info = ast.literal_eval(info)
            f.close()
            
        if price and not late_price:
            info['price'] = price
            with open('information', 'w') as f:
                f.write(json.dumps(info))
                f.close()
            manager.portal()

        elif price and late_price:
            info['price'] = price
            info['late_price'] = late_price
            with open('information', 'w') as f:
                f.write(json.dumps(info))
                f.close()
            manager.portal()
        
        elif not price and late_price:
            info['late_price'] = late_price
            with open('information', 'w') as f:
                f.write(json.dumps(info))
                f.close()
            
            manager.portal()
        
        else:
            pass
    
    #changing price input feild screen.
    def change():
        global change_screen
        
        try:
            managerscreen.destroy()

        except:
            pass
        
        change_screen = Tk()
        in_time = Label(change_screen, text='New In-time price')
        in_time.pack()
        price = Entry(change_screen)
        price.pack()
        late_time = Label(change_screen, text='New Late price')
        late_time.pack()
        late_price = Entry(change_screen)
        late_price.pack()
        btn = Button(change_screen, text='Change!', command = lambda: manager.price(price.get(), late_price.get()))
        btn.pack()

    #deleing the movie from movie data
    def delete(genre, movie):

        with open('moviedata', 'r') as f:
            movie_data = f.readline()
            movie_data = ast.literal_eval(movie_data)
            f.close()
        
        try:
            movie = [i for i in range(len(movie_data[genre])) if movie_data[genre][i][0] == movie]
            movie = movie[0]
            
            movie_data[genre].pop(movie)

            with open('moviedata', 'w') as f:
                f.write(json.dumps(movie_data))
                f.close()
        
            manager.portal()
        except:
            pass

    #delete movie
    def delete_movie():
        global delete_screen
        try:
            managerscreen.destroy()
        except:
            pass
            
        delete_screen = Tk()
        delete_screen.geometry('250x250')
        genre = Label(delete_screen, text='Pick Genre')
        genre.pack()
        genre_list = ['Horror', 'Romance', 'Adventure', 'Comedy', 'Fiction']
        setting = StringVar(delete_screen)
        setting.set("Pick Genre!")
        genre_choice = OptionMenu(delete_screen, setting, *genre_list)
        genre_choice.pack()

        movies_info = Label(delete_screen, text='Movie name')
        movies_info.pack()
        movie_entry = Entry(delete_screen)
        movie_entry.pack()
        btn = Button(delete_screen, text='Submit!', command=lambda:manager.delete(setting.get(), movie_entry.get()))
        btn.pack()



    #manager screen
    def portal():
        global managerscreen
        try:
            screen2.destroy()
        except:
            try:
                add_screen.destroy()
            except:                
                try:
                    delete_screen.destroy()
                except:
                    pass
        
        #window
        managerscreen = Tk()
        managerscreen.geometry('350x350')
        managerscreen.config(bg='white')
        
        with open('moviedata', 'r') as f:
            info = f.readline()
            info = ast.literal_eval(info)
            f.close()
        
        genre = ['Horror', 'Romance', 'Adventure', 'Comedy', 'Fiction']

        for i in genre:
            movie_genre = Label(managerscreen, text=f'| {i} |', bg='white', fg='red')
            movie_genre.pack()
            for x in info[i]:
                movie_name = Label(managerscreen, text=f'{x[0]}: There are {x[1]} movies in stock!', bg='white')
                movie_name.pack()

        add_movie = Button(managerscreen, text='Add movie!', command = manager.add_movie)
        add_movie.pack()

        delete_movie = Button(managerscreen, text='Delete movie!', command = manager.delete_movie)
        delete_movie.pack()

        price = Button(managerscreen, text='Change Price', command = manager.change)
        price.pack()

        with open('information', 'r') as file:
            credintals = file.readline()
            credintals = ast.literal_eval(credintals)
            file.close()

        revenue = 0

        for r in credintals['revenue']:
            revenue += int(r)
        
        revenue_label = Label(managerscreen, text=f'\n The total revenue for this month is ${revenue*2}.\n')
        revenue_label.pack()

        #if there are users in the system
        if len(credintals["user"]) > 1:
            #creating label to show users and their information on the screen.
            for i in range(1, len(credintals["user"])):
                credintals_display = Label(managerscreen, text=(("\nUser: {} \nEmail: {} \nCredit-Card: {} \nLogin-Code: {} \nRented-Videos: {} \nTransaction: {} \n-----------------------------------------").format(credintals["user"][i], credintals["Email"][i], credintals["credit"][i], credintals["Login-Code"][i], credintals["Rented"][i], credintals['Transaction'][i])), bg='white', fg='red')
                credintals_display.pack()
                delete = Button(managerscreen, text='Delete', fg = 'red', bg='black',command= lambda i=i:manager.delete_user(i))
                delete.pack()
        else:
            #if there aren't any users in the system.
            error = Label(managerscreen, text='No user found in the database!', fg = 'red', bg='white')
            error.pack()
        
        managerscreen.mainloop()

#this creates the login page where the user can input the login code and their name to enter the system.
class login_screen:

    #this checks the login information to make sure the inputted login code and name is correct.
    #it also check if the inputted information is the manager's information.
    def login_check():
        global current_user, current_email
        if user_password.get() == "" or user_name.get() == "":
            pass
        elif user_password.get() == 'M123' and user_name.get() == "Manager":
                manager.portal()              
        else:
            file = open('information', 'r')
            info = file.readline()
            info = ast.literal_eval(info)
            file.close()
            for i in info["user"]:
                if i == user_name.get():
                    current_user = i
                    current_email = info['Email'][info['user'].index(current_user)]
                    x = info['user'].index(i)
                    if int(user_password.get()) == info["Login-Code"][x]:
                        screen2.destroy()
                        rental.user_interface()
                    else:
                        pass
                else: 
                    error = Label(screen2, text='user doesn\'t exist', fg='red')
                    error.pack()

    #initializing screen size
    def login():
        global user_name, user_password, screen2
        try:
            screen.destroy()
        except:
            pass

        #creating screen
        screen2 = Tk()
        screen2.geometry("550x500")
        screen2.resizable(width=0, height=0)
        # screen2.pack_propagate(0)

        #font
        font = Font(family='Calibri',
              size=12,
              slant='italic',
              underline=0,
              overstrike=0)
        
        # Add image file
        bg = ImageTk.PhotoImage(Image.open("po.png"))
  
        # Show image using label
        label1 = Label(screen2, image = bg, bg = 'white')
        label1.place(x = 0,y = 0)

        #screen design
        title = Label(screen2, text="\n\n\n\n\nWelcome to the DSC Video Store\n", font=font, bg='white')
        title.pack()
        sub_1 = Label(screen2, text="Please Login using your username and password!\n\n", font=font, bg='white')
        sub_1.pack()

        logo = Label(screen2, bg='white')
        logo.pack()

        #login information UI
        username = Label(screen2, text= '\nName: ', bg='white') 
        username.pack()
        user_name = Entry(screen2, width=20)
        user_name.pack()
        userpassword = Label(screen2, text='\nLogin Code: ', bg='white')
        userpassword.pack()
        user_password = Entry(screen2, width=20)
        user_password.pack()
        login_btn = Button(screen2, text=" Login ", command=login_screen.login_check)
        login_btn.pack()
        screen2.mainloop()

#when the user clicks the sign up button it takes them to a different page where they can create an account.
#information suchs as name, email and credit card is asked.
class register:

    #this opens the existing information file to store the in users information in it.
    def write():
        try:
            int(credit_input.get())
            if fullname_input.get() == "" or email_input.get() == "" or credit_input.get() == "" or len(credit_input.get()) != 11:
                pass
            else:
                tosend = email_input.get()
                code = random.randint(1,9999)
                count = 0
                #reading the informatiom file
                file = open('information', 'r')
                info = file.readline()
                info = ast.literal_eval(info)
                file.close()

                #checking wether information already exists
                for i in info["user"]:
                    if fullname_input.get() == i:
                        error = Label(screen1, text='This user already exists!', fg='red')
                        error.pack()
                        count += 1
                    else:
                        pass
                for i in info["Login-Code"]:
                    while code == i:
                        code = random.randint(1,9999)
                    else:
                        pass

                #checking wether user exists if yes stay on the page and don't write the information in the file.
                if count >= 1:
                    pass
                #if the user doesn't exists then go and write the information into the file.
                else:
                    try:
                        pass
                        # #sending the user their login code
                        # receiver = tosend 
                        # body = "Your login code is " + str(code) + "."
                        # user_information = yagmail.SMTP("@gmail.com", 'password')
                        # user_information.send(to=receiver,subject="Video Rental Login Code!",contents=body)   
                    except:
                        register.page()

                    with open('information', 'w') as file:
                        info = info
                        info["user"].append(fullname_input.get())
                        info["Email"].append(email_input.get())
                        info["credit"].append(credit_input.get())
                        info["Login-Code"].append(code)
                        info["Rented"].append([])
                        info['Transaction'].append([])
                        file.write(json.dumps(info))
                        file.close()
                    screen1.destroy()
                    welcome_screen.front()
        except:
            pass

    #this is the layout and design for the sign up page.
    def page():
        global screen1, fullname_input, email_input, credit_input

        try:
            screen.destroy()
        except:
            pass

        #window
        screen1 = Tk()
        screen1.geometry("250x250")
        screen1.config(bg='white')
        screen1.resizable(width=0, height=0)
        screen1.pack_propagate(0)

        #font style
        font = Font(family='Calibri',
            size=12,
            slant='italic',
            underline=1,
            overstrike=0)
        
        #input name feild
        #input email feild
        #input credit card feild
        #sign-up button
        fullname = Label(screen1, text="\nEnter your Fullname", bg = "white", font=font)
        fullname.pack()
        fullname_input = Entry(screen1, width = 20)
        fullname_input.pack()

        email = Label(screen1, text="\nEnter your email", bg = "white", font=font)
        email.pack()
        email_input = Entry(screen1, width = 20)
        email_input.pack()

        credit = Label(screen1, text="\nEnter your cerdit card", bg = "white", font=font)
        credit.pack()
        credit_input = Entry(screen1, width = 20)
        credit_input.pack()

        sign_up_btn = Button(screen1, text="Sign-up", command=register.write)
        sign_up_btn.pack()
        screen1.mainloop()



#contains the layout and design for the login or signup page.
class welcome_screen():
    
    #this creates a screen with fixed size and makes sure that the screen has 2 buttons a sign up and a login.
    #when one of the is clicked the function respective to them is called.
    def front():
        global screen

        #window 
        screen = Tk()
        screen.geometry('250x250')
        screen.config(bg="white")
        screen.resizable(width=0, height=0)
        screen.pack_propagate(0)

        #font style for the page
        font = Font(family='Calibri',
                size=12,
                slant='italic',
                underline=0,
                overstrike=0)

        #title of the page
        #login button
        #signup button
        title = Label(screen, text="Login or Sign up\n\n", bg = "white", font=font)
        title.pack()
        login_btn = Button(screen, text="Login", bg="white", command= login_screen.login)
        login_btn.pack()
        signup_btn = Button(screen, text="Sign up", bg="white", command= register.page)
        signup_btn.pack()
        screen.mainloop()

#creating preset files and sending out the manager info.
#checking if the files already exists if so then don't do anything.
#if the file doesn't exists create them and preset information in them.
if os.path.exists("information") and os.path.exists("moviedata"):

    pass

else:

    with open('moviedata', 'w') as file:
        movies = {'Horror': [['Friday the 13th', 2],['Scream', 2],['It Chapter Two', 2]],'Romance':[['Emma', 2],['Last Christmas', 2],['Flipped', 2]], 'Adventure': [['Black Widow', 2],['Deadpool 2', 2], ['Dune', 2]], 'Comedy': [['Free Guy', 2],['Jungle Cruise', 2],['Ghost Busters', 2]], 'Fiction': [['The Martian', 2], ['Arrival', 2], ['The Matrix', 2]]}
        file.write(json.dumps(movies))
        file.close()
    with open('information', 'a') as file:
        preinfo = {'user': ['Manager'], 'Email': ['14118@dsc.edu.hk'], 'credit': ["None"], 'Login-Code': ['M123'], 'Rented': [['None']], 'Transaction': [["NONE"]], 'revenue': [], 'late_price': 40, 'price': 30}
        file.write(json.dumps(preinfo))
    # receiver = '14118@dsc.edu.hk'
    # body = "Manager login code is M123."
    # user_information = yagmail.SMTP("@gmail.com", 'password')
    # user_information.send(to=receiver,subject="Video Rental Manager Login Code!",contents=body)   

welcome_screen.front()