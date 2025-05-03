With everything that I’ve learned so far in this class I want to untangle my code a little and refactor a couple things. 
I’ve written this document out as a staging ground for ideas and I’ve worked on parts of it throughout the week. 
Primarily, I want to move the “player stats” which in its current iteration is based on nested dictionaries and tuples and turn it into a class feature. 
The main reasoning being that with each iteration and lesson, I was building a giant, messy, layered cake that I hoped keep organized with different modules.
Sometimes it worked, sometimes, not so much. I created nightmares for myself just as much as I impressed myself with how things worked in tandem. 
In adjusting an important part of my code and turning it into a class feature should be able to help me reduce the clutter between my multiple modules.
I’ll also be to do something with my code that has objectively bothered me: how I handled my inventory, the menus and how items are manipulated in and out of combat.
For example, at the time, the addition of a one-hit-knockout item was a last-minute detail that felt derailing and caused a lot of chaos in how I was treating items in and outside of combat. I believe that in refactoring the code I’ll be able to sort out a bunch of little bugs that I never figured out. 

I was able to find that the inventory does in fact load, but I don’t know where in the code a different state appears. 
The reason that I know that the inventory usually works but not in the aforementioned case is that prior to saving, 
any items bought before are usable in combat and it’s only after loading the game from the save state and returning 
to combat does the inventory appear empty. Hilariously, it shows up in the initial load state, just not in the combat 
setting meaning that somewhere after the load state, a different inventory is accessed. 

Things I learned from refactoring the code. Even when I was writing out blueprints for the code, 
it gets overwhelming and keeping variables aligned is hard. I sometimes just want to write things less
and I would make things more complicated as a result and sometimes what made sense one day, didn’t the other. 
The larger the scale the harder it is to manage and when problems arose I sometimes created new variables to manage
things because computers don’t hold onto information the same way. 

My objective for further development of the game has three parts: implementing durability and a way to repair items;
a way to craft or augment items; and a world that you can further explore that has collectable resources for weapon or armor crafting. 

Since monsters have been refactored into a class, and so has the player stats along with the inventory management, 
the only thing left and with doing so, is make durability a larger part of the combat mechanic and then I can use it 
to implement a new feature, repairing items. The concept of durability being that after a certain number of uses, 
the item will break. I know this was part of an earlier assignment but I never implemented it so I’m going to do 
that now for the first step in my independent feature. This will mean creating a condition in which durability of
an equipped item is checked and unequips and is returned as “broken” and will be unable to be equipped until repaired.
This same logic can be applied to healing items or other single use items, but depending on their type, such as 
“consumable” or “weapon” can be handled differently. Ie) consumables are removed from inventory and weapons are 
simply unequipped yet remain in the inventory. I was able to refactor a couple item dictionaries for various functions
and store it all in one single nested dictionary which is a lot easier to manage. One thing that I found funny was when
I implemented the blacksmith loop, I was checking for durability and only when the loop would break was finding out that 
I needed to include a new “stat” so that current durability and the initial or static durability wouldn’t be obfuscated
but making the newly organized nested dictionary format made that actually really easy. 

The user will need a way to repair these items so in the town’s shop menu, I added an option to visit a blacksmith.
The blacksmith will be able to repair items, and as an in-depth feature, it would be cool to be able to use collected materials
from exploring the broader world or as item drops from monsters and have the blacksmith function to craft or augment items. 
I’m not going to be able to do this all in a week. I’m even having a hard time wanting to re-do the shop menu so that it could 
be more dynamic and be able to be used for different “signages”. Debugging things is a lot more time consuming when there’s 
more loops to check. So I stuck to a simple text base of displaying items that had lower durability and costs. 

I think that it would be cool would be to create a moving window experience when exploring the world outside of town.
This will allow for a larger world than a 10x10 grid and can lead into maybe introducing dungeons and items that are able to be picked up.
I’m not going to do that immediately, but I think trying to add an expanded world would be enough for now. The cool thing is that this
feature does in fact lead into another that is only limited by imagination. Sometimes too though, it’s the implementing
the feature and making it work inside the old code that becomes more confusing. But I’m happy with the addition of the
blacksmith and durability. Some stuff does feel easier to do, but definitely easier to read than a couple months ago. 
The formatting of particular cases and different things is still hard at times, but I make sure to walk myself though 
each step and block and leave notes instead of writing out blocks that I have to go back and organize in my head. 
