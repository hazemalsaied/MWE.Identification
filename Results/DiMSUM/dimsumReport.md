
==================================================================================================
	EN Train (3839)
==================================================================================================
	Important sentence: 2153
	Token occurrences: 60613
	MWE number: 2497
	MWE occurrences: 3521
	Continuous occurrences: 89.0 %
	Frequent MWE occurences: 15.0 %
	MWE length: 2.34
	Recognizable MWEs: 100.0 %

==================================================================================================
	 Test (960)
==================================================================================================
	Important sentence: 490
	Token occurrences: 13213
	MWE number: 516
	MWE occurrences: 711
	Continuous occurrences: 89.0 %
	MWE length: 2.31
	Seen occurrences : 43% 
	Recognizable MWEs: 100.0 %

==================================================================================================
	Linear classifier:
==================================================================================================
	LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
     multi_class='ovr', penalty='l2', random_state=0, tol=0.0001,
     verbose=0)
==================================================================================================
	Feature number = 461012
==================================================================================================
	TRAINING TIME: 1.0 minutes 
==================================================================================================
## do not go to this salon , especially if you have to get your hair straightened .
### Annotated:
have to
TransitionType.MERGES=[have, to]                B=[ get,your, ..] Bx=you
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ get,your, ..] Bx=you
### Identified: 
have to
## i mean , i do n't care if he does n't know , but if he pretends to know and tells me bs to my face , there 's no way i 'm going to trust him when matters turn to the price of the car and financing .
### Annotated:
tell to face
go to
TransitionType.MERGES=[no, way]                 B=[ I,m, ..] Bx=s
TransitionType.MARK_AS_OTHS=[[no, way]]               B=[ I,m, ..] Bx=s
TransitionType.MERGES=[going, to]               B=[ trust,him, ..] Bx=m
TransitionType.MARK_AS_OTHS=[[going, to]]             B=[ trust,him, ..] Bx=m
TransitionType.MERGES=[turn, to]                B=[ the,price, ..] Bx=matter
TransitionType.MARK_AS_OTHS=[[turn, to]]              B=[ the,price, ..] Bx=matter
### Identified: 
no way
go to
turn to
## when having your car worked on you have to trust the mechanic & this midas is truly someone you can trust !
### Annotated:
have to
TransitionType.MERGES=[having, car]             B=[ worked,on, ..] Bx=your
TransitionType.MERGES=[[having, car]worked]     B=[ on,you, ..] Bx=your
TransitionType.MERGES=[[[having, car]worked]on] B=[ you,have, ..] Bx=your
TransitionType.MERGES=[[[[having, car]worked]on]have, to] B=[ trust,the, ..] Bx=you
TransitionType.MARK_AS_OTHS=[[[[having, car]worked]on][have, to]] B=[ trust,the, ..] Bx=you
### Identified: 
have to
## i was n't going to use them again , but i was going to leave it at that .
### Annotated:
go to
go to
leave it at that
TransitionType.MERGES=[going, to]               B=[ use,them, ..] Bx=nt
TransitionType.MARK_AS_OTHS=[[going, to]]             B=[ use,them, ..] Bx=nt
TransitionType.MERGES=[going, to]               B=[ leave,it, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[going, to]]             B=[ leave,it, ..] Bx=be
### Identified: 
go to
go to
## i really enjoyed meeting her and happy to learn she comes from oklahoma and has the values of a solid no bs country girl .
### Annotated:
come from
country girl
## i played dumb and asked him questions that i already knew the answers to and he responded with half truths and a few falsehoods .
### Annotated:
play dumb
half truth
## not only did it taste wonderful , but the texture was unbelievable , the frosting was n't overly sweet to over power the cake , and the cake itself was just amazingly soft , and fluffy , and just perfect overall .
### Annotated:
over power
## i typically have work done on my jeep at the dealership , but it is number years old now and getting charged dealership prices just did n't seem cost effective anymore .
### Annotated:
years old
TransitionType.MERGES=[a, little]               B=[ suspicious,of, ..] Bx=also
TransitionType.MARK_AS_OTHS=[[a, little]]             B=[ suspicious,of, ..] Bx=also
### Identified: 
a little
## the staff is very personable & actually care about the customers safety rather than taking there money .
### Annotated:
rather than
TransitionType.MERGES=[customers, safety]       B=[ rather,than, ..] Bx=the
TransitionType.MERGES=[[customers, safety]rather] B=[ than,taking, ..] Bx=the
TransitionType.MERGES=[[[customers, safety]rather]than] B=[ taking,there, ..] Bx=the
TransitionType.MERGES=[[[[customers, safety]rather]than]taking] B=[ there,money, ..] Bx=the
## i grew up in a small town where you knew and trusted your mechanic and was really cynical about city auto repair shops since i moved here , but phet has shown that there really are honest hard working mechanics around .
### Annotated:
grow up
TransitionType.MERGES=[grew, up]                B=[ in,a, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[grew, up]]              B=[ in,a, ..] Bx=i
### Identified: 
grow up
## however , i still like this place a lot .
### Annotated:
a lot
TransitionType.MERGES=[a, lot]                  B=[ punc,] Bx=place
TransitionType.MARK_AS_OTHS=[[a, lot]]                B=[ punc,] Bx=place
### Identified: 
a lot
## esp. the mole , tortilla soup , and guacamole .
### Annotated:
tortilla soup
## it used to be fabulous , why did you guys change it ??
### Annotated:
use to
you guy
TransitionType.MERGES=[used, to]                B=[ be,fabulous, ..] Bx=it
TransitionType.MARK_AS_OTHS=[[used, to]]              B=[ be,fabulous, ..] Bx=it
### Identified: 
use to
## *** update *** never mind !
### Annotated:
never mind
## thank you thank you
### Annotated:
thank you
thank you
TransitionType.MERGE
TransitionType.MARK_AS_OTH
TransitionType.MERGES=[thank, you]              B=[ ] Bx=you
TransitionType.MARK_AS_OTHS=[[thank, you]]            B=[ ] Bx=you
### Identified: 
thank you
thank you
## i googled garage door repair in woodinville and found ndi - johnette answered the phone and was oh - so pleasant and helpful !
### Annotated:
garage door
oh - so
TransitionType.MERGES=[Garage, Door]            B=[ Repair,in, ..] Bx=google
TransitionType.MARK_AS_OTHS=[[Garage, Door]]          B=[ Repair,in, ..] Bx=google
### Identified: 
garage door
## she sort of appologized for dan taking the day off to go skiing - but he could do the repair on sunday !
### Annotated:
sort of
take off
go ski
TransitionType.MERGES=[taking, day]             B=[ off,to, ..] Bx=the
TransitionType.MERGES=[[taking, day]off]        B=[ to,go, ..] Bx=the
TransitionType.MERGES=[[[taking, day]off]to]    B=[ go,skiing, ..] Bx=the
TransitionType.MERGES=[[[[taking, day]off]to]go] B=[ skiing,-, ..] Bx=the
TransitionType.MERGES=[[[[[taking, day]off]to]go]skiing] B=[ -,but, ..] Bx=the
TransitionType.MERGES=[[[[[[taking, day]off]to]go]skiing]-] B=[ but,he, ..] Bx=the
TransitionType.MERGES=[[[[[[[taking, day]off]to]go]skiing]-]but] B=[ he,could, ..] Bx=the
## i would highly recommend ndi - and will spread the word to my neighbors .
### Annotated:
spread the word
TransitionType.MERGES=[spread, the]             B=[ word,to, ..] Bx=will
TransitionType.MERGES=[[spread, the]word]       B=[ to,my, ..] Bx=will
TransitionType.MARK_AS_OTHS=[[[spread, the]word]]     B=[ to,my, ..] Bx=will
### Identified: 
spread the word
## roger m. , woodinville
### Annotated:
roger m
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## the best deals in town
### Annotated:
in town
TransitionType.MERGES=[in, Town]                B=[ ] Bx=deal
TransitionType.MARK_AS_OTHS=[[in, Town]]              B=[ ] Bx=deal
### Identified: 
in town
## trust me , you go there once and you -ll always go back !
### Annotated:
trust me
## thank you for fixing the leak on my bathroom !
### Annotated:
thank you
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
thank you
## i paid number k cash for a truck with a blown motor .
### Annotated:
pay cash
TransitionType.MERGES=[blown, motor]            B=[ punc,] Bx=a
TransitionType.MERGES=[[blown, motor]punc]      B=[ ] Bx=a
## their so called mechanic said the engine was good and " there is nothing mechanicly wrong with this truck " .
### Annotated:
so call
wrong with
## anyway they jimmy rigged it so i could drive it home .
### Annotated:
jimmy rig
## the next day i took it to number auto shops and they both told me the same thing , engine is junk .
### Annotated:
auto shop
TransitionType.MERGES=[took, shops]             B=[ and,they, ..] Bx=auto
TransitionType.MERGES=[[took, shops]and]        B=[ they,both, ..] Bx=auto
## i called and got the same runaround on hold and noone calls you back .
### Annotated:
on hold
call back
## from a moral standpoint , you guys are really gon na take number bucks from someone that needs that truck to work and support his family when you know it s just a piece of scrap metal ?
### Annotated:
from standpoint
gon na
scrap metal
TransitionType.MERGES=[take, bucks]             B=[ from,someone, ..] Bx=number
TransitionType.MERGES=[[take, bucks]from]       B=[ someone,that, ..] Bx=number
TransitionType.MERGES=[[[take, bucks]from]someone] B=[ that,needs, ..] Bx=number
## if it lasted number month i could suck it up but number day ?
### Annotated:
suck it up
TransitionType.MERGES=[suck, it]                B=[ up,but, ..] Bx=could
TransitionType.MERGES=[[suck, it]up]            B=[ but,number, ..] Bx=could
TransitionType.MERGES=[[[suck, it]up]but]       B=[ number,day, ..] Bx=could
TransitionType.MERGES=[[[[suck, it]up]but]number] B=[ day,punc,] Bx=could
TransitionType.MERGES=[[[[[suck, it]up]but]number]day] B=[ punc,] Bx=could
TransitionType.MERGES=[[[[[[suck, it]up]but]number]day]punc] B=[ ] Bx=could
## grimy work you guys do .
### Annotated:
you guy
## seriously , can you imagine having to live through these last few nights without heat ?
### Annotated:
have to
live through
TransitionType.MERGES=[having, to]              B=[ live,through, ..] Bx=imagine
TransitionType.MARK_AS_OTHS=[[having, to]]            B=[ live,through, ..] Bx=imagine
### Identified: 
have to
## comfort zone came out and did my house heat on the cheap .
### Annotated:
comfort zone
come out
on the cheap
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGES=[[[[[[Comfort, zone]came]out]and]did]house, heat] B=[ on,the, ..] Bx=my
TransitionType.MERGES=[[[[[[Comfort, zone]came]out]and]did][house, heat]on] B=[ the,cheap, ..] Bx=my
TransitionType.MERGES=[[[[[[Comfort, zone]came]out]and]did][[house, heat]on]the] B=[ cheap,punc,] Bx=my
TransitionType.MERGES=[[[[[[Comfort, zone]came]out]and]did][[[house, heat]on]the]cheap] B=[ punc,] Bx=my
TransitionType.MERGES=[[[[[[Comfort, zone]came]out]and]did][[[[house, heat]on]the]cheap]punc] B=[ ] Bx=my
TransitionType.MERGES=[[[[[[Comfort, zone]came]out]and]did][[[[[house, heat]on]the]cheap]punc]] B=[ ] Bx=my
## thank you comfort zone
### Annotated:
thank you
comfort zone
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
thank you
## they are very rude over the phone and in person .
### Annotated:
over the phone
in person
TransitionType.MERGES=[over, the]               B=[ phone,and, ..] Bx=rude
TransitionType.MERGES=[[over, the]phone]        B=[ and,in, ..] Bx=rude
TransitionType.MARK_AS_OTHS=[[[over, the]phone]]      B=[ and,in, ..] Bx=rude
### Identified: 
over the phone
## they talk down to you like they are supreme beings , if you hate your job so much then quit !!
### Annotated:
talk down to
supreme being
TransitionType.MERGES=[talk, down]              B=[ to,you, ..] Bx=they
TransitionType.MARK_AS_OTHS=[[talk, down]]            B=[ to,you, ..] Bx=they
### Identified: 
talk down
## how these guys can get away with being so rude with people is mind blowing .
### Annotated:
get away with
be rude
mind blow
TransitionType.MERGES=[get, away]               B=[ with,being, ..] Bx=can
TransitionType.MARK_AS_OTHS=[[get, away]]             B=[ with,being, ..] Bx=can
### Identified: 
get away
## i will never do business with sun toyota again .
### Annotated:
do business
sun toyota
TransitionType.MERGES=[Sun, Toyota]             B=[ again,punc,] Bx=with
TransitionType.MERGES=[[Sun, Toyota]again]      B=[ punc,] Bx=with
TransitionType.MERGES=[[[Sun, Toyota]again]punc] B=[ ] Bx=with
## thank god there are plenty of toyota dealerships to choose from in this city .
### Annotated:
thank god
## compare to last decade this university is gaining more prestige in international level
### Annotated:
compare to
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
compare to
## the equipment and classes are n't good enough to deal with the rudeness from the staff !!!
### Annotated:
deal with
TransitionType.MERGES=[deal, with]              B=[ the,rudeness, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[deal, with]]            B=[ the,rudeness, ..] Bx=to
### Identified: 
deal with
## there are better places on the cape - fitness number !
### Annotated:
fitness number
TransitionType.MERGES=[FITNESS, number]         B=[ punc,] Bx=-
TransitionType.MERGES=[[FITNESS, number]punc]   B=[ ] Bx=-
## great service - high class !
### Annotated:
high class
## we were in springfield , il for a family funeral from kansas city .
### Annotated:
springfield , il
kansas city
TransitionType.MERGES=[Kansas, City]            B=[ punc,] Bx=from
TransitionType.MERGES=[[Kansas, City]punc]      B=[ ] Bx=from
## we arrived early and the staff was very accomodating to our families and the situation we were in .
### Annotated:
situation be in
## this is a nice place , and i know we will return to meet my sister - in - law from chicago !!
### Annotated:
sister - in - law
## great job master keying our building .
### Annotated:
master key
## i did n't end up buying my car here , but i did think the guy who worked with me was pretty cool - he was willing to budge a little on the price which means a lot to me .
### Annotated:
end up
a little
a lot
TransitionType.MERGES=[end, up]                 B=[ buying,my, ..] Bx=nt
TransitionType.MARK_AS_OTHS=[[end, up]]               B=[ buying,my, ..] Bx=nt
TransitionType.MERGES=[a, little]               B=[ on,the, ..] Bx=budge
TransitionType.MARK_AS_OTHS=[[a, little]]             B=[ on,the, ..] Bx=budge
TransitionType.MERGES=[a, lot]                  B=[ to,me, ..] Bx=mean
TransitionType.MARK_AS_OTHS=[[a, lot]]                B=[ to,me, ..] Bx=mean
### Identified: 
end up
a little
a lot
## also they will fill your tires with air and other small maintenance tasks for free , even if you did n't buy your car there !
### Annotated:
for free
## they do n't seem to be interested in selling cars .
### Annotated:
interested in
TransitionType.MERGES=[interested, in]          B=[ selling,cars, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[interested, in]]        B=[ selling,cars, ..] Bx=be
### Identified: 
interested in
## went there yesterday : we are trying to decide between two different honda models , so we wanted to test - drive both back to back .
### Annotated:
test - drive
back to back
## claimed he was too busy for two test drives .
### Annotated:
test drive
TransitionType.MERGES=[test, drives]            B=[ punc,] Bx=two
TransitionType.MARK_AS_OTHS=[[test, drives]]          B=[ punc,] Bx=two
### Identified: 
test drive
## do n't waste time , just drive number minutes more down to stevens creek , they actually do try to help their customers there !
### Annotated:
waste time
stevens creek
TransitionType.MERGES=[waste, time]             B=[ ,,just, ..] Bx=nt
TransitionType.MARK_AS_OTHS=[[waste, time]]           B=[ ,,just, ..] Bx=nt
TransitionType.MERGES=[Stevens, Creek]          B=[ ,,they, ..] Bx=to
TransitionType.MERGES=[[Stevens, Creek],]       B=[ they,actually, ..] Bx=to
### Identified: 
waste time
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
not only
## in the past , i got a steak and there was more fat and rough pieces than there was good steak ( and this was the sirloin ! ) , the sides were drenched with butter and the salad was a little on the brown side .
### Annotated:
a little
on the side
TransitionType.MERGES=[a, little]               B=[ on,the, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[a, little]]             B=[ on,the, ..] Bx=be
### Identified: 
a little
## it took over number hours for our food to come out and by that time my number month old had it !
### Annotated:
come out
month old
have it
TransitionType.MERGES=[come, out]               B=[ and,by, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[come, out]]             B=[ and,by, ..] Bx=to
TransitionType.MERGES=[month, old]              B=[ had,it, ..] Bx=number
TransitionType.MARK_AS_OTHS=[[month, old]]            B=[ had,it, ..] Bx=number
### Identified: 
come out
month old
TransitionType.MERGES=[get, food]               B=[ punc,] Bx=my
TransitionType.MERGES=[[get, food]punc]         B=[ ] Bx=my
## texas roadhouse is way better !!
### Annotated:
texas roadhouse
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
texas roadhouse
## this is a perfect place to get your hair done .
### Annotated:
get do
TransitionType.MERGES=[get, done]               B=[ punc,] Bx=hair
TransitionType.MARK_AS_OTHS=[[get, done]]             B=[ punc,] Bx=hair
### Identified: 
get do
## i have gone there time and time again whenever i need to get my hair done or when i want a haircut .
### Annotated:
time and again
get do
TransitionType.MERGES=[get, done]               B=[ or,when, ..] Bx=hair
TransitionType.MARK_AS_OTHS=[[get, done]]             B=[ or,when, ..] Bx=hair
### Identified: 
get do
## when i get my hair done there , they use enough hairstyling products while it does not ruin your hair .
### Annotated:
get do
TransitionType.MERGES=[get, done]               B=[ there,,, ..] Bx=hair
TransitionType.MARK_AS_OTHS=[[get, done]]             B=[ there,,, ..] Bx=hair
### Identified: 
get do
## we love little farmer
### Annotated:
little farmer
TransitionType.MERGES=[Little, Farmer]          B=[ ] Bx=love
## they even want to go to school on the weekends !!
### Annotated:
go to school
## they are preparing my older son for kindergarten and looks forward to seeing his teacher and friends every day .
### Annotated:
look forward to
TransitionType.MERGES=[looks, forward]          B=[ to,seeing, ..] Bx=and
TransitionType.MERGES=[[looks, forward]to]      B=[ seeing,his, ..] Bx=and
TransitionType.MARK_AS_OTHS=[[[looks, forward]to]]    B=[ seeing,his, ..] Bx=and
### Identified: 
look forward to
## my infant is content every day when i drop off and pick up .
### Annotated:
drop off
pick up
TransitionType.MERGES=[drop, off]               B=[ and,pick, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[drop, off]]             B=[ and,pick, ..] Bx=i
TransitionType.MERGES=[pick, up]                B=[ punc,] Bx=and
TransitionType.MARK_AS_OTHS=[[pick, up]]              B=[ punc,] Bx=and
### Identified: 
drop off
pick up
## dr. faris is a great doctor !
### Annotated:
dr faris
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## i was experiencing severe back pain to the point i could barely walk or even bare to sit .
### Annotated:
back pain
TransitionType.MERGES=[back, pain]              B=[ to,the, ..] Bx=severe
TransitionType.MARK_AS_OTHS=[[back, pain]]            B=[ to,the, ..] Bx=severe
### Identified: 
back pain
## i have lived in the utc la jolla area for many years , and i never new this salon was here until a friend reffered me to see holly here .
### Annotated:
utc la jolla
TransitionType.MERGES=[UTC, La]                 B=[ Jolla,area, ..] Bx=the
TransitionType.MERGES=[[UTC, La]Jolla]          B=[ area,for, ..] Bx=the
TransitionType.MERGES=[[[UTC, La]Jolla]area]    B=[ for,many, ..] Bx=the
TransitionType.MERGES=[[[[UTC, La]Jolla]area]for] B=[ many,years, ..] Bx=the
TransitionType.MERGES=[[[[[UTC, La]Jolla]area]for]many] B=[ years,,, ..] Bx=the
TransitionType.MERGES=[[[[[[UTC, La]Jolla]area]for]many]years] B=[ ,,and, ..] Bx=the
TransitionType.MERGES=[[[[[[[UTC, La]Jolla]area]for]many]years],] B=[ and,I, ..] Bx=the
TransitionType.MERGES=[[[[[[[[UTC, La]Jolla]area]for]many]years],]and] B=[ I,never, ..] Bx=the
TransitionType.MERGES=[pleased, with]           B=[ my,experience, ..] Bx=very
TransitionType.MARK_AS_OTHS=[[pleased, with]]         B=[ my,experience, ..] Bx=very
### Identified: 
pleased with
TransitionType.MERGES=[did, a]                  B=[ great,job, ..] Bx=she
TransitionType.MERGES=[[did, a]job]             B=[ punc,] Bx=great
TransitionType.MARK_AS_OTHS=[[[did, a]job]]           B=[ punc,] Bx=great
### Identified: 
do a job
## holly is very experienced and talented , and i could tell she new what she was doing right off the bat .
### Annotated:
right off the bat
## my hair looks amazing , and i get compliments all the time .
### Annotated:
all the time
## we would like to thank you for the roofing job you did on our home .
### Annotated:
thank you
TransitionType.MERGES=[would, like]             B=[ to,thank, ..] Bx=we
TransitionType.MARK_AS_OTHS=[[would, like]]           B=[ to,thank, ..] Bx=we
TransitionType.MERGES=[thank, you]              B=[ for,the, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[thank, you]]            B=[ for,the, ..] Bx=to
### Identified: 
would like
thank you
## everything was done on a timely manner and things were cleaned and picked up every day when the crew was done .
### Annotated:
pick up
TransitionType.MERGES=[picked, up]              B=[ every,day, ..] Bx=and
TransitionType.MARK_AS_OTHS=[[picked, up]]            B=[ every,day, ..] Bx=and
### Identified: 
pick up
TransitionType.MERGES=[checked, on]             B=[ the,job, ..] Bx=ray
TransitionType.MERGES=[[checked, on]the]        B=[ job,every, ..] Bx=ray
TransitionType.MERGES=[[[checked, on]the]job]   B=[ every,day, ..] Bx=ray
TransitionType.MERGES=[[[[checked, on]the]job]every] B=[ day,punc,] Bx=ray
TransitionType.MERGES=[[[[[checked, on]the]job]every]day] B=[ punc,] Bx=ray
TransitionType.MERGES=[[[[[[checked, on]the]job]every]day]punc] B=[ ] Bx=ray
## and when the job was done every thing was cleaned up and hauled off that same day .
### Annotated:
every thing
clean up
haul off
TransitionType.MERGES=[every, thing]            B=[ was,cleaned, ..] Bx=done
TransitionType.MARK_AS_OTHS=[[every, thing]]          B=[ was,cleaned, ..] Bx=done
TransitionType.MERGES=[cleaned, up]             B=[ and,hauled, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[cleaned, up]]           B=[ and,hauled, ..] Bx=be
### Identified: 
every thing
clean up
## we would not hesitate to use spears roofing again .
### Annotated:
spears roofing
TransitionType.MERGES=[Spears, Roofing]         B=[ again,punc,] Bx=use
TransitionType.MERGES=[[Spears, Roofing]again]  B=[ punc,] Bx=use
TransitionType.MERGES=[[[Spears, Roofing]again]punc] B=[ ] Bx=use
## my favorite so far in bellevue .
### Annotated:
so far
## store is on the small side and atmosphere is just average .
### Annotated:
on the side
TransitionType.MERGES=[on, the]                 B=[ small,side, ..] Bx=be
TransitionType.MERGES=[[on, the]side]           B=[ and,atmosphere, ..] Bx=small
TransitionType.MARK_AS_OTHS=[[[on, the]side]]         B=[ and,atmosphere, ..] Bx=small
### Identified: 
on the side
## great service / deals - support this local business
### Annotated:
local business
TransitionType.MERGES=[local, business]         B=[ ] Bx=this
## i have used these guys for new snows , fixing lots of flats , used replacement tires , and oil changes .
### Annotated:
oil change
TransitionType.MERGES=[oil, changes]            B=[ punc,] Bx=and
TransitionType.MARK_AS_OTHS=[[oil, changes]]          B=[ punc,] Bx=and
### Identified: 
oil change
## they have the best prices locally and good customer service .
### Annotated:
customer service
TransitionType.MERGES=[customer, service]       B=[ punc,] Bx=good
TransitionType.MARK_AS_OTHS=[[customer, service]]     B=[ punc,] Bx=good
### Identified: 
customer service
## one guy is a little surley , but who gives a crap as long as your car 's work is outstanding .
### Annotated:
who give a crap
as long as
TransitionType.MERGES=[a, little]               B=[ surley,,, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[a, little]]             B=[ surley,,, ..] Bx=be
TransitionType.MERGES=[as, long]                B=[ as,your, ..] Bx=crap
TransitionType.MERGES=[[as, long]as]            B=[ your,car, ..] Bx=crap
TransitionType.MARK_AS_OTHS=[[[as, long]as]]          B=[ your,car, ..] Bx=crap
### Identified: 
a little
as long as
## and they 're usually able to help you as a walk - in , and they 're fast .
### Annotated:
walk - in
## i tell them : why not just go with these guys ?
### Annotated:
go with
## richard joule and the gang are pros from start to finish .
### Annotated:
richard joule
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## they set out to exceed your expectations .
### Annotated:
set out
TransitionType.MERGES=[set, out]                B=[ to,exceed, ..] Bx=they
TransitionType.MERGES=[[set, out]to]            B=[ exceed,your, ..] Bx=they
TransitionType.MERGES=[[[set, out]to]exceed]    B=[ your,expectations, ..] Bx=they
TransitionType.MERGES=[[[[set, out]to]exceed]your] B=[ expectations,punc,] Bx=they
TransitionType.MERGES=[[[[[set, out]to]exceed]your]expectations] B=[ punc,] Bx=they
TransitionType.MERGES=[[[[[[set, out]to]exceed]your]expectations]punc] B=[ ] Bx=they
## already i 'm considering future projects , and i can assure you that for my printing needs i will be choosing no other than atlanta paperback book printing .
### Annotated:
no other than
atlanta paperback book printing
TransitionType.MERGES=[other, than]             B=[ Atlanta,Paperback, ..] Bx=no
TransitionType.MARK_AS_OTHS=[[other, than]]           B=[ Atlanta,Paperback, ..] Bx=no
TransitionType.MERGES=[Atlanta, Paperback]      B=[ Book,Printing, ..] Bx=than
TransitionType.MERGES=[[Atlanta, Paperback]Book] B=[ Printing,punc,] Bx=than
TransitionType.MERGES=[[[Atlanta, Paperback]Book]Printing] B=[ punc,] Bx=than
TransitionType.MERGES=[[[[Atlanta, Paperback]Book]Printing]punc] B=[ ] Bx=than
### Identified: 
other than
## signs of saltford - an excellent supplier of value for money signs and banners etc .
### Annotated:
signs of saltford
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## i have been a friend and customer of signs of saltford for well over number years now and i also became their website supplier some number years ago .
### Annotated:
signs of saltford
## tina is the driving force of the business and you can be assured that she will endevour to satisfy all your signage requirements at the most cost effective rates .
### Annotated:
drive force
## i have been extremely pleased with the signs and pop - up banners she has supplied to me over the years - a truly first class family business run by tina and her husband chris .
### Annotated:
pop - up
over the years
first class
family business
TransitionType.MERGES=[pleased, with]           B=[ the,signs, ..] Bx=extremely
TransitionType.MARK_AS_OTHS=[[pleased, with]]         B=[ the,signs, ..] Bx=extremely
TransitionType.MERGES=[pop, -]                  B=[ up,banners, ..] Bx=and
TransitionType.MERGES=[[pop, -]up]              B=[ banners,she, ..] Bx=and
TransitionType.MERGES=[[[pop, -]up]banners]     B=[ she,has, ..] Bx=and
### Identified: 
pleased with
## keep it up .
### Annotated:
keep it up
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## - shree ghatkopar bhatia mitra mandal
### Annotated:
shree ghatkopar bhatia mitra mandal
TransitionType.MERGES=[Shree, Ghatkopar]        B=[ Bhatia,Mitra, ..] Bx=-
TransitionType.MERGES=[[Shree, Ghatkopar]Bhatia] B=[ Mitra,Mandal,] Bx=-
TransitionType.MERGES=[[[Shree, Ghatkopar]Bhatia]Mitra] B=[ Mandal,] Bx=-
TransitionType.MERGES=[[[[Shree, Ghatkopar]Bhatia]Mitra]Mandal] B=[ ] Bx=-
## we went to kobey s on saturday and had our whole team s uniforms done !
### Annotated:
kobey s
have do
## he was less than half of the price of the cheapest quote we got , and his work was top notch .
### Annotated:
less than
top notch
TransitionType.MERGES=[top, notch]              B=[ punc,] Bx=be
TransitionType.MARK_AS_OTHS=[[top, notch]]            B=[ punc,] Bx=be
### Identified: 
top notch
## down to earth and fast service .
### Annotated:
down to earth
## going back to have some lab coats done this weekend !
### Annotated:
have do
lab coat
TransitionType.MERGES=[this, weekend]           B=[ punc,] Bx=do
TransitionType.MARK_AS_OTHS=[[this, weekend]]         B=[ punc,] Bx=do
### Identified: 
this weekend
TransitionType.MERGES=[out, night]              B=[ punc,] Bx=great
TransitionType.MERGES=[[out, night]punc]        B=[ ] Bx=great
## you ca n't go wrong with tuesday prices , even if you get quite the mixed bag of comedians !
### Annotated:
ca nt go wrong
mixed bag
## extensive drink list and daily specials but wish they had a bit more on their food menu , although popcorn is a nice touch !
### Annotated:
a bit
be a nice touch
TransitionType.MERGES=[had, a, bit]             B=[ more,on, ..] Bx=they
TransitionType.MARK_AS_OTHS=[had[a, bit]]             B=[ more,on, ..] Bx=they
TransitionType.MERGES=[had, menu]               B=[ ,,although, ..] Bx=food
TransitionType.MERGES=[[had, menu],]            B=[ although,popcorn, ..] Bx=food
TransitionType.MERGES=[[[had, menu],]although]  B=[ popcorn,is, ..] Bx=food
TransitionType.MERGES=[[[[had, menu],]although]popcorn] B=[ is,a, ..] Bx=food
TransitionType.MERGES=[[[[[had, menu],]although]popcorn]is] B=[ a,nice, ..] Bx=food
### Identified: 
a bit
## ( other items : chicken fingers , wings , asian pizza , and yam and regular fries )
### Annotated:
chicken finger
## service could be a little better but it s an all round good place
### Annotated:
a little
all round
TransitionType.MERGES=[a, little]               B=[ better,but, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[a, little]]             B=[ better,but, ..] Bx=be
### Identified: 
a little
## i go to school in the area and usually wait until i go home to get my hair cut .
### Annotated:
go to school
hair cut
TransitionType.MERGES=[get, hair]               B=[ cut,punc,] Bx=my
TransitionType.MERGES=[[get, hair]cut]          B=[ punc,] Bx=my
TransitionType.MERGES=[[[get, hair]cut]punc]    B=[ ] Bx=my
## i decided it was time to grow up and made an appointment .
### Annotated:
grow up
TransitionType.MERGES=[grow, up]                B=[ and,made, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[grow, up]]              B=[ and,made, ..] Bx=to
TransitionType.MERGES=[made, an]                B=[ appointment,punc,] Bx=and
TransitionType.MERGES=[[made, an]appointment]   B=[ punc,] Bx=and
TransitionType.MERGES=[[[made, an]appointment]punc] B=[ ] Bx=and
### Identified: 
grow up
TransitionType.MERGES=[hair, style]             B=[ punc,] Bx=my
TransitionType.MARK_AS_OTHS=[[hair, style]]           B=[ punc,] Bx=my
### Identified: 
hair style
TransitionType.MERGES=[left, salon]             B=[ with,my, ..] Bx=a
TransitionType.MERGES=[[left, salon]with]       B=[ my,hair, ..] Bx=a
TransitionType.MERGES=[[[left, salon]with]my]   B=[ hair,curly, ..] Bx=a
TransitionType.MERGES=[[[[left, salon]with]my]hair] B=[ curly,punc,] Bx=a
TransitionType.MERGES=[[[[[left, salon]with]my]hair]curly] B=[ punc,] Bx=a
TransitionType.MERGES=[[[[[[left, salon]with]my]hair]curly]punc] B=[ ] Bx=a
## usually they blow dry it out and i have to wait until i wash it to see what it will look like in its natural state .
### Annotated:
dry out
have to
TransitionType.MERGES=[have, to]                B=[ wait,until, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ wait,until, ..] Bx=i
### Identified: 
have to
## but she did a fabulous job letting me know what she was doing at all times and styled my hair in a way i could do it at home .
### Annotated:
let know
TransitionType.MERGES=[did, a]                  B=[ fabulous,job, ..] Bx=she
TransitionType.MERGES=[[did, a]job]             B=[ letting,me, ..] Bx=fabulous
TransitionType.MARK_AS_OTHS=[[[did, a]job]]           B=[ letting,me, ..] Bx=fabulous
TransitionType.MERGES=[in, a]                   B=[ way,i, ..] Bx=hair
TransitionType.MERGES=[[in, a]way]              B=[ i,could, ..] Bx=hair
### Identified: 
do a job
## over charged .
### Annotated:
over charge
## i used my card to purchase a meal on the menu and the total on my receipt was $ number but when i went on line to check my transaction it show $ number .
### Annotated:
on line
TransitionType.MERGES=[on, line]                B=[ to,check, ..] Bx=go
TransitionType.MERGES=[[on, line]to]            B=[ check,my, ..] Bx=go
TransitionType.MERGES=[[[on, line]to]check]     B=[ my,transaction, ..] Bx=go
## there is something wrong or maybe the individual made a mistake but to me that is not integrity .
### Annotated:
make mistake
TransitionType.MERGES=[made, a]                 B=[ mistake,but, ..] Bx=individual
TransitionType.MERGES=[[made, a]mistake]        B=[ but,to, ..] Bx=individual
TransitionType.MARK_AS_OTHS=[[[made, a]mistake]]      B=[ but,to, ..] Bx=individual
### Identified: 
make a mistake
## these people were so helpful this week and did everything to sort out my windscreen and insurance .
### Annotated:
sort out
TransitionType.MERGES=[sort, out]               B=[ my,windscreen, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[sort, out]]             B=[ my,windscreen, ..] Bx=to
### Identified: 
sort out
## it was all sorted with no hassle at all and i 'm really grateful - they were fab .
### Annotated:
at all
TransitionType.MERGES=[at, all]                 B=[ and,I, ..] Bx=hassle
TransitionType.MARK_AS_OTHS=[[at, all]]               B=[ and,I, ..] Bx=hassle
### Identified: 
at all
## the best customer service i 've come across for long time .
### Annotated:
customer service
come across
TransitionType.MERGES=[customer, service]       B=[ I,ve, ..] Bx=best
TransitionType.MARK_AS_OTHS=[[customer, service]]     B=[ I,ve, ..] Bx=best
TransitionType.MERGES=[come, across]            B=[ for,long, ..] Bx=ve
TransitionType.MARK_AS_OTHS=[[come, across]]          B=[ for,long, ..] Bx=ve
### Identified: 
customer service
come across
## i 'm number years old and have dental problems my entire life .
### Annotated:
years old
## my fear and discomfort from dental work scared me !
### Annotated:
dental work
## it took all the courage i could muster to make an appointment .
### Annotated:
take courage
make appointment
TransitionType.MERGES=[make, an]                B=[ appointment,punc,] Bx=to
TransitionType.MERGES=[[make, an]appointment]   B=[ punc,] Bx=to
TransitionType.MERGES=[[[make, an]appointment]punc] B=[ ] Bx=to
## at the front door of his office , i nearly turned around .
### Annotated:
front door
TransitionType.MERGES=[front, door]             B=[ of,his, ..] Bx=the
TransitionType.MERGES=[[front, door]of]         B=[ his,office, ..] Bx=the
TransitionType.MERGES=[[[front, door]of]turned, around] B=[ punc,] Bx=nearly
TransitionType.MARK_AS_OTHS=[[[front, door]of][turned, around]] B=[ punc,] Bx=nearly
### Identified: 
turn around
## doctor gonzales and his entire staff are the most professional people i have ever dealt with .
### Annotated:
doctor gonzales
deal with
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGES=[[[[[[[[[[[Doctor, Gonzales]and]his]entire]staff]are]the]most]professional]people]dealt, with] B=[ punc,] Bx=ever
TransitionType.MARK_AS_OTHS=[[[[[[[[[[[Doctor, Gonzales]and]his]entire]staff]are]the]most]professional]people][dealt, with]] B=[ punc,] Bx=ever
### Identified: 
deal with
## the ability to smile and eat again can only be described as a whole new lease on life .
### Annotated:
new lease on life
## thank you doctor gonzales , doctor stout , eva marie and the entire staff !
### Annotated:
thank you
doctor gonzales
doctor stout
eva marie
TransitionType.MERGE
TransitionType.MARK_AS_OTH
TransitionType.MERGES=[Doctor, Gonzales]        B=[ ,,Doctor, ..] Bx=you
TransitionType.MERGES=[[Doctor, Gonzales]Doctor] B=[ Stout,,, ..] Bx=,
TransitionType.MERGES=[[[Doctor, Gonzales]Doctor]Stout] B=[ ,,Eva, ..] Bx=,
TransitionType.MERGES=[[[[Doctor, Gonzales]Doctor]Stout]Eva, Marie] B=[ and,the, ..] Bx=,
TransitionType.MERGES=[[[[Doctor, Gonzales]Doctor]Stout][Eva, Marie]and] B=[ the,entire, ..] Bx=,
TransitionType.MERGES=[[[[Doctor, Gonzales]Doctor]Stout][[Eva, Marie]and]the] B=[ entire,staff, ..] Bx=,
TransitionType.MERGES=[[[[Doctor, Gonzales]Doctor]Stout][[[Eva, Marie]and]the]entire] B=[ staff,punc,] Bx=,
TransitionType.MERGES=[[[[Doctor, Gonzales]Doctor]Stout][[[[Eva, Marie]and]the]entire]staff] B=[ punc,] Bx=,
TransitionType.MERGES=[[[[Doctor, Gonzales]Doctor]Stout][[[[[Eva, Marie]and]the]entire]staff]punc] B=[ ] Bx=,
TransitionType.MERGES=[[[[Doctor, Gonzales]Doctor]Stout][[[[[[Eva, Marie]and]the]entire]staff]punc]] B=[ ] Bx=,
### Identified: 
thank you
## they were very professional , respectful , completed the job on time , and well below my budget .
### Annotated:
on time
TransitionType.MERGES=[on, time]                B=[ ,,and, ..] Bx=job
TransitionType.MARK_AS_OTHS=[[on, time]]              B=[ ,,and, ..] Bx=job
### Identified: 
on time
## i had a problem with the tile in my bathroom coming apart .
### Annotated:
have a problem
come apart
TransitionType.MERGES=[had, problem]            B=[ with,the, ..] Bx=a
TransitionType.MARK_AS_OTHS=[[had, problem]]          B=[ with,the, ..] Bx=a
### Identified: 
have problem
## we have had nothing but compliments on our bathroom when guest come over - who would have guessed that one ?
### Annotated:
nothing but
come over
who would have
TransitionType.MERGES=[had, nothing, but]       B=[ compliments,on, ..] Bx=have
TransitionType.MARK_AS_OTHS=[had[nothing, but]]       B=[ compliments,on, ..] Bx=have
TransitionType.MERGES=[had, on]                 B=[ our,bathroom, ..] Bx=compliments
TransitionType.MARK_AS_OTHS=[[had, on]]               B=[ our,bathroom, ..] Bx=compliments
TransitionType.MERGES=[come, over]              B=[ -,who, ..] Bx=guest
TransitionType.MARK_AS_OTHS=[[come, over]]            B=[ -,who, ..] Bx=guest
### Identified: 
nothing but
have on
come over
## i have been growing my hair out for number year plus and went in to get number inch taken off .
### Annotated:
grow out
go in
take off
TransitionType.MERGES=[growing, out]            B=[ for,number, ..] Bx=hair
TransitionType.MARK_AS_OTHS=[[growing, out]]          B=[ for,number, ..] Bx=hair
TransitionType.MERGES=[taken, off]              B=[ punc,] Bx=inch
TransitionType.MARK_AS_OTHS=[[taken, off]]            B=[ punc,] Bx=inch
### Identified: 
grow out
take off
## susanna is the best dress maker / tailor i 've ever come across in my whole life !
### Annotated:
dress maker
come across
## home team - thanks number playin !!!
### Annotated:
home team
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
home team
## as an example they took payment for number out of number monthly plan premiums for a yearly policy and cancelled the contract for the remainder of the policy for reasons they stated was not receiving information on other licensed drivers in the household ?
### Annotated:
as an example
out of
TransitionType.MERGES=[out, of]                 B=[ number,monthly, ..] Bx=number
TransitionType.MARK_AS_OTHS=[[out, of]]               B=[ number,monthly, ..] Bx=number
### Identified: 
out of
## i felt as if i was in an over priced olive garden .
### Annotated:
as if
over priced
olive garden
TransitionType.MERGES=[over, priced]            B=[ Olive,Garden, ..] Bx=an
TransitionType.MARK_AS_OTHS=[[over, priced]]          B=[ Olive,Garden, ..] Bx=an
TransitionType.MERGES=[Olive, Garden]           B=[ punc,] Bx=priced
TransitionType.MERGES=[[Olive, Garden]punc]     B=[ ] Bx=priced
### Identified: 
over priced
## in my opinon this place should be shut down by the health inspector , and anyone who is satisfied with there service and food has never eaten at a real asian restaurant .
### Annotated:
in my opinon
shut down
health inspector
TransitionType.MERGES=[shut, down]              B=[ by,the, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[shut, down]]            B=[ by,the, ..] Bx=be
### Identified: 
shut down
## not only were my wife and i very pleased , but i also had the air duct quality tested professionally by the home inspector that i regularly use , before and after united air duct performed their work .
### Annotated:
air duct
home inspector
united air duct
TransitionType.MERGE
TransitionType.MARK_AS_OTH
TransitionType.MERGES=[air, duct]               B=[ quality,tested, ..] Bx=the
TransitionType.MERGES=[[air, duct]quality]      B=[ tested,professionally, ..] Bx=the
TransitionType.MERGES=[[[air, duct]quality]tested] B=[ professionally,by, ..] Bx=the
TransitionType.MERGES=[[[[air, duct]quality]tested]professionally] B=[ by,the, ..] Bx=the
TransitionType.MERGES=[[[[[air, duct]quality]tested]professionally]by] B=[ the,home, ..] Bx=the
TransitionType.MERGES=[[[[[[air, duct]quality]tested]professionally]by]United, Air] B=[ Duct,performed, ..] Bx=after
TransitionType.MERGES=[[[[[[air, duct]quality]tested]professionally]by][United, Air]Duct] B=[ performed,their, ..] Bx=after
TransitionType.MERGES=[[[[[[air, duct]quality]tested]professionally]by][[United, Air]Duct]performed] B=[ their,work, ..] Bx=after
TransitionType.MERGES=[[[[[[air, duct]quality]tested]professionally]by][[[United, Air]Duct]performed]] B=[ ] Bx=punc
### Identified: 
not only
## marek dzida the owner and photographer puts whole heart in his business - if you are into old fashion ( not digital ) quality photography this is best place in long beach as i think not many folks can do affordable traditional photos anymore i know marek personaly and i will always recommend him
### Annotated:
marek dzida
put heart in
old fashion
long beach
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGES=[Long, Beach]             B=[ as,I, ..] Bx=in
TransitionType.MARK_AS_OTHS=[[Long, Beach]]           B=[ as,I, ..] Bx=in
### Identified: 
long beach
## my friend called the hotel to cancel our room as soon as i called her .
### Annotated:
as soon as
TransitionType.MERGES=[as, soon]                B=[ as,I, ..] Bx=room
TransitionType.MERGES=[[as, soon]as]            B=[ I,called, ..] Bx=room
TransitionType.MARK_AS_OTHS=[[[as, soon]as]]          B=[ I,called, ..] Bx=room
### Identified: 
as soon as
## worst buffet period by far .
### Annotated:
by far
TransitionType.MERGES=[by, far]                 B=[ punc,] Bx=period
TransitionType.MARK_AS_OTHS=[[by, far]]               B=[ punc,] Bx=period
### Identified: 
by far
## mike one of owners was awesome , he explained the detailed plan , and executed on time , i am always going use them and refer them to many friends i can because of the great job they did me .
### Annotated:
on time
because of
TransitionType.MERGES=[on, time]                B=[ ,,I, ..] Bx=execute
TransitionType.MARK_AS_OTHS=[[on, time]]              B=[ ,,I, ..] Bx=execute
TransitionType.MERGES=[because, of]             B=[ the,great, ..] Bx=can
TransitionType.MARK_AS_OTHS=[[because, of]]           B=[ the,great, ..] Bx=can
### Identified: 
on time
because of
## my friend and i were to stay here for a girls night , catch up on our lives evening .
### Annotated:
girl night
catch up
TransitionType.MERGES=[girls, night]            B=[ ,,catch, ..] Bx=a
TransitionType.MERGES=[[girls, night],]         B=[ catch,up, ..] Bx=a
TransitionType.MERGES=[[[girls, night],]catch]  B=[ up,on, ..] Bx=a
TransitionType.MERGES=[[[[girls, night],]catch]up] B=[ on,our, ..] Bx=a
TransitionType.MERGES=[[[[[girls, night],]catch]up]on] B=[ our,lives, ..] Bx=a
TransitionType.MERGES=[[[[[[girls, night],]catch]up]on]lives] B=[ evening,punc,] Bx=our
TransitionType.MERGES=[[[[[[[girls, night],]catch]up]on]lives]evening] B=[ punc,] Bx=our
TransitionType.MERGES=[[[[[[[[girls, night],]catch]up]on]lives]evening]punc] B=[ ] Bx=our
## we live within number miles of the hotel and wanted to get away from our responsibilities for the night .
### Annotated:
get away
TransitionType.MERGES=[get, away]               B=[ from,our, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[get, away]]             B=[ from,our, ..] Bx=to
### Identified: 
get away
## unfortunalty my husband and i had to put our number year old lab down that morning and we were not expecting this .
### Annotated:
have to
put down
year old
TransitionType.MERGES=[had, to]                 B=[ put,our, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[had, to]]               B=[ put,our, ..] Bx=i
TransitionType.MERGES=[put, year, old]          B=[ lab,down, ..] Bx=number
TransitionType.MARK_AS_OTHS=[put[year, old]]          B=[ lab,down, ..] Bx=number
TransitionType.MERGES=[put, down]               B=[ that,morning, ..] Bx=lab
TransitionType.MARK_AS_OTHS=[[put, down]]             B=[ that,morning, ..] Bx=lab
### Identified: 
have to
year old
put down
## i called them back a few hours after putting my bodhi down and they still would n't budge .
### Annotated:
call back
put down
nt budge
TransitionType.MERGES=[called, back]            B=[ a,few, ..] Bx=them
TransitionType.MARK_AS_OTHS=[[called, back]]          B=[ a,few, ..] Bx=them
TransitionType.MERGES=[a, few]                  B=[ hours,after, ..] Bx=back
TransitionType.MARK_AS_OTHS=[[a, few]]                B=[ hours,after, ..] Bx=back
### Identified: 
call back
a few
## i called number times to talked to a manager , never a call back .
### Annotated:
call back
## i even emailed mackinaw tourist and nothing .
### Annotated:
mackinaw tourist
TransitionType.MERGES=[Mackinaw, Tourist]       B=[ and,nothing, ..] Bx=email
TransitionType.MERGES=[[Mackinaw, Tourist]and]  B=[ nothing,punc,] Bx=email
TransitionType.MERGES=[[[Mackinaw, Tourist]and]nothing] B=[ punc,] Bx=email
TransitionType.MERGES=[[[[Mackinaw, Tourist]and]nothing]punc] B=[ ] Bx=email
## this insurance co. is a joke !!!
### Annotated:
be a joke
TransitionType.MERGES=[make, every]             B=[ attempt,to, ..] Bx=will
TransitionType.MERGES=[[make, every]attempt]    B=[ to,misinform, ..] Bx=will
TransitionType.MERGES=[[[make, every]attempt]to] B=[ misinform,and, ..] Bx=will
TransitionType.MERGES=[[[[make, every]attempt]to]misinform] B=[ and,misrepresent, ..] Bx=will
TransitionType.MERGES=[[[[[make, every]attempt]to]misinform]and] B=[ misrepresent,themselves, ..] Bx=will
TransitionType.MERGES=[[[[[[make, every]attempt]to]misinform]and]misrepresent] B=[ themselves,punc,] Bx=will
TransitionType.MERGES=[[[[[[[make, every]attempt]to]misinform]and]misrepresent]themselves] B=[ punc,] Bx=will
TransitionType.MERGES=[[[[[[[[make, every]attempt]to]misinform]and]misrepresent]themselves]punc] B=[ ] Bx=will
## they make up excuses in hopes to confuse their policy holders with misinformation .
### Annotated:
make up
in hope to
TransitionType.MERGES=[make, up]                B=[ excuses,in, ..] Bx=they
TransitionType.MARK_AS_OTHS=[[make, up]]              B=[ excuses,in, ..] Bx=they
### Identified: 
make up
## home made product
### Annotated:
home make
## i sometimes go into this store just for something to do on a sunday afternoon .
### Annotated:
to do
## nothing compares to a home made product that really stands the test of time . -
### Annotated:
home make
stand the test of time
TransitionType.MERGES=[compares, to]            B=[ a,home, ..] Bx=nothing
TransitionType.MARK_AS_OTHS=[[compares, to]]          B=[ a,home, ..] Bx=nothing
### Identified: 
compare to
## the brick , ikea , and leon 's have their place .
### Annotated:
the brick
leon s
TransitionType.MERGES=[had, work]               B=[ done,in, ..] Bx=the
TransitionType.MERGES=[[had, work]done]         B=[ in,about, ..] Bx=the
TransitionType.MERGES=[[[had, work]done]in]     B=[ about,half, ..] Bx=the
TransitionType.MERGES=[[[[had, work]done]in]about] B=[ half,the, ..] Bx=the
TransitionType.MERGES=[[[[[had, work]done]in]about]half] B=[ the,time, ..] Bx=the
TransitionType.MERGES=[on, remodeling]          B=[ ever,punc,] Bx=spend
TransitionType.MERGES=[[on, remodeling]ever]    B=[ punc,] Bx=spend
TransitionType.MERGES=[[[on, remodeling]ever]punc] B=[ ] Bx=spend
## i highly recommend any one considering home repair to give these guys a call .
### Annotated:
any one
give a call
TransitionType.MERGES=[give, a]                 B=[ call,punc,] Bx=guy
TransitionType.MERGES=[[give, a]call]           B=[ punc,] Bx=guy
TransitionType.MARK_AS_OTHS=[[[give, a]call]]         B=[ punc,] Bx=guy
### Identified: 
give a call
## gets the job done
### Annotated:
get the job done
## we have utilized mr. pozza and his firm twice now in our family and both times have been very pleased .
### Annotated:
mr pozza
TransitionType.MERGES=[Mr, Pozza]               B=[ and,his, ..] Bx=utilize
TransitionType.MERGES=[[Mr, Pozza]and]          B=[ his,firm, ..] Bx=utilize
## barb does an amazing job , she is always learning new things on how to use her hands and body , to give every person an awesome massage , call today and schedule you must see her , you will fall in love she is the best of the best !
### Annotated:
give massage
fall in love
best of the best
TransitionType.MERGES=[IN, LOVE]                B=[ SHE,IS, ..] Bx=fall
TransitionType.MARK_AS_OTHS=[[IN, LOVE]]              B=[ SHE,IS, ..] Bx=fall
### Identified: 
in love
## as a very satisfied new customer , i wholeheartedly recommend united air duct cleaning .
### Annotated:
united air duct cleaning
TransitionType.MERGES=[United, Air]             B=[ Duct,Cleaning, ..] Bx=recommend
TransitionType.MERGES=[[United, Air]Duct]       B=[ Cleaning,punc,] Bx=recommend
TransitionType.MERGES=[[[United, Air]Duct]Cleaning] B=[ punc,] Bx=recommend
TransitionType.MERGES=[[[[United, Air]Duct]Cleaning]punc] B=[ ] Bx=recommend
TransitionType.MERGES=[thanks, guys]            B=[ punc,] Bx=again
TransitionType.MARK_AS_OTHS=[[thanks, guys]]          B=[ punc,] Bx=again
### Identified: 
thanks guy
## i walked out with number inch long hair on the top , number inch long hair on the sides , and number in the back .
### Annotated:
walk out
TransitionType.MERGES=[walked, out]             B=[ with,number, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[walked, out]]           B=[ with,number, ..] Bx=i
### Identified: 
walk out
## this was a terrible experience and i hope that no one else goes through that .
### Annotated:
go through
TransitionType.MERGES=[no, one]                 B=[ else,goes, ..] Bx=that
TransitionType.MARK_AS_OTHS=[[no, one]]               B=[ else,goes, ..] Bx=that
TransitionType.MERGES=[goes, through]           B=[ that,punc,] Bx=else
TransitionType.MARK_AS_OTHS=[[goes, through]]         B=[ that,punc,] Bx=else
### Identified: 
no one
go through
## do your self a favor and do not go to this establishment .
### Annotated:
do a favor
your self
## i love hellada gallery !
### Annotated:
hellada gallery
TransitionType.MERGES=[Hellada, Gallery]        B=[ punc,] Bx=love
TransitionType.MERGES=[[Hellada, Gallery]punc]  B=[ ] Bx=love
## there is no lower rating for noonan 's liquor , owners and employees .
### Annotated:
noonan s liquor
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
many thanks
## i want my money back !
### Annotated:
money back
## i used to take my cars there all the time , but management changes hands too frequently , the service has been slow , and they often try to " add on " extra services , which sometimes is not needed .
### Annotated:
use to
all the time
add on
TransitionType.MERGES=[used, to]                B=[ take,my, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[used, to]]              B=[ take,my, ..] Bx=i
### Identified: 
use to
## if possible i try the services on myself before i bring in my son .
### Annotated:
bring in
## drs. ali work wonders .
### Annotated:
drs ali
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## neither me nor my son have n't had a single cavity since we started dental care there .
### Annotated:
dental care
TransitionType.MERGES=[a, single]               B=[ cavity,since, ..] Bx=have
TransitionType.MERGES=[[a, single]cavity]       B=[ since,we, ..] Bx=have
TransitionType.MERGES=[[[a, single]cavity]since] B=[ we,started, ..] Bx=have
TransitionType.MERGES=[[[[a, single]cavity]since]we] B=[ started,dental, ..] Bx=have
TransitionType.MERGES=[[[[[a, single]cavity]since]we]started] B=[ dental,care, ..] Bx=have
TransitionType.MERGES=[[[[[[a, single]cavity]since]we]started]dental] B=[ care,there, ..] Bx=have
TransitionType.MERGES=[[[[[[[a, single]cavity]since]we]started]dental]care] B=[ there,punc,] Bx=have
TransitionType.MERGES=[[[[[[[[a, single]cavity]since]we]started]dental]care]there] B=[ punc,] Bx=have
TransitionType.MERGES=[[[[[[[[[a, single]cavity]since]we]started]dental]care]there]punc] B=[ ] Bx=have
## they are professional , knowledgeable , and take meticulous care and pride in accomplishing their work .
### Annotated:
take pride
TransitionType.MERGES=[take, care]              B=[ and,pride, ..] Bx=meticulous
TransitionType.MERGES=[[take, care]and]         B=[ pride,in, ..] Bx=meticulous
TransitionType.MERGES=[[[take, care]and]pride]  B=[ in,accomplishing, ..] Bx=meticulous
TransitionType.MERGES=[[[[take, care]and]pride]in] B=[ accomplishing,their, ..] Bx=meticulous
TransitionType.MERGES=[[[[[take, care]and]pride]in]accomplishing] B=[ their,work, ..] Bx=meticulous
## based on the test results , the home inspector stated that the quality of their job was " excellent " .
### Annotated:
home inspector
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
base on
## dr. shady
### Annotated:
dr shady
TransitionType.MERGE
## kelly hit the nail on the head .
### Annotated:
hit the nail on the head
TransitionType.MERGES=[hit, nail]               B=[ on,the, ..] Bx=the
TransitionType.MERGES=[[hit, nail]on]           B=[ the,head, ..] Bx=the
TransitionType.MERGES=[[[hit, nail]on]the]      B=[ head,punc,] Bx=the
TransitionType.MERGES=[[[[hit, nail]on]the]head] B=[ punc,] Bx=the
TransitionType.MERGES=[[[[[hit, nail]on]the]head]punc] B=[ ] Bx=the
## " dr. shady " is a jerk .
### Annotated:
dr shady
TransitionType.MERGES=[Dr, Shady]               B=[ punc,is, ..] Bx=punc
TransitionType.MERGES=[[Dr, Shady]punc]         B=[ is,a, ..] Bx=punc
TransitionType.MERGES=[[[Dr, Shady]punc]is]     B=[ a,jerk, ..] Bx=punc
TransitionType.MERGES=[[[[Dr, Shady]punc]is]a]  B=[ jerk,punc,] Bx=punc
TransitionType.MERGES=[[[[[Dr, Shady]punc]is]a]jerk] B=[ punc,] Bx=punc
TransitionType.MERGES=[[[[[[Dr, Shady]punc]is]a]jerk]punc] B=[ ] Bx=punc
## good luck keeping business with that stuck up attitude dr. shady .
### Annotated:
good luck
stick up
dr shady
TransitionType.MERGES=[stuck, up]               B=[ attitude,Dr, ..] Bx=that
TransitionType.MARK_AS_OTHS=[[stuck, up]]             B=[ attitude,Dr, ..] Bx=that
TransitionType.MERGES=[Dr, Shady]               B=[ punc,] Bx=attitude
TransitionType.MERGES=[[Dr, Shady]punc]         B=[ ] Bx=attitude
### Identified: 
stick up
## the next time you feel like being condescending to someone , it is not going to be me !!!!!!
### Annotated:
go to
TransitionType.MERGES=[going, to]               B=[ be,me, ..] Bx=not
TransitionType.MARK_AS_OTHS=[[going, to]]             B=[ be,me, ..] Bx=not
### Identified: 
go to
## dr. shady is inexperienced and prideful .
### Annotated:
dr shady
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## i had to call back up there two hours later and the lady ( who claimed to be a manager ) said my food was on the way , and she did nt offer to compensate me in any kind of way .
### Annotated:
have to
call back
on the way
TransitionType.MERGES=[had, to]                 B=[ call,back, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[had, to]]               B=[ call,back, ..] Bx=i
TransitionType.MERGES=[call, back]              B=[ up,there, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[call, back]]            B=[ up,there, ..] Bx=to
TransitionType.MERGES=[on, the]                 B=[ way,,, ..] Bx=be
TransitionType.MERGES=[[on, the]way]            B=[ ,,and, ..] Bx=be
TransitionType.MERGES=[[[on, the]way],]         B=[ and,she, ..] Bx=be
TransitionType.MERGES=[[[[on, the]way],]and]    B=[ she,did, ..] Bx=be
TransitionType.MERGES=[[[[[on, the]way],]and]she] B=[ did,nt, ..] Bx=be
TransitionType.MERGES=[[[[[[on, the]way],]and]she]did] B=[ nt,offer, ..] Bx=be
TransitionType.MERGES=[[[[[[[on, the]way],]and]she]did]nt] B=[ offer,to, ..] Bx=be
TransitionType.MERGES=[[[[[[[[on, the]way],]and]she]did]nt]offer] B=[ to,compensate, ..] Bx=be
TransitionType.MERGES=[[[[[[[[[on, the]way],]and]she]did]nt]offer]to] B=[ compensate,me, ..] Bx=be
TransitionType.MERGES=[[[[[[[[[[on, the]way],]and]she]did]nt]offer]to]compensate] B=[ me,in, ..] Bx=be
TransitionType.MERGES=[[[[[[[[[[[on, the]way],]and]she]did]nt]offer]to]compensate]in, any] B=[ kind,of, ..] Bx=me
TransitionType.MERGES=[[[[[[[[[[[on, the]way],]and]she]did]nt]offer]to]compensate][in, any]kind] B=[ of,way, ..] Bx=me
TransitionType.MERGES=[[[[[[[[[[[on, the]way],]and]she]did]nt]offer]to]compensate][[in, any]kind]of] B=[ way,punc,] Bx=me
TransitionType.MERGES=[[[[[[[[[[[on, the]way],]and]she]did]nt]offer]to]compensate][[[in, any]kind]of]way] B=[ punc,] Bx=me
TransitionType.MERGES=[[[[[[[[[[[on, the]way],]and]she]did]nt]offer]to]compensate][[[[in, any]kind]of]way]punc] B=[ ] Bx=me
TransitionType.MERGES=[[[[[[[[[[[on, the]way],]and]she]did]nt]offer]to]compensate][[[[[in, any]kind]of]way]punc]] B=[ ] Bx=me
### Identified: 
have to
call back
## if this is the best that tucson has to offer , i am out ta here ...
### Annotated:
out ta
TransitionType.MERGES=[has, to]                 B=[ offer,,, ..] Bx=tucson
TransitionType.MERGES=[[has, to]offer]          B=[ ,,I, ..] Bx=tucson
TransitionType.MARK_AS_OTHS=[[[has, to]offer]]        B=[ ,,I, ..] Bx=tucson
TransitionType.MERGES=[out, ta]                 B=[ here,punc,] Bx=be
TransitionType.MARK_AS_OTHS=[[out, ta]]               B=[ here,punc,] Bx=be
### Identified: 
have to offer
out ta
## the food was horrible not cooked like it should be , they got the order wrong on a number of occasions , and once forgot about my order .
### Annotated:
a number
TransitionType.MERGES=[a, number]               B=[ of,occasions, ..] Bx=on
TransitionType.MARK_AS_OTHS=[[a, number]]             B=[ of,occasions, ..] Bx=on
### Identified: 
a number
## even though we were only supposed to have those specific types of pizza , when guests asked for a different type , it was brought out with no charge to us !
### Annotated:
be suppose to
TransitionType.MERGES=[supposed, to]            B=[ have,those, ..] Bx=only
TransitionType.MARK_AS_OTHS=[[supposed, to]]          B=[ have,those, ..] Bx=only
TransitionType.MERGES=[brought, out]            B=[ with,no, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[brought, out]]          B=[ with,no, ..] Bx=be
### Identified: 
suppose to
bring out
## excellent service , not only did they get the exact car i wanted win in number hours but the sales man also took me out to lunch .
### Annotated:
sales man
take out
TransitionType.MERGES=[sales, man]              B=[ also,took, ..] Bx=the
TransitionType.MERGES=[[sales, man]also]        B=[ took,me, ..] Bx=the
TransitionType.MERGES=[[[sales, man]also]took]  B=[ me,out, ..] Bx=the
TransitionType.MERGES=[[[[sales, man]also]took]out] B=[ to,lunch, ..] Bx=me
TransitionType.MERGES=[[[[[sales, man]also]took]out]to] B=[ lunch,punc,] Bx=me
TransitionType.MERGES=[[[[[[sales, man]also]took]out]to]lunch] B=[ punc,] Bx=me
TransitionType.MERGES=[[[[[[[sales, man]also]took]out]to]lunch]punc] B=[ ] Bx=me
## my number year old daughter loves this place .
### Annotated:
year old
TransitionType.MERGES=[year, old]               B=[ daughter,loves, ..] Bx=number
TransitionType.MARK_AS_OTHS=[[year, old]]             B=[ daughter,loves, ..] Bx=number
### Identified: 
year old
## the moving company is actualy based in brooklyn , but advertised all over ny / nj , including fort lee .
### Annotated:
all over
fort lee
TransitionType.MERGES=[all, over]               B=[ NY,punc, ..] Bx=advertise
TransitionType.MARK_AS_OTHS=[[all, over]]             B=[ NY,punc, ..] Bx=advertise
TransitionType.MERGES=[Fort, Lee]               B=[ punc,] Bx=include
TransitionType.MERGES=[[Fort, Lee]punc]         B=[ ] Bx=include
### Identified: 
all over
## when the guys arrived ( number hours later than agreed ) they told that you have to pay all the tolls they payed coming from brooklyn and extra $ number for them to drive back from your destination .
### Annotated:
have to
TransitionType.MERGES=[have, to]                B=[ pay,all, ..] Bx=you
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ pay,all, ..] Bx=you
### Identified: 
have to
TransitionType.MERGES=[was, in]                 B=[ agreement,eather, ..] Bx=not
TransitionType.MARK_AS_OTHS=[[was, in]]               B=[ agreement,eather, ..] Bx=not
### Identified: 
be in
## guess what , was not in the initial agreement as well .
### Annotated:
as well
TransitionType.MERGES=[as, well]                B=[ punc,] Bx=agreement
TransitionType.MARK_AS_OTHS=[[as, well]]              B=[ punc,] Bx=agreement
### Identified: 
as well
## the only reason i 'm giving number stars instead of number or number , i should admit , nothing was broken .
### Annotated:
instead of
TransitionType.MERGES=[number, stars]           B=[ instead,of, ..] Bx=give
TransitionType.MARK_AS_OTHS=[[number, stars]]         B=[ instead,of, ..] Bx=give
TransitionType.MERGES=[instead, of]             B=[ number,or, ..] Bx=star
TransitionType.MARK_AS_OTHS=[[instead, of]]           B=[ number,or, ..] Bx=star
### Identified: 
number star
instead of
## one more thing , they do n't take any credit cards or checks .
### Annotated:
one more thing
credit cards
## you have to pay cash only before they start unloading track on your destination .
### Annotated:
have to
TransitionType.MERGES=[have, to]                B=[ pay,CASH, ..] Bx=you
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ pay,CASH, ..] Bx=you
### Identified: 
have to
## this is one of the worst places i have stayed , we cut out stay short and went to the mulberry .
### Annotated:
cut short
TransitionType.MERGES=[cut, stay]               B=[ short,and, ..] Bx=out
TransitionType.MERGES=[[cut, stay]short]        B=[ and,went, ..] Bx=out
TransitionType.MERGES=[[[cut, stay]short]and]   B=[ went,to, ..] Bx=out
TransitionType.MERGES=[[[[cut, stay]short]and]went] B=[ to,the, ..] Bx=out
TransitionType.MERGES=[[[[[cut, stay]short]and]went]to] B=[ the,Mulberry, ..] Bx=out
TransitionType.MERGES=[[[[[[cut, stay]short]and]went]to]the] B=[ Mulberry,punc,] Bx=out
TransitionType.MERGES=[[[[[[[cut, stay]short]and]went]to]the]Mulberry] B=[ punc,] Bx=out
TransitionType.MERGES=[[[[[[[[cut, stay]short]and]went]to]the]Mulberry]punc] B=[ ] Bx=out
## even though they still charge you the days you booked but wo n't use , it is worth the get the hell out of this crap hole .
### Annotated:
get the hell
out of
crap hole
TransitionType.MERGES=[out, of]                 B=[ this,crap, ..] Bx=hell
TransitionType.MARK_AS_OTHS=[[out, of]]               B=[ this,crap, ..] Bx=hell
### Identified: 
out of
## bad service starting from the front desk .
### Annotated:
front desk
TransitionType.MERGES=[front, desk]             B=[ punc,] Bx=the
TransitionType.MARK_AS_OTHS=[[front, desk]]           B=[ punc,] Bx=the
### Identified: 
front desk
## mercedes and dan are very thorough and on top of everything !
### Annotated:
on top of
TransitionType.MERGES=[on, top]                 B=[ of,everything, ..] Bx=and
TransitionType.MERGES=[[on, top]of]             B=[ everything,punc,] Bx=and
TransitionType.MARK_AS_OTHS=[[[on, top]of]]           B=[ everything,punc,] Bx=and
### Identified: 
on top of
## this school is the worst one i 've ever been to .
### Annotated:
be to
TransitionType.MERGES=[been, to]                B=[ punc,] Bx=ever
TransitionType.MARK_AS_OTHS=[[been, to]]              B=[ punc,] Bx=ever
### Identified: 
be to
## the staff and the principal are rediculous , they do n't listen to any input , and they make up rediculous rules ( they banned backpacks , because a teacher tripped over a student 's ) .
### Annotated:
make up
TransitionType.MERGES=[make, up]                B=[ rediculous,rules, ..] Bx=they
TransitionType.MARK_AS_OTHS=[[make, up]]              B=[ rediculous,rules, ..] Bx=they
### Identified: 
make up
## the education is horrible at best , do society a favor , and do not send your student here .
### Annotated:
at best
do a favor
TransitionType.MERGES=[at, best]                B=[ ,,do, ..] Bx=horrible
TransitionType.MARK_AS_OTHS=[[at, best]]              B=[ ,,do, ..] Bx=horrible
### Identified: 
at best
## paula has an amazing gift for creativity , vision and the ability to combine art to / with commercial purpose .
### Annotated:
have an gift for
## dr. aster and her team have been a strong advocate in the health of both my daughters .
### Annotated:
dr aster
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## dr. aster is very kind an gentle with the children , but also positive and to the point with the parents .
### Annotated:
dr aster
to the point
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
thanks again
## i heard the libido band play live and they are out of site !!
### Annotated:
the libido band
out of site
TransitionType.MERGES=[are, out]                B=[ of,site, ..] Bx=they
TransitionType.MERGES=[[are, out]of]            B=[ site,punc,] Bx=they
TransitionType.MARK_AS_OTHS=[[[are, out]of]]          B=[ site,punc,] Bx=they
### Identified: 
be out of
## quick to take money but not quick to fix a problem !
### Annotated:
fix problem
TransitionType.MERGES=[take, money]             B=[ but,not, ..] Bx=to
TransitionType.MERGES=[[take, money]but]        B=[ not,quick, ..] Bx=to
TransitionType.MERGES=[[[take, money]but]not]   B=[ quick,to, ..] Bx=to
TransitionType.MERGES=[[[[take, money]but]not]quick] B=[ to,fix, ..] Bx=to
TransitionType.MERGES=[[[[[take, money]but]not]quick]to] B=[ fix,a, ..] Bx=to
TransitionType.MERGES=[[[[[[take, money]but]not]quick]to]fix] B=[ a,problem, ..] Bx=to
TransitionType.MERGES=[[[[[[[take, money]but]not]quick]to]fix]a] B=[ problem,punc,] Bx=to
TransitionType.MERGES=[[[[[[[[take, money]but]not]quick]to]fix]a]problem] B=[ punc,] Bx=to
TransitionType.MERGES=[[[[[[[[[take, money]but]not]quick]to]fix]a]problem]punc] B=[ ] Bx=to
## b&b came out very quickly to give us our quote back in june .
### Annotated:
come out
give quote
TransitionType.MERGES=[came, out]               B=[ very,quickly, ..] Bx=bb
TransitionType.MARK_AS_OTHS=[[came, out]]             B=[ very,quickly, ..] Bx=bb
### Identified: 
come out
TransitionType.MERGES=[to, begin]               B=[ installing,our, ..] Bx=vacation
TransitionType.MERGES=[[to, begin]installing]   B=[ our,fence, ..] Bx=vacation
TransitionType.MERGES=[[[to, begin]installing]our] B=[ fence,punc,] Bx=vacation
TransitionType.MERGES=[[[[to, begin]installing]our]fence] B=[ punc,] Bx=vacation
TransitionType.MERGES=[[[[[to, begin]installing]our]fence]punc] B=[ ] Bx=vacation
## we called our representative who assured me he would call the office and have it taken care of .
### Annotated:
take care of
TransitionType.MERGES=[taken, care]             B=[ of,punc,] Bx=it
TransitionType.MERGES=[[taken, care]of]         B=[ punc,] Bx=it
TransitionType.MARK_AS_OTHS=[[[taken, care]of]]       B=[ punc,] Bx=it
### Identified: 
take care of
## we then called the office and the man we spoke to said he 'd send someone out to look at it but could n't promise when - two weeks came and went and we heard nothing .
### Annotated:
come and go
## i just called again and was told that workmanship , not wood , is guaranteed for a year - well in my opinion - the wood split due to a nail which is part of workmanship !
### Annotated:
in my opinion
due to
TransitionType.MERGES=[due, to]                 B=[ a,nail, ..] Bx=split
TransitionType.MARK_AS_OTHS=[[due, to]]               B=[ a,nail, ..] Bx=split
### Identified: 
due to
## i 'm very frustrated at this point - it would take all of number min for them to come by and replace the one board that is cracked ( the crack is deep enough to stick a penny in it and it goes clear through ) yet they do not want to take the time to bother with what once was a happy customer and has now become a dissatisfied customer .
### Annotated:
at this point
all of
come by
take the time
TransitionType.MERGES=[at, this]                B=[ point,-, ..] Bx=frustrated
TransitionType.MERGES=[[at, this]point]         B=[ -,it, ..] Bx=frustrated
TransitionType.MARK_AS_OTHS=[[[at, this]point]]       B=[ -,it, ..] Bx=frustrated
TransitionType.MERGES=[come, by]                B=[ and,replace, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[come, by]]              B=[ and,replace, ..] Bx=to
TransitionType.MERGES=[take, the]               B=[ time,to, ..] Bx=to
TransitionType.MERGES=[[take, the]time]         B=[ to,bother, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[[take, the]time]]       B=[ to,bother, ..] Bx=to
### Identified: 
at this point
come by
take the time
## so i figure if they do n't want to take the time to fix the fence that they installed then i 'll take the time to let everyone i can know about how they treat customers once they have your money !!!
### Annotated:
take the time
take the time
let know
TransitionType.MERGES=[take, the]               B=[ time,to, ..] Bx=to
TransitionType.MERGES=[[take, the]time]         B=[ to,fix, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[[take, the]time]]       B=[ to,fix, ..] Bx=to
TransitionType.MERGES=[take, the]               B=[ time,to, ..] Bx=ll
TransitionType.MERGES=[[take, the]time]         B=[ to,let, ..] Bx=ll
TransitionType.MARK_AS_OTHS=[[[take, the]time]]       B=[ to,let, ..] Bx=ll
### Identified: 
take the time
take the time
## you get what you pay for !!!
### Annotated:
you get what you pay for
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
you get what you pay for
## when the fence was first installed i would have given them five stars , now for their poor customer follow - up and unwillingness to fix the fence they have dropped to a one - star in my opinion !
### Annotated:
follow - up
one - star
in opinion
TransitionType.MERGES=[follow, -]               B=[ up,and, ..] Bx=customer
TransitionType.MERGES=[[follow, -]up]           B=[ and,unwillingness, ..] Bx=customer
TransitionType.MARK_AS_OTHS=[[[follow, -]up]]         B=[ and,unwillingness, ..] Bx=customer
TransitionType.MERGES=[one, star]               B=[ in,my, ..] Bx=-
TransitionType.MARK_AS_OTHS=[[one, star]]             B=[ in,my, ..] Bx=-
### Identified: 
follow - up
one star
## good and bad
### Annotated:
good and bad
## i had to take care of the ants myself .
### Annotated:
have to
take care of
TransitionType.MERGES=[had, to]                 B=[ take,care, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[had, to]]               B=[ take,care, ..] Bx=i
TransitionType.MERGES=[take, care]              B=[ of,the, ..] Bx=to
TransitionType.MERGES=[[take, care]of]          B=[ the,ants, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[[take, care]of]]        B=[ the,ants, ..] Bx=to
### Identified: 
have to
take care of
## never had a problem with the staff and found them very helpful when something went wrong .
### Annotated:
have a problem
go wrong
TransitionType.MERGES=[had, problem]            B=[ with,the, ..] Bx=a
TransitionType.MARK_AS_OTHS=[[had, problem]]          B=[ with,the, ..] Bx=a
### Identified: 
have problem
## because of the ants i dropped them to a number star .
### Annotated:
because of
number star
TransitionType.MERGE
TransitionType.MARK_AS_OTH
TransitionType.MERGES=[number, star]            B=[ punc,] Bx=a
TransitionType.MARK_AS_OTHS=[[number, star]]          B=[ punc,] Bx=a
### Identified: 
because of
number star
## our family has been trusting doctor hank with our teeth for the last seven years .
### Annotated:
trust with
doctor hank
TransitionType.MERGES=[Doctor, Hank]            B=[ with,our, ..] Bx=trust
TransitionType.MARK_AS_OTHS=[[Doctor, Hank]]          B=[ with,our, ..] Bx=trust
### Identified: 
doctor hank
## everyone on staff is very professional and friendly .
### Annotated:
on staff
## disatisfied customer , i went through kitchen aid and used one of their recommended vendors .
### Annotated:
kitchen aid
TransitionType.MERGES=[went, through]           B=[ Kitchen,Aid, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[went, through]]         B=[ Kitchen,Aid, ..] Bx=i
TransitionType.MERGES=[Kitchen, Aid]            B=[ and,used, ..] Bx=through
TransitionType.MERGES=[[Kitchen, Aid]and]       B=[ used,one, ..] Bx=through
TransitionType.MERGES=[[[Kitchen, Aid]and]used] B=[ one,of, ..] Bx=through
TransitionType.MERGES=[[[[Kitchen, Aid]and]used]one] B=[ of,their, ..] Bx=through
TransitionType.MERGES=[[[[[Kitchen, Aid]and]used]one]of] B=[ their,recommended, ..] Bx=through
TransitionType.MERGES=[[[[[[Kitchen, Aid]and]used]one]of]their] B=[ recommended,vendors, ..] Bx=through
TransitionType.MERGES=[[[[[[[Kitchen, Aid]and]used]one]of]their]recommended] B=[ vendors,punc,] Bx=through
TransitionType.MERGES=[[[[[[[[Kitchen, Aid]and]used]one]of]their]recommended]vendors] B=[ punc,] Bx=through
TransitionType.MERGES=[[[[[[[[[Kitchen, Aid]and]used]one]of]their]recommended]vendors]punc] B=[ ] Bx=through
### Identified: 
go through
## their quote came in at half the price of a&e for the same work and same part .
### Annotated:
come in
TransitionType.MERGES=[came, in]                B=[ at,half, ..] Bx=quote
TransitionType.MARK_AS_OTHS=[[came, in]]              B=[ at,half, ..] Bx=quote
### Identified: 
come in
## since i 'm usually at work late deb has stayed around to help me out when needed .
### Annotated:
help out
TransitionType.MERGES=[help, out]               B=[ when,needed, ..] Bx=me
TransitionType.MARK_AS_OTHS=[[help, out]]             B=[ when,needed, ..] Bx=me
### Identified: 
help out
## i knew i had found the real deal , big pies , sold by the slice , with the pizzas sitting under the glass in the front .
### Annotated:
the real deal
## we had no choice but to stay but will take this as far as we can .
### Annotated:
take as far as can
TransitionType.MERGES=[as, far]                 B=[ as,we, ..] Bx=this
TransitionType.MERGES=[[as, far]as]             B=[ we,can, ..] Bx=this
TransitionType.MARK_AS_OTHS=[[[as, far]as]]           B=[ we,can, ..] Bx=this
### Identified: 
as far as
## when we walked in , the person behind desk said : " oh well , you must wait , i am in the middle of something . "
### Annotated:
in the middle of
TransitionType.MERGES=[behind, desk]            B=[ said,punc, ..] Bx=person
TransitionType.MERGES=[[behind, desk]said]      B=[ punc,punc, ..] Bx=person
TransitionType.MERGES=[[[behind, desk]said]punc] B=[ punc,oh, ..] Bx=person
## somewhere in between his rudeness he asked if we smoked .
### Annotated:
in between
## i explained that i was already on my way and i would rush to get there as soon as i could because i needed my car for work at number am , but the guy was arguing with me saying he was gon na lock the doors right at number .
### Annotated:
on way
as soon as
gon na
TransitionType.MERGES=[as, soon]                B=[ as,i, ..] Bx=there
TransitionType.MERGES=[[as, soon]as]            B=[ i,could, ..] Bx=there
TransitionType.MARK_AS_OTHS=[[[as, soon]as]]          B=[ i,could, ..] Bx=there
### Identified: 
as soon as
## i 've read some of the reviews below and would like to state that yes , like any other doctor s office there is sometimes a wait ( depending on what other patients are being seen for ) and some of the tests and procedures that are ran can be costly ( just like they would be for any other medical tests elsewhere if you do not have insurance ) ...
### Annotated:
would like
depend on
patient see
TransitionType.MERGES=[doctor, s]               B=[ office,there, ..] Bx=other
TransitionType.MERGES=[[doctor, s]office]       B=[ there,is, ..] Bx=other
TransitionType.MARK_AS_OTHS=[[[doctor, s]office]]     B=[ there,is, ..] Bx=other
### Identified: 
doctor s office
## i called in my order and upon arriving to pick it up , they got my order confused with someone else s .
### Annotated:
call in
pick up
TransitionType.MERGES=[pick, up]                B=[ ,,they, ..] Bx=it
TransitionType.MARK_AS_OTHS=[[pick, up]]              B=[ ,,they, ..] Bx=it
### Identified: 
pick up
## it is the attention to detail and the quality of the work taught at tomipilates that sets this studio apart from the others .
### Annotated:
attention to detail
set apart
TransitionType.MERGES=[attention, to]           B=[ detail,and, ..] Bx=the
TransitionType.MERGES=[[attention, to]detail]   B=[ and,the, ..] Bx=the
TransitionType.MARK_AS_OTHS=[[[attention, to]detail]] B=[ and,the, ..] Bx=the
TransitionType.MERGES=[apart, from]             B=[ the,others, ..] Bx=studio
TransitionType.MARK_AS_OTHS=[[apart, from]]           B=[ the,others, ..] Bx=studio
### Identified: 
attention to detail
apart from
## the team at bradley chevron kept my car running for well past its expected death !
### Annotated:
bradley chevron
keep run
TransitionType.MERGES=[Bradley, Chevron]        B=[ kept,my, ..] Bx=at
TransitionType.MERGES=[[Bradley, Chevron]kept]  B=[ my,car, ..] Bx=at
## i hate to say check them out just for the salsa , but james , i need another jar badly :) all kidding aside , they are a very good company , i have a hard time giving any service biz a number star review but they came close .
### Annotated:
i hate to say
check out
all kidding aside
number star
TransitionType.MERGES=[check, out]              B=[ just,for, ..] Bx=them
TransitionType.MARK_AS_OTHS=[[check, out]]            B=[ just,for, ..] Bx=them
TransitionType.MERGES=[hard, time]              B=[ giving,any, ..] Bx=a
TransitionType.MARK_AS_OTHS=[[hard, time]]            B=[ giving,any, ..] Bx=a
TransitionType.MERGES=[number, star]            B=[ review,but, ..] Bx=a
TransitionType.MARK_AS_OTHS=[[number, star]]          B=[ review,but, ..] Bx=a
### Identified: 
check out
hard time
number star
## the apartment across from mine belonged to a gang of hookers .
### Annotated:
belong to
## they told me that this is not under warranty and want to charge me $ number just to diagnose the problem !
### Annotated:
under warranty
## seems like all they care about is the money and getting home on time , no care for the customers at all !!!
### Annotated:
on time
at all
TransitionType.MERGES=[on, time]                B=[ ,,NO, ..] Bx=home
TransitionType.MARK_AS_OTHS=[[on, time]]              B=[ ,,NO, ..] Bx=home
TransitionType.MERGES=[AT, ALL]                 B=[ punc,] Bx=customer
TransitionType.MARK_AS_OTHS=[[AT, ALL]]               B=[ punc,] Bx=customer
### Identified: 
on time
at all
## while there was n't too much available for their age ( ball pit , bouncy area and a little padded pyramid to climb on ) , we went right when they opened at number am on a winter weekday and ended up being the only ones there , so we were given a little more liberty than we would have if others had been there .
### Annotated:
for age
ball pit
end up
give liberty
TransitionType.MERGES=[a, little]               B=[ padded,pyramid, ..] Bx=and
TransitionType.MARK_AS_OTHS=[[a, little]]             B=[ padded,pyramid, ..] Bx=and
TransitionType.MERGES=[winter, weekday]         B=[ and,ended, ..] Bx=a
TransitionType.MERGES=[[winter, weekday]and]    B=[ ended,up, ..] Bx=a
TransitionType.MERGES=[[[winter, weekday]and]ended] B=[ up,being, ..] Bx=a
TransitionType.MERGES=[[[[winter, weekday]and]ended]up] B=[ being,the, ..] Bx=a
TransitionType.MERGES=[[[[[winter, weekday]and]ended]up]being] B=[ the,only, ..] Bx=a
TransitionType.MERGES=[[[[[[winter, weekday]and]ended]up]being]the] B=[ only,ones, ..] Bx=a
TransitionType.MERGES=[[[[[[[winter, weekday]and]ended]up]being]the]only] B=[ ones,there, ..] Bx=a
TransitionType.MERGES=[[[[[[[[winter, weekday]and]ended]up]being]the]only]ones] B=[ there,,, ..] Bx=a
TransitionType.MERGES=[[[[[[[[[winter, weekday]and]ended]up]being]the]only]ones]a, little] B=[ more,liberty, ..] Bx=give
TransitionType.MARK_AS_OTHS=[[[[[[[[[winter, weekday]and]ended]up]being]the]only]ones][a, little]] B=[ more,liberty, ..] Bx=give
### Identified: 
a little
a little
## we were standing in the store for number minutes to simply pick up an order .
### Annotated:
pick up
TransitionType.MERGES=[pick, up]                B=[ an,order, ..] Bx=simply
TransitionType.MARK_AS_OTHS=[[pick, up]]              B=[ an,order, ..] Bx=simply
### Identified: 
pick up
## tried crust on broad on number occasions .
### Annotated:
crust on broad
## it is the real thing - i have been practicing pilates for over number years and would not go anywhere else .
### Annotated:
the real thing
## dr. obina told me that his office closed at noon and that i should call him on monday .
### Annotated:
dr obina
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## i had been a patient of dr. olbina for number years and had spent thousands of dollars on crowns etc .
### Annotated:
dr olbina
TransitionType.MERGES=[Dr, Olbina]              B=[ for,number, ..] Bx=of
TransitionType.MERGES=[[Dr, Olbina]for]         B=[ number,years, ..] Bx=of
TransitionType.MERGES=[[[Dr, Olbina]for]number] B=[ years,and, ..] Bx=of
TransitionType.MERGES=[[[[Dr, Olbina]for]number]years] B=[ and,had, ..] Bx=of
TransitionType.MERGES=[[[[[Dr, Olbina]for]number]years]and] B=[ had,spent, ..] Bx=of
TransitionType.MERGES=[[[[[[Dr, Olbina]for]number]years]and]had] B=[ spent,thousands, ..] Bx=of
TransitionType.MERGES=[[[[[[[Dr, Olbina]for]number]years]and]had]spent] B=[ thousands,of, ..] Bx=of
TransitionType.MERGES=[[[[[[[[Dr, Olbina]for]number]years]and]had]spent]thousands] B=[ of,dollars, ..] Bx=of
TransitionType.MERGES=[[[[[[[[[Dr, Olbina]for]number]years]and]had]spent]thousands]of] B=[ dollars,on, ..] Bx=of
TransitionType.MERGES=[[[[[[[[[[Dr, Olbina]for]number]years]and]had]spent]thousands]of]dollars] B=[ on,crowns, ..] Bx=of
TransitionType.MERGES=[[[[[[[[[[[Dr, Olbina]for]number]years]and]had]spent]thousands]of]dollars]on] B=[ crowns,etc, ..] Bx=of
TransitionType.MERGES=[[[[[[[[[[[[Dr, Olbina]for]number]years]and]had]spent]thousands]of]dollars]on]crowns] B=[ etc,punc,] Bx=of
## this can tend to be a stressful experience in itself let alone adding crossing boarders for the first time .
### Annotated:
in itself
let alone
TransitionType.MERGES=[let, alone]              B=[ adding,crossing, ..] Bx=itself
TransitionType.MARK_AS_OTHS=[[let, alone]]            B=[ adding,crossing, ..] Bx=itself
### Identified: 
let alone
## i have been going to warner family for a number of years and would highly recommend it to anyone .
### Annotated:
warner family
a number
TransitionType.MERGES=[Warner, Family]          B=[ for,a, ..] Bx=to
TransitionType.MERGES=[[Warner, Family]for]     B=[ a,number, ..] Bx=to
TransitionType.MERGES=[[[Warner, Family]for]a]  B=[ number,of, ..] Bx=to
TransitionType.MERGES=[[[[Warner, Family]for]a]number] B=[ of,years, ..] Bx=to
TransitionType.MERGES=[[[[[Warner, Family]for]a]number]of] B=[ years,and, ..] Bx=to
TransitionType.MERGES=[[[[[[Warner, Family]for]a]number]of]years] B=[ and,would, ..] Bx=to
TransitionType.MERGES=[[[[[[[Warner, Family]for]a]number]of]years]and] B=[ would,highly, ..] Bx=to
TransitionType.MERGES=[[[[[[[[Warner, Family]for]a]number]of]years]and]would] B=[ highly,recommend, ..] Bx=to
TransitionType.MERGES=[[[[[[[[[Warner, Family]for]a]number]of]years]and]would]highly] B=[ recommend,it, ..] Bx=to
TransitionType.MERGES=[[[[[[[[[[Warner, Family]for]a]number]of]years]and]would]highly]recommend] B=[ it,to, ..] Bx=to
TransitionType.MERGES=[[[[[[[[[[[Warner, Family]for]a]number]of]years]and]would]highly]recommend]it] B=[ to,anyone, ..] Bx=to
TransitionType.MERGES=[[[[[[[[[[[[Warner, Family]for]a]number]of]years]and]would]highly]recommend]it]to] B=[ anyone,punc,] Bx=to
## cathy ****** five stars for lake forest tots .
### Annotated:
five star
lake forest tots
TransitionType.MERGES=[Five, Stars]             B=[ for,Lake, ..] Bx=punc
TransitionType.MERGES=[[Five, Stars]for]        B=[ Lake,Forest, ..] Bx=punc
TransitionType.MERGES=[[[Five, Stars]for]Lake]  B=[ Forest,Tots, ..] Bx=punc
TransitionType.MERGES=[[[[Five, Stars]for]Lake]Forest] B=[ Tots,punc,] Bx=punc
TransitionType.MERGES=[[[[[Five, Stars]for]Lake]Forest]Tots] B=[ punc,] Bx=punc
TransitionType.MERGES=[[[[[[Five, Stars]for]Lake]Forest]Tots]punc] B=[ ] Bx=punc
## i needed a part for my appliance , the cost was very high so i said never mind , paid the fee and called a local business for a second quote .
### Annotated:
never mind
TransitionType.MERGES=[local, business]         B=[ for,a, ..] Bx=a
TransitionType.MERGES=[[local, business]for]    B=[ a,second, ..] Bx=a
## very disappointed in kitchen aid as well , i thought that they pre-screened their vendors for price and quality of work , obviously they do not !
### Annotated:
disappointed in
kitchen aid
as well
TransitionType.MERGES=[Kitchen, Aid]            B=[ as,well, ..] Bx=in
TransitionType.MERGES=[[Kitchen, Aid]as]        B=[ well,,, ..] Bx=in
TransitionType.MERGES=[[[Kitchen, Aid]as]well]  B=[ ,,I, ..] Bx=in
## i congratulated this establishment for doing the research on making nyc pizza because these scots fcking nailed it .
### Annotated:
nyc pizza
nail it
TransitionType.MERGES=[doing, research]         B=[ on,making, ..] Bx=the
TransitionType.MARK_AS_OTHS=[[doing, research]]       B=[ on,making, ..] Bx=the
### Identified: 
do research
## it was a little to high dollar for me
### Annotated:
a little
high dollar
TransitionType.MERGES=[a, little]               B=[ to,high, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[a, little]]             B=[ to,high, ..] Bx=be
### Identified: 
a little
## anyone else find it a little suspicious that there are not only number reviews for this dentist ( a huge number compared to the others in the area ) , but that they all have the same unique grammar structure ?
### Annotated:
compare to
grammar structure
TransitionType.MERGES=[a, little]               B=[ suspicious,that, ..] Bx=it
TransitionType.MARK_AS_OTHS=[[a, little]]             B=[ suspicious,that, ..] Bx=it
TransitionType.MERGES=[compared, to]            B=[ the,others, ..] Bx=number
TransitionType.MARK_AS_OTHS=[[compared, to]]          B=[ the,others, ..] Bx=number
### Identified: 
a little
compare to
## number p for tap water !
### Annotated:
tap water
TransitionType.MERGES=[tap, water]              B=[ punc,] Bx=for
TransitionType.MARK_AS_OTHS=[[tap, water]]            B=[ punc,] Bx=for
### Identified: 
tap water
## i ca nt speak for them but any tests or appointments they recommend are probably in the best interests of us ( the patient ) and you have the ability to decline anything that they suggest to you .
### Annotated:
i ca nt speak for
in the best interest
## i personally have had wonderful service and if you re truely looking for a family practice ... warner family is the place for you .
### Annotated:
family practice
warner family
TransitionType.MERGES=[Warner, Family]          B=[ is,the, ..] Bx=punc
TransitionType.MERGES=[[Warner, Family]is]      B=[ the,place, ..] Bx=punc
TransitionType.MERGES=[[[Warner, Family]is]the] B=[ place,for, ..] Bx=punc
TransitionType.MERGES=[[[[Warner, Family]is]the]place] B=[ for,you, ..] Bx=punc
TransitionType.MERGES=[[[[[Warner, Family]is]the]place]for] B=[ you,punc,] Bx=punc
TransitionType.MERGES=[[[[[[Warner, Family]is]the]place]for]you] B=[ punc,] Bx=punc
TransitionType.MERGES=[[[[[[[Warner, Family]is]the]place]for]you]punc] B=[ ] Bx=punc
## she asked for the dinner combo and they gave her two dinner plates instead .
### Annotated:
dinner plate
TransitionType.MERGES=[gave, dinner]            B=[ plates,instead, ..] Bx=two
TransitionType.MERGES=[[gave, dinner]plates]    B=[ instead,punc,] Bx=two
TransitionType.MERGES=[[[gave, dinner]plates]instead] B=[ punc,] Bx=two
TransitionType.MERGES=[[[[gave, dinner]plates]instead]punc] B=[ ] Bx=two
## you have to bring in your own models and they have to pay for you to use them if you do nt then you can graduate !
### Annotated:
have to
bring in
have to
TransitionType.MERGES=[have, to]                B=[ bring,in, ..] Bx=you
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ bring,in, ..] Bx=you
TransitionType.MERGES=[have, to]                B=[ pay,for, ..] Bx=they
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ pay,for, ..] Bx=they
### Identified: 
have to
have to
## the staff will not even answer the phone for take out .
### Annotated:
take out
TransitionType.MERGES=[take, out]               B=[ punc,] Bx=for
TransitionType.MARK_AS_OTHS=[[take, out]]             B=[ punc,] Bx=for
### Identified: 
take out
## and the salsa , be sure to ask for a jar and have plenty of chips around , you will need them .....
### Annotated:
be sure to
## parking spaces are just big enough for a mini cooper .
### Annotated:
parking space
mini cooper
TransitionType.MERGES=[Mini, Cooper]            B=[ punc,] Bx=a
TransitionType.MERGES=[[Mini, Cooper]punc]      B=[ ] Bx=a
## thank you again for great customer service !
### Annotated:
thank you
customer service
TransitionType.MERGE
TransitionType.MARK_AS_OTH
TransitionType.MERGES=[customer, service]       B=[ punc,] Bx=great
TransitionType.MARK_AS_OTHS=[[customer, service]]     B=[ punc,] Bx=great
### Identified: 
thank you
customer service
## nothing too much trouble for ian , thanks for a great stay .
### Annotated:
too much trouble
## i work for a large retail company recently expanding our operations into canada and had to travel to ensure all of our computer network equipment was installed properly and on time .
### Annotated:
have to
computer network
on time
TransitionType.MERGES=[had, to]                 B=[ travel,to, ..] Bx=and
TransitionType.MARK_AS_OTHS=[[had, to]]               B=[ travel,to, ..] Bx=and
TransitionType.MERGES=[on, time]                B=[ punc,] Bx=and
TransitionType.MARK_AS_OTHS=[[on, time]]              B=[ punc,] Bx=and
### Identified: 
have to
on time
## the other guy was pulled over one day and a cop saw suspicious papers with names and social security numbers on it .
### Annotated:
pull over
social security numbers
TransitionType.MERGES=[a, bit]                  B=[ surprised,by, ..] Bx=m
TransitionType.MARK_AS_OTHS=[[a, bit]]                B=[ surprised,by, ..] Bx=m
### Identified: 
a bit
TransitionType.MERGES=[offered, to]             B=[ help,me, ..] Bx=they
TransitionType.MERGES=[[offered, to]help]       B=[ me,again, ..] Bx=they
TransitionType.MERGES=[[[offered, to]help]me]   B=[ again,punc,] Bx=they
TransitionType.MERGES=[[[[offered, to]help]me]again] B=[ punc,] Bx=they
TransitionType.MERGES=[[[[[offered, to]help]me]again]punc] B=[ ] Bx=they
## we had to throw out about number percent of our meals because the food tasted so horrible .
### Annotated:
have to
throw out
TransitionType.MERGES=[had, to]                 B=[ throw,out, ..] Bx=we
TransitionType.MARK_AS_OTHS=[[had, to]]               B=[ throw,out, ..] Bx=we
### Identified: 
have to
## this place is identical to the youngstown sports grille , so i imagine they are owned / operated by the same people .
### Annotated:
youngstown sports grille
TransitionType.MERGES=[Youngstown, Sports]      B=[ Grille,,, ..] Bx=the
TransitionType.MERGES=[[Youngstown, Sports]Grille] B=[ ,,so, ..] Bx=the
TransitionType.MERGES=[[[Youngstown, Sports]Grille],] B=[ so,I, ..] Bx=the
TransitionType.MERGES=[[[[Youngstown, Sports]Grille],]so] B=[ I,imagine, ..] Bx=the
TransitionType.MERGES=[[[[[Youngstown, Sports]Grille],]so]I] B=[ imagine,they, ..] Bx=the
TransitionType.MERGES=[[[[[[Youngstown, Sports]Grille],]so]I]imagine] B=[ they,are, ..] Bx=the
TransitionType.MERGES=[[[[[[[Youngstown, Sports]Grille],]so]I]imagine]they] B=[ are,owned, ..] Bx=the
TransitionType.MERGES=[[[[[[[[Youngstown, Sports]Grille],]so]I]imagine]they]are] B=[ owned,punc, ..] Bx=the
TransitionType.MERGES=[[[[[[[[[Youngstown, Sports]Grille],]so]I]imagine]they]are]owned] B=[ punc,operated, ..] Bx=the
## definitely not going to purchase a car from here .
### Annotated:
go to
TransitionType.MERGES=[going, to]               B=[ purchase,a, ..] Bx=not
TransitionType.MARK_AS_OTHS=[[going, to]]             B=[ purchase,a, ..] Bx=not
### Identified: 
go to
## we order take out from here all the time and we are never disappointed .
### Annotated:
take out
all the time
TransitionType.MERGES=[take, out]               B=[ from,here, ..] Bx=order
TransitionType.MARK_AS_OTHS=[[take, out]]             B=[ from,here, ..] Bx=order
TransitionType.MERGES=[all, the]                B=[ time,and, ..] Bx=here
TransitionType.MERGES=[[all, the]time]          B=[ and,we, ..] Bx=here
TransitionType.MARK_AS_OTHS=[[[all, the]time]]        B=[ and,we, ..] Bx=here
### Identified: 
take out
all the time
## these guys took customer service number from a neanderthal .
### Annotated:
customer service
TransitionType.MERGES=[Customer, Service]       B=[ number,from, ..] Bx=take
TransitionType.MARK_AS_OTHS=[[Customer, Service]]     B=[ number,from, ..] Bx=take
### Identified: 
customer service
## and from a place that specializes in high quality meat , too .
### Annotated:
specialize in
TransitionType.MERGES=[specializes, in]         B=[ high,quality, ..] Bx=that
TransitionType.MARK_AS_OTHS=[[specializes, in]]       B=[ high,quality, ..] Bx=that
### Identified: 
specialize in
## yes the parking can be a challenge but being from nj i am no stranger to tight corners .
### Annotated:
be no stranger to
tight corner
## not to mention that the wait staff was about as pleasant as dealing with an angry bull .
### Annotated:
not to mention
wait staff
deal with
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MARK_AS_OTH
TransitionType.MERGES=[wait, staff]             B=[ was,about, ..] Bx=the
TransitionType.MARK_AS_OTHS=[[wait, staff]]           B=[ was,about, ..] Bx=the
TransitionType.MERGES=[dealing, with]           B=[ an,angry, ..] Bx=as
TransitionType.MARK_AS_OTHS=[[dealing, with]]         B=[ an,angry, ..] Bx=as
### Identified: 
not to mention
wait staff
deal with
## this is by far the worst chinese food i have ever had .
### Annotated:
by far
TransitionType.MERGES=[by, far]                 B=[ the,worst, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[by, far]]               B=[ the,worst, ..] Bx=be
### Identified: 
by far
## i do nt know how it is possible to make orange chicken , sesame chicken and kung pao chicken as well as cheese puffs taste that bad but china delight accomplished that .
### Annotated:
orange chicken
kung pao chicken
as well as
china delight
TransitionType.MERGES=[as, well]                B=[ as,cheese, ..] Bx=chicken
TransitionType.MERGES=[[as, well]as]            B=[ cheese,puffs, ..] Bx=chicken
TransitionType.MARK_AS_OTHS=[[[as, well]as]]          B=[ cheese,puffs, ..] Bx=chicken
TransitionType.MERGES=[China, Delight]          B=[ accomplished,that, ..] Bx=but
TransitionType.MERGES=[[China, Delight]accomplished] B=[ that,punc,] Bx=but
TransitionType.MERGES=[[[China, Delight]accomplished]that] B=[ punc,] Bx=but
TransitionType.MERGES=[[[[China, Delight]accomplished]that]punc] B=[ ] Bx=but
### Identified: 
as well as
TransitionType.MERGES=[the, Hilton]             B=[ punc,which, ..] Bx=over
TransitionType.MARK_AS_OTHS=[[the, Hilton]]           B=[ punc,which, ..] Bx=over
### Identified: 
the hilton
## such a convenient location as well with coffee shop and bradley food and beverage right around corner .
### Annotated:
as well
bradley food and beverage
TransitionType.MERGES=[as, well]                B=[ with,coffee, ..] Bx=location
TransitionType.MARK_AS_OTHS=[[as, well]]              B=[ with,coffee, ..] Bx=location
TransitionType.MERGES=[bradley, food]           B=[ and,beverage, ..] Bx=and
TransitionType.MERGES=[[bradley, food]and]      B=[ beverage,right, ..] Bx=and
TransitionType.MERGES=[[[bradley, food]and]beverage] B=[ right,around, ..] Bx=and
TransitionType.MERGES=[[[[bradley, food]and]beverage]right] B=[ around,corner, ..] Bx=and
TransitionType.MERGES=[[[[[bradley, food]and]beverage]right]around] B=[ corner,punc,] Bx=and
TransitionType.MERGES=[[[[[[bradley, food]and]beverage]right]around]corner] B=[ punc,] Bx=and
TransitionType.MERGES=[[[[[[[bradley, food]and]beverage]right]around]corner]punc] B=[ ] Bx=and
### Identified: 
as well
## the employees make you feel very comfortable and are very helpful , whether you are very knowledgeable or do n't know anything at all about wine .
### Annotated:
at all
TransitionType.MERGES=[make, feel]              B=[ very,comfortable, ..] Bx=you
TransitionType.MARK_AS_OTHS=[[make, feel]]            B=[ very,comfortable, ..] Bx=you
TransitionType.MERGES=[at, all]                 B=[ about,wine, ..] Bx=anything
TransitionType.MARK_AS_OTHS=[[at, all]]               B=[ about,wine, ..] Bx=anything
### Identified: 
make feel
at all
## do n't even get me started on how expensive it is to drink there .
### Annotated:
do nt even get me start
## i completely enjoyed my whole check in experience and was impressed with the friendliness and professionalism of the staff as well as the accommodations themselves .
### Annotated:
check in
as well as
TransitionType.MERGES=[check, in]               B=[ experience,and, ..] Bx=whole
TransitionType.MARK_AS_OTHS=[[check, in]]             B=[ experience,and, ..] Bx=whole
TransitionType.MERGES=[as, well]                B=[ as,the, ..] Bx=staff
TransitionType.MERGES=[[as, well]as]            B=[ the,accommodations, ..] Bx=staff
TransitionType.MARK_AS_OTHS=[[[as, well]as]]          B=[ the,accommodations, ..] Bx=staff
### Identified: 
check in
as well as
## the second vendor charged $ number ( less than half of what a&e charges ) to come and applied that to the price of the repair service ( which a&e does not ) .
### Annotated:
less than
TransitionType.MERGES=[less, than]              B=[ half,of, ..] Bx=punc
TransitionType.MARK_AS_OTHS=[[less, than]]            B=[ half,of, ..] Bx=punc
### Identified: 
less than
## they also got my friend s order mixed up and wanted to charger her $ number more than what she had wanted .
### Annotated:
mix up
TransitionType.MERGES=[mixed, up]               B=[ and,wanted, ..] Bx=order
TransitionType.MERGES=[[mixed, up]and]          B=[ wanted,to, ..] Bx=order
TransitionType.MERGES=[[[mixed, up]and]wanted]  B=[ to,charger, ..] Bx=order
TransitionType.MERGES=[[[[mixed, up]and]wanted]to] B=[ charger,her, ..] Bx=order
TransitionType.MERGES=[[[[[mixed, up]and]wanted]to]charger] B=[ her,punc, ..] Bx=order
TransitionType.MERGES=[[[[[[mixed, up]and]wanted]to]charger]more, than] B=[ what,she, ..] Bx=number
TransitionType.MARK_AS_OTHS=[[[[[[mixed, up]and]wanted]to]charger][more, than]] B=[ what,she, ..] Bx=number
### Identified: 
more than
## they have a great selection of wine from all over the world with all different prices .
### Annotated:
all over
TransitionType.MERGES=[all, over]               B=[ the,world, ..] Bx=from
TransitionType.MARK_AS_OTHS=[[all, over]]             B=[ the,world, ..] Bx=from
### Identified: 
all over
## instead of rescheduling they chose to waste my time instead .
### Annotated:
instead of
waste time
TransitionType.MERGE
TransitionType.MARK_AS_OTH
TransitionType.MERGES=[waste, time]             B=[ instead,punc,] Bx=my
TransitionType.MARK_AS_OTHS=[[waste, time]]           B=[ instead,punc,] Bx=my
### Identified: 
instead of
waste time
## they were abrasive and rude - when they were the ones who messed everything up .
### Annotated:
mess up
TransitionType.MERGES=[messed, everything]      B=[ up,punc,] Bx=who
TransitionType.MERGES=[[messed, everything]up]  B=[ punc,] Bx=who
TransitionType.MERGES=[[[messed, everything]up]punc] B=[ ] Bx=who
## the only thing that was edible was the steamed rice and the vegetable lo mein was barely tolerable .
### Annotated:
lo mein
## lucky panda in willis is a billion times better in service and quality of the meal .
### Annotated:
lucky panda
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## i have no idea how china delight won number number chinese restaurant in montgomery - there needs to be a recount on that vote .
### Annotated:
china delight
number number
TransitionType.MERGES=[China, Delight]          B=[ won,number, ..] Bx=how
TransitionType.MERGES=[[China, Delight]won]     B=[ number,number, ..] Bx=how
TransitionType.MERGES=[[[China, Delight]won]number] B=[ number,Chinese, ..] Bx=how
TransitionType.MERGES=[[[[China, Delight]won]number]number] B=[ Chinese,restaurant, ..] Bx=how
TransitionType.MERGES=[[[[[China, Delight]won]number]number]Chinese] B=[ restaurant,in, ..] Bx=how
TransitionType.MERGES=[[[[[[China, Delight]won]number]number]Chinese]restaurant] B=[ in,Montgomery, ..] Bx=how
TransitionType.MERGES=[[[[[[[China, Delight]won]number]number]Chinese]restaurant]in] B=[ Montgomery,-, ..] Bx=how
TransitionType.MERGES=[[[[[[[[China, Delight]won]number]number]Chinese]restaurant]in]Montgomery] B=[ -,There, ..] Bx=how
TransitionType.MERGES=[[[[[[[[[China, Delight]won]number]number]Chinese]restaurant]in]Montgomery]-] B=[ There,needs, ..] Bx=how
## college is a joke and the salon is a joke !
### Annotated:
be a joke
be a joke
## went to the school here over priced !!!!!!
### Annotated:
over priced
TransitionType.MERGES=[OVER, PRICED]            B=[ punc,] Bx=here
TransitionType.MARK_AS_OTHS=[[OVER, PRICED]]          B=[ punc,] Bx=here
### Identified: 
over priced
TransitionType.MERGES=[under, educated]         B=[ punc,] Bx=be
TransitionType.MERGES=[[under, educated]punc]   B=[ ] Bx=be
## over priced for students to learn !
### Annotated:
over priced
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
over priced
## beware of the nail program you are not taught to use a nail drill at all you learn the old fashioned way of doing nails you will not be able to do well in a salon !!!
### Annotated:
nail drill
at all
old fashioned
TransitionType.MERGES=[nail, drill]             B=[ AT,ALL, ..] Bx=a
TransitionType.MERGES=[[nail, drill]AT]         B=[ ALL,you, ..] Bx=a
TransitionType.MERGES=[[[nail, drill]AT]ALL]    B=[ you,learn, ..] Bx=a
TransitionType.MERGES=[[[[nail, drill]AT]ALL]you] B=[ learn,the, ..] Bx=a
TransitionType.MERGES=[[[[[nail, drill]AT]ALL]you]learn] B=[ the,old, ..] Bx=a
TransitionType.MERGES=[[[[[[nail, drill]AT]ALL]you]learn]the] B=[ old,fashioned, ..] Bx=a
TransitionType.MERGES=[[[[[[[nail, drill]AT]ALL]you]learn]the]old] B=[ fashioned,way, ..] Bx=a
TransitionType.MERGES=[[[[[[[[nail, drill]AT]ALL]you]learn]the]old]fashioned] B=[ way,of, ..] Bx=a
TransitionType.MERGES=[[[[[[[[[nail, drill]AT]ALL]you]learn]the]old]fashioned]way] B=[ of,doing, ..] Bx=a
TransitionType.MERGES=[[[[[[[[[[nail, drill]AT]ALL]you]learn]the]old]fashioned]way]of] B=[ doing,nails, ..] Bx=a
TransitionType.MERGES=[[[[[[[[[[[nail, drill]AT]ALL]you]learn]the]old]fashioned]way]of]doing] B=[ nails,you, ..] Bx=a
TransitionType.MERGES=[[[[[[[[[[[[nail, drill]AT]ALL]you]learn]the]old]fashioned]way]of]doing]nails] B=[ you,will, ..] Bx=a
## the food is mediocre at best , and largely overpriced given the portion size and quality .
### Annotated:
at best
TransitionType.MERGES=[at, best]                B=[ ,,and, ..] Bx=mediocre
TransitionType.MARK_AS_OTHS=[[at, best]]              B=[ ,,and, ..] Bx=mediocre
TransitionType.MERGES=[given, the]              B=[ portion,size, ..] Bx=overpriced
TransitionType.MERGES=[[given, the]portion]     B=[ size,and, ..] Bx=overpriced
TransitionType.MERGES=[[[given, the]portion]size] B=[ and,quality, ..] Bx=overpriced
TransitionType.MERGES=[[[[given, the]portion]size]and] B=[ quality,punc,] Bx=overpriced
TransitionType.MERGES=[[[[[given, the]portion]size]and]quality] B=[ punc,] Bx=overpriced
TransitionType.MERGES=[[[[[[given, the]portion]size]and]quality]punc] B=[ ] Bx=overpriced
### Identified: 
at best
## i have ate here number times since they first opened , and the service has been poor each time , the staff always comes across as somewhat rude and slow .
### Annotated:
come across
TransitionType.MERGES=[comes, across]           B=[ as,somewhat, ..] Bx=always
TransitionType.MARK_AS_OTHS=[[comes, across]]         B=[ as,somewhat, ..] Bx=always
### Identified: 
come across
## i came to la crosse to go to college , and my mom would send me birthday flowers though here .
### Annotated:
la crosse
TransitionType.MERGES=[La, Crosse]              B=[ to,go, ..] Bx=to
TransitionType.MERGES=[[La, Crosse]to]          B=[ go,to, ..] Bx=to
TransitionType.MERGES=[[[La, Crosse]to]go]      B=[ to,college, ..] Bx=to
TransitionType.MERGES=[[[[La, Crosse]to]go]to]  B=[ college,,, ..] Bx=to
TransitionType.MERGES=[[[[[La, Crosse]to]go]to]college] B=[ ,,and, ..] Bx=to
TransitionType.MERGES=[[[[[[La, Crosse]to]go]to]college]birthday, flowers] B=[ though,here, ..] Bx=me
TransitionType.MERGES=[[[[[[La, Crosse]to]go]to]college][birthday, flowers]though] B=[ here,punc,] Bx=me
TransitionType.MERGES=[[[[[[La, Crosse]to]go]to]college][[birthday, flowers]though]here] B=[ punc,] Bx=me
TransitionType.MERGES=[[[[[[La, Crosse]to]go]to]college][[[birthday, flowers]though]here]punc] B=[ ] Bx=me
TransitionType.MERGES=[[[[[[La, Crosse]to]go]to]college][[[[birthday, flowers]though]here]punc]] B=[ ] Bx=me
## hands down , best place in the area !
### Annotated:
hands down
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
hands down
## do n't go to amelia gentle dentistry .
### Annotated:
amelia gentle dentistry
TransitionType.MERGES=[Amelia, Gentle]          B=[ Dentistry,punc,] Bx=to
TransitionType.MERGES=[[Amelia, Gentle]Dentistry] B=[ punc,] Bx=to
TransitionType.MERGES=[[[Amelia, Gentle]Dentistry]punc] B=[ ] Bx=to
## how a pizza place should be !
### Annotated:
pizza place
## i have had all three of my children attend lake forest tots .
### Annotated:
lake forest tots
TransitionType.MERGES=[Lake, Forest]            B=[ Tots,punc,] Bx=attend
TransitionType.MERGES=[[Lake, Forest]Tots]      B=[ punc,] Bx=attend
TransitionType.MERGES=[[[Lake, Forest]Tots]punc] B=[ ] Bx=attend
## good job , lake forest tots !
### Annotated:
good job
lake forest tots
TransitionType.MERGES=[Lake, Forest]            B=[ Tots,punc,] Bx=,
TransitionType.MERGES=[[Lake, Forest]Tots]      B=[ punc,] Bx=,
TransitionType.MERGES=[[[Lake, Forest]Tots]punc] B=[ ] Bx=,
## a&e came out , charged $ number fee just to walk in the door .
### Annotated:
come out
TransitionType.MERGES=[came, out]               B=[ ,,charged, ..] Bx=ae
TransitionType.MARK_AS_OTHS=[[came, out]]             B=[ ,,charged, ..] Bx=ae
### Identified: 
come out
## deb watson is the contact person and she and the rest of the staff were great !!!
### Annotated:
deb watson
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## we just got our sunroom built by patio world and can say that i 'm extremely happy with the whole thing .
### Annotated:
patio world
TransitionType.MERGES=[Patio, World]            B=[ and,can, ..] Bx=by
TransitionType.MERGES=[[Patio, World]and]       B=[ can,say, ..] Bx=by
TransitionType.MERGES=[[[Patio, World]and]can]  B=[ say,that, ..] Bx=by
TransitionType.MERGES=[[[[Patio, World]and]can]say] B=[ that,I, ..] Bx=by
TransitionType.MERGES=[[[[[Patio, World]and]can]say]that] B=[ I,m, ..] Bx=by
TransitionType.MERGES=[have, to]                B=[ say,punc,] Bx=bad
TransitionType.MERGES=[[have, to]say]           B=[ punc,] Bx=bad
TransitionType.MARK_AS_OTHS=[[[have, to]say]]         B=[ punc,] Bx=bad
### Identified: 
have to say
## very glad that we went with them .
### Annotated:
go with
## i just had the best experience at this kal tire location .
### Annotated:
kal tire
TransitionType.MERGES=[had, experience]         B=[ at,this, ..] Bx=best
TransitionType.MARK_AS_OTHS=[[had, experience]]       B=[ at,this, ..] Bx=best
TransitionType.MERGES=[Kal, Tire]               B=[ location,punc,] Bx=this
TransitionType.MERGES=[[Kal, Tire]location]     B=[ punc,] Bx=this
TransitionType.MERGES=[[[Kal, Tire]location]punc] B=[ ] Bx=this
### Identified: 
have experience
## rip off !
### Annotated:
rip off
TransitionType.MERGE
TransitionType.MERGE
## the front desk staff was very pleasant and efficient .
### Annotated:
front desk
TransitionType.MERGES=[front, desk]             B=[ staff,was, ..] Bx=the
TransitionType.MARK_AS_OTHS=[[front, desk]]           B=[ staff,was, ..] Bx=the
### Identified: 
front desk
TransitionType.MERGES=[brought, car]            B=[ punc,punc,] Bx=the
TransitionType.MERGES=[[brought, car]punc]      B=[ punc,] Bx=the
TransitionType.MERGES=[[[brought, car]punc]punc] B=[ ] Bx=the
## well then i went on a trip to glasgow and was walking around .
### Annotated:
go on a trip
TransitionType.MERGES=[salad, cream]            B=[ ,,not, ..] Bx=and
TransitionType.MERGES=[[salad, cream],]         B=[ not,mayonnaise, ..] Bx=and
TransitionType.MERGES=[[[salad, cream],]not]    B=[ mayonnaise,,, ..] Bx=and
TransitionType.MERGES=[[[[salad, cream],]not]mayonnaise] B=[ ,,on, ..] Bx=and
TransitionType.MERGES=[[[[[salad, cream],]not]mayonnaise],] B=[ on,the, ..] Bx=and
TransitionType.MERGES=[[[[[[salad, cream],]not]mayonnaise],]on] B=[ the,coleslaw, ..] Bx=and
TransitionType.MERGES=[[[[[[[salad, cream],]not]mayonnaise],]on]the] B=[ coleslaw,punc,] Bx=and
TransitionType.MERGES=[[[[[[[[salad, cream],]not]mayonnaise],]on]the]coleslaw] B=[ punc,] Bx=and
TransitionType.MERGES=[[[[[[[[[salad, cream],]not]mayonnaise],]on]the]coleslaw]punc] B=[ ] Bx=and
## it can be a little on the spicy side but just ask them exactly what you want and they are very helpful .
### Annotated:
on the side
TransitionType.MERGES=[a, little]               B=[ on,the, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[a, little]]             B=[ on,the, ..] Bx=be
### Identified: 
a little
## after a good few minutes , he asked : " what do you want ? "
### Annotated:
a good few
## going back after graduating you r told you get a discount on services nope you do nt .
### Annotated:
go back
TransitionType.MERGES=[just, about]             B=[ the,money, ..] Bx=give
TransitionType.MARK_AS_OTHS=[[just, about]]           B=[ the,money, ..] Bx=give
### Identified: 
just about
## quality has fallen over the years , but still the best go - to burger place on the east bay .
### Annotated:
over the years
go - to
east bay
TransitionType.MERGES=[go, -]                   B=[ to,burger, ..] Bx=best
TransitionType.MERGES=[[go, -]to]               B=[ burger,place, ..] Bx=best
TransitionType.MARK_AS_OTHS=[[[go, -]to]]             B=[ burger,place, ..] Bx=best
TransitionType.MERGES=[East, Bay]               B=[ punc,] Bx=the
TransitionType.MERGES=[[East, Bay]punc]         B=[ ] Bx=the
### Identified: 
go - to
## they sent over someone who said he knows nothing about curtains and could not show me fabric options or give an estimate .
### Annotated:
send over
TransitionType.MERGES=[sent, over]              B=[ someone,who, ..] Bx=they
TransitionType.MARK_AS_OTHS=[[sent, over]]            B=[ someone,who, ..] Bx=they
TransitionType.MERGES=[give, an]                B=[ estimate,punc,] Bx=or
TransitionType.MERGES=[[give, an]estimate]      B=[ punc,] Bx=or
TransitionType.MERGES=[[[give, an]estimate]punc] B=[ ] Bx=or
### Identified: 
send over
## i got yelled at , literally yelled at because i asked if i could pick up my car number - number minutes late .
### Annotated:
pick up
TransitionType.MERGES=[pick, up]                B=[ my,car, ..] Bx=could
TransitionType.MARK_AS_OTHS=[[pick, up]]              B=[ my,car, ..] Bx=could
### Identified: 
pick up
## tonight , i called several times with no answer ( btwn number and number pm ) and finally drove there to place my order in person .
### Annotated:
place order
in person
## there was not a customer to be found .
### Annotated:
not a to be find
## pure pilates !!
### Annotated:
pure pilate
## no customer service
### Annotated:
customer service
TransitionType.MERGES=[Customer, Service]       B=[ ] Bx=no
TransitionType.MARK_AS_OTHS=[[Customer, Service]]     B=[ ] Bx=no
### Identified: 
customer service
## employees seemed to be having a good time chatting and laughing with each other , while myself and other customers were completely ignored .
### Annotated:
have a time
TransitionType.MERGES=[good, time]              B=[ chatting,and, ..] Bx=a
TransitionType.MARK_AS_OTHS=[[good, time]]            B=[ chatting,and, ..] Bx=a
TransitionType.MERGES=[each, other]             B=[ ,,while, ..] Bx=with
TransitionType.MARK_AS_OTHS=[[each, other]]           B=[ ,,while, ..] Bx=with
### Identified: 
good time
each other
## another person in the store stood there with an item and repeatedly tried to get a sales person s attention .
### Annotated:
sales person
## it was n't until he gave up and walked out the door that someone asked can i help you .
### Annotated:
give up
TransitionType.MERGES=[gave, up]                B=[ and,walked, ..] Bx=he
TransitionType.MARK_AS_OTHS=[[gave, up]]              B=[ and,walked, ..] Bx=he
### Identified: 
give up
TransitionType.MERGES=[just, off]               B=[ the,river, ..] Bx=locate
TransitionType.MERGES=[[just, off]the]          B=[ river,road, ..] Bx=locate
TransitionType.MERGES=[[[just, off]the]river]   B=[ road,punc,] Bx=locate
TransitionType.MERGES=[[[[just, off]the]river]road] B=[ punc,] Bx=locate
TransitionType.MERGES=[[[[[just, off]the]river]road]punc] B=[ ] Bx=locate
## good sports bar .
### Annotated:
sport bar
## hyatt web site improved .
### Annotated:
web site
TransitionType.MERGES=[web, site]               B=[ improved,punc,] Bx=hyatt
TransitionType.MARK_AS_OTHS=[[web, site]]             B=[ improved,punc,] Bx=hyatt
### Identified: 
web site
## accurate check - out .
### Annotated:
check - out
## a +
### Annotated:
a punc
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
a punc
## excellent customer service and honest feedback .
### Annotated:
customer service
TransitionType.MERGES=[customer, service]       B=[ and,honest, ..] Bx=excellent
TransitionType.MARK_AS_OTHS=[[customer, service]]     B=[ and,honest, ..] Bx=excellent
### Identified: 
customer service
## i gave dr. rohatgi number stars because her assistant was very pleasant .
### Annotated:
dr rohatgi
number star
TransitionType.MERGES=[gave, Dr]                B=[ Rohatgi,number, ..] Bx=i
TransitionType.MERGES=[[gave, Dr]Rohatgi]       B=[ number,stars, ..] Bx=i
TransitionType.MERGES=[[[gave, Dr]Rohatgi]number] B=[ stars,because, ..] Bx=i
TransitionType.MERGES=[[[[gave, Dr]Rohatgi]number]stars] B=[ because,her, ..] Bx=i
TransitionType.MERGES=[[[[[gave, Dr]Rohatgi]number]stars]because] B=[ her,assistant, ..] Bx=i
## i moved into the tanglewood apartments in late number and it 's been a refreshing change .
### Annotated:
tanglewood apartments
TransitionType.MERGES=[Tanglewood, Apartments]  B=[ in,late, ..] Bx=the
TransitionType.MERGES=[[Tanglewood, Apartments]in] B=[ late,number, ..] Bx=the
TransitionType.MERGES=[[[Tanglewood, Apartments]in]late] B=[ number,and, ..] Bx=the
TransitionType.MERGES=[[[[Tanglewood, Apartments]in]late]number] B=[ and,it, ..] Bx=the
TransitionType.MERGES=[[[[[Tanglewood, Apartments]in]late]number]and] B=[ it,s, ..] Bx=the
TransitionType.MERGES=[[[[[[Tanglewood, Apartments]in]late]number]and]it] B=[ s,been, ..] Bx=the
TransitionType.MERGES=[[[[[[[Tanglewood, Apartments]in]late]number]and]it]s] B=[ been,a, ..] Bx=the
TransitionType.MERGES=[[[[[[[[Tanglewood, Apartments]in]late]number]and]it]s]been] B=[ a,refreshing, ..] Bx=the
## i used to live at meadowrun and that was a nightmare .
### Annotated:
use to
TransitionType.MERGES=[used, to]                B=[ live,at, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[used, to]]              B=[ live,at, ..] Bx=i
### Identified: 
use to
## old time grocery , best steaks i have ever had !
### Annotated:
old time
## sure enough he charged it to the credit card .
### Annotated:
sure enough
credit card
TransitionType.MERGES=[credit, card]            B=[ punc,] Bx=the
TransitionType.MARK_AS_OTHS=[[credit, card]]          B=[ punc,] Bx=the
### Identified: 
credit card
## ok i am a new yorker who has been going to school in oxford , england .
### Annotated:
new yorker
oxford , england
TransitionType.MERGES=[New, Yorker]             B=[ who,has, ..] Bx=a
TransitionType.MERGES=[[New, Yorker]who]        B=[ has,been, ..] Bx=a
TransitionType.MERGES=[[[New, Yorker]who]has]   B=[ been,going, ..] Bx=a
TransitionType.MERGES=[[[[New, Yorker]who]has]been] B=[ going,to, ..] Bx=a
TransitionType.MERGES=[[[[[New, Yorker]who]has]been]going] B=[ to,school, ..] Bx=a
TransitionType.MERGES=[[[[[[New, Yorker]who]has]been]going]to] B=[ school,in, ..] Bx=a
TransitionType.MERGES=[[[[[[[New, Yorker]who]has]been]going]to]school] B=[ in,Oxford, ..] Bx=a
TransitionType.MERGES=[[[[[[[[New, Yorker]who]has]been]going]to]school]in] B=[ Oxford,,, ..] Bx=a
TransitionType.MERGES=[[[[[[[[[New, Yorker]who]has]been]going]to]school]in]Oxford] B=[ ,,England, ..] Bx=a
## this is the worst sam s club i 've ever been to
### Annotated:
sam s club
be to
TransitionType.MERGES=[been, to]                B=[ ] Bx=ever
TransitionType.MARK_AS_OTHS=[[been, to]]              B=[ ] Bx=ever
### Identified: 
be to
## after my trees were cleaned up , they gave me a jar of salsa .
### Annotated:
clean up
TransitionType.MERGES=[cleaned, up]             B=[ ,,they, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[cleaned, up]]           B=[ ,,they, ..] Bx=be
TransitionType.MERGES=[gave, a]                 B=[ jar,of, ..] Bx=me
TransitionType.MERGES=[[gave, a]jar]            B=[ of,salsa, ..] Bx=me
TransitionType.MERGES=[[[gave, a]jar]of]        B=[ salsa,punc,] Bx=me
TransitionType.MERGES=[[[[gave, a]jar]of]salsa] B=[ punc,] Bx=me
TransitionType.MERGES=[[[[[gave, a]jar]of]salsa]punc] B=[ ] Bx=me
### Identified: 
clean up
## anna marie and govind are very sweet people , and the minute you steep into their school , the calm loving atmosphere takes over , and tension and worries stay outside in the street , whether or not you pick them up again after class is probably a question of practice .
### Annotated:
anna marie
take over
whether or not
pick up
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGES=[[[[[Anna, Marie]and]Govind]are]takes, over] B=[ ,,and, ..] Bx=atmosphere
TransitionType.MARK_AS_OTHS=[[[[[Anna, Marie]and]Govind]are][takes, over]] B=[ ,,and, ..] Bx=atmosphere
TransitionType.MERGES=[[[[[Anna, Marie]and]Govind]are]pick, up] B=[ again,after, ..] Bx=them
TransitionType.MARK_AS_OTHS=[[[[[Anna, Marie]and]Govind]are][pick, up]] B=[ again,after, ..] Bx=them
### Identified: 
take over
pick up
## i will be traveling in this area in the future and you can be assured that this experience will be helpful in my choice of hotels and novotel will be my first selection .
### Annotated:
can be assure
## i came to find out the person was the hotel owner also .
### Annotated:
find out
TransitionType.MERGES=[find, out]               B=[ the,person, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[find, out]]             B=[ the,person, ..] Bx=to
### Identified: 
find out
TransitionType.MERGES=[had, experience]         B=[ buying,from, ..] Bx=bad
TransitionType.MARK_AS_OTHS=[[had, experience]]       B=[ buying,from, ..] Bx=bad
### Identified: 
have experience
## i purchased a number - year old certified pre-owned bmw from this dealership .
### Annotated:
year old
TransitionType.MERGES=[number, -]               B=[ year,old, ..] Bx=a
TransitionType.MERGES=[[number, -]year]         B=[ old,certified, ..] Bx=a
TransitionType.MERGES=[[[number, -]year]old]    B=[ certified,preowned, ..] Bx=a
TransitionType.MERGES=[[[[number, -]year]old]certified] B=[ preowned,BMW, ..] Bx=a
TransitionType.MERGES=[[[[[number, -]year]old]certified]preowned] B=[ BMW,from, ..] Bx=a
TransitionType.MERGES=[[[[[[number, -]year]old]certified]preowned]BMW] B=[ from,this, ..] Bx=a
TransitionType.MERGES=[[[[[[[number, -]year]old]certified]preowned]BMW]from] B=[ this,dealership, ..] Bx=a
TransitionType.MERGES=[[[[[[[[number, -]year]old]certified]preowned]BMW]from]this] B=[ dealership,punc,] Bx=a
TransitionType.MERGES=[[[[[[[[[number, -]year]old]certified]preowned]BMW]from]this]dealership] B=[ punc,] Bx=a
TransitionType.MERGES=[[[[[[[[[[number, -]year]old]certified]preowned]BMW]from]this]dealership]punc] B=[ ] Bx=a
## from my first encounter at check in to my regrettable check out i found the staff and facility to exceed my expectation .
### Annotated:
check in
check out
TransitionType.MERGES=[check, in]               B=[ to,my, ..] Bx=at
TransitionType.MARK_AS_OTHS=[[check, in]]             B=[ to,my, ..] Bx=at
TransitionType.MERGES=[check, out]              B=[ I,found, ..] Bx=regrettable
TransitionType.MARK_AS_OTHS=[[check, out]]            B=[ I,found, ..] Bx=regrettable
### Identified: 
check in
check out
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
buyer beware
## $ number later my jaw dropped when the receptionist told me the total .
### Annotated:
jaw drop
TransitionType.MERGES=[do, a]                   B=[ good,job, ..] Bx=nt
TransitionType.MERGES=[[do, a]job]              B=[ and,they, ..] Bx=good
TransitionType.MARK_AS_OTHS=[[[do, a]job]]            B=[ and,they, ..] Bx=good
### Identified: 
do a job
## i 'm sure it s not every day that a funeral director sees the same family in such a short time .
### Annotated:
a short time
TransitionType.MERGES=[pleased, with]           B=[ the,tattoos, ..] Bx=very
TransitionType.MARK_AS_OTHS=[[pleased, with]]         B=[ the,tattoos, ..] Bx=very
### Identified: 
pleased with
## i would recommend this shop to anyone looking to get a tattoo .
### Annotated:
look to
TransitionType.MERGES=[get, tattoo]             B=[ punc,] Bx=a
TransitionType.MERGES=[[get, tattoo]punc]       B=[ ] Bx=a
## i have been going to the wildwood , nj for over number years for summer vacations and always call the madrid first .
### Annotated:
wildwood , nj
## i rated it number stars .
### Annotated:
number star
TransitionType.MERGES=[number, stars]           B=[ punc,] Bx=it
TransitionType.MARK_AS_OTHS=[[number, stars]]         B=[ punc,] Bx=it
### Identified: 
number star
## i am not saying it is a number star hotel .
### Annotated:
number star
TransitionType.MERGES=[number, star]            B=[ hotel,punc,] Bx=a
TransitionType.MARK_AS_OTHS=[[number, star]]          B=[ hotel,punc,] Bx=a
### Identified: 
number star
## it is the hospitality from tom and staff , that makes it feel like a number star hotel in the middle of the beach .
### Annotated:
number star
TransitionType.MERGES=[number, star]            B=[ hotel,in, ..] Bx=a
TransitionType.MARK_AS_OTHS=[[number, star]]          B=[ hotel,in, ..] Bx=a
### Identified: 
number star
## unfortunately , a family emergency required me to conquer this fear .
### Annotated:
family emergency
## she highly recommended him and described him as the " saintly instructor and simply the best instructor there is .... very calm , pleasant and very detailed in giving instructions " .
### Annotated:
give instructions
## i had to cancel my initial lesson number times and on the number attempt the management was quick enough to associate my cancellations with my fear and finally encouraged me into taking my initial lesson .
### Annotated:
have to
TransitionType.MERGES=[had, to]                 B=[ cancel,my, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[had, to]]               B=[ cancel,my, ..] Bx=i
### Identified: 
have to
## hopefully they spice things up or they wo nt be in business long .
### Annotated:
spice up
in business
TransitionType.MERGES=[in, business]            B=[ long,punc,] Bx=be
TransitionType.MARK_AS_OTHS=[[in, business]]          B=[ long,punc,] Bx=be
### Identified: 
in business
## i recommend la hacienda
### Annotated:
la hacienda
## extremely bad customer service
### Annotated:
customer service
TransitionType.MERGES=[customer, service]       B=[ ] Bx=bad
TransitionType.MARK_AS_OTHS=[[customer, service]]     B=[ ] Bx=bad
### Identified: 
customer service
## dr mcdonald is wonderful .
### Annotated:
dr mcdonald
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGES=[all, questions]          B=[ asked,and, ..] Bx=answer
TransitionType.MERGES=[[all, questions]asked]   B=[ and,provides, ..] Bx=answer
TransitionType.MERGES=[[[all, questions]asked]and] B=[ provides,the, ..] Bx=answer
TransitionType.MERGES=[[[[all, questions]asked]and]provides] B=[ the,best, ..] Bx=answer
## i have a new born daughter and she helped me with a lot .
### Annotated:
new born
a lot
TransitionType.MERGES=[a, lot]                  B=[ punc,] Bx=with
TransitionType.MARK_AS_OTHS=[[a, lot]]                B=[ punc,] Bx=with
### Identified: 
a lot
## be careful of who your sales guy is
### Annotated:
sales guy
TransitionType.MERGES=[Sales, Guy]              B=[ Is,] Bx=your
TransitionType.MARK_AS_OTHS=[[Sales, Guy]]            B=[ Is,] Bx=your
### Identified: 
sales guy
## i was extremely interested in the car and very likely would have bought it , but the sales guy i dealt with ruined the deal .
### Annotated:
sales guy
deal with
TransitionType.MERGES=[dealt, with]             B=[ ruined,the, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[dealt, with]]           B=[ ruined,the, ..] Bx=i
### Identified: 
deal with
## essentially , i told him i did n't trust him cause he was a car salesman , but he got so incredibly offended at that statement that he had to go cry to another salesman and compose himself before coming back .
### Annotated:
have to
go cry
TransitionType.MERGES=[had, to]                 B=[ go,cry, ..] Bx=he
TransitionType.MARK_AS_OTHS=[[had, to]]               B=[ go,cry, ..] Bx=he
### Identified: 
have to
## after that , i just tried to ignore his lack of professionalism and test drive the car .
### Annotated:
test drive
TransitionType.MERGES=[test, drive]             B=[ the,car, ..] Bx=and
TransitionType.MARK_AS_OTHS=[[test, drive]]           B=[ the,car, ..] Bx=and
### Identified: 
test drive
## joe removed a wasp nest for our condominium building and we appreciated the environmentally friendly method and prompt , friendly and informative service .
### Annotated:
environmentally friendly
## suzanne , vancouver
### Annotated:
suzanne , vancouver
## i have a saab ... which everything is expensive on and they have been extrememly fair and price a lot lower than any other shop i called .
### Annotated:
a lot
TransitionType.MERGES=[a, lot]                  B=[ lower,than, ..] Bx=price
TransitionType.MARK_AS_OTHS=[[a, lot]]                B=[ lower,than, ..] Bx=price
### Identified: 
a lot
## they came through on all of their promises and we had a very successful day .
### Annotated:
come through
TransitionType.MERGES=[came, through]           B=[ on,all, ..] Bx=they
TransitionType.MARK_AS_OTHS=[[came, through]]         B=[ on,all, ..] Bx=they
### Identified: 
come through
## there might be bigger and more well known bagel places in the area but family bagels are nice people , small shop and incredibly friendly .
### Annotated:
well know
family bagels
TransitionType.MERGES=[Family, Bagels]          B=[ are,nice, ..] Bx=but
TransitionType.MERGES=[[Family, Bagels]are]     B=[ nice,people, ..] Bx=but
TransitionType.MERGES=[[[Family, Bagels]are]nice] B=[ people,,, ..] Bx=but
TransitionType.MERGES=[[[[Family, Bagels]are]nice]people] B=[ ,,small, ..] Bx=but
## while other may be ok waiting in line at town bagel we are happy with the quality and service we get at family bagels
### Annotated:
town bagel
family bagels
TransitionType.MERGES=[in, line]                B=[ at,Town, ..] Bx=wait
TransitionType.MARK_AS_OTHS=[[in, line]]              B=[ at,Town, ..] Bx=wait
### Identified: 
in line
## my girlfriend and i took a chance on this place because we did n't want to wait in line at outback .
### Annotated:
take a chance on
TransitionType.MERGES=[took, chance]            B=[ on,this, ..] Bx=a
TransitionType.MARK_AS_OTHS=[[took, chance]]          B=[ on,this, ..] Bx=a
TransitionType.MERGES=[in, line]                B=[ at,Outback, ..] Bx=wait
TransitionType.MARK_AS_OTHS=[[in, line]]              B=[ at,Outback, ..] Bx=wait
### Identified: 
take chance
in line
## the down side was that sometimes there was a lot of noise in the hallway from other patients / doctors .
### Annotated:
down side
a lot
TransitionType.MERGES=[a, lot]                  B=[ of,noise, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[a, lot]]                B=[ of,noise, ..] Bx=be
### Identified: 
a lot
TransitionType.MERGES=[take, a]                 B=[ while,for, ..] Bx=can
TransitionType.MERGES=[[take, a]while]          B=[ for,results, ..] Bx=can
TransitionType.MERGES=[[[take, a]while]for]     B=[ results,and, ..] Bx=can
TransitionType.MERGES=[[[[take, a]while]for]results] B=[ and,did, ..] Bx=can
TransitionType.MERGES=[[[[[take, a]while]for]results]and] B=[ did,nt, ..] Bx=can
## great cookies , cakes , and customer service
### Annotated:
customer service
TransitionType.MERGES=[Customer, Service]       B=[ ] Bx=and
TransitionType.MARK_AS_OTHS=[[Customer, Service]]     B=[ ] Bx=and
### Identified: 
customer service
## although i 'll have to drive a little out of my way to go there , i 'll gladly do it knowing that since she 's been astounding to me once before that she 'll always be that way !
### Annotated:
have to
out of way
TransitionType.MERGES=[have, to]                B=[ drive,a, ..] Bx=ll
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ drive,a, ..] Bx=ll
TransitionType.MERGES=[a, little]               B=[ out,of, ..] Bx=drive
TransitionType.MARK_AS_OTHS=[[a, little]]             B=[ out,of, ..] Bx=drive
TransitionType.MERGES=[out, of]                 B=[ my,way, ..] Bx=little
TransitionType.MERGES=[[out, of]my]             B=[ way,to, ..] Bx=little
TransitionType.MERGES=[[[out, of]my]way]        B=[ to,go, ..] Bx=little
TransitionType.MERGES=[[[[out, of]my]way]to]    B=[ go,there, ..] Bx=little
TransitionType.MERGES=[[[[[out, of]my]way]to]go] B=[ there,,, ..] Bx=little
TransitionType.MERGES=[[[[[[out, of]my]way]to]go]there] B=[ ,,I, ..] Bx=little
### Identified: 
have to
a little
## she deserves many number star reviews !!
### Annotated:
number star
TransitionType.MERGES=[number, star]            B=[ reviews,punc,] Bx=many
TransitionType.MARK_AS_OTHS=[[number, star]]          B=[ reviews,punc,] Bx=many
### Identified: 
number star
## ham s on friendly ... rip
### Annotated:
ham s
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## this is the original ham 's restaurant , expanded into a regional chain in the late number -- but this one is no more .
### Annotated:
ham s
be no more
## victim of hard times and i suspect failing corporate management .
### Annotated:
hard times
TransitionType.MERGES=[hard, times]             B=[ and,I, ..] Bx=of
TransitionType.MARK_AS_OTHS=[[hard, times]]           B=[ and,I, ..] Bx=of
### Identified: 
hard times
## according to news accounts , the company is struggling .
### Annotated:
accord to
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
accord to
## so long ham s ... you will be missed .
### Annotated:
so long
ham s
## i 've stayed at this fabulous little motel two years running , and i have to say it 's one of the best lodging experiences i 've ever had on the coast ... and i 'm even comparing it to the big resorts i 've stayed at !
### Annotated:
have to
TransitionType.MERGES=[have, to]                B=[ say,it, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ say,it, ..] Bx=i
### Identified: 
have to
## the motel is very well maintained , and the managers are so accomodating , it 's kind of like visiting family each year ! ;-)
### Annotated:
kind of
## i honestly ca n't rave enough about this place ... it 's really a hidden gem worth checking out !
### Annotated:
check out
TransitionType.MERGES=[checking, out]           B=[ punc,] Bx=worth
TransitionType.MARK_AS_OTHS=[[checking, out]]         B=[ punc,] Bx=worth
### Identified: 
check out
## it had listed that there was a hot breakfast but all this meant is that they added a waffle maker to the common continental affair at most cheap hotels .
### Annotated:
waffle maker
TransitionType.MERGES=[cheap, hotels]           B=[ punc,] Bx=most
TransitionType.MERGES=[[cheap, hotels]punc]     B=[ ] Bx=most
## i used to go here almost every day since i work in the neighbourhood and loved their turkey and meatball sandwiches .
### Annotated:
use to
TransitionType.MERGES=[used, to]                B=[ go,here, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[used, to]]              B=[ go,here, ..] Bx=i
### Identified: 
use to
## chicken salad salad is great too .
### Annotated:
chicken salad
## best of all , the staff is quick on their feet and even with long lines , usually serve you in number minutes or less .
### Annotated:
quick on foot
## for the quality , the prices ( $ number - $ number ) have to be the best in town .
### Annotated:
have to
TransitionType.MERGES=[have, to]                B=[ be,the, ..] Bx=punc
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ be,the, ..] Bx=punc
TransitionType.MERGES=[in, town]                B=[ punc,] Bx=best
TransitionType.MARK_AS_OTHS=[[in, town]]              B=[ punc,] Bx=best
### Identified: 
have to
in town
## the staff get to know regulars and do their job very well .
### Annotated:
do job
TransitionType.MERGES=[get, to]                 B=[ know,regulars, ..] Bx=staff
TransitionType.MARK_AS_OTHS=[[get, to]]               B=[ know,regulars, ..] Bx=staff
### Identified: 
get to
## this is n't a tgif or cafe , it s a lunch sandwich place and a good one at that .
### Annotated:
at that
TransitionType.MERGES=[repeat, customer]        B=[ with,discount, ..] Bx=a
TransitionType.MARK_AS_OTHS=[[repeat, customer]]      B=[ with,discount, ..] Bx=a
### Identified: 
repeat customer
## i beg to differ .
### Annotated:
beg to differ
TransitionType.MERGES=[beg, to]                 B=[ differ,punc,] Bx=i
TransitionType.MERGES=[[beg, to]differ]         B=[ punc,] Bx=i
TransitionType.MERGES=[[[beg, to]differ]punc]   B=[ ] Bx=i
## this place is marginal at best .
### Annotated:
at best
TransitionType.MERGES=[at, best]                B=[ punc,] Bx=marginal
TransitionType.MARK_AS_OTHS=[[at, best]]              B=[ punc,] Bx=marginal
### Identified: 
at best
TransitionType.MERGES=[one, course]             B=[ to,another, ..] Bx=of
TransitionType.MERGES=[[one, course]to]         B=[ another,is, ..] Bx=of
TransitionType.MERGES=[[[one, course]to]another] B=[ is,nice, ..] Bx=of
TransitionType.MERGES=[[[[one, course]to]another]is] B=[ nice,when, ..] Bx=of
TransitionType.MERGES=[[[[[one, course]to]another]is]nice] B=[ when,you, ..] Bx=of
## class act .
### Annotated:
class act
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
class act
## it was late in the day and i was worried i would get charged an arm and a leg and have to wait forever .
### Annotated:
an arm and a leg
have to
TransitionType.MERGES=[have, to]                B=[ wait,forever, ..] Bx=and
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ wait,forever, ..] Bx=and
### Identified: 
have to
## would do business with them again .
### Annotated:
do business
TransitionType.MERGES=[do, business]            B=[ with,them, ..] Bx=would
TransitionType.MERGES=[[do, business]with]      B=[ them,again, ..] Bx=would
TransitionType.MARK_AS_OTHS=[[[do, business]with]]    B=[ them,again, ..] Bx=would
### Identified: 
do business with
## trust the midas touch
### Annotated:
trust the midas touch
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## this is however a very busy shop but there are appointments available & the staff up front will surely make sure you get back in a timely manner .
### Annotated:
up front
TransitionType.MERGES=[up, front]               B=[ will,surely, ..] Bx=staff
TransitionType.MARK_AS_OTHS=[[up, front]]             B=[ will,surely, ..] Bx=staff
TransitionType.MERGES=[make, sure]              B=[ you,get, ..] Bx=surely
TransitionType.MARK_AS_OTHS=[[make, sure]]            B=[ you,get, ..] Bx=surely
TransitionType.MERGES=[get, in]                 B=[ a,timely, ..] Bx=back
TransitionType.MARK_AS_OTHS=[[get, in]]               B=[ a,timely, ..] Bx=back
### Identified: 
up front
make sure
get in
## i look at some of these other comments & laugh because people think that the world revolves around them !
### Annotated:
the world revolve around
## midas has the most high tech equipment in town & i guarantee you if they told you it was electrical then in deed it s electrical !
### Annotated:
high tech
in town
in deed
TransitionType.MERGES=[in, town]                B=[ punc,I, ..] Bx=equipment
TransitionType.MARK_AS_OTHS=[[in, town]]              B=[ punc,I, ..] Bx=equipment
### Identified: 
in town
## maybe you should understand how the world works & realize you are just like any other person & not put yourself on a pedestal .
### Annotated:
put on a pedestal
TransitionType.MERGES=[put, on]                 B=[ a,pedestal, ..] Bx=yourself
TransitionType.MARK_AS_OTHS=[[put, on]]               B=[ a,pedestal, ..] Bx=yourself
### Identified: 
put on
TransitionType.MERGES=[honest, business]        B=[ owners,in, ..] Bx=most
TransitionType.MERGES=[[honest, business]owners] B=[ in,this, ..] Bx=most
TransitionType.MERGES=[[[honest, business]owners]in] B=[ this,town, ..] Bx=most
TransitionType.MERGES=[[[[honest, business]owners]in]this] B=[ town,punc,] Bx=most
TransitionType.MERGES=[[[[[honest, business]owners]in]this]town] B=[ punc,] Bx=most
TransitionType.MERGES=[[[[[[honest, business]owners]in]this]town]punc] B=[ ] Bx=most
## working with rod jacobsen was my first experience working with a cpa , so i did not know what to expect .
### Annotated:
rod jacobsen
TransitionType.MERGES=[Rod, Jacobsen]           B=[ was,my, ..] Bx=with
TransitionType.MERGES=[[Rod, Jacobsen]was]      B=[ my,first, ..] Bx=with
## that said - he seemed to be doing well enough .
### Annotated:
that say
## last year , after all was said and done , i asked rod whether my payment structure would leave me with no / little tax liability at the end of the year .
### Annotated:
be say and do
## well , again , i am now faced with a tax bill of $ number + , all due on april number , number and all that rod has to say to the matter is ' well , you wo n't have to pay a penalty . '
### Annotated:
face with
have to
TransitionType.MERGES=[has, to]                 B=[ say,to, ..] Bx=rod
TransitionType.MERGES=[[has, to]say]            B=[ to,the, ..] Bx=rod
TransitionType.MARK_AS_OTHS=[[[has, to]say]]          B=[ to,the, ..] Bx=rod
TransitionType.MERGES=[have, to]                B=[ pay,a, ..] Bx=nt
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ pay,a, ..] Bx=nt
### Identified: 
have to say
have to
## i may not have to pay a penalty , yet , but this is not what i had in mind when hired these guys .
### Annotated:
have to
have in mind
TransitionType.MERGES=[have, to]                B=[ pay,a, ..] Bx=not
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ pay,a, ..] Bx=not
TransitionType.MERGES=[had, in]                 B=[ mind,when, ..] Bx=i
TransitionType.MERGES=[[had, in]mind]           B=[ when,hired, ..] Bx=i
TransitionType.MERGES=[[[had, in]mind]when]     B=[ hired,these, ..] Bx=i
TransitionType.MERGES=[[[[had, in]mind]when]hired] B=[ these,guys, ..] Bx=i
### Identified: 
have to
## in the words of my new accountant , they let me down !
### Annotated:
let down
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGES=[[[[In, the]words]of]LET, DOWN] B=[ punc,] Bx=me
TransitionType.MARK_AS_OTHS=[[[[In, the]words]of][LET, DOWN]] B=[ punc,] Bx=me
### Identified: 
let down
## we read the good reviews before going and had high hopes .. but to our dismay it did nt turn out that way !
### Annotated:
high hope
turn out
TransitionType.MERGES=[turn, out]               B=[ that,way, ..] Bx=nt
TransitionType.MARK_AS_OTHS=[[turn, out]]             B=[ that,way, ..] Bx=nt
### Identified: 
turn out
## scallops were overcooked and the foie gras was cold but the rest of the food was lovely .
### Annotated:
foie gras
TransitionType.MERGES=[foie, gras]              B=[ was,cold, ..] Bx=the
TransitionType.MARK_AS_OTHS=[[foie, gras]]            B=[ was,cold, ..] Bx=the
### Identified: 
foie gras
## top notch eats !
### Annotated:
top notch
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
top notch
## a short but wide - ranging menu executed with innovative perfection in a cozy hole in the wall just off the main street .
### Annotated:
hole in the wall
TransitionType.MERGES=[just, off]               B=[ the,main, ..] Bx=wall
TransitionType.MERGES=[[just, off]the]          B=[ main,street, ..] Bx=wall
TransitionType.MERGES=[[[just, off]the]main]    B=[ street,punc,] Bx=wall
TransitionType.MERGES=[[[[just, off]the]main]street] B=[ punc,] Bx=wall
TransitionType.MERGES=[[[[[just, off]the]main]street]punc] B=[ ] Bx=wall
TransitionType.MERGES=[wine, selections]        B=[ punc,] Bx=price
TransitionType.MERGES=[[wine, selections]punc]  B=[ ] Bx=price
## a great place to go for dinner after a day of wine tasting .
### Annotated:
wine tasting
TransitionType.MERGES=[wine, tasting]           B=[ punc,] Bx=of
TransitionType.MERGES=[[wine, tasting]punc]     B=[ ] Bx=of
## mr. squeege is the best .
### Annotated:
mr squeege
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## absoul is the greatest donair man on the planet .
### Annotated:
on the planet
## if you enjoy amazing things , you must go to world 's finest donair .
### Annotated:
world s finest donair
TransitionType.MERGES=[World, s]                B=[ Finest,Donair, ..] Bx=to
TransitionType.MERGES=[[World, s]Finest]        B=[ Donair,punc,] Bx=to
TransitionType.MERGES=[[[World, s]Finest]Donair] B=[ punc,] Bx=to
TransitionType.MERGES=[[[[World, s]Finest]Donair]punc] B=[ ] Bx=to
TransitionType.MERGES=[give, place]             B=[ number,punc, ..] Bx=this
TransitionType.MERGES=[[give, place]number]     B=[ punc,number, ..] Bx=this
TransitionType.MERGES=[[[give, place]number]punc] B=[ number,punc,] Bx=this
TransitionType.MERGES=[[[[give, place]number]punc]number] B=[ punc,] Bx=this
TransitionType.MERGES=[[[[[give, place]number]punc]number]punc] B=[ ] Bx=this
## number thumbs up .
### Annotated:
thumb up
## bon appetit !
### Annotated:
bon appetit
## craft wonderland with history
### Annotated:
craft wonderland
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGES=[making, the]             B=[ filigree,forms, ..] Bx=like
TransitionType.MARK_AS_OTHS=[[making, the]]           B=[ filigree,forms, ..] Bx=like
### Identified: 
make the
## she is a super sweet , lovable and well - informed woman with a great sense of humor .
### Annotated:
sense of humor
TransitionType.MERGES=[sense, of]               B=[ humor,punc,] Bx=great
TransitionType.MERGES=[[sense, of]humor]        B=[ punc,] Bx=great
TransitionType.MERGES=[[[sense, of]humor]punc]  B=[ ] Bx=great
TransitionType.MERGES=[has, to]                 B=[ offer,the, ..] Bx=much
TransitionType.MERGES=[[has, to]offer]          B=[ the,serious, ..] Bx=much
TransitionType.MARK_AS_OTHS=[[[has, to]offer]]        B=[ the,serious, ..] Bx=much
### Identified: 
have to offer
## barbara quimba number
### Annotated:
barbara quimba
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
barbara quimba
## fantastic nova scotia cottage
### Annotated:
nova scotia
TransitionType.MERGES=[Nova, Scotia]            B=[ Cottage,] Bx=fantastic
TransitionType.MERGES=[[Nova, Scotia]Cottage]   B=[ ] Bx=fantastic
## we had a fantastic time .
### Annotated:
have a time
## sand hill park was a great beach ...
### Annotated:
sand hill park
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## thank - you for sharing your cottage !
### Annotated:
thank - you
## i had tried out few place around the area and had been ripped off a few times .
### Annotated:
try out
rip off
TransitionType.MERGES=[tried, out]              B=[ few,place, ..] Bx=have
TransitionType.MARK_AS_OTHS=[[tried, out]]            B=[ few,place, ..] Bx=have
TransitionType.MERGES=[ripped, off]             B=[ a,few, ..] Bx=be
TransitionType.MERGES=[[ripped, off]a]          B=[ few,times, ..] Bx=be
TransitionType.MERGES=[[[ripped, off]a]few]     B=[ times,punc,] Bx=be
TransitionType.MERGES=[[[[ripped, off]a]few]times] B=[ punc,] Bx=be
TransitionType.MERGES=[[[[[ripped, off]a]few]times]punc] B=[ ] Bx=be
### Identified: 
try out
## i had hear great things about phet and g&g automotive so i decided to give him a try .
### Annotated:
phet and gg automotive
give a try
TransitionType.MERGES=[GG, Automotive]          B=[ so,I, ..] Bx=and
TransitionType.MERGES=[[GG, Automotive]so]      B=[ I,decided, ..] Bx=and
TransitionType.MERGES=[[[GG, Automotive]so]give, a] B=[ try,punc,] Bx=him
TransitionType.MERGES=[[[GG, Automotive]so][give, a]try] B=[ punc,] Bx=him
TransitionType.MARK_AS_OTHS=[[[GG, Automotive]so][[give, a]try]] B=[ punc,] Bx=him
### Identified: 
give a try
## he checked out what i needed to have done told me what needed be fixed before he did any work and did great repair work .
### Annotated:
check out
do work
do work
TransitionType.MERGES=[checked, out]            B=[ what,I, ..] Bx=he
TransitionType.MARK_AS_OTHS=[[checked, out]]          B=[ what,I, ..] Bx=he
TransitionType.MERGES=[did, work]               B=[ and,did, ..] Bx=any
TransitionType.MARK_AS_OTHS=[[did, work]]             B=[ and,did, ..] Bx=any
### Identified: 
check out
do work
## the price was actually lower than what i had anticipated and used to compared to other places , plus he showed me the work he did when i came in to pick up the car .
### Annotated:
used to
work do
come in
pick up
TransitionType.MERGES=[compared, to]            B=[ other,places, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[compared, to]]          B=[ other,places, ..] Bx=to
TransitionType.MERGES=[came, in]                B=[ to,pick, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[came, in]]              B=[ to,pick, ..] Bx=i
TransitionType.MERGES=[pick, up]                B=[ the,car, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[pick, up]]              B=[ the,car, ..] Bx=to
### Identified: 
compare to
come in
pick up
## also , a week after the work , phet called me up to see how my car was running and to let me know that they had accidentally overcharged me for part of the work and wanted to give me a refund for that amount .
### Annotated:
call up
let know
TransitionType.MERGES=[called, up]              B=[ to,see, ..] Bx=me
TransitionType.MARK_AS_OTHS=[[called, up]]            B=[ to,see, ..] Bx=me
TransitionType.MERGES=[let, know]               B=[ that,they, ..] Bx=me
TransitionType.MARK_AS_OTHS=[[let, know]]             B=[ that,they, ..] Bx=me
### Identified: 
call up
let know
## that is just unheard of these days !
### Annotated:
unheard of
these days
## common room was comfortable and clean , very good room to read or relax . -
### Annotated:
common room
## a great breakfast which was included every morning until number am ; yummy fresh parisian croissants .
### Annotated:
parisian croissant
## it is close to bus lines for opera plaza , galleries lafayette , and the famous flea market .
### Annotated:
bus line
opera plaza
galleries lafayette
flea market
TransitionType.MERGES=[close, to]               B=[ bus,lines, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[close, to]]             B=[ bus,lines, ..] Bx=be
TransitionType.MERGES=[Opera, Plaza]            B=[ ,,Galleries, ..] Bx=for
TransitionType.MERGES=[[Opera, Plaza],]         B=[ Galleries,Lafayette, ..] Bx=for
TransitionType.MERGES=[[[Opera, Plaza],]Galleries] B=[ Lafayette,,, ..] Bx=for
TransitionType.MERGES=[[[[Opera, Plaza],]Galleries]Lafayette] B=[ ,,and, ..] Bx=for
TransitionType.MERGES=[[[[[Opera, Plaza],]Galleries]Lafayette],] B=[ and,the, ..] Bx=for
TransitionType.MERGES=[[[[[[Opera, Plaza],]Galleries]Lafayette],]and] B=[ the,famous, ..] Bx=for
TransitionType.MERGES=[[[[[[[Opera, Plaza],]Galleries]Lafayette],]and]the] B=[ famous,flea, ..] Bx=for
TransitionType.MERGES=[[[[[[[[Opera, Plaza],]Galleries]Lafayette],]and]the]famous] B=[ flea,Market, ..] Bx=for
TransitionType.MERGES=[[[[[[[[[Opera, Plaza],]Galleries]Lafayette],]and]the]famous]flea] B=[ Market,punc,] Bx=for
TransitionType.MERGES=[[[[[[[[[[Opera, Plaza],]Galleries]Lafayette],]and]the]famous]flea]Market] B=[ punc,] Bx=for
TransitionType.MERGES=[[[[[[[[[[[Opera, Plaza],]Galleries]Lafayette],]and]the]famous]flea]Market]punc] B=[ ] Bx=for
### Identified: 
close to
## we really enjoyed our stay and would definitely stay at the vintage hostel again .
### Annotated:
vintage hostel
TransitionType.MERGES=[Vintage, Hostel]         B=[ again,punc,] Bx=the
TransitionType.MERGES=[[Vintage, Hostel]again]  B=[ punc,] Bx=the
TransitionType.MERGES=[[[Vintage, Hostel]again]punc] B=[ ] Bx=the
## rocky m. lange retired coordinator , clark county school district
### Annotated:
rocky m lange
clark county school district
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGES=[[[[[Rocky, M]Lange]Retired]Coordinator]Clark, County] B=[ School,District,] Bx=,
TransitionType.MERGES=[[[[[Rocky, M]Lange]Retired]Coordinator][Clark, County]School] B=[ District,] Bx=,
TransitionType.MERGES=[[[[[Rocky, M]Lange]Retired]Coordinator][[Clark, County]School]District] B=[ ] Bx=,
TransitionType.MERGES=[[[[[Rocky, M]Lange]Retired]Coordinator][[[Clark, County]School]District]] B=[ ] Bx=,
## what a mind blowing servicing
### Annotated:
mind blow
## prominent builders nj
### Annotated:
prominent builders
TransitionType.MERGE
TransitionType.MERGE
## prominent builders in new jersey are one the best building contractors , i was referred to them by my friend , i am so glad i used them for my home renovation , and addition .
### Annotated:
prominent builder
new jersey
TransitionType.MERGES=[New, Jersey]             B=[ are,one, ..] Bx=in
TransitionType.MERGES=[[New, Jersey]are]        B=[ one,the, ..] Bx=in
TransitionType.MERGES=[[[New, Jersey]are]one]   B=[ the,best, ..] Bx=in
## i had my wedding luncheon at this bj s restaurant , and it was one of the best choices that i made .
### Annotated:
bj s
## we had a large party , about fifty people or so , and yet everything was served quickly and we all had a wonderful time .
### Annotated:
have a time
## i really appreciate bj s for making that special day even better with their wonderful food and service .
### Annotated:
bj s
## the finest german bedding and linens store .
### Annotated:
german bedding
TransitionType.MERGES=[a, little]               B=[ girl,and, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[a, little]]             B=[ girl,and, ..] Bx=be
### Identified: 
a little
## dr. stiefvater has always been very professional and helpful .
### Annotated:
dr stiefvater
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## i would recommend bayside chiropractic to anyone who is in need of a regular adjustment or is suffering from a chronic condition .
### Annotated:
bayside chiropractic
in need
TransitionType.MERGES=[Bayside, Chiropractic]   B=[ to,anyone, ..] Bx=recommend
TransitionType.MERGES=[[Bayside, Chiropractic]to] B=[ anyone,who, ..] Bx=recommend
TransitionType.MERGES=[[[Bayside, Chiropractic]to]anyone] B=[ who,is, ..] Bx=recommend
TransitionType.MERGES=[[[[Bayside, Chiropractic]to]anyone]is, in] B=[ need,of, ..] Bx=who
TransitionType.MARK_AS_OTHS=[[[[Bayside, Chiropractic]to]anyone][is, in]] B=[ need,of, ..] Bx=who
### Identified: 
be in
## they offer a large variety of quality hotdogs and hamburgers they also offer veggie dogs .
### Annotated:
veggie dog
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
close to
## bland and over cooked .
### Annotated:
over cooked
TransitionType.MERGES=[over, cooked]            B=[ punc,] Bx=and
TransitionType.MERGES=[[over, cooked]punc]      B=[ ] Bx=and
## first time ballerina
### Annotated:
first time
## i 'm a soccer mom so i was n't sure what i was looking for when it comes to dancewear .
### Annotated:
soccer mom
TransitionType.MERGES=[when, it]                B=[ comes,to, ..] Bx=for
TransitionType.MERGES=[[when, it]comes]         B=[ to,dancewear, ..] Bx=for
TransitionType.MERGES=[[[when, it]comes]to]     B=[ dancewear,punc,] Bx=for
TransitionType.MARK_AS_OTHS=[[[[when, it]comes]to]]   B=[ dancewear,punc,] Bx=for
### Identified: 
when it come to
## this place and its sister store peking garden are the worst places to order from .
### Annotated:
peking garden
TransitionType.MERGES=[Peking, Garden]          B=[ are,the, ..] Bx=store
TransitionType.MERGES=[[Peking, Garden]are]     B=[ the,worst, ..] Bx=store
TransitionType.MERGES=[[[Peking, Garden]are]the] B=[ worst,places, ..] Bx=store
TransitionType.MERGES=[[[[Peking, Garden]are]the]worst] B=[ places,to, ..] Bx=store
TransitionType.MERGES=[[[[[Peking, Garden]are]the]worst]places] B=[ to,order, ..] Bx=store
TransitionType.MERGES=[[[[[[Peking, Garden]are]the]worst]places]to] B=[ order,from, ..] Bx=store
TransitionType.MERGES=[[[[[[[Peking, Garden]are]the]worst]places]to]order] B=[ from,punc,] Bx=store
TransitionType.MERGES=[[[[[[[[Peking, Garden]are]the]worst]places]to]order]from] B=[ punc,] Bx=store
TransitionType.MERGES=[[[[[[[[[Peking, Garden]are]the]worst]places]to]order]from]punc] B=[ ] Bx=store
## beware they will rip u off
### Annotated:
rip off
## i do n't get it .
### Annotated:
get it
## you order at the counter and there is a space for tip on your credit card receipt .
### Annotated:
credit card
TransitionType.MERGES=[credit, card]            B=[ receipt,punc,] Bx=your
TransitionType.MARK_AS_OTHS=[[credit, card]]          B=[ receipt,punc,] Bx=your
### Identified: 
credit card
## both were excellent sales men who put my needs first .
### Annotated:
sales men
TransitionType.MERGES=[sales, men]              B=[ who,put, ..] Bx=excellent
TransitionType.MARK_AS_OTHS=[[sales, men]]            B=[ who,put, ..] Bx=excellent
### Identified: 
sales men
## i brought my car in for a simple emissions test .
### Annotated:
emission test
TransitionType.MERGES=[brought, in]             B=[ for,a, ..] Bx=car
TransitionType.MARK_AS_OTHS=[[brought, in]]           B=[ for,a, ..] Bx=car
TransitionType.MERGES=[emissions, test]         B=[ punc,] Bx=simple
TransitionType.MERGES=[[emissions, test]punc]   B=[ ] Bx=simple
### Identified: 
bring in
## ten minutes later , i took my car down the street and it passed the emissions test with flying colors .
### Annotated:
emission test
with fly colors
TransitionType.MERGES=[took, car]               B=[ down,the, ..] Bx=my
TransitionType.MERGES=[[took, car]down]         B=[ the,street, ..] Bx=my
TransitionType.MERGES=[[[took, car]down]the]    B=[ street,and, ..] Bx=my
TransitionType.MERGES=[[[[took, car]down]the]street] B=[ and,it, ..] Bx=my
TransitionType.MERGES=[[[[[took, car]down]the]street]and] B=[ it,passed, ..] Bx=my
TransitionType.MERGES=[[[[[[took, car]down]the]street]and]it] B=[ passed,the, ..] Bx=my
TransitionType.MERGES=[[[[[[[took, car]down]the]street]and]it]passed] B=[ the,emissions, ..] Bx=my
TransitionType.MERGES=[[[[[[[[took, car]down]the]street]and]it]passed]the] B=[ emissions,test, ..] Bx=my
TransitionType.MERGES=[[[[[[[[[took, car]down]the]street]and]it]passed]the]emissions] B=[ test,with, ..] Bx=my
TransitionType.MERGES=[[[[[[[[[[took, car]down]the]street]and]it]passed]the]emissions]test] B=[ with,flying, ..] Bx=my
TransitionType.MERGES=[[[[[[[[[[[took, car]down]the]street]and]it]passed]the]emissions]test]with] B=[ flying,colors, ..] Bx=my
TransitionType.MERGES=[[[[[[[[[[[[took, car]down]the]street]and]it]passed]the]emissions]test]with]flying] B=[ colors,punc,] Bx=my
## if you 're a fan of herpes , being ripped off , and child molesters , this is the garage for you .
### Annotated:
rip off
child molester
TransitionType.MERGES=[ripped, off]             B=[ ,,and, ..] Bx=be
TransitionType.MERGES=[[ripped, off],]          B=[ and,child, ..] Bx=be
TransitionType.MERGES=[[[ripped, off],]and]     B=[ child,molesters, ..] Bx=be
TransitionType.MERGES=[[[[ripped, off],]and]child] B=[ molesters,,, ..] Bx=be
TransitionType.MERGES=[[[[[ripped, off],]and]child]molesters] B=[ ,,this, ..] Bx=be
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## congratulations prestige hino !
### Annotated:
prestige hino
TransitionType.MERGES=[Prestige, Hino]          B=[ punc,] Bx=congratulations
TransitionType.MERGES=[[Prestige, Hino]punc]    B=[ ] Bx=congratulations
TransitionType.MERGES=[Hino, Dealer]            B=[ of,the, ..] Bx=converted
TransitionType.MERGES=[[Hino, Dealer]of]        B=[ the,Year, ..] Bx=converted
TransitionType.MERGES=[[[Hino, Dealer]of]the]   B=[ Year,punc,] Bx=converted
TransitionType.MERGES=[[[[Hino, Dealer]of]the]Year] B=[ punc,] Bx=converted
TransitionType.MERGES=[[[[[Hino, Dealer]of]the]Year]punc] B=[ ] Bx=converted
TransitionType.MERGES=[Dandenong, PMA]          B=[ ,,sales, ..] Bx=,
TransitionType.MERGES=[[Dandenong, PMA],]       B=[ sales,punc,] Bx=,
TransitionType.MERGES=[[[Dandenong, PMA],]sales] B=[ punc,] Bx=,
TransitionType.MERGES=[[[[Dandenong, PMA],]sales]punc] B=[ ] Bx=,
## market leader medium duty , sales .
### Annotated:
medium duty
## well done to anthony and the team !
### Annotated:
well do
## well done to brendan and the team !
### Annotated:
well do
## gold award parts excellence , metro .
### Annotated:
gold award
## well done to jason and the team !
### Annotated:
well do
## not friendly , not helpful , overall poor customer service .
### Annotated:
customer service
TransitionType.MERGES=[customer, service]       B=[ punc,] Bx=poor
TransitionType.MARK_AS_OTHS=[[customer, service]]     B=[ punc,] Bx=poor
### Identified: 
customer service
## i thought the uk was completely devoid of good nyc style pizza .
### Annotated:
nyc style pizza
## i thought to get a decent pizza the only way was at a fancy restaurant , and i have to get a whole pie .
### Annotated:
have to
TransitionType.MERGES=[have, to]                B=[ get,a, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ get,a, ..] Bx=i
### Identified: 
have to
## i thought i would have to wait until i went home to nyc .
### Annotated:
have to
TransitionType.MERGES=[have, to]                B=[ wait,until, ..] Bx=would
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ wait,until, ..] Bx=would
### Identified: 
have to
## i saw this place and it looked like the holy grail .
### Annotated:
the holy grail
## i du n no how they did it , but scottish friends --- this is the real deal .
### Annotated:
the real deal
## that being said , i do n't know how their delivery service is .
### Annotated:
that be say
TransitionType.MERGES=[delivery, service]       B=[ is,punc,] Bx=their
TransitionType.MERGES=[[delivery, service]is]   B=[ punc,] Bx=their
TransitionType.MERGES=[[[delivery, service]is]punc] B=[ ] Bx=their
## they might want to change the name to reflect the new yorkedness of the pizza , scrummy yummy sounds gimmicky to me .
### Annotated:
want to
new yorkedness
scrummy yummy
TransitionType.MERGES=[to, see]                 B=[ if,it, ..] Bx=,
TransitionType.MERGES=[[to, see]if]             B=[ it,fits, ..] Bx=,
TransitionType.MERGES=[[[to, see]if]it]         B=[ fits,you, ..] Bx=,
TransitionType.MERGES=[[[[to, see]if]it]fits]   B=[ you,punc,] Bx=,
TransitionType.MERGES=[[[[[to, see]if]it]fits]you] B=[ punc,] Bx=,
TransitionType.MERGES=[[[[[[to, see]if]it]fits]you]punc] B=[ ] Bx=,
## they are out of business .
### Annotated:
out of business
TransitionType.MERGES=[are, out]                B=[ of,business, ..] Bx=they
TransitionType.MERGES=[[are, out]of]            B=[ business,punc,] Bx=they
TransitionType.MARK_AS_OTHS=[[[are, out]of]]          B=[ business,punc,] Bx=they
### Identified: 
be out of
## calls are now forwarded to malcolm smith motorsports down the road .
### Annotated:
malcolm smith motorsports
down the road
TransitionType.MERGES=[Malcolm, Smith]          B=[ Motorsports,down, ..] Bx=to
TransitionType.MERGES=[[Malcolm, Smith]Motorsports] B=[ down,the, ..] Bx=to
TransitionType.MERGES=[[[Malcolm, Smith]Motorsports]down] B=[ the,road, ..] Bx=to
TransitionType.MERGES=[[[[Malcolm, Smith]Motorsports]down]the] B=[ road,punc,] Bx=to
TransitionType.MERGES=[[[[[Malcolm, Smith]Motorsports]down]the]road] B=[ punc,] Bx=to
TransitionType.MERGES=[[[[[[Malcolm, Smith]Motorsports]down]the]road]punc] B=[ ] Bx=to
## when i inquired he rudely replied " in the morning when things are checked out you 'll get it back . "
### Annotated:
check out
TransitionType.MERGES=[checked, out]            B=[ you,ll, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[checked, out]]          B=[ you,ll, ..] Bx=be
TransitionType.MERGES=[get, it]                 B=[ back,punc, ..] Bx=ll
TransitionType.MARK_AS_OTHS=[[get, it]]               B=[ back,punc, ..] Bx=ll
### Identified: 
check out
get it
## i called customer service about it because the website specifically states that there are no other charges at the check - in .
### Annotated:
customer service
check - in
TransitionType.MERGES=[customer, service]       B=[ about,it, ..] Bx=call
TransitionType.MARK_AS_OTHS=[[customer, service]]     B=[ about,it, ..] Bx=call
### Identified: 
customer service
TransitionType.MERGES=[mentioned, to]           B=[ the,reception, ..] Bx=also
TransitionType.MERGES=[[mentioned, to]the]      B=[ reception,person, ..] Bx=also
TransitionType.MERGES=[[[mentioned, to]the]reception] B=[ person,punc,] Bx=also
TransitionType.MERGES=[[[[mentioned, to]the]reception]person] B=[ punc,] Bx=also
TransitionType.MERGES=[[[[[mentioned, to]the]reception]person]punc] B=[ ] Bx=also
TransitionType.MERGES=[had, too]                B=[ punc,] Bx=i
TransitionType.MERGES=[[had, too]punc]          B=[ ] Bx=i
## excellent medical care !!!!!!
### Annotated:
medical care
## i went to this urgent care center and was blown away with their service .
### Annotated:
urgent care
blow away
TransitionType.MERGES=[blown, away]             B=[ with,their, ..] Bx=be
TransitionType.MARK_AS_OTHS=[[blown, away]]           B=[ with,their, ..] Bx=be
### Identified: 
blow away
TransitionType.MERGES=[close, to]               B=[ home,punc,] Bx=place
TransitionType.MARK_AS_OTHS=[[close, to]]             B=[ home,punc,] Bx=place
### Identified: 
close to
## will definitely go back when i need medical care .
### Annotated:
go back
medical care
## a friend and i recently took our number and number month olds here .
### Annotated:
month old
TransitionType.MERGES=[month, olds]             B=[ here,punc,] Bx=number
TransitionType.MARK_AS_OTHS=[[month, olds]]           B=[ here,punc,] Bx=number
### Identified: 
month old
## go down number block to super number .
### Annotated:
go down
super number
TransitionType.MERGE
TransitionType.MARK_AS_OTH
TransitionType.MERGES=[Super, number]           B=[ punc,] Bx=to
TransitionType.MERGES=[[Super, number]punc]     B=[ ] Bx=to
### Identified: 
go down
## james bateman came the day i called and fixed the problem quickly and efficiently .
### Annotated:
james bateman
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
james bateman
## when the next hailstorm blows through , i will not hesitate to contact james at team texas construction .
### Annotated:
team texas construction
TransitionType.MERGES=[blows, through]          B=[ ,,I, ..] Bx=hailstorm
TransitionType.MERGES=[[blows, through],]       B=[ I,will, ..] Bx=hailstorm
TransitionType.MERGES=[[[blows, through],]Team, Texas] B=[ Construction,punc,] Bx=at
TransitionType.MERGES=[[[blows, through],][Team, Texas]Construction] B=[ punc,] Bx=at
TransitionType.MERGES=[[[blows, through],][[Team, Texas]Construction]punc] B=[ ] Bx=at
TransitionType.MERGES=[[[blows, through],][[[Team, Texas]Construction]punc]] B=[ ] Bx=at
## midtown reston has great location and luxurious environment .
### Annotated:
midtown reston
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
## check out their wine tastings every friday night !
### Annotated:
check out
wine tasting
TransitionType.MERGE
TransitionType.MARK_AS_OTH
TransitionType.MERGES=[Friday, night]           B=[ punc,] Bx=every
TransitionType.MARK_AS_OTHS=[[Friday, night]]         B=[ punc,] Bx=every
### Identified: 
check out
friday night
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGE
TransitionType.MERGES=[[[[[Made, an]appointment]to]have]give, an] B=[ estimate,punc,] Bx=and
TransitionType.MERGES=[[[[[Made, an]appointment]to]have][give, an]estimate] B=[ punc,] Bx=and
TransitionType.MERGES=[[[[[Made, an]appointment]to]have][[give, an]estimate]punc] B=[ ] Bx=and
TransitionType.MERGES=[[[[[Made, an]appointment]to]have][[[give, an]estimate]punc]] B=[ ] Bx=and
## when i called the manager to complain , she said she knew the guy did n't know about curtains and that the usual lady called in sick hours earlier !
### Annotated:
call in sick
TransitionType.MERGES=[called, in]              B=[ sick,hours, ..] Bx=lady
TransitionType.MARK_AS_OTHS=[[called, in]]            B=[ sick,hours, ..] Bx=lady
### Identified: 
call in
## so what was the point of the appointment !?!
### Annotated:
the point
## to just come over and hang out ?!?
### Annotated:
come over
hang out
TransitionType.MERGES=[come, over]              B=[ and,hang, ..] Bx=just
TransitionType.MARK_AS_OTHS=[[come, over]]            B=[ and,hang, ..] Bx=just
TransitionType.MERGES=[hang, out]               B=[ punc,] Bx=and
TransitionType.MARK_AS_OTHS=[[hang, out]]             B=[ punc,] Bx=and
### Identified: 
come over
hang out
## i will never do business with this company !
### Annotated:
do business
## what a great deal thank you
### Annotated:
thank you
TransitionType.MERGES=[THANK, YOU]              B=[ ] Bx=deal
TransitionType.MARK_AS_OTHS=[[THANK, YOU]]            B=[ ] Bx=deal
### Identified: 
thank you
TransitionType.MERGES=[sandwiches, had]         B=[ in,Seattle, ..] Bx=ve
TransitionType.MERGES=[[sandwiches, had]in]     B=[ Seattle,punc,] Bx=ve
TransitionType.MERGES=[[[sandwiches, had]in]Seattle] B=[ punc,] Bx=ve
TransitionType.MERGES=[[[[sandwiches, had]in]Seattle]punc] B=[ ] Bx=ve
TransitionType.MERGES=[warned, me]              B=[ that,it, ..] Bx=owner
TransitionType.MERGES=[[warned, me]that]        B=[ it,was, ..] Bx=owner
TransitionType.MERGES=[[[warned, me]that]it]    B=[ was,the, ..] Bx=owner
TransitionType.MERGES=[[[[warned, me]that]it]was] B=[ the,best, ..] Bx=owner
## no joke !
### Annotated:
no joke
## identity theft
### Annotated:
identity theft
## it was a black female that use to work in the office .
### Annotated:
use to
TransitionType.MERGES=[use, to]                 B=[ work,in, ..] Bx=that
TransitionType.MARK_AS_OTHS=[[use, to]]               B=[ work,in, ..] Bx=that
### Identified: 
use to
## they both went to jail and a new manager was put in charge of the apartments .
### Annotated:
put in charge
TransitionType.MERGES=[in, charge]              B=[ of,the, ..] Bx=put
TransitionType.MERGES=[[in, charge]of]          B=[ the,apartments, ..] Bx=put
TransitionType.MERGES=[[[in, charge]of]the]     B=[ apartments,punc,] Bx=put
TransitionType.MERGES=[[[[in, charge]of]the]apartments] B=[ punc,] Bx=put
TransitionType.MERGES=[[[[[in, charge]of]the]apartments]punc] B=[ ] Bx=put
## a girl would show up , then a guy in a nice car would show up .
### Annotated:
show up
show up
TransitionType.MERGES=[show, up]                B=[ ,,then, ..] Bx=would
TransitionType.MARK_AS_OTHS=[[show, up]]              B=[ ,,then, ..] Bx=would
TransitionType.MERGES=[show, up]                B=[ punc,] Bx=would
TransitionType.MARK_AS_OTHS=[[show, up]]              B=[ punc,] Bx=would
### Identified: 
show up
show up
## i lived in one that did not face the parking lot .
### Annotated:
parking lot
TransitionType.MERGES=[parking, lot]            B=[ punc,] Bx=the
TransitionType.MARK_AS_OTHS=[[parking, lot]]          B=[ punc,] Bx=the
### Identified: 
parking lot
## gates worked number % of the time at best .
### Annotated:
at best
TransitionType.MERGES=[at, best]                B=[ punc,] Bx=time
TransitionType.MARK_AS_OTHS=[[at, best]]              B=[ punc,] Bx=time
### Identified: 
at best
TransitionType.MERGES=[car, number]             B=[ number,we, ..] Bx=be
TransitionType.MERGES=[[car, number]number]     B=[ we,ve, ..] Bx=be
TransitionType.MERGES=[[[car, number]number]we] B=[ ve,purchased, ..] Bx=be
TransitionType.MERGES=[[[[car, number]number]we]ve] B=[ purchased,through, ..] Bx=be
TransitionType.MERGES=[[[[[car, number]number]we]ve]purchased] B=[ through,them, ..] Bx=be
TransitionType.MERGES=[[[[[[car, number]number]we]ve]purchased]through] B=[ them,punc,] Bx=be
TransitionType.MERGES=[[[[[[[car, number]number]we]ve]purchased]through]them] B=[ punc,] Bx=be
TransitionType.MERGES=[[[[[[[[car, number]number]we]ve]purchased]through]them]punc] B=[ ] Bx=be
## we trust and appreciate scott larson and know that he will always take good care of us and listen to our needs !
### Annotated:
scott larson
take care of
TransitionType.MERGES=[Scott, Larson]           B=[ and,know, ..] Bx=appreciate
TransitionType.MERGES=[[Scott, Larson]and]      B=[ know,that, ..] Bx=appreciate
TransitionType.MERGES=[[[Scott, Larson]and]know] B=[ that,he, ..] Bx=appreciate
TransitionType.MERGES=[[[[Scott, Larson]and]know]that] B=[ he,will, ..] Bx=appreciate
TransitionType.MERGES=[[[[[Scott, Larson]and]know]that]he] B=[ will,always, ..] Bx=appreciate
TransitionType.MERGES=[[[[[[Scott, Larson]and]know]that]he]will] B=[ always,take, ..] Bx=appreciate
TransitionType.MERGES=[[[[[[[Scott, Larson]and]know]that]he]will]always] B=[ take,good, ..] Bx=appreciate
TransitionType.MERGES=[[[[[[[[Scott, Larson]and]know]that]he]will]always]take] B=[ good,care, ..] Bx=appreciate
TransitionType.MERGES=[[[[[[[[[Scott, Larson]and]know]that]he]will]always]take]good] B=[ care,of, ..] Bx=appreciate
TransitionType.MERGES=[[[[[[[[[[Scott, Larson]and]know]that]he]will]always]take]good]care] B=[ of,us, ..] Bx=appreciate
TransitionType.MERGES=[[[[[[[[[[[Scott, Larson]and]know]that]he]will]always]take]good]care]of] B=[ us,and, ..] Bx=appreciate
## the night i drove back home , i found that the rear window has some leakage .
### Annotated:
rear window
TransitionType.MERGES=[rear, window]            B=[ has,some, ..] Bx=the
TransitionType.MARK_AS_OTHS=[[rear, window]]          B=[ has,some, ..] Bx=the
### Identified: 
rear window
## i admit that i should have paid attention to this kind of little things while test drive .
### Annotated:
pay attention
test drive
TransitionType.MERGES=[paid, attention]         B=[ to,this, ..] Bx=have
TransitionType.MARK_AS_OTHS=[[paid, attention]]       B=[ to,this, ..] Bx=have
TransitionType.MERGES=[test, drive]             B=[ punc,] Bx=while
TransitionType.MARK_AS_OTHS=[[test, drive]]           B=[ punc,] Bx=while
### Identified: 
pay attention
test drive
TransitionType.MERGES=[brought, back]           B=[ the,second, ..] Bx=car
TransitionType.MARK_AS_OTHS=[[brought, back]]         B=[ the,second, ..] Bx=car
### Identified: 
bring back
## who knows how much they want me to pay to fix this thing .
### Annotated:
who know
TransitionType.MERGES=[walked, away]            B=[ punc,] Bx=i
TransitionType.MARK_AS_OTHS=[[walked, away]]          B=[ punc,] Bx=i
### Identified: 
walk away
TransitionType.MERGE
TransitionType.MARK_AS_OTH
### Identified: 
stay away
TransitionType.MERGES=[on, business]            B=[ and,had, ..] Bx=canada
TransitionType.MARK_AS_OTHS=[[on, business]]          B=[ and,had, ..] Bx=canada
### Identified: 
on business
TransitionType.MERGES=[not, to]                 B=[ mention,very, ..] Bx=,
TransitionType.MERGES=[[not, to]mention]        B=[ very,well, ..] Bx=,
TransitionType.MARK_AS_OTHS=[[[not, to]mention]]      B=[ very,well, ..] Bx=,
### Identified: 
not to mention
## it turned out being very good quality tmobile service and i was happy with the new tmobile phone .
### Annotated:
turn out
TransitionType.MERGES=[turned, out]             B=[ being,very, ..] Bx=it
TransitionType.MARK_AS_OTHS=[[turned, out]]           B=[ being,very, ..] Bx=it
### Identified: 
turn out
## hit or miss on the service .
### Annotated:
hit or miss
## i still have surgically induced hair loss .
### Annotated:
hair loss
TransitionType.MERGES=[hair, loss]              B=[ punc,] Bx=induce
TransitionType.MERGES=[[hair, loss]punc]        B=[ ] Bx=induce
## excellent customer service and quality work .
### Annotated:
customer service
TransitionType.MERGES=[customer, service]       B=[ and,quality, ..] Bx=excellent
TransitionType.MARK_AS_OTHS=[[customer, service]]     B=[ and,quality, ..] Bx=excellent
### Identified: 
customer service
## they went the extra mile to repair my cowboy boots -- they had to have a special kind of paper that looked like wood grain to fix the heels .
### Annotated:
go the extra mile
cowboy boot
have to
wood grain
TransitionType.MERGES=[went, the]               B=[ extra,mile, ..] Bx=they
TransitionType.MERGES=[[went, the]extra]        B=[ mile,to, ..] Bx=they
TransitionType.MERGES=[[[went, the]extra]mile]  B=[ to,repair, ..] Bx=they
TransitionType.MARK_AS_OTHS=[[[[went, the]extra]mile]] B=[ to,repair, ..] Bx=they
TransitionType.MERGES=[cowboy, boots]           B=[ punc,they, ..] Bx=my
TransitionType.MERGES=[[cowboy, boots]punc]     B=[ they,had, ..] Bx=my
TransitionType.MERGES=[[[cowboy, boots]punc]had, to] B=[ have,a, ..] Bx=they
TransitionType.MARK_AS_OTHS=[[[cowboy, boots]punc][had, to]] B=[ have,a, ..] Bx=they
### Identified: 
go the extra mile
have to
## if i had time to drive to tacoma before they closed during the work week , i would just so i could get those boots fixed properly again .
### Annotated:
work week
TransitionType.MERGES=[had, time]               B=[ to,drive, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[had, time]]             B=[ to,drive, ..] Bx=i
TransitionType.MERGES=[work, week]              B=[ ,,I, ..] Bx=the
TransitionType.MARK_AS_OTHS=[[work, week]]            B=[ ,,I, ..] Bx=the
### Identified: 
have time
work week
## number days for get that ...
### Annotated:
for get that
## i called dominos tonight , it rang forever , i get put on hold twice without saying a word and finally someone says , may i help you ?
### Annotated:
put on hold
TransitionType.MERGES=[put, on]                 B=[ hold,twice, ..] Bx=get
TransitionType.MARK_AS_OTHS=[[put, on]]               B=[ hold,twice, ..] Bx=get
### Identified: 
put on
## they say no , warwick in new jersey , call new jersey .
### Annotated:
new jersey
new jersey
TransitionType.MERGES=[New, Jersey]             B=[ ,,Call, ..] Bx=in
TransitionType.MERGES=[[New, Jersey],]          B=[ Call,New, ..] Bx=in
TransitionType.MERGES=[[[New, Jersey],]Call]    B=[ New,Jersey, ..] Bx=in
TransitionType.MERGES=[[[[New, Jersey],]Call]New] B=[ Jersey,punc,] Bx=in
TransitionType.MERGES=[[[[[New, Jersey],]Call]New]Jersey] B=[ punc,] Bx=in
TransitionType.MERGES=[[[[[[New, Jersey],]Call]New]Jersey]punc] B=[ ] Bx=in
## i laugh and say , no , that warwick is in new york , but i 'm at the radison - warwick .
### Annotated:
new york
radison - warwick
TransitionType.MERGES=[New, York]               B=[ ,,but, ..] Bx=in
TransitionType.MARK_AS_OTHS=[[New, York]]             B=[ ,,but, ..] Bx=in
TransitionType.MERGES=[Radison, -]              B=[ Warwick,punc,] Bx=the
TransitionType.MERGES=[[Radison, -]Warwick]     B=[ punc,] Bx=the
TransitionType.MERGES=[[[Radison, -]Warwick]punc] B=[ ] Bx=the
### Identified: 
new york
## and i said , yes , center city philly , and he says , no , warwick is a township , if you 're at a radison in warwick that s too far , try dominos in pottstown .
### Annotated:
center city philly
TransitionType.MERGES=[CENTER, CITY]            B=[ PHILLY,,, ..] Bx=,
TransitionType.MERGES=[[CENTER, CITY]PHILLY]    B=[ ,,and, ..] Bx=,
TransitionType.MERGES=[[[CENTER, CITY]PHILLY],] B=[ and,he, ..] Bx=,
TransitionType.MERGES=[[[[CENTER, CITY]PHILLY],]and] B=[ he,says, ..] Bx=,
TransitionType.MERGES=[[[[[CENTER, CITY]PHILLY],]and]he] B=[ says,,, ..] Bx=,
TransitionType.MERGES=[[[[[[CENTER, CITY]PHILLY],]and]he]says] B=[ ,,NO, ..] Bx=,
## i say , no , i am at the radison warwick hotel in rittenhouse square .
### Annotated:
radison warwick
rittenhouse square
TransitionType.MERGES=[RADISON, WARWICK]        B=[ HOTEL,in, ..] Bx=the
TransitionType.MARK_AS_OTHS=[[RADISON, WARWICK]]      B=[ HOTEL,in, ..] Bx=the
TransitionType.MERGES=[Rittenhouse, Square]     B=[ punc,] Bx=in
TransitionType.MARK_AS_OTHS=[[Rittenhouse, Square]]   B=[ punc,] Bx=in
### Identified: 
radison warwick
rittenhouse square
## he says : i not know that town , i have to get to work , i 'm in philly .
### Annotated:
have to
get to work
TransitionType.MERGES=[have, to]                B=[ get,to, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ get,to, ..] Bx=i
TransitionType.MERGES=[get, to]                 B=[ work,,, ..] Bx=to
TransitionType.MARK_AS_OTHS=[[get, to]]               B=[ work,,, ..] Bx=to
### Identified: 
have to
get to
## he says , i have to have an exact address .
### Annotated:
have to
TransitionType.MERGES=[have, to]                B=[ have,an, ..] Bx=i
TransitionType.MARK_AS_OTHS=[[have, to]]              B=[ have,an, ..] Bx=i
### Identified: 
have to
## ok , number locust street i say .
### Annotated:
locust street
TransitionType.MERGES=[LOCUST, STREET]          B=[ i,say, ..] Bx=number
TransitionType.MERGES=[[LOCUST, STREET]i]       B=[ say,punc,] Bx=number
TransitionType.MERGES=[[[LOCUST, STREET]i]say]  B=[ punc,] Bx=number
TransitionType.MERGES=[[[[LOCUST, STREET]i]say]punc] B=[ ] Bx=number
## he says : why you tell me you r in warwick township ?
### Annotated:
warwick township
TransitionType.MERGES=[WARWICK, TOWNSHIP]       B=[ punc,] Bx=in
TransitionType.MERGES=[[WARWICK, TOWNSHIP]punc] B=[ ] Bx=in
## would not recommend i was in a fair amount of pain for several weeks .
### Annotated:
in pain
## his clinic is very very dirty he is a real disaster to go totally not organized for every step he take .
### Annotated:
step take
## is not a service office
### Annotated:
service office
## this is a delivery office only and does not take walk ins but they do have a blue box out front .
### Annotated:
take walk ins
out front
TransitionType.MERGES=[blue, box]               B=[ out,front, ..] Bx=a
TransitionType.MERGES=[[blue, box]out]          B=[ front,punc,] Bx=a
TransitionType.MERGES=[[[blue, box]out]front]   B=[ punc,] Bx=a
TransitionType.MERGES=[[[[blue, box]out]front]punc] B=[ ] Bx=a
## i have used just like family several times now and they have provided great care for my two dogs .
### Annotated:
just like family
TransitionType.MERGES=[Just, Like]              B=[ Family,several, ..] Bx=use
TransitionType.MERGES=[[Just, Like]Family]      B=[ several,times, ..] Bx=use
TransitionType.MERGES=[[[Just, Like]Family]several] B=[ times,now, ..] Bx=use
TransitionType.MERGES=[[[[Just, Like]Family]several]times] B=[ now,and, ..] Bx=use
TransitionType.MERGES=[[[[[Just, Like]Family]several]times]now] B=[ and,they, ..] Bx=use
TransitionType.MERGES=[[[[[[Just, Like]Family]several]times]now]and] B=[ they,have, ..] Bx=use
## the real testament is not in how much she likes your animals but how much they like her .
### Annotated:
be in
	PARSING TIME: 0.18 minutes 
