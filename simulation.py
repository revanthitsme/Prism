import numpy as np
import simpy
from networkgen import *
from models import *
from datetime import datetime

# used the libraries simpy(for simulation) and numpy

#input---------------------------------------------------------------------------------------------------------
n = int(input("Enter the number of nodes(n): "))
z = int(input("Enter the percent of slow nodes(z): "))
T_tx = int(input("Enter the mean interarrival time of transactions(T_tx): "))
high_cpu = int(input("Enter the percent of High CPU nodes: "))
B_Tx = int(input("Enter block interarrival time(in sec): "))

# Setup--------------------------------------------------------------------------------------------------------

# Global Variables
env = simpy.Environment()
stop_time = 5
all_balance=20 # initial balance of all users
invalid_ratio = 0.1
total_hash_power = 0 

node_list=[]
weights = []

# nodes creation
for i in range(n):
	speed = np.random.uniform()
	cpu = np.random.uniform()
	if speed<(z/100):
		speed = 0
	else:
		speed=1
	if cpu<(high_cpu/100):
		hash_power = 2
	else:
		hash_power = 1
	total_hash_power = total_hash_power+hash_power

	genesis_block = Block('gen','none',[],0,'none')
	node = Node(i,speed,genesis_block,genesis_block,hash_power)
	node_list.append(node)
	weights.append(1+9*speed)

#network generation
adj = networkgen(n,2,weights)
for i in range(n):
	for j in range(i+1):
		if(adj[i][j]==1):
			r_ij = np.random.uniform(10,500)
			if(node_list[i].speed==1 and node_list[j].speed==1):
				c_ij=100
			else:
				c_ij=5
			connect_j = link(j,r_ij,c_ij)
			connect_i = link(i,r_ij,c_ij)
			node_list[i].peers.append(connect_j)
			node_list[j].peers.append(connect_i)

# helper functions-----------------------------------------------------------------------------------------------------

# def get_balance(itr_blk): # returns list of balance of nodes from using gen to itr_node blockchain 
# 	calc_bal = []
# 	for i in range(n):
# 		calc_bal.append(all_balance)
# 	while itr_blk.level!= 0: #changed while condition from level
# 		trxn_blks = itr_blk.proposer_content #Assuming itr_blk is a leader. Assuming proposer blk content are direct list pointer nodes.
# 		for trnblk in trxn_blks:
# 			for  t in trnblk.trxn_list:
# 				if t.payer!=-1:
# 					calc_bal[t.payer] = calc_bal[t.payer]-t.coins
# 				calc_bal[t.payee] = calc_bal[t.payee]+t.coins
# 			itr_blk =  getpointertolevelleader(itr_blk.level-1)#How to get previous level leader?
# 	return calc_bal

# def get_trxns(itr_blk): # returns all trxns in blocks from genesis block to itr_node
# 	all_trxns = []
# 	while itr_blk.level!=0:#assuming itr_blk is leader block at last level
# 		trxn_blks = itr_blk.proposer_content #Assuming itr_blk is a leader. Assuming proposer blk content are direct list pointer nodes.
# 		for trnblk in trxn_blks:
# 			all_trxns.extend(trnblk.trxn_list)
# 		itr_blk = getpointertolevelleader(itr_blk.level-1)
# 	return list(set(all_trxns))

def get_txn_blks(blk):
	proposer_chain = [node_list[node_id].genesis_proposer_blk]
	voter_chains = node_list[node_id].voterchains
	transaction_blks = []
	all_votes = []

	for i in range(len(voter_chains)):
		voter_chain = voter_chains[i]
		votes= []
		while voter_chain!=None:
			votes.append(voter_chain.voterblock_content)
			voter_chain = voter_chain.parent_ptr
		all_votes.append(votes)
	

	for i in range(blk.level):
		level = i
		votes = []
		child_proposer_chain = []

		for j in all_votes:
			p = [x for x in j if x[0]=level]
			votes.extend(p)
		
		leader_blk = max(lst,key=lst.count)
		leader_blkid_level_i = leader_blk[1]

		for j in proposer_chain:
			if j.blk_id == leader_blkid_level_i:
				transaction_blks.append(j.proposer_content)
			child_proposer_chain.append(j.child_ptr_list)

		proposer_chain = child_proposer_chain
	
	return transaction_blks
		

