import hashlib,sys,json
import random

def hashFunction(data):

    if type(data) != str:
        data = json.dumps(data, sort_keys=True)

    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(data).hexdigest(), "utf-8")
    else:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()



def makeTransaction(amount=3):
    operations = [-1,1]
    sign = random.choice(operations)
    user2Pays = sign * amount
    user1Pays = user2Pays * -1
    

    uniqueHash = hashFunction("user 1 / user 2")

    
    return  f"User 1: {user1Pays} User 2: {user2Pays} transaction hash : {uniqueHash}"



def updateState(amount, state):
    state = state.copy()

    for amo in amount:
        if amo in state.keys():
            state[amo] += amount[amo]
        else:
            state[amo] = amount[amo]
    return state

accountBalance = 0

def isValid(txn,keys):
    if sum(txn.values()) is not 0:
        return False
    for key in txn.keys():
        if key in state.keys():
            accountBalance = txn[key]
        else:
            accountBalance = 0
            if (accountBalance + txn[key]) < 0:
                return False
    return True
transactionsBuffer = [makeTransaction() for i in range(30)]




state = {u'Alice':5,u'Bob':5}

genesisBlockAmount = [state]

genesisBlockContents = {u"block_number": 0, u"parent_hash": None,u"txns": genesisBlockAmount}


genesisHash = hashFunction(genesisBlockContents)


genesisBlock = {u"hash": genesisHash, u"contents: ": genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)








chain = [genesisBlock]

def makeBlock(txns,chain):
    parent_block = chain[-1]







print(genesisBlockStr)

print(transactionsBuffer)
print(isValid({u'Alice': -3, u'Bob': 3},state))
print(isValid({u'Alice': -2, u'Bob': 3},state))
print(isValid({u'Alice': -3, u'Bob': 4},state))
print(isValid({u'Alice': -7, u'Bob': 7},state))
print(isValid({u'Alice': -4, u'Bob': 4},state))