==================================================================================================
	Identification : 0.477
	P, R  : 0.73, 0.354
	Token-based : 0.482
	P, R  : 0.78, 0.349
	DiMSUM : 0.454
	P, R  : 0.767, 0.322

==================================================================================================

==================================================================================================
Seen MWEs
==================================================================================================
	Gold: 43.7
	Predicted: 99.1
	F : 0.763
	P, R  : 0.728, 0.801

==================================================================================================
Seen MWEs(Frequently)
==================================================================================================
	Gold: 18.0
	Predicted: 39.7
	F : 0.906
	P, R  : 0.876, 0.938

==================================================================================================
Seen MWEs(Barely)
==================================================================================================
	Gold: 25.7
	Predicted: 59.4
	F : 0.665
	P, R  : 0.629, 0.705

==================================================================================================
Partially-seen MWEs
==================================================================================================
	Gold: 51.9
	Predicted: 0.9
	F : 0.016
	P, R  : 1.0, 0.008

==================================================================================================
Partially-seen MWEs (Without Noise)
==================================================================================================
	Gold: 43.7
	Predicted: 0.9
	F : 0.02
	P, R  : 1.0, 0.01

==================================================================================================
Non-seen MWEs
==================================================================================================
	Gold: 56.3
	Predicted: 0.9
	F : 0.014
	P, R  : 1.0, 0.007

