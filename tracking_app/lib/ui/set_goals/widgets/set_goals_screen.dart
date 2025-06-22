import 'package:flutter/material.dart';


class SetGoalsPage extends StatelessWidget {
  const SetGoalsPage({super.key});

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
                  Text('Set a Goal', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold,)),
                  const SizedBox(height:30),
                  TextField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'Snacking time (in min): ',
                      ),
                    ),
                    const SizedBox(height:30),
                    FilledButton(
                      onPressed: () {}, 
                      child: const Text('Save'),
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


