import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class JobService {
  final String baseUrl = dotenv.env['BASE_URL'] ?? "";
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();
  final http.Client httpClient;

  // Constructor accepts an optional HTTP client
  JobService([http.Client? client]) : httpClient = client ?? http.Client();

  Future<List<dynamic>> fetchJobList() async {
    final accessToken = await _secureStorage.read(key: "access_token");

    if (accessToken == null) {
      throw Exception("Access token not found");
    }

    final response = await httpClient.get(
      Uri.parse("$baseUrl/jobs/"),
      headers: {
        "Authorization": "Bearer $accessToken",
        "Content-Type": "application/json",
      },
    );

    if (response.statusCode == 200) {
      return json.decode(response.body); // Return the list of jobs
    } else {
      final error = json.decode(response.body)["detail"];
      throw Exception(error ?? "Failed to fetch job list");
    }
  }

  Future<void> createJob(Map<String, dynamic> jobData) async {
    final accessToken = await _secureStorage.read(key: "access_token");

    if (accessToken == null) {
      throw Exception("Access token not found");
    }

    final response = await httpClient.post(
      Uri.parse("$baseUrl/jobs/create/"),
      headers: {
        "Authorization": "Bearer $accessToken",
        "Content-Type": "application/json",
      },
      body: json.encode(jobData),
    );

    if (response.statusCode == 201) {
      print("Job created successfully");
    } else {
      final error = json.decode(response.body)["detail"];
      throw Exception(error ?? "Failed to create job");
    }
  }
}
