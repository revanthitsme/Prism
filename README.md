# Prism
Implementation of both prism and bitcoin consensus protocol in python

Go to bitcoin directory:
Run:
python3 simulation.py

Enter the number of nodes(n): 10

Enter the percent of slow nodes(z): 20

Enter the mean interarrival time of transactions(T_tx): 2

Enter the percent of High CPU nodes: 80

Enter block interarrival time(in sec): 5


We get number of transactions in the bitcoin ledger as output.

Go to prism directory:

python3 simulation.py

Enter the number of nodes(n): 10

Enter the percent of slow nodes(z): 20

Enter the mean interarrival time of transactions(T_tx): 2

Enter the percent of High CPU nodes: 80

Enter block interarrival time(in sec): 5

Enter no of voter chains: 10


We get number of transactions entered into the chain as output.

To get tree diagram:

Copy output of prism simulation and paste it in plot.py

Run plot.py:

python3 plot.py

Install Graphviz,PyDot and NetworkX for tree diagram.
