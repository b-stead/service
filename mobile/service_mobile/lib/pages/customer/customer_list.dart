import 'package:flutter/material.dart';

class CustomerListPage extends StatelessWidget {
  const CustomerListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Customers"),
      ),
      body: const Center(
        child: Text("Manage Customers"),
      ),
    );
  }
}