import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:go_router/go_router.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';


class ExportPage extends StatelessWidget {
  const ExportPage({super.key});

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
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'Choose Export Format', 
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold,), 
                    textAlign: TextAlign.center),
                  const SizedBox(height:30),
                  FilledButton(
                      onPressed: () {}, 
                      child: const Text('CSV'),
                    ),
                    const SizedBox(height:15),
                    FilledButton(
                      onPressed: () {}, 
                      child: const Text('PDF'),
                    ),
                    const SizedBox(height:15),
                    FilledButton(
                      onPressed: () {}, 
                      child: const Text('Excel'),
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


