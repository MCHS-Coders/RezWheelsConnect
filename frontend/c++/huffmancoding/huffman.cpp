#include <iostream>
#include <string>
#include <queue>
#include <unordered_map>
#include <cassert>
#include <vector>

using namespace std;
using Bit = int; // For binary operations (0 or 1)

// Data structure representing a node in the encoding tree.
struct EncodingTreeNode {
    char ch;
    EncodingTreeNode* zero;
    EncodingTreeNode* one;

    EncodingTreeNode(char character = '\0') : ch(character), zero(nullptr), one(nullptr) {}
    EncodingTreeNode(EncodingTreeNode* left, EncodingTreeNode* right) : ch('\0'), zero(left), one(right) {}

    bool isLeaf() const {
        return !zero && !one;
    }
};

// EncodedData struct to hold the necessary queues for the encoding and decoding processes.
struct EncodedData {
    queue<Bit> treeShape;
    queue<char> treeLeaves;
    queue<Bit> messageBits;
};

// Helper function to deallocate memory for an encoding tree.
void deallocateTree(EncodingTreeNode* t) {
    if (t) {
        deallocateTree(t->zero);
        deallocateTree(t->one);
        delete t;
    }
}

// Helper function to compare two encoding trees for equality.
bool areEqual(EncodingTreeNode* a, EncodingTreeNode* b) {
    if (a == nullptr || b == nullptr) return a == b;
    return a->ch == b->ch && areEqual(a->zero, b->zero) && areEqual(a->one, b->one);
}

// Frequency map builder.
unordered_map<char, int> frequencyMap(const string& text) {
    unordered_map<char, int> freqMap;
    for (char ch : text) {
        freqMap[ch]++;
    }
    return freqMap;
}

// Huffman Tree builder.
EncodingTreeNode* buildHuffmanTree(const string& text) {
    auto freqMap = frequencyMap(text);
    if (freqMap.size() < 2) {
        cerr << "Cannot create a Huffman tree with less than two distinct characters." << endl;
        exit(1);
    }

    auto cmp = [](pair<int, EncodingTreeNode*> left, pair<int, EncodingTreeNode*> right) { return left.first > right.first; };
    priority_queue<pair<int, EncodingTreeNode*>, vector<pair<int, EncodingTreeNode*>>, decltype(cmp)> pq(cmp);

    for (auto& [ch, freq] : freqMap) {
        pq.push({freq, new EncodingTreeNode(ch)});
    }

    while (pq.size() > 1) {
        auto left = pq.top(); pq.pop();
        auto right = pq.top(); pq.pop();
        int combinedFreq = left.first + right.first;
        pq.push({combinedFreq, new EncodingTreeNode(left.second, right.second)});
    }

    return pq.top().second;
}

// Recursive function to build the encoding map for characters.
void buildMap(EncodingTreeNode* tree, unordered_map<char, string>& encodingMap, string path) {
    if (tree->isLeaf()) {
        encodingMap[tree->ch] = path;
        cout << "Character '" << tree->ch << "': " << path << endl;
    } else {
        buildMap(tree->zero, encodingMap, path + "0");
        buildMap(tree->one, encodingMap, path + "1");
    }
}

// Encode text using the Huffman tree.
queue<Bit> encodeText(EncodingTreeNode* tree, const string& text) {
    unordered_map<char, string> encodingMap;
    buildMap(tree, encodingMap, "");

    queue<Bit> result;
    for (char ch : text) {
        string bits = encodingMap[ch];
        for (char bit : bits) {
            result.push(bit - '0');
        }
    }
    return result;
}

// Decode text using the Huffman tree and encoded bits.
string decodeText(EncodingTreeNode* tree, queue<Bit> messageBits) {
    string result;
    EncodingTreeNode* current = tree;
    while (!messageBits.empty()) {
        Bit bit = messageBits.front();
        messageBits.pop();
        current = (bit == 0) ? current->zero : current->one;

        if (current->isLeaf()) {
            result += current->ch;
            current = tree;
        }
    }
    return result;
}

