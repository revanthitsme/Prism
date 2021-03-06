import numpy as np
import random

# node_list=[]

class Node:
	def __init__(self,id,proposer_block,voterchains,genesis_proposer_blk,genesis_voterchains,speed,hash_power):
		self.id = id #id
		self.txn_blockpool = [] #all txn blocks generated
		self.proposer_block = proposer_block #proposer block on which mining happens at a time instant
		self.trxn_cnt = 0 # count of trxns generated by node
		self.blk_cnt = 0 # count of blocks generated by node(diff types included)
		self.voterchains = voterchains #list of voter blocks on which mining happens at a time instant
		self.txn_pool = [] #pending txns 
		self.genesis_proposer_blk = genesis_proposer_blk #
		self.genesis_voterchains = genesis_voterchains #
		self.peers = [] #list of link object
		self.orphan_blocks = [] # list of blocks whose parents not seen
		self.timestamp_list = [] # list used to store arrival times of blocks
		self.speed= speed
		self.hash_power = hash_power


		# self.speed= speed # fast(1) or slow(0) node
		# self.genesis_blk = gen_blk
		# self.mining_blk = mining_block #block on which mining happens at a time instant
		# self.trxn_cnt = 0 # count of trxns generated by node
		# self.blk_cnt = 0 # count of blocks generated by node
		# self.trxn_pool=[] # all trxns seen so far 
		# self.peers = [] # list of link object
		# self.orphan_blocks = [] # list of blocks whose parents not seen
		# self.timestamp_list = [] # list used to store arrival times of blocks
		# self.hash_power = hash_power # hash power of node

class Trxn:
	def __init__(self,txnID,F,to,coins): #payer and payee are id's
		self.id = txnID
		self.payer = F
		self.payee = to
		self.coins = coins

class link:
	def __init__(self,j,r_ij,c_ij): #j is id
		self.j = j
		self.r_ij = r_ij #speed of light propogation
		self.c_ij = c_ij #link speed

class Block:
	def __init__(self,blk_id,block_type,voterchainindex,parent_id,trxn_list,proposer_content,voterblock_content,level,parent_ptr):
		self.blk_id = blk_id
		self.block_type = block_type
		self.voterchainindex = voterchainindex
		self.parent_id = parent_id # NULL for transaction
		self.trxn_list = trxn_list
		self.proposer_content = proposer_content
		self.voterblock_content = voterblock_content# [(level,blk_id)]
		self.level = level # level of blk in its chain. For txn block level is always 0.
		self.parent_ptr = parent_ptr # parent pointer # NULL for transaction
		self.child_ptr_list = [] # list of child pointers