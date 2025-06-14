import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthService {
  final String baseUrl = "http://127.0.0.1:8000/api"; // Replace with your Django server URL
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();
  final http.Client httpClient;

  // Constructor accepts an optional HTTP client
  AuthService([http.Client? client]) : httpClient = client ?? http.Client();
  // Register a new user
  Future<String> registerUser(String email, String password, String confirmPassword) async {
    final response = await http.post(
      Uri.parse("$baseUrl/register/"),
      headers: {"Content-Type": "application/json"},
      body: json.encode({
        "email": email,
        "password": password,
        "confirm_password": confirmPassword,
      }),
    );

    if (response.statusCode == 201) {
      return "User registered successfully";
    } else {
      final error = json.decode(response.body)['error'];
      throw Exception("Failed to register: $error");
    }
  }

  // Log in an existing user and store JWT tokens
  Future<Map<String, dynamic>> loginUser(String email, String password) async {
    final response = await httpClient.post(
      Uri.parse("$baseUrl/auth/token/"),
      headers: {"Content-Type": "application/json"},
      body: json.encode({
        "email": email,
        "password": password,
      }),
    );

    if (response.statusCode == 200) {
      // Parse the response data
      final responseData = json.decode(response.body);

      // Save tokens securely
      await _secureStorage.write(key: "access_token", value: responseData["access"]);
      await _secureStorage.write(key: "refresh_token", value: responseData["refresh"]);

      return responseData;
    } else {
      // Handle errors
      final error = json.decode(response.body)["detail"];
      throw Exception(error ?? "Failed to log in.");
    }
  }

  // Refresh the access token using the refresh token
  Future<void> refreshAccessToken() async {
    final refreshToken = await _secureStorage.read(key: "refresh_token");

    if (refreshToken == null) {
      throw Exception("No refresh token found");
    }

    final response = await httpClient.post(
      Uri.parse("$baseUrl/auth/token/refresh/"),
      headers: {"Content-Type": "application/json"},
      body: json.encode({"refresh": refreshToken}),
    );

    if (response.statusCode == 200) {
      final responseData = json.decode(response.body);
      await _secureStorage.write(key: "access_token", value: responseData["access"]);
    } else {
      final error = json.decode(response.body)["detail"];
      throw Exception(error ?? "Failed to refresh token.");
    }
  }

  // Retrieve the access token from secure storage
  Future<String?> getAccessToken() async {
    return await _secureStorage.read(key: "access_token");
  }

  // Logout the user by clearing tokens
  Future<void> logoutUser() async {
    await _secureStorage.delete(key: "access_token");
    await _secureStorage.delete(key: "refresh_token");
  }

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