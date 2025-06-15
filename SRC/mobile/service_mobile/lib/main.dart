import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:service_mobile/providers/auth_provider.dart';
import 'pages/login/login_page.dart';
import 'pages/login/register_page.dart';
import 'pages/home/home_page.dart';
import 'pages/jobs/jobs_list.dart';
import 'pages/jobs/create_job.dart';
import 'pages/customer/customer_list.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

void main() async {
  // Ensure Flutter bindings are initialized
  WidgetsFlutterBinding.ensureInitialized();

  // Load environment variables
  try {
    await dotenv.load(fileName: "assets/.env");
  } catch (e) {
    print("Failed to load .env file: $e");
  }

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (context) => AuthProvider()..checkAuthentication(),
        ),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final authProvider = Provider.of<AuthProvider>(context);

    return MaterialApp(
      title: 'Servify',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color.fromARGB(255, 124, 180, 46)),
      ),
      initialRoute: authProvider.isAuthenticated ? '/home' : '/login',
      routes: {
        '/login': (context) => const LoginPage(),
        '/home': (context) => const HomePage(),
        '/jobs': (context) => const JobsPage(),
        '/customers': (context) => const CustomerListPage(),
        '/register': (context) => const RegisterPage(),
        '/create-job': (context) => const CreateJobsPage(),
      },
    );
  }
}