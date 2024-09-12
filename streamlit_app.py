import streamlit as st
import pandas as pd

st.title("Jump Rope Freestyle Score Calculator!")
url = "https://rules.ijru.sport/technical-manual/calculations/freestyle/single-rope"
st.subheader("Scoring Calculations and Rules Taken From [IJRU Rulebook 4.0.0](%s)" % url)
st.write("Developed and Maintained By Ari Davidson")


maxPresentationAffect = 0.60
minEntertainmentPercent = maxPresentationAffect * 0.25 # 15% - 0.15
minExecutionPercent = maxPresentationAffect * 0.25 # 15% - 0.15
minMusicalityPercent = maxPresentationAffect * 0.20 # 12% - 0.12 
minCreativityPercent = maxPresentationAffect * 0.15 # 9% - 0.09
minVarietyPercent = maxPresentationAffect * 0.15 # 9% - 0.09


#equation taken from IJRU for calculating the point value per level
def getPointValue(level):
    if level!= 0:
        pointValue = round(0.1 * (1.5**level), 2)
    else:
        pointValue = 0
    return pointValue


#cycles through all tricks and adds difficulty together
def calculateNewDifficulty(input):
    totalDifficultyRaw = 0
    for trick in input:
        totalDifficultyRaw = round(
            (totalDifficultyRaw + getPointValue(int(trick))), 2)
    averagedDifficulty = round((totalDifficultyRaw/3), 2)
    return (averagedDifficulty)
def calculateOldDifficulty(input):
    totalDifficultyRaw = 0
    for trick in input:
        totalDifficultyRaw = round(
            (totalDifficultyRaw + getPointValue(int(trick))), 2)
    averagedDifficulty = round((totalDifficultyRaw), 2)
    return (averagedDifficulty)


#calculates the minimum and maximum with presentation and it's parts
def calculatePresentation(totalScore):
    maxWithPresentation = round((totalScore + (totalScore * maxPresentationAffect)), 2)
    minWithPresentation = round(totalScore - (totalScore * maxPresentationAffect), 2)
    maxWithEntertainment = round((totalScore + (totalScore * minEntertainmentPercent)), 2)
    minWithEntertainment = round((totalScore - (totalScore * minEntertainmentPercent)), 2)
    maxWithExecution = round((totalScore + (totalScore * minExecutionPercent)), 2)
    minWithExecution = round((totalScore - (totalScore * minExecutionPercent)), 2)
    maxWithMusicality = round((totalScore + (totalScore * minMusicalityPercent)), 2)
    minWithMusicality = round((totalScore - (totalScore * minMusicalityPercent)), 2)
    maxWithCreativity = round((totalScore + (totalScore * minCreativityPercent)), 2)
    minWithCreativity = round((totalScore - (totalScore * minCreativityPercent)), 2)
    maxWithVariety = round((totalScore + (totalScore * minVarietyPercent)), 2)
    minWithVariety = round((totalScore - (totalScore * minVarietyPercent)), 2)
    dict = {"presMax": maxWithPresentation,
        "presMin":  minWithPresentation,
        "entertainMax": maxWithEntertainment,
        "entertainMin": minWithEntertainment,
        "execMax": maxWithExecution,
        "execMin": minWithExecution,
        "musicMax": maxWithMusicality,
        "musicMin": minWithMusicality,
        "createMax": maxWithCreativity,
        "createMin": minWithCreativity,
        "varietyMax": maxWithVariety,
        "varietyMin": minWithVariety}
    return (dict)

def calculateEditedPresentation(totalScore, entertainment, execution, musicality, creativity, variety):
    print(totalScore)
    editedScore = (totalScore 
    + (totalScore*execution)
    + (totalScore*entertainment)
    + (totalScore*musicality)
    + (totalScore*creativity)
    + (totalScore*variety))
    return(round(editedScore, 2))

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
def printOutput( presentation):
    output = [
    ["Presentation", presentation["presMax"], presentation["presMin"]],
    ["Entertainment", presentation["entertainMax"], presentation["entertainMin"]],
    ["Execution", presentation["execMax"],  presentation["execMin"]],
    ["Musicality", presentation["musicMax"],  presentation["musicMin"]],
    ["Creativity", presentation["createMax"],  presentation["createMin"]],
    ["Variety", presentation["varietyMax"],  presentation["varietyMin"]]]
    return( output)
