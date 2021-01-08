import xlrd
fileloc = "/Academic Projects/Subject projects/Data Analysis/Classification/Dataset/ign.xls"
wb = xlrd.open_workbook(fileloc)
sheet=wb.sheet_by_index(0)
score_phrase,title,platform,score=sheet.col_values(1,1),sheet.col_values(2,1),sheet.col_values(4,1),sheet.col_values(5,1)
genre,editor_choice,release_year,release_month=sheet.col_values(6,1),sheet.col_values(7,1),sheet.col_values(8,1),sheet.col_values(9,1)

def ratings():
    rating=0
    for sum in score:
        rating+=sum
    ratingss=rating/len(sheet.col_values(0,1))
    print(ratingss)
print("\nAverage score of all games in 20 years: ")
ratings()

# can be used with inbuilt min and max functions
print("\nMaximum score in 20 years: ")
def maximum(l):
    Max = 0
    for num in l:
        if Max < num:
            Max = num
    return Max
print(maximum(score))

print("\nMinimum score in 20 years: ")
def minimum(l):
    Min = l[0]
    for num in l:
        if Min > num:
            Min = num
    return Min
print(minimum(score))

#   Function for getting distinct values(platforms/genre/games) used
#   over 20 years into a list
# def get_distinct(col_no):
#     temp_list = []
#     i = 1   # for ignoring the first row, since it contains headers
#     while i<len(score):
#         if sheet.cell_value(i,col_no) not in temp_list:
#             temp_list.append(sheet.cell_value(i,col_no))
#         i=i+1
#     return temp_list

# creating and inserting distinct values of platforms used over 20 years into a list
p=[]
i=1
while i<len(score):
   if sheet.cell_value(i,4) not in p:
       p.append(sheet.cell_value(i,4))
   i=i+1
#Calculating the number of distinct genre used in 20 years
gen=[]
i=1
while i<len(score):
   if sheet.cell_value(i,6) not in gen:
       gen.append(sheet.cell_value(i,6))
   i=i+1
#Calculating the distinct number of games used in 20 years
g=[]
i=1
while i<len(score):
    if sheet.cell_value(i,2) not in g:
        g.append(sheet.cell_value(i,2))
    i=i+1
#Calculating the number of games which got editors choice as 'Yes'
edy=[]
i=1
while i<len(score):
    if "Y" in sheet.cell_value(i,7):
        edy.append(sheet.cell_value(i,7))
    i=i+1
edn=[]
i=1
while i<len(score):
    if "N" in sheet.cell_value(i,7):
        edn.append(sheet.cell_value(i,7))
    i=i+1
row=sheet.col_values(9,1)
month={int(i):row.count(i) for i in row}
print("\nMonths which games released:")
print(month)
aa_plat,bb_genre,cc_game,dd_edi=len(p),len(gen),len(g),len(edy)
#Finding the most used month to release a game
findmaxmonth = [(value, key) for key, value in month.items()]
print("\n*** GAME STATISTICS OF 20 YEARS ***")
print("Platforms Used  | Genre Used |  Games released | Selected for Editors choice  |  Month where Most games released ")
print("    ",aa_plat,"     \t\t",bb_genre,"    \t\t",cc_game,"         \t\t", dd_edi, "\t\t\t\t\t\t    ",max(findmaxmonth)[1],"\n")
#Inserting 20 years into a list for further use
years=list(range(1995,2017))
years=years[::-1]
years[21]=1970
#year with number of games released within that particular year
year_dict = {int(i):release_year.count(i) for i in release_year}
#creating a new list to find the range of years used in the excel
list,lists=[],[]
for i in range(0,len(year_dict)):
    list.append(year_dict[years[i]])
sum,i=0,0
while i<len(years):
    sum=sum+list[i]
    lists.append(sum)
    i=i+1

print("Year | Max score  |  Min score  |  Total games Released    |   Average Score")
print("____________________________________________________________________________")
def details(y,int,pos):
    return max(sheet.col_values(5,int,pos))

def details1(y,int,pos):
    return min(sheet.col_values(5,int,pos))

