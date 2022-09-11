import pandas as pd
import matplotlib.pyplot as plt
from optparse import OptionParser
import sys

# ----------------()----------------()

parser = OptionParser()

# parser.add_option('--prob',dest='prob_sys1',type=float,help='Probability of picking system 1')
# parser.add_option('--food_thresh',dest='food_thresh',type=float,help='System switch threshold')

# options, otherjunk = parser.parse_args(sys.argv[1:])
# if len(otherjunk) != 0:
#     raise Exception('Command line input not understood: ' + str(otherjunk))
# args = dict()
#
# food_thresh = float(options.food_thresh)

food_thresh = [0.1,0.3,0.5,0.7,0.9]

# Load data files for plotting
df1 = pd.read_csv("data/system_2.csv") #System2(depth=2)
df2 = pd.read_csv("data/system_1.csv")#System1
df_thresh = []
for i in food_thresh:
    df_thresh.append(pd.read_csv("data/food_thresh_" + str(food_thresh) + ".csv"))
# df3 = #System 0 random

# Set parameters
from pylab import rcParams
rcParams['figure.figsize'] = 10, 10

# Define colours for easier mapping
colours = {"sys2_d2":'r',"sys2_d1":'orange',"sys1":'b',"sys0":'g'}

df1 = df1.sort_values(['score'], ascending=False)
df2 = df2.sort_values(['score'], ascending=False)
df3 = df3.sort_values(['score'], ascending=False)
df1 = df1.reset_index(drop=True)
df2 = df2.reset_index(drop=True)
df3 = df3.reset_index(drop=True)

# ----------------(Plot time graph)----------------(start)

fig = plt.figure()

mean1 = df1["time"].mean()
mean2 = df2["time"].mean()
mean3 = df3["time"].mean()

plt.plot(df1["time"], label='System2', color=colours["sys2_d2"],figure=fig)
plt.axhline(y=mean1, color=colours["sys2_d2"], linestyle='--',figure=fig)

plt.plot(df2["time"]  ,label='System1',color=colours["sys1"],figure=fig)
plt.axhline(y=mean2, color=colours["sys1"], linestyle='--',figure=fig)

plt.plot(df3["time"]  ,label='System0',color=colours["sys0"],figure=fig)
plt.axhline(y=mean3, color=colours["sys0"], linestyle='--',figure=fig)

plt.xlabel('Game Number',figure=fig)
plt.ylabel('Time',figure=fig)
plt.title('Sys1 Prob = ' + str(prob_sys1),figure=fig)
# plt.plot()
plt.legend()
plt.savefig('plots/random_choice_'+str(prob_sys1)+'/time.png',figure=fig)

# ----------------(Plot time graph)----------------(end)


# ----------------(Plot score graph)----------------(start)

fig = plt.figure()

mean1 = df1["score"].mean()
mean2 = df2["score"].mean()
mean3 = df3["score"].mean()

plt.plot(df1["score"],label='System2(depth=2)',color=colours["sys2_d2"],figure=fig)
plt.axhline(y=mean1, color=colours["sys2_d2"], linestyle='--',figure=fig)

plt.plot(df2["score"]  ,label='System1', color=colours["sys1"],figure=fig)
plt.axhline(y=mean2, color=colours["sys1"], linestyle='--',figure=fig)

plt.plot(df3["score"]  ,label='System0',color=colours["sys0"],figure=fig)
plt.axhline(y=mean3, color=colours["sys0"], linestyle='--',figure=fig)

plt.axhline(y=0, color='black', linestyle='-',figure=fig)
plt.xlabel('Game Number',figure=fig)
plt.ylabel('Score',figure=fig)
plt.title('Sys1 Prob = ' + str(prob_sys1),figure=fig)
# plt.plot()
plt.legend()
plt.savefig('plots/random_choice_'+str(prob_sys1)+'/score.png',figure=fig)

# ----------------(Plot score graph)----------------(end)


# ----------------(Win rate)----------------(start)

df1 = df1[df1.result != 0]
df2 = df2[df2.result != 0]
df3 = df3[df3.result != 0]

print ("System2(Depth=2) = ",df1["result"].count())
print ("System2(Depth=1) = ",df2["result"].count())
print ("System1 = ",df3["result"].count())

# ----------------(Win rate)----------------(end)
