import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

"""
Approach:
1.	SUR and TUR datasets ----------------- Abdiel  (DONE)
2.	Show correlation matrix –-------------- Abdiel (DONE)
3.	Indicate the number of universities (Top 25 universities) --- --------------Cabel
    a.	Cap at 2
    b.	Both universitys need to be in both datasets
4.	We give the user ranking or score –----------------- Brandon
5.	Rankings or score changes throughout 2012 to 2015 --- --------Abdiel
6.	Plot the rankings or score against the features of interest --- Brandon
    a.	SUR = Publications, alumni awards, staff awards, and cited research vs Ranking or score
    b.	TUR = Teaching and Research vs Ranking or score

"""

#############################################################################################################################################################
# This section of code will find commonly ranked universities between two of the datasets, and allow the user to pick which two to run analysis on.
# Read the times data and shanghai datasets

times_df = pd.read_csv('./timesData.csv')
shanghai_df = pd.read_csv('./shanghaiData.csv')

# Change dtypes to string
times_df = times_df.astype({'world_rank':'string', 
                  'university_name':'string'})
shanghai_df = shanghai_df.astype({'world_rank':'string', 
                  'university_name':'string'})

# replace values '-' for empty ones
times_df.international = times_df.international.str.replace('-','0')
times_df.income = times_df.income.str.replace('-','0')
times_df.total_score = times_df.total_score.str.replace('-','0')

# Check -- https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.filter.html
shanghai_df['world_rank'] = shanghai_df['world_rank'].str.replace('-', '')
times_df['world_rank'] = times_df['world_rank'].str.replace('-', '')
times_df['world_rank'] = times_df['world_rank'].str.replace('=', '')
shanghai_df["world_rank"] = shanghai_df["world_rank"].astype('int64')
times_df["world_rank"] = times_df["world_rank"].astype('int64')
times_df["income"] = times_df["income"].astype('float64')
times_df["total_score"] = times_df["total_score"].astype('float64')
times_df["international"] = times_df["international"].astype('float64')

elim_yr = np.arange(2005,2012)
shanghai_df = shanghai_df[shanghai_df.year.isin(elim_yr) == False]
times_df = times_df.drop(times_df.index[times_df['year'] == 2011])
times_df = times_df.drop(times_df.index[times_df['year'] == 2016])

print('Times University Rankings Information:')
print(times_df.info(), end='\n\n')
print(times_df.describe(), end='\n\n')

print('Shanghai University Rankings Information:')
print(shanghai_df.info(),end='\n\n')
print(shanghai_df.describe(),end='\n\n')

sns.heatmap(times_df.corr(), annot =True, cmap = 'PiYG')
plt.title('Correlation Matrix of Times University Rankings', fontsize = 20) # title with fontsize 20
plt.show()

sns.heatmap(shanghai_df.corr(), annot =True, cmap = 'PiYG')
plt.title('Correlation Matrix of Shanghai University Rankings', fontsize = 20) # title with fontsize 20
plt.show()

# Get the list of top universities present in both dataframes
top_universities = list(set(times_df.head(25)['university_name']).intersection(set(shanghai_df.head(25)['university_name'])))

top_universities.sort() 

# Print the list of top universities and prompt the user to choose two
print('Choose two universities to compare from the following list of top ranked universities:')
for i, university in enumerate(top_universities):
    print(f'{i+1}. {university}')

# Get the user's choices, ensure they are different, and on the provided list
choice_1 = 0
choice_2 = 0
while choice_1 == choice_2:
    try:
        choice_1 = int(input('Enter the number corresponding to the first university you want to compare: '))
        choice_2 = int(input('Enter the number corresponding to the second university you want to compare: '))
        if choice_1 == choice_2:
            print('Please choose two different universities.')
            choice_1 = 0
            choice_2 = 0
        elif choice_1 < 1 or choice_1 > len(top_universities) or choice_2 < 1 or choice_2 > len(top_universities):
            print('Please choose a university from the list.')
            choice_1 = 0
            choice_2 = 0
    except ValueError:
        print('Please enter a valid number.')
        choice_1 = 0
        choice_2 = 0

# Get the selected universities and their data from the Times and Shanghai dataframes
university_1 = top_universities[choice_1-1]
university_2 = top_universities[choice_2-1]
times_uni_1 = times_df[times_df['university_name'] == university_1]
times_uni_2 = times_df[times_df['university_name'] == university_2]
shanghai_uni_1 = shanghai_df[shanghai_df['university_name'] == university_1]
shanghai_uni_2 = shanghai_df[shanghai_df['university_name'] == university_2]

acc1 = np.unique(times_uni_1['university_name'])
acc2 = np.unique(times_uni_2['university_name'])
acc3 = np.unique(shanghai_uni_1['university_name'])
acc4 = np.unique(shanghai_uni_2['university_name'])