def avg_score(y,int,pos):
    score=0
    for sum in sheet.col_values(5,int,pos):
        score+=sum
    scores=score/len(sheet.col_values(5,int,pos))
    return scores

print(years[0],"\t",details(2016,1,lists[0]),"\t\t\t",details1(2016,1,lists[0]),"\t\t\t",year_dict[2016],"\t\t\t\t",avg_score(2016,1,lists[0]))
#If else just to print in alignment
i=1
while i<len(years):
    int=lists[i-1]
    pos=lists[i]
    if i==21:
        print(years[i],"\t",details(years[i],int,pos),"\t\t\t",details1(years[i],int,pos),"\t\t\t",year_dict[years[i]],"\t\t\t\t\t",avg_score(years[i],int,pos))
    else:
        print(years[i],"\t",details(years[i],int,pos),"\t\t\t",details1(years[i],int,pos),"\t\t\t",year_dict[years[i]],"\t\t\t\t",avg_score(years[i],int,pos))
    i=i+1
#List of score phrase
ph=[]
i=1
while i<len(score):
    if sheet.cell_value(i,1) not in ph:
        ph.append(sheet.cell_value(i,1))
    i=i+1
#Seperating the score phrase into two positive and negative classes
positive=['Great','Amazing','Masterpiece','Good']
negative=['Okay','Bad','Mediocre','Disaster','Awful','Unbearable','Painful']
i=1
sumpos=0
while i<len(sheet.col_values(0,1)):
    if sheet.cell_value(i,1) in positive:
        sumpos=sumpos+1
        i=i+1
    else:
        i=i+1
i=1
sumneg=0
while i<len(sheet.col_values(0,1)):
    if sheet.cell_value(i,1) in negative:
        sumneg=sumneg+1
        i=i+1
    else:
        i=i+1

prob_success=sumpos/len(score)
prob_failure=sumneg/len(score)
platform_class1=p
genre_class2=gen
editor_class3=['Y','N']
platform_dict = {i:platform.count(i) for i in platform}
genre_dict={i:genre.count(i) for i in genre}
editor_dict={'Y':len(edy),'N':len(edn)}

# Naive Bayes' Algorithm to calculate the probability of 3 variants(genre,platform,editor choice) with two classes postitive and negative review
def naive_bayes(x,y,z):
    i,j,k=1,1,1
    aa,bb,cc=[],[],[]
    while i<len(score):
        if sheet.cell_value(i,4)==x and sheet.cell_value(i,1) in positive:
            aa.append(1)
        i=i+1

    while j <len(score):
        if sheet.cell_value(j,6)==y and sheet.cell_value(j,1) in positive:
            bb.append(1)
        j=j+1

    while k<len(score):
        if sheet.cell_value(k,7)==z and sheet.cell_value(k,1) in positive:
            cc.append(1)
        k=k+1
    a=len(aa)/sumpos
    b=len(bb)/sumpos
    c=len(cc)/sumpos
    d=sumpos/(len(score))
    res=a*b*c*d
    print("Possible of Success Rate:",res)
    i,j,k=1,1,1
    aa,bb,cc=[],[],[]
    while i<len(score):
        if sheet.cell_value(i,4)==x and sheet.cell_value(i,1) in negative:
            aa.append(1)
        i=i+1

    while j <len(score):
        if sheet.cell_value(j,6)==y and sheet.cell_value(j,1) in negative:
            bb.append(1)
        j=j+1

    while k<len(score):
        if sheet.cell_value(k,7)==z and sheet.cell_value(k,1) in negative:
            cc.append(1)
        k=k+1
    a=len(aa)/sumneg
    b=len(bb)/sumneg
    c=len(cc)/sumneg
    d=sumneg/(len(score))
    res=a*b*c*d
    print("Possible Failure Rate:",res)

