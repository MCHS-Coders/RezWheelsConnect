Huffman Encoding: A Comprehensive Guide

Overview

Huffman encoding is a widely used method of lossless data compression. It is based on the frequency of occurrence of data items (characters, in this case) and assigns variable-length codes to each character. The most frequently occurring characters are assigned shorter codes, while less frequent characters are assigned longer codes. This method is efficient and helps reduce the overall size of the data.

How Huffman Encoding Works

    Frequency Analysis

The first step in Huffman encoding is to analyze the frequency of each character in the input data. For example, consider the string "BOOKKEEPER":

Character    Frequency
B            1
O            2
K            1
E            2
P            1
R            1

    Building the Huffman Tree

Using the frequency table, we build a binary tree (Huffman tree) as follows:

    Create a leaf node for each character and build a priority queue (or min-heap) of all leaf nodes based on their frequencies.
    While there is more than one node in the queue:
        Remove the two nodes of the lowest frequency.
        Create a new internal node with these two nodes as children and a frequency equal to the sum of their frequencies.
        Add the new node back to the queue.
    The remaining node is the root of the Huffman tree.

For the string "BOOKKEEPER", the resulting Huffman tree would look like this:

        *
      /   \
     *     *
    / \   /  \
   O   E K    *
             / \
            R   *
               / \
              B   P

3. Assigning Codes

Once the Huffman tree is built, we can assign binary codes to each character. Starting from the root, we assign '0' for the left branch and '1' for the right branch. The codes for the characters in "BOOKKEEPER" would be:

Character    Huffman Code
B            110
O            00
K            111
E            01
P            10
R            101

    Encoding the Data

To encode a string, replace each character with its corresponding Huffman code. For "BOOKKEEPER", the encoded string would be:

B -> 110
O -> 00
O -> 00
K -> 111
K -> 111
E -> 01
E -> 01
R -> 101

Thus, "BOOKKEEPER" is encoded as:

Encoded: 110000111111010101

    Decoding the Data

To decode the encoded string, traverse the Huffman tree according to the bits in the encoded string. Starting from the root, move left for '0' and right for '1' until you reach a leaf node, which gives you the original character.

Example: Encoding the String "SONS"

Given the following character-to-bit mapping:

Character    Bit Sequence
N            00
M            010
S            011
O            1

To encode the string "SONS":

S -> 011
O -> 1
N -> 00
S -> 011

Thus, "SONS" is encoded as:

Encoded: 011100011

Maps and Trees

Encoding Map

An encoding map is a table that lists each character alongside its assigned bit sequence. This map is crucial for both encoding and decoding processes.

Huffman Tree

The Huffman tree is a binary tree used to represent the encoding of characters. Each leaf node represents a character, and the path from the root to the leaf node represents the binary code for that character.

Mathematical Foundation

Compression Ratio

The efficiency of Huffman encoding can be measured using the compression ratio, which is calculated as:

Compression Ratio = Original Size / Compressed Size

Average Code Length

The average code length can be calculated as:

L = sum(p_i * l_i)

Where:
p_i is the probability of character i,
l_i is the length of the code for character i.

Entropy

The theoretical limit of compression can be estimated using entropy, which measures the average amount of information produced by a stochastic source of data.
