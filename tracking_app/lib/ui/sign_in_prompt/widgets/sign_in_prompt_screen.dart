import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:go_router/go_router.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';


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
              onPressed: () {}, 
              // style: FilledButton.styleFrom(
              //   backgroundColor: const Color(0x8405BE),
              // ),
              child: const Text('Sign Up'), 
            ),
            const SizedBox(height:15),
            FilledButton(
              onPressed: () {}, 
              child: const Text('Login'),
            ),
          ],
        )
      )
    );
  }

}


