import 'package:flutter/material.dart';
// import 'package:provider/provider.dart';
// import '../../main.dart'; // Import AuthState if needed


class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Home Page"),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              // Handle logout logic here
              Navigator.pushReplacementNamed(context, '/login');
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Welcome to the Home Page!",
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/jobs'); // Navigate to Jobs section
              },
              child: const Text("Manage Jobs"),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/customers'); // Navigate to Customers section
              },
              child: const Text("Manage Customers"),
            ),
          ],
        ),
      ),
    );
  }
}