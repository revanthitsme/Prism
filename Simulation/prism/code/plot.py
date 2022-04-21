import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edges_from([('prop_blk_6_2', 'gen_proposer'), ('prop_blk_3_7', 'prop_blk_6_2'), ('prop_blk_2_9', 'prop_blk_3_7'), ('prop_blk_2_13', 'prop_blk_2_9'), ('prop_blk_7_19', 'prop_blk_2_13'), ('prop_blk_1_30', 'prop_blk_7_19'), ('prop_blk_7_19', 'trxn_blk_1_1'), ('prop_blk_7_19', 'trxn_blk_1_5'), ('prop_blk_7_19', 'trxn_blk_1_7'), ('prop_blk_7_19', 'trxn_blk_4_8'), ('prop_blk_7_19', 'trxn_blk_5_10'), ('prop_blk_2_13', 'trxn_blk_1_1'), ('prop_blk_2_13', 'trxn_blk_1_5'), ('prop_blk_2_13', 'trxn_blk_1_7'), ('prop_blk_2_13', 'trxn_blk_4_8'), ('prop_blk_2_13', 'trxn_blk_5_10'), ('prop_blk_2_9', 'trxn_blk_1_1'), ('prop_blk_2_9', 'trxn_blk_1_5'), ('prop_blk_2_9', 'trxn_blk_1_7'), ('prop_blk_2_9', 'trxn_blk_4_8'), ('prop_blk_3_7', 'trxn_blk_1_1'), ('prop_blk_3_7', 'trxn_blk_1_5'), ('vot0_blk_0_10', 'gen_voter_0'), ('vot0_blk_0_25', 'vot0_blk_0_10'), ('vot0_blk_0_10', 'prop_blk_6_2'), ('vot0_blk_0_10', 'prop_blk_3_7'), ('gen_voter_0', 'gen_proposer'), ('vot1_blk_8_1', 'gen_voter_1'), ('vot1_blk_0_11', 'vot1_blk_8_1'), ('gen_voter_1', 'gen_proposer'), ('vot2_blk_6_20', 'gen_voter_2'), ('vot2_blk_9_19', 'vot2_blk_6_20'), ('vot2_blk_6_20', 'prop_blk_6_2'), ('vot2_blk_6_20', 'prop_blk_3_7'), ('vot2_blk_6_20', 'prop_blk_2_9'), ('vot2_blk_6_20', 'prop_blk_2_13'), ('gen_voter_2', 'gen_proposer'), ('vot3_blk_5_6', 'gen_voter_3'), ('vot3_blk_7_14', 'vot3_blk_5_6'), ('vot3_blk_7_24', 'vot3_blk_7_14'), ('vot3_blk_6_22', 'vot3_blk_7_24'), ('vot3_blk_7_24', 'prop_blk_2_13'), ('vot3_blk_7_14', 'prop_blk_3_7'), ('vot3_blk_7_14', 'prop_blk_2_9'), ('vot3_blk_5_6', 'prop_blk_6_2'), ('gen_voter_3', 'gen_proposer'), ('vot4_blk_8_11', 'gen_voter_4'), ('vot4_blk_0_15', 'vot4_blk_8_11'), ('vot4_blk_0_17', 'vot4_blk_0_15'), ('vot4_blk_8_11', 'prop_blk_6_2'), ('vot4_blk_8_11', 'prop_blk_3_7'), ('vot4_blk_8_11', 'prop_blk_2_9'), ('gen_voter_4', 'gen_proposer'), ('vot5_blk_0_1', 'gen_voter_5'), ('vot5_blk_0_8', 'vot5_blk_0_1'), ('vot5_blk_0_22', 'vot5_blk_0_8'), ('vot5_blk_0_32', 'vot5_blk_0_22'), ('vot5_blk_0_22', 'prop_blk_3_7'), ('vot5_blk_0_22', 'prop_blk_2_9'), ('vot5_blk_0_22', 'prop_blk_2_13'), ('vot5_blk_0_8', 'prop_blk_6_2'), ('gen_voter_5', 'gen_proposer'), ('vot6_blk_6_1', 'gen_voter_6'), ('vot6_blk_5_3', 'vot6_blk_6_1'), ('vot6_blk_2_5', 'vot6_blk_5_3'), ('vot6_blk_0_7', 'vot6_blk_2_5'), ('vot6_blk_2_5', 'prop_blk_6_2'), ('gen_voter_6', 'gen_proposer'), ('vot7_blk_0_26', 'gen_voter_7'), ('gen_voter_7', 'gen_proposer'), ('vot8_blk_0_16', 'gen_voter_8'), ('gen_voter_8', 'gen_proposer'), ('vot9_blk_2_8', 'gen_voter_9'), ('vot9_blk_6_12', 'vot9_blk_2_8'), ('vot9_blk_7_20', 'vot9_blk_6_12'), ('vot9_blk_9_22', 'vot9_blk_7_20'), ('vot9_blk_7_20', 'prop_blk_2_13'), ('vot9_blk_6_12', 'prop_blk_2_9'), ('vot9_blk_2_8', 'prop_blk_6_2'), ('vot9_blk_2_8', 'prop_blk_3_7'), ('gen_voter_9', 'gen_proposer')])
p=nx.drawing.nx_pydot.to_pydot(G)

p.write_png('graph.png')