==================================================================================================
Continuous MWEs
==================================================================================================
	Gold: 89.5
	Predicted: 89.0
	F : 0.496
	P, R  : 0.762, 0.368

==================================================================================================
Discontinuous MWEs
==================================================================================================
	Gold: 10.5
	Predicted: 11.0
	F : 0.319
	P, R  : 0.474, 0.24

==================================================================================================
Identic
==================================================================================================
	Gold: 34.0 / (all:seen + non seen)
	Predicted: 80.3 / (all:seen + non seen)
	F : 0.794
	P, R  : 0.744, 0.851

==================================================================================================
Variant
==================================================================================================
	Gold: 9.7 / (all:seen + non seen)
	Predicted: 18.8 / (all:seen + non seen)
	F : 0.642
	P, R  : 0.662, 0.623

==================================================================================================
Embeddeds
==================================================================================================
	Gold: 0.0
	Predicted: 0.0
	F : 0
	P, R  : 0.0, 0.0

==================================================================================================
MWTs
==================================================================================================
	Gold: 0.0
	Predicted: 0.0
	F : 0
	P, R  : 0.0, 0.0

==================================================================================================
Multitokens
==================================================================================================
	Gold: 100.0
	Predicted: 100.0
	F : 0.477
	P, R  : 0.73, 0.354

