import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthProvider extends ChangeNotifier {
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();

  bool _isAuthenticated = false;
  String? _accessToken;
  String? _refreshToken;

  bool get isAuthenticated => _isAuthenticated;

  Future<void> login(String accessToken, String refreshToken) async {
    // Store tokens securely
    await _secureStorage.write(key: "access_token", value: accessToken);
    await _secureStorage.write(key: "refresh_token", value: refreshToken);

    // Update state
    _accessToken = accessToken;
    _refreshToken = refreshToken;
    _isAuthenticated = true;
    notifyListeners(); // Notify widgets to rebuild
  }

  Future<void> logout() async {
    // Clear tokens from secure storage
    await _secureStorage.delete(key: "access_token");
    await _secureStorage.delete(key: "refresh_token");

    // Update state
    _accessToken = null;
    _refreshToken = null;
    _isAuthenticated = false;
    notifyListeners(); // Notify widgets to rebuild
  }

  Future<void> checkAuthentication() async {
    // Check if tokens exist in secure storage
    _accessToken = await _secureStorage.read(key: "access_token");
    _refreshToken = await _secureStorage.read(key: "refresh_token");

    // Update authentication state
    _isAuthenticated = _accessToken != null;
    notifyListeners();
  }

  String? get accessToken => _accessToken;

  Future<void> refreshToken() async {
    // Implement token refresh logic here (e.g., call API to refresh token)
    // For now, we'll simulate refreshing the token
    if (_refreshToken != null) {
      // Simulate refreshing the token
      _accessToken = "new_access_token"; // Replace with actual refreshed token
      await _secureStorage.write(key: "access_token", value: _accessToken);
      notifyListeners();
    }
  }
}