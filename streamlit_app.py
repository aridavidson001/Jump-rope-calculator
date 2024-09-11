import streamlit as st

st.title("Jump Rope Freestyle Score Calculator!")
url = "https://rules.ijru.sport/technical-manual/calculations/freestyle/single-rope"
st.subheader("Scoring Calculations and Rules Taken From [IJRU Rulebook 4.0.0](%s)" % url)
st.write("Developed and Maintained By Ari Davidson")


minPresentationPercent = 0.60
minEntertainmentPercent = minPresentationPercent * 0.25
minExecutionPercent = minPresentationPercent * 0.25
minMusicalityPercent = minPresentationPercent * 0.20
minCreativityPercent = minPresentationPercent * 0.15
minVarietyPercent = minPresentationPercent * 0.15


#equation taken from IJRU for calculating the point value per level
def getPointValue(level):
    if level!= 0:
        pointValue = round(0.1 * (1.5**level), 2)
    else:
        pointValue = 0
    return pointValue


#cycles through all tricks and adds difficulty together
def calculateDifficulty(input):
    totalDifficultyRaw = 0
    for trick in input:
        totalDifficultyRaw = round(
            (totalDifficultyRaw + getPointValue(int(trick))), 2)
    averagedDifficulty = round((totalDifficultyRaw/3), 2)
    return (averagedDifficulty)


#calculates the minimum and maximum with presentation and it's parts
def calculatePresentation(totalScore):
    maxWithPresentation = round(
        (totalScore + (totalScore * minPresentationPercent)), 2)
    minWithPresentation = round(totalScore - (totalScore * minPresentationPercent), 2)
    maxWithEntertainment = round(
        (totalScore + (totalScore * minEntertainmentPercent)), 2)
    minWithEntertainment = round(
        (totalScore - (totalScore * minEntertainmentPercent)), 2)
    maxWithExecution = round((totalScore + (totalScore * minExecutionPercent)),
                             2)
    minWithExecution = round((totalScore - (totalScore * minExecutionPercent)),
                             2)
    maxWithMusicality = round(
        (totalScore + (totalScore * minMusicalityPercent)), 2)
    minWithMusicality = round(
        (totalScore - (totalScore * minMusicalityPercent)), 2)
    maxWithCreativity = round(
        (totalScore + (totalScore * minCreativityPercent)), 2)
    minWithCreativity = round(
        (totalScore - (totalScore * minCreativityPercent)), 2)
    maxWithVariety = round((totalScore + (totalScore * minVarietyPercent)), 2)
    minWithVariety = round((totalScore - (totalScore * minVarietyPercent)), 2)

    return ([
        maxWithPresentation, minWithPresentation, maxWithEntertainment,
        minWithEntertainment, maxWithExecution, minWithExecution,
        maxWithMusicality, minWithMusicality, maxWithCreativity,
        minWithCreativity, maxWithVariety, minWithVariety
    ])


#takes input and turns it into a list of tricks
def editInput(text):
    text.replace(", ", ",")
    text.replace(";", ",")
    text.replace("; ", ",")
    text.replace(".", ",")
    text.replace(". ", ",")
    trickList = text.split(",")
    return trickList


#prints the output
def printOutput(totalDifficultyRaw, presentation):
    return(["Averaged Difficulty Score:", totalDifficultyRaw, "", ""],
    ["Presentation Max:", presentation[0], "Min:", presentation[1]],
    ["Entertainment Max:", presentation[2], "Min:", presentation[3]],
    ["Execution Max:", presentation[4], "Min:", presentation[5]],
    ["Musicality Max:", presentation[6], "Min:", presentation[7]],
    ["Creativity Max:", presentation[8], "Min:", presentation[9]],
    ["Variety Max:", presentation[10], "Min:", presentation[11]])
st.subheader("Calculator")
input = str(st.text_input(label="", placeholder="Input difficulty levels(2, 3, 4, etc.)"))
# Checks if there is an input and if it works
if(input!= ""):
    try:
        difficulty = calculateDifficulty(editInput(input))
        presentation = calculatePresentation(difficulty)
        st.dataframe(printOutput(difficulty, presentation), hide_index=True)

    except ValueError:
        st.write("Please check your input and make sure it follows the example, something isn't right!")
else:
    difficulty = calculateDifficulty(editInput("0"))
    presentation = calculatePresentation(difficulty)
    st.dataframe(printOutput(difficulty, presentation), hide_index=True)
    print(printOutput(difficulty, presentation))