merged_df = pd.merge(times_uni_1, times_uni_2, on='year', suffixes=('_Times', '_Times'))
merged_df = pd.merge(merged_df, shanghai_uni_1, on='year', suffixes=('_Shanghai', '_Shanghai'))
merged_df = pd.merge(merged_df, shanghai_uni_2, on='year', suffixes=('_Shanghai', '_Shanghai'))

# save the DataFrame as a CSV file (good way to check the merged data and understand it)
merged_df.to_csv('MergedUniData.csv', index=False)  # set index=False to exclude the index column in the output file

######################################################################################################################################################

# Prompt the user for rank or score until a valid input is recieved
y_axis = input("Please enter the preferred metric for evaluation as either Rank or Score:  ")
y_axis = y_axis.lower()

while y_axis not in ['rank','score']:
    print('Invalid Input')
    y_axis = input("Please enter Rank or Score: ")
    y_axis = y_axis.lower()
    
#print(merged_df.dtypes)


# With the users input determine the data we want and stores it in the y_axis_data
# For future code (ie for steps 5 and 6 use this as the y-axis)

if(y_axis == 'rank'):
    y_axis_data = merged_df[['world_rank_Times','world_rank_Shanghai']]
    y_axis_data.columns = [f"{col}_{i}" for i, col in enumerate(y_axis_data.columns)]
    y_axis_data.rename(columns={'world_rank_Times_0': "world_rank_time_" + university_1,
                                'world_rank_Times_1': "world_rank_time_" + university_2,
                                'world_rank_Shanghai_2': "world_rank_Shanghai_" + university_1,
                                'world_rank_Shanghai_3': "world_rank_Shanghai_" + university_2}, inplace=True)
    str1 = f'Ranking of {acc1[0]} by the Times Rankings'
    str2 = f'Ranking of {acc2[0]} by the Times Rankings'
    str3 = f'Ranking of {acc3[0]} by the Shanghai Rankings'
    str4 = f'Ranking of {acc4[0]} by the Shanghai Rankings'
    plt.figure(figsize=(8,6))
    plt.plot(times_uni_1.year, times_uni_1.world_rank, label = str1, linestyle='--', marker='v')
    plt.plot(times_uni_2.year, times_uni_2.world_rank, label = str2, linestyle=':', marker='D')
    plt.plot(shanghai_uni_1.year, shanghai_uni_1.world_rank, label = str3, linestyle='-.', marker='s')
    plt.plot(shanghai_uni_2.year, shanghai_uni_2.world_rank, label = str4, linestyle='-', marker='o')
    plt.gca().invert_yaxis()
    plt.xticks(np.arange(2012, 2016, 1))
    #plt.xticks(rotation = 90)
    plt.xlabel('Year', fontsize = 12)
    plt.ylabel('Ranking', fontsize = 12) 
    plt.tick_params(axis='both', labelsize = 10)
    plt.title('University ranking comparision between the Times and Shanghai Rankings', fontsize = 12, fontweight="bold")
    plt.legend(loc='best')
    plt.show()

if(y_axis == 'score'):
    y_axis_data = merged_df[['total_score_Times','total_score_Shanghai']]
    y_axis_data.columns = [f"{col}_{i}" for i, col in enumerate(y_axis_data.columns)]
    y_axis_data.rename(columns={'total_score_Times_0': "total_score_time_" + university_1,
                                'total_score_Times_1': "total_score_time_" + university_2,
                                'total_score_Shanghai_2': "total_score_Shanghai_" + university_1,
                                'total_score_Shanghai_3': "total_score_Shanghai_" + university_2}, inplace=True)
    str1 = f'Score of {acc1[0]} by the Times Rankings'
    str2 = f'Score of {acc2[0]} by the Times Rankings'
    str3 = f'Score of {acc3[0]} by the Shanghai Rankings'
    str4 = f'Score of {acc4[0]} by the Shanghai Rankings'
    plt.figure(figsize=(8,6))
    plt.plot(times_uni_1.year, times_uni_1.total_score, label = str1, linestyle='--', marker='v')
    plt.plot(times_uni_2.year, times_uni_2.total_score, label = str2, linestyle=':', marker='D')
    plt.plot(shanghai_uni_1.year, shanghai_uni_1.total_score, label = str3, linestyle='-.', marker='s')
    plt.plot(shanghai_uni_2.year, shanghai_uni_2.total_score, label = str4, linestyle='-', marker='o')
    plt.xticks(np.arange(2012, 2016, 1))
    #plt.xticks(rotation = 90)
    plt.xlabel('Year', fontsize = 12)
    plt.ylabel('Score', fontsize = 12) 
    plt.tick_params(axis='both', labelsize = 10)
    plt.title('University scoring comparision between the Times and Shanghai Rankings', fontsize = 12, fontweight="bold")
    plt.legend(loc='best')
    plt.show()