st.header("Calculator")
input = str(st.text_input(label="", placeholder="Input difficulty levels(2, 3, 4, etc.)"))
with st.popover("Customize Presentation"):
    entertainment = st.slider("Entertainment", min_value=-0.15, max_value=0.15, value=0.00)
    execution = st.slider("Execution", min_value=-0.15, max_value=0.15, value=0.00)
    musicality = st.slider("Musicality", min_value=-0.12, max_value=0.12, value=0.00)
    creativity = st.slider("Creativity", min_value=-0.09, max_value=0.09, value=0.00)
    variety = st.slider("Variety", min_value=-0.09, max_value=0.09, value=0.00)

# Checks if there is an input and if it works
if(input!= ""):
    try:
        difficulty = calculateNewDifficulty(editInput(input))
        presentation = calculatePresentation(difficulty)
        oldDifficulty = calculateOldDifficulty(editInput(input))
        oldPresentation = calculatePresentation(oldDifficulty)
        tab1, tab2 = st.tabs(["New Difficulty (Rulebook 4.0.0)", "Old Difficulty (Rulebook 3.0.0)"])
        with tab1:

            st.write("Difficulty: ", difficulty)

            st.write("Custom Presentation Score: ", round(calculateEditedPresentation(difficulty, entertainment, execution, musicality, creativity, variety), 2))
            st.write("Custom Presentation Percent: ", round((entertainment+execution+musicality+creativity+variety), 2) * 100)
            data = pd.DataFrame(printOutput(presentation), columns=("Presentation Type", "Max", "Min"))
            st.dataframe(data, hide_index=True)
        with tab2:
            st.write("Difficulty: ", oldDifficulty)
            st.write("Custom Presentation Score: ", round(calculateEditedPresentation(oldDifficulty, entertainment, execution, musicality, creativity, variety), 2))
            st.write("Custom Presentation Percent: ", (round((entertainment+execution+musicality+creativity+variety), 2) * 100))
          
            oldData = pd.DataFrame(printOutput(oldPresentation), columns=("Presentation Type", "Max", "Min"))
            st.dataframe(oldData, hide_index=True)
    except ValueError:
        st.write("Please check your input and make sure it follows the example, something isn't right!")
else:
    difficulty = calculateNewDifficulty(editInput("0"))
    presentation = calculatePresentation(difficulty)
    data = pd.DataFrame(printOutput(presentation), columns=("Presentation Type", "Max", "Min"))
    st.write("Difficulty: ", difficulty)
    st.dataframe(data, hide_index=True)

st.header("Rule Change in Calculating Difficulty Score")
st.write("The difficulty score will be the average of the power difficulty score, the wraps/releases difficulty score, and the multiples difficulty score.")
st.write("This effectively changes the equation for calculating the difficulty of a trick from")
st.write("$\ D = 0.1*1.5^x $")
st.write("to")
st.write("$\ D = \dfrac{0.1*1.5^x}{3} $")
st.write("As a result, these are the new point values for different levels compared to the old point values.")
oldVNewPointValues = pd.DataFrame(
                                [[0.5, 0.12, 0.04],
                                  [1, 0.15, 0.05],
                                  [2, 0.23, 0.08],
                                  [3, 0.34, 0.11],
                                  [4, 0.51, 0.17],
                                  [5, 0.76, 0.25],
                                  [6, 1.14, 0.38],
                                  [7, 1.76, 0.57],
                                  [8, 2.56, 0.85],], 
                                  columns=("Level", "Old Point Value", "New Point Value"))
