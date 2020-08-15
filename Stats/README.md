# GT stats extraction

Unfortunatelly, tools like Poker Tracker or Holdem Manager don't properly understand GT stats. This spreadsheet addresses that, synthesising the stats you should care about.

The spreadsheets produces some common sense stats (number of games, profit, ROI, etc.), and three graphs: $ won, table win rate, and bounties / game. The last two are the defining GT stats, and are taken from a sliding window of the average for the last 200 rows at each step in the graph.

## Input

The data required is the PokerStars player audit. You can request it from the client:

* Tools
* History & Stats
* Playing History Audit
* Select the date range
* Add a password (this will be the password for the archive file, doesn't have to be your account password)
* You shouldn't care about StarsCoin/Reward point
* Select **Excel** as format

You should receive the spreadsheet in an email shortly.

![Requesting PokerStars audit file](img/audit.PNG)

## Filtering GT input

The audit includes *everything* that touches your cashier. Naturally, there's going to be a lot of stuff non-GT related.

To select just the GT data, we'll filter by *"Action"*.

Click on the cell called *"Action"*, and then on *"Sort & Filter"* and select *"Filter"*:

![Turning on filter](img/filter.png)

You should now see the filter icon on the top cells; click on the one for the *"Action"* column, and in the text box type *"Pool"* (all GT-related actions seem to have this in their name):

![Applying filter](img/pool.png)

Now, we'll copy this (raw) data and use it in the spreadsheet.

Select everything that's been filtered, not including the headers (should be from **A4** to the left and down) and press **Ctrl+C**.

*Hint: you can use **Ctrl + Arrows** to efficiently navigate blocks of cells*

## Replacing data with your own

Select the A2 cell with the placeholder text in our sheet. Now right click and **Paste**, but use only *"Values"*:

![Pasting](img/paste.png)

The stats + graphs should update automatically.

Feel free to tinker with the visualisation - i.e., your data set size might allow for better graphs.

## Extra Bounties -> chips sheet

You can find it in the *"BountyChips"* sheet.

You can input the initial + current bounties for each player, and get the chips equivalent. With it, you can estimate the odds you need to call as for normal chip amounts.

If you need to quickly do the ratio for the odds, fill in the *"Pot"* field and how much you still need to call them.

## Feedback and contributions

All welcome! Feel free to create a pull request.
