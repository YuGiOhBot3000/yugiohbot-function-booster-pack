# YuGiOhBot: Booster Pack Function
Build status: ![](https://travis-ci.org/Tohaker/yugiohbot-function-booster-pack.svg?branch=master)

This project sets up the Booster Pack cloud function for the YuGiOhBot.

## What it does
Once a week, the bot will collect all posts and count their reactions. If the reaction count is above a specified threshold, it will consider it for
a Booster Pack; A facebook photo album. As packs are either 5 or 9 cards in size, these sizes will be used if enough cards are above the threshold.