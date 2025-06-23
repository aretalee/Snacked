import 'package:flutter/material.dart';
import 'package:intl/intl.dart';


class PastSummaryPage extends StatelessWidget {
  const PastSummaryPage({super.key, required this.date});
  final DateTime date;

  @override
  Widget build(BuildContext context) {
    return Scaffold (
      appBar: AppBar(
        title: Text('Summary for ${DateFormat('MMMM d, y').format(date)} ', style: TextStyle(color: Colors.white)), backgroundColor: Colors.black, 
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new),
          onPressed: () => Navigator.of(context).pop(),
        )
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Text('You spent:', style: TextStyle(fontSize: 16)),
                    const SizedBox(height:15),
                    Text('Approximately 180 min eating', style: TextStyle(fontSize: 20)),
                    Text('60 min were likely to be snacking', style: TextStyle(fontSize: 20)),
                    const SizedBox(height:30),
                    Text('Compared to yesterday:', style: TextStyle(fontSize: 16)),
                    const SizedBox(height:15),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('Down by 30 min', style: TextStyle(fontSize: 20)),
                        const SizedBox(width:5),
                        Icon(Icons.arrow_downward, color: Colors.green, size: 20,)
                      ]
                    ),
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
                    Text('Based on your goals:', style: TextStyle(fontSize: 16)),
                    const SizedBox(height:15),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('You\'re on track, keep it up!', style: TextStyle(fontSize: 20)),
                        const SizedBox(width:5),
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