st.markdown('''
### Rule Change in Calculating Difficulty Score
The difficulty score will be the average of the power difficulty score, the wraps/releases difficulty score, and the multiples difficulty score

            
This effectively changes the equation for calculating the difficulty of a trick from 
            
$\ D = 0.1*1.5^x $ 
            
to 
            
$\ D = \dfrac{0.1*1.5^x}{3} $\
            

As a result, these are the new point values for different levels compared to the old point values
            
| Level | Old Point Value | New Point Value|
| ---  | --- | --- |
| 0.5  | 0.12 | 0.04 |
| 1 | 0.15 | 0.05 |   
| 2 | 0.23 | 0.08 |   
| 3 | 0.34 | 0.11 |   
| 4 | 0.51 | 0.17 |   
| 5 | 0.76 | 0.25 |   
| 6 | 1.14 | 0.38 |   
| 7 | 1.76 | 0.57 |   
| 8 | 2.56 | 0.85 |   
# Determining the Level of a Trick

### Gymnastics and Power

> | Level | Gymnastics | Power |
> | ----- | -------- | -------- |
> | 1     | Cartwheel, Roundoff, Forward/backward roll, Butterfly Kick (B kick) | Standing to Frog/Push-up without pulling the rope, Frog/Push-up to standing without pulling the rope, Basic power skill entrance |
> | 2     | Front Handspring, Kip, Dive roll | Frog, Push-up, Crab, Split | 
> | 3     | Aerial, Barani, Back Handspring, ¾ flip (front ¾ flip landing in a crab position or back ¾ landing in a push-up position)| One-handed power Frog/Push-up to standing, Frog from Two Feet(no revolutions of the rope), Frog to single bounce cross landing in standing |
> | 4     | Front Aerial, Front Flip, Back Flip, Butterfly Twist (B twist) | Push-up to Pushup, Frog to Pushup, Punch Frog |
> | 5     | Flips with twists (half or full), Front flip with double under, ¾ flip  with triple under  | One-handed Punch Frog, Double Under Frog, Push-Up to Push-Up or Belch with double under or cross |
> | 6     | Flips with 1.5 or 2 Spins, Kip Whip, Front Handspring Whip, Backflip with Triple Under, Front Flip with Triple Under | Split to backwards open single bounce landing in standing (must be full split with rope on the ground before pulling) |
> | 7     | Back Flip with a TJ, Kip Whip with a Cross  | Sunny D, Darkside, Triple under landing in Frog |
> | 8     | Double Back, Triple Full, Back Flip Triple Under with an AS Cross | Moneymaker |
> 
### Gymnastics and Power Modifiers
> - +1 for Cross performed with power or gymnastics skills and/or flips
> 
> - +1 to the level of a multiple landing in Push-up, Split or Crab position
> 
> - +2 to the level of the starting skill if landing in a frog position
> 
> - +1 for assisted flips without supporting interaction
> 
> - -1 for assisted flips with supporting interactions all the way around
> 
> - +1 for every 90-degree turn in power when the rope is pulled (90° = +1,  180° = +2,  270° = +3,  etc.)
> 
> - -1 for gymnastics with rope held with only one hand and not jumping the rope (for example, one-hand handspring (L2) with both handles in one hand (-1) = L1; front aerial (L3) with both handles in one hand (-1) = L2)
>
--------------------------------------------------
### Multiples and Rope Manipulation
> | Level | Multiples | Rope Manipulation |
> | ----- | -------- | ----- |
> | 0.5   |          | Foot work (performed at a slow pace), Criss Cross, Basic arm wrap | 
> | 1     | Double Under | Restricted side-swing, Toad, Crougar, EB, Basic rope release, Foot work (performed at a fast pace) |
> | 2     | Triple Under, Double Under with One-arm Restriction | AS, CL, TS, Elephant toad, KN, EM, Caboose, Mic release, Crougar wrap |
> | 3     | Quadruple Under, Triple Under TJ (Triple Under toad), Double Under AS, Double Under mic, Triple Under EK  | Lasso release caught in the air, Forward French Trick, One-arm restriction with a double wrap (For example, Toad jumped with double wrap), AS go-go/crazy-cross, Catching a mic release in a one arm restriction |
> | 4     | Quintuple Under, Quadruple Under TJ, Triple Under EB TJ, Triple Under AS, Double Under AS×AS | Backward French-trick, Catching mic release in backward two-arm restriction |
> | 5     | Sextuple Under, Quintuple Under EB, Quadruple Under CL, Hummingbird, Double Under AS switch TS, Double Under AS Switch CL |
> | 6     | Quintuple Under AS, Triple Under AS CL TS, Quintuple EB open AS, Quadruple Under AS×AS, Backward Quadruple Under AS open, landing in AS |
> | 7     | Quintuple Under with under-the-leg mic caught in one handed restricted position, Quintuple Under 360° with backward leg-over cross and forward leg-over cross |
> | 8     | Quintuple with under-the-leg mic caught in a two handed restriction, Backwards quintuple under TS open CL open AS |
>
### Multiples Modifiers
> - +1 for body rotation more than 270° in twist or flip direction (for example, EK, BC, full twist)
> 
> - +1 for every additional 180° turned in the air beyond a 360° turn when jumped. (540° = total +2,  720° = total +3,  900° = total +4,  etc.)
> 
### Rope Manipulation Modifiers
> - +1 for switch crosses (AS×AS, criss-cross×criss-cross, AS×CL as long as the arm on top changes, etc.)
> 
> - +1 per layer for go-go's/crazy criss-cross (one hand crosses twice across body, leg or arm without uncrossing)
> 
> - +1 (max +3) per extra wrap layer for wraps
> 
> - +1 for changing the direction of rope movement in the air (Note, skills like EK where the rope continues in the same direction but the athlete turns doesn't count)
> 
> - +1 for switching handles
> 
> - +1 for transition jumps (jumping a one-hand restricted skill and in one jump, jumping the opposite side one-hand restricted skill, such as crougar-crougar)
> 
> - +1 for each restricted arm catching the release when catching a release in a one-arm restricted position
> 
> - +1 to the release for releasing a handle in a restricted position if, and only if, the hand is completely behind the body (behind the back or behind both legs)
> 
> - +1 for catching a release with something other than a hand (such as scooping the rope, squeezing it with a body part, or landing the rope on a foot, shoulder, or similar, jumping the rope with the rope caught on a body part)
''')
