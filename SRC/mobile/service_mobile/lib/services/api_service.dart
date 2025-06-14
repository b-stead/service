import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = "http://127.0.0.1:8000"; // Replace with your backend URL

  Future<Map<String, dynamic>> fetchData() async {
    final url = Uri.parse("$baseUrl/api/test"); // Replace with your API endpoint
    final response = await http.get(url);

    if (response.statusCode == 200) {
      return jsonDecode(response.body); // Parse JSON response
    } else {
      throw Exception("Failed to fetch data: ${response.body}");
    }
  }
}