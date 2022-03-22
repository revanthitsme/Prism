### tree diagram with gnuplot
reset session

#ID  Parent   Name
$Data <<EOD
   1    NaN   Ant
   2      1   Ape
   3      1   Ass
   4      2   Bat
   5      2   Bee
   6      2   Cat
   7      3   Cod
   8      3   Cow
   9      3   Dog
  10      7   Eel
  11      7   Elk
  12      7   Emu
  13      9   Fly
  14      9   Fox
  15      4   Gnu
  16      1   Hen
  17     16   Hog
  18     12   Jay
  19     12   Owl
  20     15   Pig
  21     15   Pug
  22     12   Ram
  23     14   Rat
  24     12   Sow
  25      7   Yak
EOD

# put datablock into strings
IDs = Parents = Names = ''
set table $Dummy
    plot $Data u (IDs = IDs.strcol(1).' '): \
                 (Parents = Parents.strcol(2).' '): \
                 (Names = Names.strcol(3).' ') w table
unset table

# Top node has no parent ID 'NaN'
Start(n) = int(sum [i=1:words(Parents)] (word(Parents,i) eq 'NaN' ? int(word(IDs,i)) : 0))

# get list index by ID
ItemIdx(s,n) = n == n ? (tmp=NaN, sum [i=1:words(s)] ((word(s,i)) == n ? (tmp=i,0) : 0), tmp) : NaN

# get parent of ID n
Parent(n) = word(Parents,ItemIdx(IDs,n))

# get level of ID n, recursive function
Level(n) = n == n ? Parent(n)>0 ? Level(Parent(n))-1 : 0 : NaN

# get number of children of ID n
ChildCount(n) = int(sum [i=1:words(Parents)] (word(Parents,i)==n))

# Create child list of ID n
ChildList(n) = (Ch = ' ', sum [i=1:words(IDs)] (word(Parents,i)==n ? (Ch = Ch.word(IDs,i).' ',1) : (Ch,0) ), Ch )

# m-th child of ID n
Child(n,m) = word(ChildList(n),m)

# List of leaves, recursive function
LeafList(n) = (LL='', ChildCount(n)==0 ? LL=LL.n.' ' : sum [i=1:ChildCount(n)] (LL=LL.LeafList(Child(n,i)), 0),LL)

# create list of all leaves
LeafAll = LeafList(Start(0))

# get x-position of ID n, recursive function
XPos(n) = ChildCount(n) == 0 ? ItemIdx(LeafAll,n) : (sum [i=1:ChildCount(n)] (XPos(Child(n,i))))/(ChildCount(n))

# create the tree datablock for plotting
set print $Tree
    do for [j=1:words(IDs)] {
        n = int(word(IDs,j))
        print sprintf("% 3d % 7.2f % 4d % 5s", n, XPos(n), Level(n), word(Names,j))
    }
set print
print $Tree

# get x and y distance from ID n to its parent
dx(n) = XPos(Parent(int(n))) - XPos(int(n))
dy(n) = Level(Parent(int(n))) - Level(int(n))

unset border
unset tics
set offsets 0.25, 0.25, 0.25, 0.25

plot $Tree u 2:3:(dx($1)):(dy($1)) w vec nohead ls -1 not,\
        '' u 2:3 w p pt 7 ps 6 lc rgb 0xccffcc not, \
        '' u 2:3 w p pt 6 ps 6 lw 1.5 lc rgb "black" not, \
        '' u 2:3:4 w labels offset 0,0.1 center not
### end of code