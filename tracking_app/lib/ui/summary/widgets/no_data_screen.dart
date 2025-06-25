import 'package:flutter/material.dart';


class NoDataSummary extends StatelessWidget {
  const NoDataSummary({super.key});

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
                  const SizedBox(height:100),
                  Text('No data available yet', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold,) ),
                  const SizedBox(height:30),
                  Text('Please check back in tomorrow at 8am', 
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                  const SizedBox(height:100),
                ]
              )
            )
          )
        )
      )
    );
  }
  
}


