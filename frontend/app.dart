import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:geolocator/geolocator.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App with Huffman Coding and GPS',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  late GoogleMapController mapController;
  Set<Marker> _markers = {};
  LatLng _currentLocation = LatLng(0.0, 0.0);
  Position? _position;

  // Huffman Encoding / Decoding
  String huffmanEncode(String input) {
    var freqTable = _buildFrequencyTable(input);
    var root = _buildHuffmanTree(freqTable);
    var codes = _generateHuffmanCodes(root, '');
    var encoded = input.split('').map((e) => codes[e]!).join();
    return encoded;
  }

  String huffmanDecode(String encoded, Map<String, String> codes) {
    var reverseCodes = codes.map((key, value) => MapEntry(value, key));
    String currentCode = '';
    String decoded = '';
    for (var bit in encoded.split('')) {
      currentCode += bit;
      if (reverseCodes.containsKey(currentCode)) {
        decoded += reverseCodes[currentCode]!;
        currentCode = '';
      }
    }
    return decoded;
  }

  // Build the frequency table for the input text.
  Map<String, int> _buildFrequencyTable(String input) {
    Map<String, int> frequencyTable = {};
    for (int i = 0; i < input.length; i++) {
      String char = input[i];
      frequencyTable[char] = (frequencyTable[char] ?? 0) + 1;
    }
    return frequencyTable;
  }

  // Build the Huffman Tree.
  HuffmanNode _buildHuffmanTree(Map<String, int> frequencyTable) {
    List<HuffmanNode> nodes = [];
    frequencyTable.forEach((char, freq) {
      nodes.add(HuffmanNode(value: char, frequency: freq));
    });

    while (nodes.length > 1) {
      nodes.sort((a, b) => a.frequency.compareTo(b.frequency));

      HuffmanNode left = nodes.removeAt(0);
      HuffmanNode right = nodes.removeAt(0);

      HuffmanNode parent = HuffmanNode(
        value: '',
        frequency: left.frequency + right.frequency,
        left: left,
        right: right,
      );

      nodes.add(parent);
    }

    return nodes.first;
  }

  // Generate Huffman codes from the tree.
  Map<String, String> _generateHuffmanCodes(HuffmanNode root, String prefix) {
    Map<String, String> codes = {};

    if (root.left == null && root.right == null) {
      codes[root.value] = prefix;
    } else {
      if (root.left != null) {
        codes.addAll(_generateHuffmanCodes(root.left!, prefix + '0'));
      }
      if (root.right != null) {
        codes.addAll(_generateHuffmanCodes(root.right!, prefix + '1'));
      }
    }
    return codes;
  }

  // Fetch GPS coordinates
  Future<void> _getCurrentLocation() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Location services are disabled')));
      return;
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }

    if (permission == LocationPermission.deniedForever) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Location permission denied forever')));
      return;
    }

    Position position = await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high);
    setState(() {
      _position = position;
      _currentLocation = LatLng(position.latitude, position.longitude);
      _markers.add(
        Marker(
          markerId: MarkerId('current_location'),
          position: _currentLocation,
        ),
      );
    });

    // Send the GPS data to the server
    _sendGpsDataToServer(position);
  }

  // Send the GPS data to the server with Huffman encoding
  Future<void> _sendGpsDataToServer(Position position) async {
    String gpsData = json.encode({
      'latitude': position.latitude,
      'longitude': position.longitude,
    });

    String encodedGpsData = huffmanEncode(gpsData);

    final response = await http.post(
      Uri.parse('http://<YOUR_SERVER_URL>/process_gps'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'gps_data': encodedGpsData}),
    );

    if (response.statusCode == 200) {
      // Process the response (e.g., display in UI)
      print('Server Response: ${response.body}');
    } else {
      print('Failed to send GPS data');
    }
  }

  @override
  void initState() {
    super.initState();
    _getCurrentLocation(); // Fetch GPS data as soon as the app starts
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Flutter GPS and Huffman Encoding'),
      ),
      body: Column(
        children: [
          Expanded(
            child: GoogleMap(
              initialCameraPosition: CameraPosition(
                target: _currentLocation,
                zoom: 14.0,
              ),
              markers: _markers,
              onMapCreated: (GoogleMapController controller) {
                mapController = controller;
              },
            ),
          ),
          ElevatedButton(
            onPressed: _getCurrentLocation,
            child: Text('Get Current Location'),
          ),
        ],
      ),
    );
  }
}

class HuffmanNode {
  final String value;
  final int frequency;
  final HuffmanNode? left;
  final HuffmanNode? right;

  HuffmanNode({required this.value, required this.frequency, this.left, this.right});
}
