# cyclic-voltammetry-Data-analysis-data-viz
If you're an electrochemist working on the oxygen evolution reaction and ran 100 CVs and you're looking to process all that data and graph it this is the place for you. 

What the code does: 

1)   takes your giant CSV file containing 100+ CV ( or however many  you have ) and splits it into smaller CSV where it will then analyze all your data in the smaller files
then it will take the E(RHE) column and Current density column of all 100 files, and put them into one excel spreadsheet. You can then drag and drop that file into the origin to plot your data. 

2)  If your lab has no RHE, do not fret. This code will convert the potential vs whatever reference electrode you have to 'Potential vs RHE' and convert your current into current density ( Geometric surface area).  For example, if you have an Ag/AgCl reference electrode, convert the reference electrode's potential to the normal hydrogen electrode (NHE), and the code will do the rest.


How to use the code: 
1) Get your data from the potentiostat and copy and paste it into the Template CSV provided.
2) Change the parameters on lines 204 to 208 to your values. ( the constant stays the same) and the other variable names are self-explanatory.
3) Change the directories on lines 263-265.
4) press the play button and watch as the code works its magic.


 