def get_trxns(blk):
	trxn_blk_list = get_txn_blks(blk)
	trxn_list = []
	for i in trxn_blk_list:
		trxn_list.append(i.trxn_list)

	return trxn_list

def get_balance(blk):
	trxn_list = get_trxns(blk)
	calc_bal = []
	for i in range(n):
		calc_bal.append(all_balance)
	for t in trxn_list:
		if t.payer!=-1:
			calc_bal[t.payer] = calc_bal[t.payer]-t.coins
		calc_bal[t.payee] = calc_bal[t.payee]+t.coins
	return calc_bal

def get_parent(parent_id,check_blk): # returns parent blk if present in the tree from check_blk or returns 0
	if(check_blk.blk_id == parent_id):
		return check_blk
	elif (len(check_blk.child_ptr_list)==0):
		return 0
	else:
		for child in check_blk.child_ptr_list:
			temp = get_parent(parent_id,child)
			if temp!=0:
				return temp
		return 0 

def is_valid(node_id,blk): # returns parent_blk if valid or returns 0
	if(blk.block_type == "voter"):
		parent = get_parent(blk.parent_id,node_list[node_id].genesis_voterchains[blk.voterchainindex])
	# parent = get_parent(blk.parent_id,node_list[node_id].genesis_blk)
		if(parent!=0):
			lastvoterlevel = parent.voterblock_content[:-1][0]
			for i in blk.voterblock_content:
				if i[0]!=lastvoterlevel+1:
					return 0
				else:
					lastvoterlevel=lastvoterlevel+1

			if lastvoterlevel!=node_list[node_id].proposer_block.level:
				return 0
			else:
				return parent
		else:
			return 0

	elif blk.block_type == "proposer":
		parent = get_parent(blk.parent_id,node_list[node_id].genesis_proposer_blk)
		if(parent!=0):
			for child in parent.child_ptr_list:
				if blk.blk_id == child.blk_id:
					return 0 # already in blockchain
			return parent
		else:
			return 0
	elif blk.block_type == "transaction":
		for i in node_list[node_id].txn_blockpool:
			if i.blk_id == blk.blk_id:
				return 0

		return blk



	# if parent!=0: # has parent
	# 	done_trxns = get_trxns(parent)
	# 	repeated = [x for x in blk.trxn_list if x in done_trxns]
	# 	if len(repeated)>0:
	# 		return 0 # has a trxn from blockchain
	# 	for child in parent.child_ptr_list:
	# 		if blk.blk_id == child.blk_id:
	# 			return 0 # already in blockchain
	# 	calc_bal = get_balance(parent)
	# 	for t in blk.trxn_list:
	# 		if t.payer!=-1:
	# 			calc_bal[t.payer] = calc_bal[t.payer]-t.coins
	# 		calc_bal[t.payee] = calc_bal[t.payee]+t.coins
	# 	valid = True
	# 	for i in calc_bal:
	# 		if i<0:
	# 			valid = False
	# 	if valid: # valid
	# 		return parent
	# 	else:
	# 		return 0 # balance goes negative
	# return 0 # no parent

def child_num(node_id,parent_id): # returns the number of childs of parent
	parent = get_parent(parent_id,node_list[node_id].genesis_blk)
	return len(parent.child_ptr_list)

def add_orphans(node_id,blk): # adds the orphan blocks to blockchain
	for child_blk in node_list[node_id].orphan_blocks:
		if(child_blk.parent_id==blk.blk_id):
			child_blk.level = blk.level+1
			child_blk.parent_ptr = blk
			blk.child_ptr_list.append(child)

			if blk.block_type == "proposer":

				if(child.level>node_list[node_id].proposer_block.level):
					node_list[node_id].proposer_block = child
					print('longest chain changed for node %d' % node_id)
					create_blk(node_id)

			elif blk.block_type == "voter":
				if(child.level>node_list[node_id].voterchains[blk.voterchainindex].level):
					node_list[node_id].voterchains[blk.voterchainindex] = child
					print('longest chain changed for node %d' % node_id)
					create_blk(node_id)


			add_orphans(node_id,child_blk)