==================================================================================================
Length(2)
==================================================================================================
	Gold: 76.2
	Predicted: 88.4
	F : 0.536
	P, R  : 0.744, 0.419

==================================================================================================
Length(3)
==================================================================================================
	Gold: 18.6
	Predicted: 10.7
	F : 0.272
	P, R  : 0.622, 0.174

==================================================================================================
4 < Length < 100
==================================================================================================
	Gold: 5.2
	Predicted: 0.9
	F : 0.1
	P, R  : 0.667, 0.054

==================================================================================================
Misidentified:
==================================================================================================
	Seens: 100.0
	Non Seens: 0.0
	Frequently Seen: 18.3
	Barely Seen: 81.7
	Partially Seen: 0.0
	Partially Seen (Without stop words): 0.0
	Three Token MWEs: 15.1
	Two Token MWEs: 83.9
	MWTs: 0.0

==================================================================================================
Non-identified:
==================================================================================================
	Seens: 13.5
	Non Seens: 86.5
	Frequently Seen: 1.7
	Barely Seen: 11.8
	Partially Seen: 79.7
	Partially Seen (Without stop words): 67.1
	Three Token MWEs: 23.7
	Two Token MWEs: 68.6
	MWTs: 0.0

==================================================================================================
	XP Ends: 25/2 (14 h:46)
==================================================================================================

Process finished with exit code 0
