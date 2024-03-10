import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox


rozmFont=12
# Create a subplot

fig, ax = plt.subplots(figsize = (15,7))
plt.subplots_adjust(bottom=0.35)

# Create and plot a bar chart
Energy = [0,5,10,15,20,25,30] #MWh
Price = [2,2,10,17,27,32,37]
plot1 = ax.step(Energy, Price, where='mid')
plt.xlim([0, max(Energy)+2])
plt.ylim([0, max(Price)+10])
ax.set_xlabel('Electricity Demand [GWh]', loc='right', fontsize=rozmFont)
ax.set_ylabel('Generator Price\n[EUR/MWh]', loc='top', rotation='horizontal', fontsize=rozmFont)

####
PS_N =15 #  scheduled net demand at the day-ahead market (total scheduled net power consumption (demand minus stochastic production))
PB_N =10 # the net demand at balancing time
PDmax_Bi =0 # maximum quantity of scheduled own production that balancing generator i offers to repurchase at the balancing stage
PUmax_Bi=0 #  the capacity of production of balancing generator i at the balancing stage
LU_Bi=0 # the cost offer of balancing generator i for additional production at the balancing stage.U -> up-regulation.
LS=15 #clearing price in the day-ahead market
LB=25 #balancing market price
LD_Bi=0 # price offer of balancing generator i for repurchase at the balancing stage of own production scheduled
# at the day-ahead market. D -> down-regulation
left = [0,0,0,0,0,0,0]

def main_plot():
    ax.clear()  # czyscimy osie
    dah_price = ax.vlines(x=PS_N, color="red", linestyle=":", ymin=0, ymax=max(Price) + 5, linewidth=3)
    balance_price = ax.vlines(x=PB_N, color="blue", linestyle=":", ymin=0, ymax=max(Price) + 5, linewidth=3)
    LS_price = ax.hlines(y=LS, color="black", linestyle=":", xmin=0, xmax=max(Price) + 5, linewidth=3)
    LB_price = ax.hlines(y=LB, color="orange", linestyle=":", xmin=0, xmax=max(Price) + 5, linewidth=3)

    plot1 = ax.step(Energy, Price)

    ax.set_xlim(left=0, right=max(Energy) + 2)
    ax.set_ylim(bottom=0, top=max(Price) + 5)

    ax.text(PB_N - 0.5, -6, 'BAL', rotation=360, color='black', weight='bold', fontsize=rozmFont)
    ax.text(PS_N - 0.5, -6, 'DAM', rotation=360, color='black', weight='bold', fontsize=rozmFont)
    ax.text(-3, LS , 'DAM ->', rotation=360, color='black', weight='bold', fontsize=rozmFont)
    ax.text(-3, LB , 'BAL ->', rotation=360, color='black', weight='bold', fontsize=rozmFont)

    ax.set_title(
        f'Balancing Market Auction    Market Clearing Price = {LS} [EUR]  Balancing Market Price = {LB} [EUR]',
        fontsize=rozmFont, weight='bold')

    ax.set_xlabel('Electricity Demand [GWh]', loc='right', fontsize=rozmFont)
    ax.set_ylabel('Generator Price\n[EUR/MWh]', loc='top', rotation='horizontal', fontsize=rozmFont)

    # plt.arrow(x=PS_N, y=max(Price), dx=PB_N-PS_N, dy=0, width=0.7, head_width = 1.5, edgecolor='red',facecolor='red',linestyle='-',linewidth=3)
    ax.annotate('', xy=(PB_N, max(Price)), xytext=(PS_N, max(Price)),
                arrowprops=dict(facecolor='green', width=5, edgecolor='none'))
    ax.axvspan(PB_N, PS_N, alpha=0.1, color='red')
    if PS_N < PB_N:
        ax.text(0.48 * abs(PB_N + PS_N), max(Price) + 1, 'Excess\nDemand', rotation=360, color='black', weight='bold',fontsize=rozmFont)
        ax.text(0.48 * abs(PB_N + PS_N), max(Price) - 2,f"{PB_N - PS_N} [GWh]", rotation=360, color='black',weight='bold', fontsize=rozmFont)
    else:
        ax.text(0.48 * abs(PB_N + PS_N), max(Price) + 1, 'Excess\nProduction', rotation=360, color='black',weight='bold', fontsize=rozmFont)
        ax.text(0.48 * abs(PB_N + PS_N), max(Price) - 2,f"{-1*(PB_N - PS_N)} [GWh]", rotation=360, color='black',weight='bold', fontsize=rozmFont)

    plt.draw()

def update_line_dah(val):

    global PS_N
    PS_N = slider_PS_N.val

    global Energy
    global LS

    for i in range(len(Energy)):
        print(Energy[i])
        if Energy[i] >= PS_N:
            LS = Price[i]
            print(LS)
            break

    main_plot()


def update_line_bal(val):
    global PB_N
    global Energy
    global LB
    PB_N = slider_PB_N.val

    for i in range(len(Energy)):
        print(Energy[i])
        if Energy[i] >= PB_N :
            LB = Price[i]
            break

    main_plot()

#def update_price(text):
    #print(text)
   #main_plot()

ax_slider_PS_N = plt.axes([0.18,0.15,0.7,0.05], facecolor = 'teal')
ax_slider_PB_N = plt.axes([0.18,0.10,0.7,0.05], facecolor = 'teal')
#ax_textbox_PDAM = plt.axes([0.55,0.15,0.35,0.05], facecolor = 'teal')


slider_PS_N = Slider(ax_slider_PS_N, "Demand Day-Ahead [GWh]", valmin=0, valmax=32, valinit=0, valstep=1)
slider_PB_N = Slider(ax_slider_PB_N, "Demand Balancing [GWh]", valmin=0, valmax=32, valinit=0, valstep=1)
#textbox_PDAM = TextBox(ax_textbox_PDAM,'MCP\nDAM [EUR]', initial=0)

slider_PS_N.on_changed(update_line_dah)
slider_PB_N.on_changed(update_line_bal)
#textbox_PDAM.on_submit(update_price)
ax.set_xlim(0,30)
ax.set_xticks(np.arange(0,30, 1))
#plt.legend(labels=["balancing generators"])

plt.show()