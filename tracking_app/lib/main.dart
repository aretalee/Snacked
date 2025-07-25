import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';

import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

import 'package:Snacked/routing/nav_router.dart';
import 'global.dart';

final thisRouter = router(authRepo);


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  await Supabase.initialize(
    url: "https://cjmbvpgdeehdgpvovjty.supabase.co",
    anonKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNqbWJ2cGdkZWVoZGdwdm92anR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwODcxOTIsImV4cCI6MjA2NzY2MzE5Mn0.3cZfwv4SiE_23RnJNM9BTU83U_DvmH_gd6aCg-2oqLc",
  );
  runApp(const MyApp());
}


class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Snacked',
      theme: FlexThemeData.dark(scheme: FlexScheme.blue, fontFamily: GoogleFonts.inter().fontFamily),
      routerConfig: thisRouter,
    );
  }
}


