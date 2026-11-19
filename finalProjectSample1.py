# Harrison Niswander
# ECET 114 / ITC 150
# 11-15-26
# This program is allows the user to play hangman and has a leaderboard

#--------------------------------------------------------------------------------------------
#                                           FUNCTIONS
#--------------------------------------------------------------------------------------------

# obtainMysteryWord() -> function to obtain mystery word from file of words
def obtainMysteryWord():
    # open wordBank.txt
    wordFile = open("wordBank.txt", 'r')

    # list to hold all words in file
    wordList = []

    # for -> read all lines of words into list
    for word in wordFile:
        # add word to list
        wordList.append(word.strip())

    # close file
    wordFile.close()

    # obtain random element
    import random
    randWord = random.choice(wordList)
    
    # return mystery word
    return randWord

# createBlankList() -> convert mystery word into list and make list with blanks for each letter
def createBlankList(word):
    # list to hold mystery word
    lstMystery = [" "] * len(word)

    # variable to hold count
    count = 0

    # convert word into list with each character as an element of the list
    for char in word:
        # add current char to list
        lstMystery[count] = char

        # increment count
        count += 1

    # create list that holds user's guess (blanks)
    lstGuess = [""] * len(word)

    # populate guessList with blanks since no guesses made
    for index in range(len(word)):
        # add blank (_)
        lstGuess[index] = "_"

    return lstMystery, lstGuess

# obtain1OR2() -> obtain response from user for given prompt (either 1 or 2)
def obtain1OR2(prompt):
    # boolean for good data entered
    goodData = False

    # while -> ask user for 1 or 2 until they give it
    while goodData == False:
        # determine user response (1 or 2)
        try:
            # obtain user response
            userAnswer = int(input(prompt))

            if(userAnswer == 1 or userAnswer == 2):
                # entered 1 or 2
                goodData = True

            else:
                print("\nPlease Enter in either 1 or 2.\n")
                
        # except -> non numeric value entered
        except ValueError:
            print("\nError: Please Enter only numeric data.\n")

        # except -> other errors
        except Exception:
            print("\nAn Error has occured please try again.\n")

    # return answer (1 or 2)
    return userAnswer

# checkWord() -> check to see if guess was correct
def checkWord(mysteryW, guess):
    # check to see if mystery word was guessed
    if(mysteryW == guess.lower().strip()):
        return True
   
    # else -> guess was wrong
    else:
        return False

# checkLetter() -> check to see if letter is present in mList (if so add to guess List)
def checkLetter(mList, gList, letter):
    # variable to keep track of indexing and bool for if guess is Right
    count = 0
    guessRight = False

    # for -> go through and see if letter is present in word
    for char in mList:
        if(char == letter):
            # add correct guess to guess list
            gList[count] = letter

            # flip boolean since guess was right
            guessRight = True

        # increment count
        count += 1

    # return guess list and whether guess was correct
    return gList, guessRight

def generateLeaderboard(userName, userGuesses, userWord):
    # open leaderboard file
    leaderboardFile = open("leaderboard.txt", "r")

    # save contents into each list
    name = []
    score = []
    word = []

    # read first line of leaderboard
    line = leaderboardFile.readline().strip()

    # while -> read through file until last line
    while line != "":
        temp = []
        temp = line.split(",")

        # add contents to each list
        name.append(temp[0])
        score.append(int(temp[1]))
        word.append(temp[2])

        # read next line
        line = leaderboardFile.readline().strip()

    # add user's new score
    name.append(userName)
    score.append(int(userGuesses))
    word.append(userWord)

    # leaderboard 2d list
    leaderboard = []

    # for -> combine lists into leaderboard 2d list (each row is record of name, score, word)
    for name, score, word in zip(name, score, word):
        # add to list
        leaderboard.append([name, score, word])


    # reorder leaderboard to be from lowest guess to highest guess (tie breaker is word alphabetical)
    leaderboard.sort(key=lambda row: (row[1], row[2]), reverse=False)

    print("Word of Fortune All Time Top 10\n")
    print(f"{'    \tName':<10}   {'  Guesses':<3}   {'\tWord':<12}")
    print("-" * 40)

    # display sorted leaderboard
    for place in range(10):
        print(f"{place + 1}.)\t{leaderboard[place][0]:<10}   {leaderboard[place][1]:<3}  \t{leaderboard[place][2]:<12}")

def playHangman():
    # mystery word (word that user will guess)
    mysteryWord = obtainMysteryWord()
    
    # convert word into list and list with blanks
    mysteryList, guessList = createBlankList(mysteryWord)

    # explain rules
    print("Welcome to Word of Fortune!\nRules: \n")

    # boolean for if word is solved
    wordSolved = False

    # Create a count variable
    attempts = 0

    # while -> allow user to keep guessing until word is solved
    while wordSolved == False:
        # Increment attempt count
        attempts += 1

        # for -> display all blanks in guessList
        print("Mystery Word: ", end=" ")
        for blank in guessList:
            print(blank, end=" ")

        # ask user for guess
        guessSolveAnswer = obtain1OR2("\nWould you like to guess a letter or solve [1 - Guess letter | 2 - Solve]: ")

        # if-> user wishes to guess letter
        if(guessSolveAnswer == 1):
            # obtain user letter guess
            userLetterGuess = input("Enter in guess (letter): ")

            # boolean for if guess is right or not
            guessRight = False

            # check guess
            guessList, guessRight = checkLetter(mysteryList, guessList, userLetterGuess)

            # USE guessRight Variable to keep track of Score!!!!
            #
            #
            if(guessRight == True):
                print("Correct Guess\n")

            else:
                print("Wrong Guess\n")


        # else -> user wishes to solve word
        else:
            # obtain user letter guess
            userWordGuess = input("Enter in guess (word): ")
            
            # boolean to hold whether word was solved
            wordGCorrect = False

            # check if word matches mystery word
            wordGCorrect = checkWord(mysteryWord, userWordGuess)

            # if -> check if guess was correct
            if(wordGCorrect == True):
                # word solved flip boolean
                wordSolved = True

                # print guess was right
                print("Your guess was correct!\n")

            else:
                print("Incorrect word guess!\n")

        # boolean for if there are still blanks
        missingLetter = False

        # for -> check to see if guess List is complete (no more blanks)
        for g in guessList:
            # if -> check to see if there are still blanks
            if(g == "_"):
                # still has missing letter
                missingLetter = True

        # if-> no more missing letters then word is solved
        if (missingLetter == False):
            
            # flip boolean for word solved
            wordSolved = True

    print("Word is solved!\n\n")


#--------------------------------------------------------------------------------------------
#                                         MAIN BLOCK
#--------------------------------------------------------------------------------------------

#boolean for if user wishes to play game
playAgain = True

# while -> allow user to keep playing game until they say their done
while playAgain == True:

    # play the game
    playHangman()

    userResponse = obtain1OR2("Would you like to play again [1 - Yes | 2 - No]: ")

    # if -> 2 entered so no more playing
    if(userResponse == 2):
        # user doesn't want to play again
        playAgain = False

# thank you message
print("Thank you for playing Word of Fortune!")

# generateLeaderboard("Frank", 6, "hotdog")