# trxn generation,broadcasting and routing----------------------------------------------
def route_trxn(node_id,trxn,lat,f_id):
	yield env.timeout(lat)
	print('Node %d : got packet %s from %d at %f' % (node_id,trxn.id,f_id,env.now))
	present = False
	for i in node_list[node_id].trxn_pool:
		if(i.id == trxn.id):
			present=True
	if(not present):
		node_list[node_id].trxn_pool.append(trxn)
		for l in node_list[node_id].peers:
			if(l.j!=f_id): 
				d_ij = np.random.exponential(96/l.c_ij) #Should change here the latency value
				lat = (l.r_ij+d_ij+8/l.c_ij)*(0.001)
				print('routing trxn %s to %d with delay = %f' % (trxn.id,l.j,lat))
				env.process(route_trxn(l.j,trxn,lat,node_id))

def broadcast_trxn(node_id,trxn):
	for l in node_list[node_id].peers:
		d_ij = np.random.exponential(96/l.c_ij)
		lat = (l.r_ij+ d_ij+ 8/l.c_ij)*(0.001)
		print('broadcasting trxn %s to %d with delay = %f' % (trxn.id,l.j,lat))
		env.process(route_trxn(l.j,trxn,lat,node_id))

def create_trxn(node_id):
	while True:
		yield env.timeout(np.random.exponential(T_tx))
		vendor = random.randint(0,n-2)
		if(vendor>=node_id):
			vendor=vendor+1
		valid = np.random.uniform()
		pay=0
		temp = get_balance(node_list[node_id].mining_blk)
		bal = temp[node_id]
		# if valid<invalid_ratio:
		# 	pay = bal+10000
		# else:
		pay = random.randint(1,bal)#we have not considered invalid trns yet.

		node_list[node_id].trxn_cnt = node_list[node_id].trxn_cnt+1
		trxn_id = str(node_id)+"_"+str(node_list[node_id].trxn_cnt)
		str_trxn = str(trxn_id)+": "+str(node_id)+" pays "+str(vendor)+" "+str(pay)+" coins"
		print(str_trxn + ' at %f' % env.now)
		real_trxn = Trxn(trxn_id,node_id,vendor,pay)
		broadcast_trxn(node_id,real_trxn)
		node_list[node_id].trxn_pool.append(real_trxn)

# block generation,broadcasting and routing------------------------------------------------------

def route_blk(node_id,blk,lat,f_id): #checked
	yield env.timeout(lat)
	print('Node %d : got blk %s from %d at %f' % (node_id,blk.blk_id,f_id,env.now))
	parent = is_valid(node_id,blk)

	if(parent!=0):
		
		if blk.block_type == "voter" or blk.block_type == "proposer":
			blk = Block(blk.blk_id,blk.block_type,blk.voterchainindex,blk.parent_id,blk.trxn_list,blk.proposer_content,blk.voterblock_content,parent.level+1,parent)
			parent.child_ptr_list.append(blk)

		elif blk.block_type == "transaction":
			blk = Block(blk.blk_id,blk.block_type,blk.voterchainindex,blk.parent_id,blk.trxn_list,blk.proposer_content,blk.voterblock_content,0,parent)
			node_list[node_id].txn_blockpool.append(blk)
	

		#blk = Block(blk.blk_id,parent.blk_id,blk.trxn_list,parent.level+1,parent)
		#parent.child_ptr_list.append(blk)
		node_list[node_id].timestamp_list.append([blk.blk_id,blk.block_type,blk.voterchainindex,blk.level,env.now,blk.parent_id])
		print('childs of parent = %d' %child_num(node_id,blk.parent_id))
		for l in node_list[node_id].peers:
			if(l.j!=f_id):
				d_ij = np.random.exponential(96/l.c_ij)   
				blk_size= len(blk.trxn_list)
				lat = (l.r_ij+d_ij+8*blk_size/l.c_ij)*(0.001)    # change latency information
				print('routing block %s to %d with delay = %f' % (blk.blk_id,l.j,lat))
				env.process(route_blk(l.j,blk,lat,node_id))

		if blk.block_type == "proposer":
			if blk.level > node_list[node_id].proposer_block.level:
				node_list[node_id].proposer_block = blk
				print('longest chain changed for node %d' % node_id)
				create_blk(node_id)
			add_orphans(node_id,blk) # why add to orphan blocks??
		elif blk.block_type == "voter":
			if blk.level > node_list[node_id].voterchains[blk.voterchainindex].level:
				node_list[node_id].voterchains[blk.voterchainindex] = blk
				print('longest chain changed for node %d' % node_id)
				create_blk(node_id)
			add_orphans(node_id,blk) # why add to orphan blocks??
	else:
		temp = get_parent(blk.parent_id,node_list[node_id].genesis_blk)
		if(temp==0):
			blk = Block(blk.blk_id,blk.parent_id,blk.trxn_list,0,'none')
			node_list[node_id].orphan_blocks.append(blk)
			node_list[node_id].timestamp_list.append([blk.blk_id,blk.block_type,blk.voterchainindex,blk.level,env.now,blk.parent_id])


