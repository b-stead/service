import 'package:flutter/material.dart';
import '../../services/auth_service.dart';
import '../../providers/auth_provider.dart';
import 'package:provider/provider.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _authService = AuthService();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  Future<void> _login() async {
    try {
      final response = await _authService.loginUser(
        _emailController.text,
        _passwordController.text,
      );

      if (!mounted) return; // Check if the widget is still mounted

      // Extract tokens from the response
      final accessToken = response["access"];
      final refreshToken = response["refresh"];

      // Update authentication state
      Provider.of<AuthProvider>(context, listen: false).login(accessToken, refreshToken);

      // Navigate to Home Page
      Navigator.pushReplacementNamed(context, '/home');
    } catch (error) {
      if (!mounted) return; // Check if the widget is still mounted

      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(error.toString())));
    }
  }

  @override
  void dispose() {
    // Dispose controllers to free resources
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Login")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: "Email"),
            ),
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: "Password"),
              obscureText: true,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _login,
              child: const Text("Login"),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/register'); // Navigate to Registration Page
              },
              child: const Text("Register"),
            ),
          ],
        ),
      ),
    );
  }
}