#All the values are case sensitive
xx=input("Enter value for Platform(eg: RPG,PC,etc): ")
#Distinct list of used platforms over 20 years
#['Wii U', 'PlayStation 4', 'PC', 'Nintendo 3DS', 'Xbox One', 'Macintosh', 'iPhone', 'New Nintendo 3DS', 'PlayStation 3', 'PlayStation Vita', 'Android', 'Xbox 360', 'iPad', 'SteamOS', 'Linux', 'Windows Phone', 'PlayStation Portable', 'Wii', 'Windows Surface', 'Ouya', 'Nintendo DS', 'Nintendo DSi', 'Web Games', 'Arcade', 'PlayStation 2', 'Wireless', 'NES', 'Super NES', 'Genesis', 'Master System', 'NeoGeo', 'Commodore 64/128', 'TurboGrafx-16', 'iPod', 'Atari 5200', 'TurboGrafx-CD', 'Saturn', 'Atari 2600', 'Sega 32X', 'Vectrex', 'Game Boy', 'Sega CD', 'Game Boy Advance', 'Xbox', 'GameCube', 'N-Gage', 'Dreamcast', 'PlayStation', 'Pocket PC', 'Game Boy Color', 'Nintendo 64', 'DVD / HD Video Game', 'WonderSwan Color', 'Lynx', 'NeoGeo Pocket Color', 'WonderSwan', 'Nintendo 64DD', 'Game.Com', 'Dreamcast VMU']
yy=input("Enter value for Genre(eg: Racing,Action,Puzzle,etc):")
#Distinct list of used Genre over 20 years
#['Racing, Action', 'RPG', 'Puzzle', 'Shooter', 'Strategy, RPG', 'Strategy', 'Adventure', 'Action, Adventure', 'Sports', 'Action', 'Fighting', 'Fighting, Simulation', 'Platformer', 'Music, Action', 'Racing', 'Simulation', 'Flight', 'RPG, Simulation', 'Action, RPG', 'Hardware', 'Action, Platformer', 'Sports, Action', 'Shooter, Adventure', 'Battle', 'Puzzle, Action', 'Party', 'Other', 'Strategy, Simulation', 'Card, Battle', 'Adventure, RPG', 'Platformer, Adventure', 'Action, Strategy', 'Puzzle, Platformer', 'Shooter, RPG', 'Music, Adventure', 'Sports, Golf', 'Action, Compilation', 'Wrestling', 'Music', 'Board', 'Sports, Other', 'Compilation, RPG', 'Platformer, Action', 'Shooter, First-Person', 'Adventure, Adventure', 'Sports, Party', 'Sports, Simulation', 'Sports, Baseball', '', 'Puzzle, Adventure', 'Baseball', 'Flight, Action', 'Compilation', 'Action, Simulation', 'Sports, Compilation', 'Music, RPG', 'Card', 'Productivity, Action', 'RPG, Action', 'Educational, Puzzle', 'Hunting', 'Fighting, Action', 'Adventure, Episodic', 'Adventure, Adult', 'Pinball', 'Puzzle, RPG', 'Sports, Fighting', 'Adventure, Platformer', 'Action, Puzzle', 'Productivity', 'Puzzle, Word Game', 'Simulation, Adventure', 'Adventure, Compilation', 'Flight, Simulation', 'Other, Adventure', 'Trivia', 'Educational', 'Virtual Pet', 'Fighting, Compilation', 'Educational, Adventure', 'Puzzle, Compilation', 'Card, RPG', 'Educational, Productivity', 'Educational, Action', 'Music, Compilation', 'Adult, Card', 'Board, Compilation', 'Strategy, Compilation', 'Racing, Shooter', 'Casino', 'RPG, Compilation', 'Racing, Simulation', 'Educational, Card', 'Educational, Simulation', 'Card, Compilation', 'Shooter, Platformer', 'Racing, Editor', 'Action, Editor', 'Hunting, Action', 'Music, Editor', 'Fighting, Adventure', 'Educational, Trivia', 'Compilation, Compilation', 'Sports, Racing', 'Fighting, RPG', 'Other, Action', 'Racing, Compilation', 'RPG, Editor', 'Hunting, Simulation', 'Pinball, Compilation', 'Flight, Racing', 'Wrestling, Simulation', 'Sports, Editor']
zz=input("Editor's Choice(Y or N)?: ")
if xx not in platform_class1 or yy not in genre_class2 or zz not in editor_class3:
    raise SystemExit("\nIts not entered properly")

naive_bayes(xx,yy,zz)
#Code takes some time to run