#print(y_axis_data)



######################################################################################################################################################

# Feature descriptions
print()
print('Key features that have influence in both ranking and scoring of an university for each Ranking Dataset.', end='\n\n')
print('For the Times Higher Education World University Rankings, the features of interest are:')

features1 = ["Research", "Citations", "Teaching"]

for i, f1 in enumerate(features1):
    print(f'{i+1}. {f1}')
# Prompt the user for features of interest
x_axis = int(input('Enter the number corresponding to the feature of interest to be evaluated: '))

while x_axis not in range(1,4):
    print('Invalid Input')
    x_axis = int(input('Enter the number corresponding to the feature of interest to be evaluated: '))
 
if x_axis == 1:
    x_axis = "research_Times"
elif x_axis == 2:
    x_axis = "citations_Times"
elif x_axis == 3:
    x_axis = "teaching_Times"
    
colors = {"2012": "red", "2013": "orange", "2014": "blue", "2015": "green"}

temp = merged_df[x_axis]
data1 = pd.DataFrame()
data1[x_axis] = temp.iloc[:,0]
data1[y_axis] = y_axis_data.iloc[:,0]
data1["year"] = merged_df["year"]

temp = merged_df[x_axis]
data2 = pd.DataFrame()
data2[x_axis] = temp.iloc[:,1]
data2[y_axis] = y_axis_data.iloc[:,1]
data2["year"] = merged_df["year"]

fig, ax = plt.subplots()
handles, labels = [], []
for year in colors:
    year_data1 = data1[data1["year"] == int(year)]
    year_data2 = data2[data2["year"] == int(year)]
    s1 = ax.scatter(year_data1[x_axis], year_data1[y_axis], color=colors[year], marker ='o', label=university_1+f' ({year})')
    s2 = ax.scatter(year_data2[x_axis], year_data2[y_axis], color=colors[year], marker ='^', label=university_2+f'( {year})')
    handles.extend([s1, s2])
    labels.extend([f'University 1 ({year})', f'University 2 ({year})'])
ax.set_ylabel(y_axis.capitalize())
ax.set_xlabel(x_axis.split('_')[0].capitalize())
ax.set_title("Data from Times Higher Education World University Rankings")
plt.legend()
plt.show()

print()

print('For the Shanghai Academic Ranking of World Universities, the features of interest are:')
features2 = ["Highly Cited Researchers", "Publications in Nature and Science Journals", "Staff Awards"]
for i, f2 in enumerate(features2):
    print(f'{i+1}. {f2}')
# Prompt the user for features of interest
x_axis = int(input('Enter the number corresponding to the feature of interest to be evaluated: '))

while x_axis not in range(1,4):
    print('Invalid Input')
    x_axis = int(input('Enter the number corresponding to the feature of interest to be evaluated: '))
    
if x_axis == 1:
    x_axis = "hici_Shanghai"
elif x_axis == 2:
    x_axis = "ns_Shanghai"
elif x_axis == 3:
    x_axis = "award_Shanghai"

if x_axis == "hici_Shanghai":
    x_axis_label = "Highly Cited Researchers"
elif x_axis == "ns_Shanghai":
    x_axis_label = "Publications in Nature and Science Journals"
elif x_axis == "award_Shanghai":
    x_axis_label = "Staff Awards"
    
temp = merged_df[x_axis]
data1 = pd.DataFrame()
data1[x_axis] = temp.iloc[:,0]
data1[y_axis] = y_axis_data.iloc[:,2]
data1["year"] = merged_df["year"]

temp = merged_df[x_axis]
data2 = pd.DataFrame()
data2[x_axis] = temp.iloc[:,1]
data2[y_axis] = y_axis_data.iloc[:,3]
data2["year"] = merged_df["year"]

combined_data = pd.concat([data1, data2])

fig, ax = plt.subplots()
handles, labels = [], []
for year in colors:
    year_data1 = data1[data1["year"] == int(year)]
    year_data2 = data2[data2["year"] == int(year)]
    s1 = ax.scatter(year_data1[x_axis], year_data1[y_axis], color=colors[year], marker ='o', label=university_1+f' ({year})')
    s2 = ax.scatter(year_data2[x_axis], year_data2[y_axis], color=colors[year], marker ='^', label=university_2+f'( {year})')
    handles.extend([s1, s2])
    labels.extend([f'University 1 ({year})', f'University 2 ({year})'])
ax.set_ylabel(y_axis.capitalize())
ax.set_xlabel(x_axis_label)
ax.set_title("Data from Shanghai Academic Ranking of World Universities")
plt.legend()
plt.show()