def broadcast_blk(node_id,blk): #checked
	yield env.timeout(np.random.exponential()*(B_Tx*total_hash_power/node_list[node_id].hash_power)) # change block generation time
	is_route = False
	if blk.block_type == "proposer":

		if node_list[node_id].proposer_block.blk_id == blk.parent_id:
			node_list[node_id].proposer_block.child_ptr_list.append(blk)
			node_list[node_id].proposer_block = blk
			node_list[node_id].timestamp_list.append([blk.blk_id,blk.block_type,blk.voterchainindex,blk.level,env.now,blk.parent_id])
			is_route = True

	elif blk.block_type == "voter":
		if node_list[node_id].voterchains[blk.voterchainindex].blk_id == blk.parent_id:
			node_list[node_id].voterchains[blk.voterchainindex].child_ptr_list.append(blk)
			node_list[node_id].voterchains[blk.voterchainindex] = blk
			node_list[node_id].timestamp_list.append([blk.blk_id,blk.block_type,blk.voterchainindex,blk.level,env.now,blk.parent_id])
			is_route= True
			

	elif blk.block_type == "transaction":
		node_list[node_id].txn_blockpool.append(blk)
		is_route = True

	if is_route:
		print('longest chain changed for node %d' % node_id)
		print('childs of parent = %d' %child_num(node_id,blk.parent_id))
		print("broadcasting block %s at %f" %(blk.blk_id,env.now))
		for l in node_list[node_id].peers:
			d_ij = np.random.exponential(96/l.c_ij)
			blk_size= len(blk.trxn_list)
			lat = (l.r_ij+ d_ij+ 8*blk_size/l.c_ij)*(0.001)
			print('to %d with delay = %f' % (l.j,lat))
			env.process(route_blk(l.j,blk,lat,node_id))
		create_blk(node_id)

def get_proposer_blk_i(level):
	proposer_chain = [node_list[node_id].genesis_proposer_blk]
	for i in range(level):
		present_level = i
		child_proposer_chain = []
		for j in proposer_chain:
			child_proposer_chain.append(j.child_ptr_list)
		
		proposer_chain = child_proposer_chain

	return proposer_chain



def getvoterblkcontent(blk):
	last_proposer_block = node_list[node_id].proposer_block 
	last_level = last_proposer_block.level
	votes = blk.voterblock_content
	max_level = max([x[0] for x in votes])
	
	level = max_level+1
	voter_block_content = [] 
	while level <=last_level:
		proposer_chain_current = get_proposer_blk_i(level)
		voter_blk_id = proposer_chain_current[0].blk_id
		voter_block_content.append([level,voter_blk_id])
		level = level+1
	
	return voter_block_content




