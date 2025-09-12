import 'package:flutter/material.dart';
import 'package:service_mobile/services/job_service.dart';

class JobsPage extends StatefulWidget {
  const JobsPage({Key? key}) : super(key: key);

  @override
  _JobsPageState createState() => _JobsPageState();
}

class _JobsPageState extends State<JobsPage> {
  final JobService _jobService = JobService();
  late Future<List<dynamic>> _jobListFuture;

  @override
  void initState() {
    super.initState();
    _jobListFuture = _jobService.fetchJobList(); // Fetch jobs on page load
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
      title: const Text("Jobs"),
      actions: [
        IconButton(
          icon: const Icon(Icons.add),
          onPressed: () {
            Navigator.pushNamed(context, '/create-job'); // Navigate to Create Jobs Page
          },
        ),
      ],
    ),
      body: FutureBuilder<List<dynamic>>(
        future: _jobListFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error: ${snapshot.error}"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text("No jobs found"));
          } else {
            final jobs = snapshot.data!;
            return ListView.builder(
              itemCount: jobs.length,
              itemBuilder: (context, index) {
                final job = jobs[index];
                return ListTile(
                  title: Text(job["title"]),
                  subtitle: Text(job["description"]),
                  onTap: () {
                    // Navigate to job details page (if implemented)
                  },
                );
              },
            );
          }
        },
      ),
    );
  }
}