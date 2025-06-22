import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';

import 'package:snacktrac/ui/past_summary/widgets/past_summary_screen.dart';


class ArchivePage extends StatelessWidget {
  const ArchivePage({super.key});

  @override
  Widget build(BuildContext context) {


    return Scaffold (
      appBar: AppBar(title: const Text('Find a Past Report:', 
        style: TextStyle(color: Colors.white)), backgroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            FilledButton(
              onPressed: () {
                Navigator.push(
                  context, MaterialPageRoute(builder: (context) => const PastSummaryPage()),
                );
              }, 
              child: const Text('Placeholder'),
            ),

            // Card(
            //   child: Padding(
            //     padding: const EdgeInsets.all(20.0),
            //     child: Column(
            //       children: [
            //         Text('You spent:', style: TextStyle(fontSize: 16)),
            //         const SizedBox(height:15),
            //         Text('Approximately 180 min eating', style: TextStyle(fontSize: 20)),
            //         Text('60 min were likely to be snacking', style: TextStyle(fontSize: 20)),
            //         const SizedBox(height:30),
            //         Text('Compared to yesterday:', style: TextStyle(fontSize: 16)),
            //         const SizedBox(height:15),
            //         Row(
            //           mainAxisAlignment: MainAxisAlignment.center,
            //           children: [
            //             Text('Down by 30 min', style: TextStyle(fontSize: 20)),
            //             const SizedBox(width:5),
            //             Icon(Icons.arrow_downward, color: Colors.green, size: 20,)
            //           ]
            //         ),
            //       ],
            //     ),
            //   ),
            // ),
          ],
        )
      )
    );

  }

}