def create_blk(node_id): # checked
	node_list[node_id].blk_cnt = node_list[node_id].blk_cnt+1
	blk_id = 'b'+str(node_id)+'_'+str(node_list[node_id].blk_cnt)
	problist = []#we have to assign probs to diff blocks??
	x = np.random.choice(m+2,1,problist)
	if(x==0):#Trxn
		parent_id = None
		block_type = "transaction"
		trxn_list = []# get the trxn list
		node_list[node_id].trxn_cnt =node_list[node_id].trxn_cnt+1
		mining_trxnid = str(node_id)+'_'+str(node_list[node_id].trxn_cnt)
		trxn_list.append(Trxn(mining_trxnid,-1,node_id,50))
		calc_bal = get_balance(node_list[node_id].proposer_block)#change get_balance f
		done_trxns = get_trxns(node_list[node_id].proposer_block)
		useful_trxns = [ele for ele in node_list[node_id].trxn_pool if ele not in done_trxns]
		for t in useful_trxns:#check how many to include in a trxn blk
			if(((calc_bal[t.payer]-t.coins)>=0) and len(trxn_list)<1000):#change number from 1000
				trxn_list.append(t)
				calc_bal[t.payer] = calc_bal[t.payer]-t.coins
				calc_bal[t.payee] = calc_bal[t.payee]+t.coins

		level = 0
		parent_ptr = None
		proposer_content = None
		voterblock_content = None
		voterchainindex = -1
		new_blk = Block(blk_id,block_type,voterchainindex,parent_id,trxn_list,proposer_content,voterblock_content,level,parent_ptr)
	elif x==1:#proposer
		parent_id = node_list[node_id].proposer_block.blk_id
		block_type = "proposer"
		txn_blk_list = []
		done_txn_blks = get_txn_blks(node_id[node_id].proposer_block)#have to write this new function??
		useful_trxn_blks = [ele for ele in node_list[node_id].txn_blockpool if ele not in done_txn_blks]
		txn_blk_list = useful_trxn_blks
		level = node_list[node_id].proposer_block.level+1
		parent_ptr = node_list[node_id].proposer_block
		proposer_content = txn_blk_list
		voterblock_content = None
		voterchainindex = -1
		trxn_list = None
		new_blk = Block(blk_id,block_type,voterchainindex,parent_id,trxn_list,proposer_content,voterblock_content,level,parent_ptr)

	else:#voterchain-2
		parent_id = node_list[node_id].voterchains[x-2].blk_id
		block_type = "voter"
		voterchainindex = x-2

		voterblock_content = getvoterblkcontent(node_id,node_list[node_id].voterchains[x-2]) #the output of this funcion is
																			# list of (index,blk_ids))
		proposer_content = None
		level = node_list[node_id].voterchains[x-2].level+1
		parent_ptr = node_list[node_id].voterchains[x-2]
		trxn_list = None
		new_blk = Block(blk_id,block_type,voterchainindex,parent_id,trxn_list,proposer_content,voterblock_content,level,parent_ptr)

			# calc_bal = get_balance(node_list[node_id].mining_blk)
			# done_trxns = get_trxns(node_list[node_id].mining_blk)
			# useful_trxns = [ele for ele in node_list[node_id].trxn_pool if ele not in done_trxns]
			# for t in useful_trxns:
			# 	if(((calc_bal[t.payer]-t.coins)>=0) and len(trxn_list)<1000):
			# 		trxn_list.append(t)
			# 		calc_bal[t.payer] = calc_bal[t.payer]-t.coins
			# 		calc_bal[t.payee] = calc_bal[t.payee]+t.coins

			# level = node_list[node_id].mining_blk.level+1
			# parent_ptr = node_list[node_id].mining_blk
			# new_blk = Block(blk_id,parent_id,trxn_list,level,parent_ptr)

	print('Block %s is created at t = %f with num_trxns = %d' % (blk_id,env.now,len(trxn_list)))
	print('parent_blk_id = %s' %parent_id)
	# print('trxn list:')
	# for i in trxn_list:
	# 	print(i.id)
	# print('level:%d' %level)
	
	env.process(broadcast_blk(node_id,new_blk))


# Simulation---------------------------------------------------------------------------------------------------

for i in node_list:
	env.process(create_trxn(i.id))
	create_blk(i.id)

env.run(until=stop_time)

# writing treefiles
for node in node_list:
	filename = 'treefile'+str(node.id)+'.txt'
	file = open(filename,'w')
	line=''
	for info in node.timestamp_list:
		line = line+str(info[0])+','+str(info[1])+','+str(info[2])+','+str(info[3])+'\n'
	file.write(line)
	file.close()

# to do--------------------------------------------------------------------------------------------------------

# changing B_Tx for every node
# histogram of branch lengths