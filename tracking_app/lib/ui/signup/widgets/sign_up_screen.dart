import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:go_router/go_router.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';


class SignUpPage extends StatelessWidget {
  const SignUpPage({super.key});

  @override
  Widget build(BuildContext context) {

    return Scaffold (
      appBar: AppBar(backgroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('Sign Up', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  const SizedBox(height:15),
                  TextField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'Email: ',
                      ),
                    ),
                    const SizedBox(height:15),
                    TextField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'Password: ',
                      ),
                    ),
                    const SizedBox(height:30),
                    FilledButton(
                      onPressed: () {}, 
                      child: const Text('Register'),
                    ),
                ]
              )
            )
          )
        )
      )
    );
  }

}

