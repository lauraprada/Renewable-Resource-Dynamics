********************************************
*******Code to replicate stock graph *******
********************************************

/*Declare a global with the path of current directory*/

global RunPath ""


*************************
***Social dilemma data***
*************************

import  excel "$RunPath/xxxxx", sheet("xxxxx") firstrow clear // put here the name of the excel file with social dilemma data.
drop if participantlabel=="" // use this code only if you are using the rooms option 
keep if sessioncode=="xxxxxxx" // put here the "sessioncode" of your session

collapse (mean) playerstock_registro_del_jugado, by(subsessionround_number)
gen     treatment="Dilemma"
save    data_stock_by_round_dilemma.dta,replace

**************************
***Social planner data***
**************************

clear
import  excel "$RunPath/xxxxx", sheet("xxxxxx") firstrow 
drop if participantlabel=="" 
keep if sessioncode=="xxxxxxx" 


collapse (mean) playerstock_registro_del_jugado, by(subsessionround_number)
gen     treatment="Planner"

append  using data_stock_by_round_dilemma.dta

la var  subsessionround_number "Round"
la var  playerstock_registro_del_jugado "Stock(mean)" 

twoway  (line playerstock_registro_del_jugado subsessionround_number if treatment=="Planner", sort) (line playerstock_registro_del_jugado subsessionround_number if treatment=="Dilemma", sort), xlabel(1(1)10) title(Fish stock, margin(medium)) legend(order(1 "Social planner" 2 "Social dilemma")) scheme(s2mono) graphregion(fcolor(white)) plotregion(fcolor(white))

graph export "$RunPath/Stock.png", as(png) name("Stock")

