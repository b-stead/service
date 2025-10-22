import 'package:flutter/material.dart';
import 'package:service_mobile/services/job_service.dart';
import 'package:intl/intl.dart';

class CreateJobsPage extends StatefulWidget {
  const CreateJobsPage({super.key});

  @override
  _CreateJobsPageState createState() => _CreateJobsPageState();
}

class _CreateJobsPageState extends State<CreateJobsPage> {
  final JobService _jobService = JobService();
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();
  final _startDateController = TextEditingController();
  int? _selectedCustomerId;

  Future<void> _submitJob() async {
    if (_formKey.currentState!.validate()) {
      try {
        final jobData = {
          "title": _titleController.text,
          "description": _descriptionController.text,
          "customer": _selectedCustomerId, // Assuming you have a way to select a customer
          // You can add more fields as needed
          "start_date": DateTime.now().toIso8601String(), // Example start date
        };

        await _jobService.createJob(jobData);

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Job created successfully")),
        );

        Navigator.pop(context); // Navigate back after successful creation
      } catch (error) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Failed to create job: $error")),
        );
      }
    }
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Create Job")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _titleController,
                decoration: const InputDecoration(labelText: "Title"),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return "Please enter a title";
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _descriptionController,
                decoration: const InputDecoration(labelText: "Description"),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return "Please enter a description";
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _startDateController,
                decoration: const InputDecoration(labelText: "Start Date (YYYY-MM-DD)"),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return "Please enter a start date";
                  }
                  // Validate the date format
                  final dateRegex = RegExp(r'^\d{4}-\d{2}-\d{2}$');
                  if (!dateRegex.hasMatch(value)) {
                    return "Date must be in YYYY-MM-DD format";
                  }
                  return null;
                },
                onSaved: (value) {
                if (value != null && value.isNotEmpty) {
                  // Format the date to YYYY-MM-DD
                  final parsedDate = DateTime.parse(value);
                  _startDateController.text = DateFormat('yyyy-MM-dd').format(parsedDate);
                }
              },
              ),
              DropdownButtonFormField<int>(
                value: _selectedCustomerId,
                items: [
                  DropdownMenuItem(value: 1, child: Text("Customer 1")),
                  DropdownMenuItem(value: 2, child: Text("Customer 2")),
                  // Add more customers dynamically if needed
                ],
                onChanged: (value) {
                  setState(() {
                    _selectedCustomerId = value;
                  });
                },
                decoration: const InputDecoration(labelText: "Customer"),
                validator: (value) {
                  if (value == null) {
                    return "Please select a customer";
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _submitJob,
                child: const Text("Create Job"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}