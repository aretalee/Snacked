import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';

import 'package:snacktrac/ui/signup/widgets/sign_up_screen.dart';
import 'package:snacktrac/ui/login/widgets/login_screen.dart';

class SignInPage extends StatelessWidget {
  const SignInPage({super.key});

  @override
  Widget build(BuildContext context) {

    return Scaffold (
      appBar: AppBar(backgroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => const SignUpPage()),
                );
              }, 
              child: const Text('Sign Up'), 
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => const LoginPage()),
                );
              }, 
              child: const Text('Login'),
            ),
          ],
        )
      )
    );
  }

}


