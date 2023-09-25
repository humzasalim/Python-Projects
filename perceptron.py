#This takes five arguments which are the threshold, adjustment number,
#initial weights, examples and number of passes
## adjusts the weight and learns from the examples,
# No value returned
def perceptron(threshold, adjustment, weights, examples, passNum):
    # initial print to show starting weight and threshold
    print("Starting weights:", weights)
    print("Threshold:",threshold, "Adjustment:",adjustment)

    for currentPassNum in range(passNum): # loop for pass number (pass 1, pass 2...)
        print("\nPass", currentPassNum + 1)
        print()
        for example in examples:
            answer = example[0] 
            input = example[1] 
            print("inputs:", input)
            
            prediction = checkExample(threshold, input, weights)
            print("prediction:",prediction,"answer:", answer) 
            if (prediction != answer):
                if (answer): 
                    weightsUp = adjustmentUp(adjustment, input, weights)
                    weights = weightsUp
                else: 
                    weightsDown = adjustmentDown(adjustment, input, weights)
                    weights = weightsDown
            print("adjusted weights:",weights)
    return

# finds sum and returns true if it is greater than the threshold, if it is otherwise then it returns false
def checkExample(threshold, example, weights):
    sum = 0
    for i in range(len(weights)):
        sum += (example[i]*weights[i])
    if sum > threshold:
        return True
    else: 
        return False

# increases weight element and returns the adjusted weight
def adjustmentUp(adjustment, example, weights):
    for i in range(len(example)):
        if (example[i] == 1):
            weights[i] += adjustment
    return weights

# decreases weight element and returns the adjusted weight
def adjustmentDown(adjustment, example, weights):
    for i in range(len(example)):
        if (example[i] == 1):
            weights[i] -= adjustment
    return weights
