import 'package:flutter/material.dart';


class InfoPage extends StatelessWidget {
  const InfoPage({super.key});

  @override
  Widget build(BuildContext context) {


    return Scaffold (
      appBar: AppBar(
        title:Text('About Snacked', style: TextStyle(fontWeight: FontWeight.bold)), 
        backgroundColor: Colors.black
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: SingleChildScrollView(
          child: Column(
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(50.0),
                  child: Column(
                    children: [
                      Text('Your bespoke snacking report for the previous day is released at 9am daily', style: TextStyle(fontSize: 18), textAlign: TextAlign.center),
                      const SizedBox(height:20),
                      Text('We aim to give an overview of how much time you spend eating every day', style: TextStyle(fontSize: 18), textAlign: TextAlign.center),
                      const SizedBox(height:20),
                      Text('But what and when you eat is up to you!', style: TextStyle(fontSize: 18), textAlign: TextAlign.center),
                    ],
                  ),
                ),
              ),
              const SizedBox(height:30),
              Text('Potential Snacking Triggers', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height:5),
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
                          Text('Stress? Boredom? Exercise?', style: TextStyle(fontSize: 18, color: const Color.fromARGB(255, 157, 105, 253))),
                          const SizedBox(height:10),
                          Text('Out of habit? Fatigue? Peers?', style: TextStyle(fontSize: 18, color: const Color.fromARGB(255, 157, 105, 253))),
                        ]
                      ),
                    ]
                  ),
                ),
              ),
              const SizedBox(height:30),
              Text('Did you know?', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height:15),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(30.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text('Nutrient-poor snacking may be linked to obesity', style: TextStyle(fontSize: 17), textAlign: TextAlign.center),
                          const SizedBox(height:20),
                          Text('In fact, obesity is mostly caused by modifiable behaviours', style: TextStyle(fontSize: 17), textAlign: TextAlign.center),
                          const SizedBox(height:20),
                          Text('Habit strength is one of the biggest predictors and drivers of snacking', style: TextStyle(fontSize: 17), textAlign: TextAlign.center),
                          const SizedBox(height:20),
                          Text('Tracking personal data is a good way to encourage self-reflection', style: TextStyle(fontSize: 17), textAlign: TextAlign.center),
                          const SizedBox(height:20),
                          Text('With determination, snacking behaviour can be changed!', style: TextStyle(fontSize: 17), textAlign: TextAlign.center),
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
      )
    );


  }

}