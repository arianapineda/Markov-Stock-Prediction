"""
Stock market prediction using Markov chains.

"""
from collections import defaultdict
import comp140_module3 as stocks
import random

### Model

def markov_chain(data, order):
    """
    Create a Markov chain with the given order from the given data.

    inputs:
        - data: a list of ints or floats representing previously collected data
        - order: an integer repesenting the desired order of the markov chain

    returns: a dictionary that represents the Markov chain
    """
    dicti = defaultdict(int)
    key_dict = defaultdict(int)

    #set up keys - DONE
    for num in range(len(data)-order):
        dicti[tuple(data[num:num+order])] = {}
    #add possibilities to the nested dictionary- DONE
    for key in dicti:
        key_dict = defaultdict(int)      
        for num in range(len(data)-order):
            if tuple(data[num:num+order])==key:
                key_dict[data[num+order]]+=1
              
        
        dicti[key] = key_dict
    # convert frequencies to probabilities
    for key in dicti:
        count = 0
        for keys in dicti[key]:
            count+=dicti[key][keys]
        for keys in dicti[key]:
            dicti[key][keys] = dicti[key][keys]/count        
   
       
    
    return dicti

def weightedprob(dicti):
    """
    Returns a randomly-selected bucket based on weighted probabilities.
    
    inputs:
        -dicti: a dictionary representing a Markov chain
        
    returns: an integer representing the predicted next bucket    
    """
    count = 0
    randomprob = random.random()
    for key in dicti:
        count+=dicti[key]
        if count>=randomprob:
            return key
    return None	
def predict(model, last, num):
    
    """
    Predict the next num values given the model and the last values.

    inputs:
        - model: a dictionary representing a Markov chain
        - last: a list (with length of the order of the Markov chain)
                representing the previous states
        - num: an integer representing the number of desired future states

    returns: a list of integers that are the next num states
    """
    
    finallist=[]
    modifiedlast=list(last)
 
    while len(finallist)!=num:
        nextnum = random.randint(0,3)

        for tup in model:
            if tuple(modifiedlast) == tuple(tup):
                nextnum = weightedprob(model[tup])
                break

        modifiedlast.append(nextnum)
        finallist.append(nextnum)
        modifiedlast.pop(0)           
     
    return finallist     

  
### Error

def mse(result, expected):
    """
    Calculate the mean squared error between two data sets.

    The length of the inputs, result and expected, must be the same.

    inputs:
        - result: a list of integers or floats representing the actual output
        - expected: a list of integers or floats representing the predicted output

    returns: a float that is the mean squared error between the two data sets
    """
    count = 0
    for spot in range(len(result)):
        count+=(result[spot]-expected[spot])**2
    return count/len(result)    


### Experiment

def run_experiment(train, order, test, future, actual, trials):
    """
    Run an experiment to predict the future of the test
    data given the training data.

    inputs:
        - train: a list of integers representing past stock price data
        - order: an integer representing the order of the markov chain
                 that will be used
        - test: a list of integers of length "order" representing past
                stock price data (different time period than "train")
        - future: an integer representing the number of future days to
                  predict
        - actual: a list representing the actual results for the next
                  "future" days
        - trials: an integer representing the number of trials to run

    returns: a float that is the mean squared error over the number of trials
    """
    count = 0
    
    for trial in range(trials):
        count+=mse(predict(markov_chain(train,order),test,future),actual)
        trial+=1
    return count/trials


### Application

def run():
    """
    Run application.

    You do not need to modify any code in this function.  You should
    feel free to look it over and understand it, though.
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()

    # Get stock data and process it

    # Training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    #   Comment these 2 lines out if you don't want to see the plots
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)
        print()


run()