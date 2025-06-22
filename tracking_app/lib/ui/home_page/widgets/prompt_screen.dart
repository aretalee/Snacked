import 'package:flutter/material.dart';


class PromptPage extends StatelessWidget {
  const PromptPage({super.key});

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
                  const SizedBox(height:30),
                  Text(
                    'Were you happy with yesterday’s eating habits?', 
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold,), 
                    textAlign: TextAlign.center),
                  const SizedBox(height:30),
                  FilledButton(
                      onPressed: () {}, 
                      child: const Text('I feel great!'),
                    ),
                    const SizedBox(height:15),
                    FilledButton(
                      onPressed: () {}, 
                      child: const Text('Not really...'),
                    ),
                    const SizedBox(height:15),
                    FilledButton(
                      onPressed: () {}, 
                      child: const Text('Maybe?'),
                    ),
                    const SizedBox(height:30),
                ]
              )
            )
          )
        )
      )
    );
  }
  
}


