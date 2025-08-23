# service_mobile

A service for tradespeople to manage thier customers and payments

## AUTH

Using simple JWT with custom token which includes sub parameter as an identifier of the user.

Mobile refresh to be done in the background through an intercpetion client to handle token refresh if required

ENV for mobile

```
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Load environment-specific .env file
  const environment = String.fromEnvironment('ENV', defaultValue: 'development');
  await dotenv.load(fileName: ".env.$environment");

  runApp(const MyApp());
}

flutter run --dart-define=ENV=development
flutter run --dart-define=ENV=staging
flutter run --dart-define=ENV=production

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: "3.0.0"

      - name: Build Flutter app
        run: flutter build apk --dart-define=BASE_URL=$BASE_URL
        env:
          BASE_URL: https://api.example.com
```



## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.
