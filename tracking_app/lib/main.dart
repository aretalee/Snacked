import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:go_router/go_router.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';

import 'ui/home_page/widgets/home_page_screen.dart';
import 'ui/info/widgets/info_screen.dart';
import 'ui/sign_in_prompt/widgets/sign_in_prompt_screen.dart';
import 'ui/signup/widgets/sign_up_screen.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SnackTrac',
      // themeMode: ThemeMode.system,
      // theme: FlexThemeData.light(scheme: FlexScheme.blue),
      // darkTheme: FlexThemeData.dark(scheme: FlexScheme.blue),
      theme: FlexThemeData.dark(scheme: FlexScheme.blue, fontFamily: GoogleFonts.inter().fontFamily),
      // home: SignInPage(),
      home: SignUpPage(),
    );
  }
}


