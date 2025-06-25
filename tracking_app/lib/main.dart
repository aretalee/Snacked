import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';

import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

import 'package:snacktrac/routing/nav_router.dart';
import 'global.dart';

final thisRouter = router(authRepo);


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const MyApp());
}


class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'SnackTrac',
      theme: FlexThemeData.dark(scheme: FlexScheme.blue, fontFamily: GoogleFonts.inter().fontFamily),
      routerConfig: thisRouter,
    );
  }
}


