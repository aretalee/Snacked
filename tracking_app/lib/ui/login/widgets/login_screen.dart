import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:go_router/go_router.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';


class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {

    return Scaffold (
      appBar: AppBar(backgroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(30.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text('Login', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold,)),
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
                      child: const Text('Go'),
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