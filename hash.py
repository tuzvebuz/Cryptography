import hashlib,sys,json
import random
from pprint import pprint
state = {
    "Alice": 7423,
    "Bob": 1589,
    "Charlie": 9345,
    "Diana": 276,
    "Eve": 6012,
    "Frank": 4897,
    "Grace": 8201,
    "Hank": 3456,
    "Ivy": 1234,
    "Jack": 9999
}

def hashFunction(data):

    if type(data) != str:
        data = json.dumps(data, sort_keys=True)

    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(data).hexdigest(), "utf-8")
    else:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()



def makeTransaction(sender,recipient,amount=5):
    operations = [-1,1]
    sign = random.choice(operations)
    user2Pays = sign * amount
    user1Pays = user2Pays * -1
    

    uniqueHash = hashFunction(f"{user1Pays} | {user2Pays}")

    
    return  {f"{sender}": user1Pays, f"{recipient}": user2Pays}



def updateState(amount, state):
    state = state.copy()

    for amo in amount:
        if amo in state.keys():
            state[amo] += amount[amo]
        else:
            state[amo] = amount[amo]
    return state







sub = list(state.keys())


def randomSender(): 

    sender = random.choice(sub)
    return sender

def randomReceiver():
    receiver = random.choice(sub)
    return receiver
    
txnBuffer = [makeTransaction(randomSender(), randomReceiver(), random.randint(0,10000)) for i in range(30)]





genesisBlockAmount = [state]

genesisBlockContents = {u"block_number": 0, u"parent_hash": None,u"txns": genesisBlockAmount}


genesisHash = hashFunction(genesisBlockContents)


genesisBlock = {u"Hash": genesisHash, u"contents": genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)








chain = [genesisBlock]

def makeBlock(txns,chain):
    parent_block = chain[-1]
    parentHash = parent_block["Hash"]
    block_number = parent_block[u"contents"][u'block_number'] +  1 
    txnCount = len(txns)

    block_contents = {
            u"block_number": block_number,
            u"parentHash": parentHash,
            u'txnCount': len(txns),
            "txns": txns

        }
    blockHash = hashFunction(block_contents)

    block = {u"Hash": blockHash, "contents": block_contents}

    return block
blockSizeLimit = 2 


def isValid(txn,state):
    # If the amounts don't add up, if they seem to be generating currencies out of no where, return false

    
    for key in txn.keys():
        if key in state.keys(): 
            acctBalance = state[key]
        else:
            acctBalance = 0
        if (acctBalance + txn[key]) < 0:
            return False
    
    return True



while len(txnBuffer) > 0:
    bufferStartSize = len(txnBuffer)
    
    txnList = []

    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        # TODO CHECK VALIDITY
        txnList.append(newTxn)
        state = updateState(newTxn, state)

    myBlock = makeBlock(txnList, chain)
    chain.append(myBlock)
    print("New Block added")

pprint(genesisBlockStr)
for i in chain:
    pprint(i)
