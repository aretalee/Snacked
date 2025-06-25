import 'package:flutter/material.dart';


class InfoPage extends StatelessWidget {
  const InfoPage({super.key});

  @override
  Widget build(BuildContext context) {


    return Scaffold (
      appBar: AppBar(
        title:Text('About SnackTrac', style: TextStyle(fontWeight: FontWeight.bold)), 
        backgroundColor: Colors.black
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(45.0),
                child: Column(
                  children: [
                    Text('Your bespoke snacking report for the previous day is released at 7am daily', style: TextStyle(fontSize: 18), textAlign: TextAlign.center),
                    const SizedBox(height:24),
                    Text('We aim to give an overview of how much time you spend  eating every day', style: TextStyle(fontSize: 18), textAlign: TextAlign.center),
                    const SizedBox(height:24),
                    Text('But what and when you eat is up to you!', style: TextStyle(fontSize: 18), textAlign: TextAlign.center),
                  ],
                ),
              ),
            ),
            const SizedBox(height:30),
            Text('Potential Snacking Triggers', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            Text('Do any of these apply to you?', style: TextStyle(fontSize: 16)),
            const SizedBox(height:15),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('Stress', style: TextStyle(fontSize: 16)),
                        const SizedBox(width:15),
                        Text('Boredom', style: TextStyle(fontSize: 16)),
                        const SizedBox(width:15),
                        Text('Exercise', style: TextStyle(fontSize: 16)),
                      ]
                    ),
                  ]
                ),
              ),
            ),
            const SizedBox(height:15),
          ],
        )
      )
    );


  }

}