# a catch-all file until I can build an object-oriented class file to nest
# all of the compartmentalized files in

def filmRecs():
    #First we'll make a couple of dictionaries that allow you to find
    #movie names given the ID number, and the ID number given the name
    filmnames = {}
    filmids = {}
    with open("u.item","r") as file:
        done = False
        while not done:
            f = file.readline()
            f = f.split('|')
            ID = f[0]
            try:
                movie = f[1][0:len(f[1])-7]
                #this block tested for duplicates in the data
                try:
                    filmids[movie]
                except KeyError:
                    filmids[movie] = ID
                    filmnames[ID] = movie
            except IndexError:
                done = True
                
    # next we'll build the user's own dictionary of films and ratings
    user = {}
    done = False
    while not done:
        x = input("Enter film title. When finished, enter DONE : ")
        if x.lower()=="done":
            print(user)
            done = True
        else:
            try:
                filmids[x]
                y = input("Enter your rating [1,2,3,4,5] for this film: ")
                user[filmids[x]] = y
            except KeyError:
                print("Film not recognized in the database. Try another!")

    #now we can build a nested dictionary of all the users' ratings
    usersRecs = {}
    for i in user:
        for j in open('u.data','r'):
            j = j.split('\t')
            if i==j[1] and j[0] not in usersRecs:
                #print(j[0])
                usersRecs[j[0]] = {j[1]:j[2]}
                for k in open('u.data','r'):
                    k = k.split('\t')
                    if k[0]==j[0]:
                        usersRecs[j[0]][k[1]] = k[2]
            else:
                pass
            
    # Now we'll create a nested dictionary of the users' ratings to
    # compare and find a correlation coefficient to the user's ratings
    #usersCor = {}
    #for i in user:
    #    for j in open('u.data','r'):
    #        j = j.split('\t')
    #        if i==j[1] and j[0] not in usersCor:
    #            usersCor[j[0]] = {j[1]:j[2]}
    #        elif i==j[1] and j[0] in usersCor:
    #            usersCor[j[0]][j[1]] = j[2]
    #        else:
    #            pass

    #From here we'll find the Pearson correlation coefficient of each
    #user when compared to the primary user and make a dictionary linking
    #each user to their correlation coefficient
    import numpy
    usersCor = {}
    for i in usersRecs:
        complst = []
        userlst = []
        for j in user:
            if j in usersRecs[i]:
                userlst.append(int(user[j]))
                complst.append(int(usersRecs[i][j]))
        try:
            c=int(numpy.corrcoef(userlst, complst)[0][1])
            usersCor[i] = numpy.ma.corrcoef(userlst, complst)[0][1]
        except ValueError:
            pass

    RecsNum={}
    RecsDen={}
    num = 0
    den = 0
    for i in usersRecs:
        if i in usersCor:
            for j in usersRecs[i]:
                if j not in RecsNum:
                    RecsNum[j] = 0
                    RecsDen[j] = 0
                #else:
                RecsNum[j] += float(usersCor[i]) * int(usersRecs[i][j])
                RecsDen[j] += float(usersCor[i])
                    
    Recs = {}
    for i in RecsNum:
        try:
            Recs[i] = RecsNum[i]/RecsDen[i]
        except ZeroDivisionError:
            print("User excluded, bad taste in films.")
    
    recs = sorted(Recs, key=Recs.get, reverse = True)

    for i in recs[0:30]:
        print(filmnames[i])
        
    # okay, we should have all of the users and all of the films they
    # have rated now in a nested dictionary. get recommendations~*
    
        


    
