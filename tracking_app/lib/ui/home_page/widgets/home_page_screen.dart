import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';


class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {


    return Scaffold (
      appBar: AppBar(
        title: const Text('June 17 Summary', style: TextStyle(color: Colors.white)), 
        backgroundColor: Colors.black, automaticallyImplyLeading:false),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Text('You spent:', style: TextStyle(fontSize: 20)),
                    const SizedBox(height:10),
                    Text('Approximately 180 min eating', style: TextStyle(fontSize: 16)),
                    const SizedBox(height:5),
                    Text('60 min were likely to be snacking', style: TextStyle(fontSize: 16)),
                    const SizedBox(height:30),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('That\'s 30 min less than yesterday', style: TextStyle(fontSize: 16)),
                        const SizedBox(width:5),
                        Icon(Icons.arrow_downward, color: Colors.green, size: 20,)
                      ]
                    ),
                    const SizedBox(height:20),
                    SizedBox(
                      height: 100,
                      child: PieChart(
                        PieChartData(
                          sections: [
                            PieChartSectionData(
                              value: 90,
                              radius: 50,
                              color: Colors.white,
                              title: '',
                            ),
                            PieChartSectionData(
                              value: 10,
                              radius: 50,
                              color: const Color.fromARGB(255, 90, 174, 239),
                              title: '',
                            ),
                          ]
                        )
                      )
                    ),
                    const SizedBox(height:15),
                    Text('10% of total time spent eating', style: TextStyle(fontSize: 16)),
                  ],
                ),
              ),
            ),
            const SizedBox(height:15),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Text('Based on your goals:', style: TextStyle(fontSize: 20)),
                    const SizedBox(height:10),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('You\'re on track, keep it up!', style: TextStyle(fontSize: 16)),
                        const SizedBox(width:10),
                        Icon(Icons.thumb_up, color: Colors.green, size: 20,)
                      ]
                    ),
                  ]
                ),
              ),
            ),
            const SizedBox(height:15),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Text('Anything that contributed to snacking?', style: TextStyle(fontSize: 16)),
                    const SizedBox(height:15),
                    TextField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        hintText: 'Type here: ',
                      ),
                    ),
                    const SizedBox(height:15),
                    // FilledButton(
                    //   onPressed: () {}, 
                    //   child: const Text('Save'),
                    // ),
                  ]
                ),
              ),
            ),
          ],
        )
      )
    );

  }

}





