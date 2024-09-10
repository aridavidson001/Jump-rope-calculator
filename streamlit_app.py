import streamlit as st

st.title("Jump Rope Freestyle Score Calculator!")
url = "https://rules.ijru.sport/technical-manual/calculations/freestyle/single-rope"
st.write("Developed By Ari Davidson. Scoring Calculations Taken From [IJRU Rulebook 4.0.0](%s)" % url)
st.write("Input difficulty levels separated by commas")
st.write("(Example: 3, 5, 6)")
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
    return (totalDifficultyRaw)


#calculates the minimum and maximum with presentation and it's parts
def calculatePresentation(totalScore):
    maxWithPresentation = round(
        (totalScore + (totalScore * minPresentationPercent)), 2)
    minWithPresentation = round((totalScore * minPresentationPercent), 2)
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
    st.write("Total Raw Difficulty:", totalDifficultyRaw)
    st.write("Presentation Max:", presentation[0], ",  Min:", presentation[1])
    st.write("Entertainment Max:", presentation[2], ",  Min:", presentation[3])
    st.write("Execution Max:", presentation[4], ",  Min:", presentation[5])
    st.write("Musicality Max:", presentation[6], ",  Min:", presentation[7])
    st.write("Creativity Max:", presentation[8], ",  Min:", presentation[9])
    st.write("Variety Max:", presentation[10], ",  Min:", presentation[11])

input = str(st.text_input(""))
# Checks if there is an input and if it works
if(input!= ""):
    try:
        difficulty = calculateDifficulty(editInput(input))
        presentation = calculatePresentation(difficulty)
        printOutput(difficulty, presentation)
    except ValueError:
        st.write("Please check your input and make sure it follows the example, something isn't right!")