st.dataframe(oldVNewPointValues, hide_index=True)
st.header("Determining the Level of a Trick")
st.subheader("Gymnastics and Power")
gymnasticsAndPower = pd.DataFrame(
                                    [
                                        [1, " - Cartwheel <br> Roundoff <br> Forward/backward roll <br> Butterfly Kick (B kick)", 
                                        "Standing to Frog/Push-up without pulling the rope <br> Frog/Push-up to standing without pulling the rope <br> Basic power skill entrance"],
                                        [2, "Front Handspring <br> Kip <br> Dive roll", 
                                        "Frog <br> Push-up <br> Crab <br> Split"],
                                        [3, "Aerial <br> Barani <br> Back Handspring <br> ¾ flip (front ¾ flip landing in a crab position or back ¾ landing in a push-up position)", 
                                        "One-handed power Frog/Push-up to standing <br> Frog from Two Feet(no revolutions of the rope) <br> Frog to single bounce cross landing in standing"],
                                        [4, "Front Aerial <br> Front Flip <br> Back Flip <br> Butterfly Twist (B twist)", 
                                        "Push-up to Pushup <br> Frog to Pushup <br> Punch Frog"],
                                        [5, "Flips with twists (half or full) <br> Front flip with double under <br> ¾ flip with triple under", 
                                        "One-handed Punch Frog <br> Double Under Frog <br> Push-Up to Push-Up or Belch with double under or cross"],
                                        [6, "Flips with 1.5 or 2 Spins <br> Kip Whip <br> Front Handspring Whip <br> Backflip with Triple Under <br> Front Flip with Triple Under", 
                                        "Split to backwards open single bounce landing in standing (must be full split with rope on the ground before pulling)"],
                                        [7, "Back Flip with a TJ <br> Kip Whip with a Cross", 
                                        "Sunny D <br> Darkside <br> Triple under landing in Frog"],
                                        [8, "Double Back <br> Triple Full <br> Back Flip Triple Under with an AS Cross", 
                                        "Moneymaker"]],
                                        columns=("Level", "Gymnastics", "Power"))

st.markdown(gymnasticsAndPower.to_html(index=False), unsafe_allow_html=True)
st.write("")

st.write("""### Gymnastics and Power Modifiers
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
""")
multiplesAndRopeManipulation = pd.DataFrame(
    [
        [0.5, "", "Foot work (performed at a slow pace) <br> Criss Cross <br> Basic arm wrap"],
        [1, "Double Under", "Restricted side-swing <br> Toad <br> Crougar <br> EB <br> Basic rope release <br> Foot work (performed at a fast pace)"],
        [2, "Triple Under <br> Double Under with One-arm Restriction", "AS <br> CL <br> TS <br> Elephant toad <br> KN <br> EM <br> Caboose <br> Mic release <br> Crougar wrap"],
        [3, "Quadruple Under <br> Triple Under TJ (Triple Under toad) <br> Double Under AS <br> Double Under mic <br> Triple Under EK", "Lasso release caught in the air <br> Forward French Trick <br> One-arm restriction with a double wrap (For example, Toad jumped with double wrap) <br> AS go-go/crazy-cross <br> Catching a mic release in a one arm restriction"],
        [4, "Quintuple Under <br> Quadruple Under TJ <br> Triple Under EB TJ <br> Triple Under AS <br> Double Under AS×AS", "Backward French-trick <br> Catching mic release in backward two-arm restriction"],
        [5, "Sextuple Under <br> Quintuple Under EB <br> Quadruple Under CL <br> Hummingbird <br> Double Under AS switch TS <br> Double Under AS Switch CL", ""],
        [6, "Quintuple Under AS <br> Triple Under AS CL TS <br> Quintuple EB open AS <br> Quadruple Under AS×AS <br> Backward Quadruple Under AS open <br> landing in AS", ""],
        [7, "Quintuple Under with under-the-leg mic caught in one handed restricted position <br> Quintuple Under 360° with backward leg-over cross and forward leg-over cross", ""],
        [8, "Quintuple with under-the-leg mic caught in a two handed restriction <br> Backwards quintuple under TS open CL open AS", ""]
    ],
    columns=["Level", "Multiples", "Rope Manipulation"],
)
st.markdown(multiplesAndRopeManipulation.to_html(index=False), unsafe_allow_html=True)
st.write("")
st.write('''
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