// Flatten tree into queues for encoding.
void flattenTree(EncodingTreeNode* tree, queue<Bit>& treeShape, queue<char>& treeLeaves) {
    if (tree->isLeaf()) {
        treeShape.push(0);
        treeLeaves.push(tree->ch);
    } else {
        treeShape.push(1);
        flattenTree(tree->zero, treeShape, treeLeaves);
        flattenTree(tree->one, treeShape, treeLeaves);
    }
}

// Unflatten tree from queues.
EncodingTreeNode* unflattenTree(queue<Bit>& treeShape, queue<char>& treeLeaves) {
    Bit shape = treeShape.front();
    treeShape.pop();

    if (shape == 0) {
        char ch = treeLeaves.front();
        treeLeaves.pop();
        return new EncodingTreeNode(ch);
    } else {
        EncodingTreeNode* left = unflattenTree(treeShape, treeLeaves);
        EncodingTreeNode* right = unflattenTree(treeShape, treeLeaves);
        return new EncodingTreeNode(left, right);
    }
}

// Compress text using Huffman encoding.
EncodedData compress(const string& text) {
    EncodedData data;
    EncodingTreeNode* tree = buildHuffmanTree(text);

    data.messageBits = encodeText(tree, text);
    flattenTree(tree, data.treeShape, data.treeLeaves);

    deallocateTree(tree);
    return data;
}

// Decompress encoded data back to original text.
string decompress(EncodedData& data) {
    EncodingTreeNode* tree = unflattenTree(data.treeShape, data.treeLeaves);
    string decodedText = decodeText(tree, data.messageBits);

    deallocateTree(tree);
    return decodedText;
}

void printHuffmanTree(EncodingTreeNode* root, const std::string& prefix = "", bool isLeft = true) {
    if (root != nullptr) {
        // Print the prefix for the current node
        std::cout << prefix;

        // Use box-drawing characters for branches
        std::cout << (isLeft ? "├─ " : "└─ ");

        // Print the character for leaf nodes or a box symbol for internal nodes
        if (root->isLeaf()) {
            std::cout << root->ch << std::endl;
        } else {
            std::cout << "▢" << std::endl;  // Using ▢ for internal nodes, as an example
        }

        // Build the prefix for the child nodes with box-drawing characters
        std::string childPrefix = prefix + (isLeft ? "│  " : "   ");

        // Recursively print the left and right subtrees
        printHuffmanTree(root->zero, childPrefix, true);
        printHuffmanTree(root->one, childPrefix, false);
    }
}

// Utility function for testing.
void testHuffmanEncoding() {
    string text;

    cout << "Enter your message to encode: ";
    getline(cin, text);
    cout << endl;

    // Build Huffman Tree
    cout << "Building Huffman tree..." << endl;
    EncodingTreeNode* huffmanTree = buildHuffmanTree(text);

    // Print Huffman Tree
    cout << "Huffman tree structure:" << endl;
    printHuffmanTree(huffmanTree);
    cout << endl;

    // Encode the message
    cout << "Encoding the message..." << endl;
    queue<Bit> encodedBits = encodeText(huffmanTree, text);

    // Display the binary representation of the message
    cout << "Binary representation of the encoded message:" << endl;
    queue<Bit> encodedBitsCopy = encodedBits;
    while (!encodedBitsCopy.empty()) {
        cout << encodedBitsCopy.front();
        encodedBitsCopy.pop();
    }
    cout << endl << endl;

    // Decode and verify
    assert(decodeText(huffmanTree, encodedBits) == text);
    cout << "Encoding and decoding test passed for text: " << text << endl;

    // Test compress and decompress
    EncodedData compressedData = compress(text);
    assert(decompress(compressedData) == text);
    cout << "Compression and decompression test passed for text: " << text << endl;

    deallocateTree(huffmanTree);
}

// Main function to run tests.
int main() {
    testHuffmanEncoding();
    cout << "All tests passed!" << endl;
    return 0;
}
